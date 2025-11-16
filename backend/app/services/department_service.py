from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException

from app.models.department import Department
from app.schemas.department import DepartmentCreate, DepartmentUpdate


# ---------------------------------------------
# CREATE DEPARTMENT
# ---------------------------------------------
async def create_department(db: AsyncSession, payload: DepartmentCreate):
    dept = Department(**payload.model_dump())
    db.add(dept)

    try:
        await db.commit()
        await db.refresh(dept)
        return dept

    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Department name already exists. Choose another name."
        )


# ---------------------------------------------
# LIST DEPARTMENTS
# ---------------------------------------------
async def list_departments(db: AsyncSession):
    result = await db.execute(select(Department))
    return result.scalars().all()


# ---------------------------------------------
# GET DEPARTMENT
# ---------------------------------------------
async def get_department(db: AsyncSession, dept_id: int):
    result = await db.execute(select(Department).where(Department.id == dept_id))
    return result.scalars().first()


# ---------------------------------------------
# UPDATE DEPARTMENT
# ---------------------------------------------
async def update_department(db: AsyncSession, dept_id: int, payload: DepartmentUpdate):
    dept = await get_department(db, dept_id)
    if not dept:
        return None

    for key, value in payload.model_dump(exclude_none=True).items():
        setattr(dept, key, value)

    try:
        await db.commit()
        await db.refresh(dept)
        return dept

    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Department name already exists."
        )


# ---------------------------------------------
# DELETE DEPARTMENT
# ---------------------------------------------
async def delete_department(db: AsyncSession, dept_id: int):
    dept = await get_department(db, dept_id)
    if not dept:
        return None

    await db.delete(dept)
    await db.commit()
    return True


# ---------------------------------------------
# EMPLOYEES UNDER A DEPARTMENT
# ---------------------------------------------
async def get_department_employees(db: AsyncSession, dept_id: int):
    dept = await get_department(db, dept_id)
    if not dept:
        return None
    return dept.employees
