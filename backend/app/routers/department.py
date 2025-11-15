from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.database import get_db
from app.schemas.department import DepartmentCreate, DepartmentResponse, DepartmentUpdate
from app.schemas.employee import EmployeeResponse
from app.services.department_service import (
    create_department,
    list_departments,
    get_department,
    update_department,
    delete_department,
    get_department_employees
)

router = APIRouter(prefix="/departments", tags=["departments"])


# ======================================
# Create Department
# ======================================
@router.post("/", response_model=DepartmentResponse, status_code=201)
async def create_department_endpoint(payload: DepartmentCreate, db: AsyncSession = Depends(get_db)):
    return await create_department(db, payload)


# ======================================
# List All Departments
# ======================================
@router.get("/", response_model=List[DepartmentResponse])
async def get_departments(db: AsyncSession = Depends(get_db)):
    return await list_departments(db)


# ======================================
# Get Department by ID
# ======================================
@router.get("/{dept_id}", response_model=DepartmentResponse)
async def get_department_endpoint(dept_id: int, db: AsyncSession = Depends(get_db)):
    dept = await get_department(db, dept_id)
    if not dept:
        raise HTTPException(404, "Department not found")
    return dept


# ======================================
# Update Department
# ======================================
@router.put("/{dept_id}", response_model=DepartmentResponse)
async def update_department_endpoint(dept_id: int, payload: DepartmentUpdate, db: AsyncSession = Depends(get_db)):
    updated = await update_department(db, dept_id, payload)
    if not updated:
        raise HTTPException(404, "Department not found")
    return updated


# ======================================
# Delete Department
# ======================================
@router.delete("/{dept_id}")
async def delete_department_endpoint(dept_id: int, db: AsyncSession = Depends(get_db)):
    dept = await get_department(db, dept_id)
    if not dept:
        raise HTTPException(404, "Department not found")
    await delete_department(db, dept_id)
    return {"message": "Department deleted successfully"}


# ======================================
# Employees Under a Department
# ======================================
@router.get("/{dept_id}/employees", response_model=List[EmployeeResponse])
async def get_department_employees_endpoint(dept_id: int, db: AsyncSession = Depends(get_db)):
    return await get_department_employees(db, dept_id)
