from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from typing import List, Optional

from app.models.role import Role
from app.models.employee import Employee
from app.schemas.role import RoleCreate, RoleUpdate


# ---------------------------
# Create Role
# ---------------------------
async def create_role(db: AsyncSession, payload: RoleCreate) -> Role:
    role = Role(**payload.model_dump())
    db.add(role)
    await db.commit()
    await db.refresh(role)
    return role


# ---------------------------
# List All Roles
# ---------------------------
async def list_roles(db: AsyncSession) -> List[Role]:
    result = await db.execute(select(Role))
    return result.scalars().all()


# ---------------------------
# Get Role
# ---------------------------
async def get_role(db: AsyncSession, role_id: int) -> Optional[Role]:
    result = await db.execute(select(Role).where(Role.id == role_id))
    return result.scalars().first()


# ---------------------------
# Update Role
# ---------------------------
async def update_role(db: AsyncSession, role_id: int, payload: RoleUpdate):
    await db.execute(
        update(Role)
        .where(Role.id == role_id)
        .values(**payload.model_dump(exclude_none=True))
    )
    await db.commit()
    return await get_role(db, role_id)


# ---------------------------
# Delete Role
# ---------------------------
async def delete_role(db: AsyncSession, role_id: int) -> bool:
    await db.execute(delete(Role).where(Role.id == role_id))
    await db.commit()
    return True


# ---------------------------
# Get Employees Under Role
# ---------------------------
async def get_role_employees(db: AsyncSession, role_id: int):
    result = await db.execute(select(Employee).where(Employee.role_id == role_id))
    return result.scalars().all()
