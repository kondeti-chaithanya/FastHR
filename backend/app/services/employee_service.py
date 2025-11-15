from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from typing import List, Optional

from app.models.employee import Employee
from app.schemas.employee import EmployeeCreate, EmployeeUpdate


# ---------------------------
# Create Employee
# ---------------------------
async def create_employee(db: AsyncSession, payload: EmployeeCreate) -> Employee:
    emp = Employee(**payload.model_dump())
    db.add(emp)
    await db.commit()
    await db.refresh(emp)
    return emp


# ---------------------------
# Get Employee by ID
# ---------------------------
async def get_employee(db: AsyncSession, employee_id: int) -> Optional[Employee]:
    result = await db.execute(select(Employee).where(Employee.id == employee_id))
    return result.scalars().first()


# ---------------------------
# List Employees
# ---------------------------
async def list_employees(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(Employee).offset(skip).limit(limit))
    return result.scalars().all()


# ---------------------------
# Update Employee
# ---------------------------
async def update_employee(db: AsyncSession, employee_id: int, payload: EmployeeUpdate):
    await db.execute(
        update(Employee)
        .where(Employee.id == employee_id)
        .values(**payload.model_dump(exclude_none=True))
    )
    await db.commit()
    return await get_employee(db, employee_id)


# ---------------------------
# Delete Employee
# ---------------------------
async def delete_employee(db: AsyncSession, employee_id: int) -> bool:
    await db.execute(delete(Employee).where(Employee.id == employee_id))
    await db.commit()
    return True


# ---------------------------
# List Subordinates (Direct Reports)
# ---------------------------
async def list_subordinates(db: AsyncSession, manager_id: int):
    result = await db.execute(select(Employee).where(Employee.manager_id == manager_id))
    return result.scalars().all()
