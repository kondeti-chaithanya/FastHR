from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database import get_db
from app.models.employee import Employee

router = APIRouter(prefix="/structure", tags=["structure"])


# ----------------------------------------
# Helper: Build Recursive Tree
# ----------------------------------------
async def build_tree(db: AsyncSession, employee: Employee):
    # Fetch direct subordinates
    result = await db.execute(
        select(Employee).where(Employee.manager_id == employee.id)
    )
    subs = result.scalars().all()

    # Recursively build tree
    return {
        "id": employee.id,
        "name": employee.name,
        "role": employee.role,
        "subordinates": [
            await build_tree(db, sub) for sub in subs
        ]
    }


# ----------------------------------------
# Get Full Org Tree
# ----------------------------------------
@router.get("/tree")
async def get_full_tree(db: AsyncSession = Depends(get_db)):
    # Root employees = employees who have NO manager
    result = await db.execute(
        select(Employee).where(Employee.manager_id.is_(None))
    )
    roots = result.scalars().all()

    # Build trees for every root (CEO/CTO/Heads)
    tree = []
    for emp in roots:
        tree.append(await build_tree(db, emp))

    return tree
