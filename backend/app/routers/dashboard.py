from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.database import get_db
from app.models.employee import Employee
from app.models.department import Department
from app.models.role import Role

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


# ---------------------------------------------
# 1️⃣ TOTAL COUNTS
# ---------------------------------------------
@router.get("/counts")
async def get_employee_counts(db: AsyncSession = Depends(get_db)):
    total = await db.execute(select(func.count(Employee.id)))
    total_active = await db.execute(select(func.count()).where(Employee.resignation_date.is_(None)))
    total_resigned = await db.execute(select(func.count()).where(Employee.resignation_date.is_not(None)))
    total_managers = await db.execute(select(func.count()).where(Employee.id.in_(select(Employee.manager_id).where(Employee.manager_id.is_not(None)))))

    return {
        "total_employees": total.scalar(),
        "active_employees": total_active.scalar(),
        "resigned_employees": total_resigned.scalar(),
        "total_managers": total_managers.scalar()
    }


# ---------------------------------------------
# 2️⃣ EMPLOYEES PER DEPARTMENT
# ---------------------------------------------
@router.get("/employees-per-department")
async def employees_per_department(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Department.name, func.count(Employee.id))
        .join(Employee, Department.id == Employee.department_id, isouter=True)
        .group_by(Department.id)
    )
    rows = result.all()
    return [{"department": r[0], "count": r[1]} for r in rows]


# ---------------------------------------------
# 3️⃣ EMPLOYEES PER ROLE
# ---------------------------------------------
@router.get("/employees-per-role")
async def employees_per_role(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Role.title, func.count(Employee.id))
        .join(Employee, Role.id == Employee.role_id, isouter=True)
        .group_by(Role.id)
    )
    rows = result.all()
    return [{"role": r[0], "count": r[1]} for r in rows]


# ---------------------------------------------
# 4️⃣ EXPERIENCE DISTRIBUTION
# ---------------------------------------------
@router.get("/experience-distribution")
async def experience_distribution(db: AsyncSession = Depends(get_db)):
    buckets = {
        "0-2": (0, 2),
        "2-5": (2, 5),
        "5-10": (5, 10),
        "10+": (10, 50),
    }
    output = {}

    for label, (start, end) in buckets.items():
        result = await db.execute(
            select(func.count())
            .where(Employee.experience >= start)
            .where(Employee.experience < end)
        )
        output[label] = result.scalar()

    return output


# ---------------------------------------------
# 5️⃣ YEAR OF JOINING CHART DATA
# ---------------------------------------------
@router.get("/joining-year")
async def joining_year_graph(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Employee.year_of_joining, func.count())
        .group_by(Employee.year_of_joining)
        .order_by(Employee.year_of_joining)
    )
    rows = result.all()
    return [{"year": r[0], "count": r[1]} for r in rows]


# ---------------------------------------------
# 6️⃣ MANAGER → TEAM COUNT
# ---------------------------------------------
@router.get("/manager-team-count")
async def manager_team_count(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Employee.name, func.count())
        .join(Employee, Employee.manager_id == Employee.id, isouter=True)
        .group_by(Employee.id)
    )
    rows = result.all()
    return [{"manager": r[0], "team_count": r[1]} for r in rows]
