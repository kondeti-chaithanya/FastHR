from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.database import get_db
from app.models.employee import Employee

router = APIRouter(prefix="/analytics", tags=["analytics"])


# ---------------------------
# 1. Attrition Stats
# ---------------------------
@router.get("/attrition")
async def attrition_stats(db: AsyncSession = Depends(get_db)):

    total = await db.execute(select(func.count()).select_from(Employee))
    total = total.scalar()

    resigned = await db.execute(
        select(func.count()).select_from(Employee).where(Employee.resignation_date.isnot(None))
    )
    resigned = resigned.scalar()

    active = total - resigned

    percent = (resigned / total * 100) if total > 0 else 0

    return {
        "total_employees": total,
        "active_employees": active,
        "resigned_employees": resigned,
        "attrition_percentage": round(percent, 2)
    }


# ---------------------------
# 2. Year-wise Resignation Trend
# ---------------------------
@router.get("/resignation-trend")
async def resignation_trend(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(func.extract('year', Employee.resignation_date).label("year"),
               func.count().label("count"))
        .where(Employee.resignation_date.isnot(None))
        .group_by("year")
        .order_by("year")
    )

    return [{"year": int(row.year), "count": row.count} for row in result]


# ---------------------------
# 3. Search Employees by Skill
# ---------------------------
@router.get("/search/skills")
async def search_employees(skill: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Employee).where(Employee.tech_stack.ilike(f"%{skill}%"))
    )
    return result.scalars().all()


# ---------------------------
# 4. Experience Distribution Buckets
# ---------------------------
@router.get("/experience-buckets")
async def experience_buckets(db: AsyncSession = Depends(get_db)):
    buckets = {
        "0-2 years": 0,
        "3-5 years": 0,
        "6-10 years": 0,
        "10+ years": 0
    }

    result = await db.execute(select(Employee.experience))
    all_exp = result.scalars().all()

    for exp in all_exp:
        if exp is None:
            continue
        if exp <= 2:
            buckets["0-2 years"] += 1
        elif exp <= 5:
            buckets["3-5 years"] += 1
        elif exp <= 10:
            buckets["6-10 years"] += 1
        else:
            buckets["10+ years"] += 1

    return buckets


# ---------------------------
# 5. Manager → Team Strength Level
# ---------------------------
@router.get("/manager-level")
async def manager_levels(db: AsyncSession = Depends(get_db)):

    result = await db.execute(
        select(Employee.id, Employee.name, func.count(Employee.id))
        .join(Employee, Employee.manager_id == Employee.id, isouter=True)
        .group_by(Employee.id)
    )

    levels = []
    for manager_id, name, count in result:
        if count <= 3:
            level = "L1 Manager"
        elif count <= 8:
            level = "L2 Manager"
        else:
            level = "L3 Manager"

        levels.append({
            "manager_id": manager_id,
            "name": name,
            "team_size": count,
            "manager_level": level
        })

    return levels
