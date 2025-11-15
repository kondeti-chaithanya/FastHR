from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.database import get_db
from app.schemas.employee import EmployeeCreate, EmployeeUpdate, EmployeeResponse
from app.services.employee_service import (
    create_employee,
    get_employee,
    list_employees,
    update_employee,
    delete_employee,
    list_subordinates
)

router = APIRouter(prefix="/employees", tags=["employees"])


# ============================================
# Create Employee
# ============================================
@router.post("/", response_model=EmployeeResponse, status_code=201)
async def create_employee_endpoint(payload: EmployeeCreate, db: AsyncSession = Depends(get_db)):
    return await create_employee(db, payload)


# ============================================
# Get All Employees
# ============================================
@router.get("/", response_model=List[EmployeeResponse])
async def get_all_employees(db: AsyncSession = Depends(get_db)):
    return await list_employees(db)


# ============================================
# Get Employee by ID
# ============================================
@router.get("/{employee_id}", response_model=EmployeeResponse)
async def get_employee_endpoint(employee_id: int, db: AsyncSession = Depends(get_db)):
    emp = await get_employee(db, employee_id)
    if not emp:
        raise HTTPException(404, "Employee not found")
    return emp


# ============================================
# Update Employee
# ============================================
@router.put("/{employee_id}", response_model=EmployeeResponse)
async def update_employee_endpoint(
    employee_id: int,
    payload: EmployeeUpdate,
    db: AsyncSession = Depends(get_db)
):
    updated = await update_employee(db, employee_id, payload)
    if not updated:
        raise HTTPException(404, "Employee not found")
    return updated


# ============================================
# Delete Employee
# ============================================
@router.delete("/{employee_id}")
async def delete_employee_endpoint(employee_id: int, db: AsyncSession = Depends(get_db)):
    emp = await get_employee(db, employee_id)
    if not emp:
        raise HTTPException(404, "Employee not found")
    await delete_employee(db, employee_id)
    return {"message": "Employee deleted successfully"}


# ============================================
# Get Subordinates (Direct Reports)
# ============================================
@router.get("/{employee_id}/subordinates", response_model=List[EmployeeResponse])
async def get_subordinates_endpoint(employee_id: int, db: AsyncSession = Depends(get_db)):
    emp = await get_employee(db, employee_id)
    if not emp:
        raise HTTPException(404, "Employee not found")
    return await list_subordinates(db, employee_id)


# ============================================
# Get Employees by Department
# ============================================
@router.get("/department/{dept_id}", response_model=List[EmployeeResponse])
async def get_employees_by_department(dept_id: int, db: AsyncSession = Depends(get_db)):
    employees = await list_employees(db)
    return [e for e in employees if e.department_id == dept_id]


# ============================================
# Get Employees by Role
# ============================================
@router.get("/role/{role_id}", response_model=List[EmployeeResponse])
async def get_employees_by_role(role_id: int, db: AsyncSession = Depends(get_db)):
    employees = await list_employees(db)
    return [e for e in employees if e.role_id == role_id]


# ============================================
# Get Full Hierarchy Tree of an Employee
# ============================================
@router.get("/{employee_id}/hierarchy")
async def get_hierarchy(employee_id: int, db: AsyncSession = Depends(get_db)):
    emp = await get_employee(db, employee_id)
    if not emp:
        raise HTTPException(404, "Employee not found")

    async def build_tree(emp_id):
        emp = await get_employee(db, emp_id)
        subs = await list_subordinates(db, emp_id)
        return {
            "id": emp.id,
            "name": emp.name,
            "role_id": emp.role_id,
            "department_id": emp.department_id,
            "subordinates": [await build_tree(s.id) for s in subs]
        }

    return await build_tree(employee_id)


# ============================================
# Search Employees by Name
# ============================================
@router.get("/search/", response_model=List[EmployeeResponse])
async def search_employees(
    q: str = Query(..., description="Search employees by name"),
    db: AsyncSession = Depends(get_db)
):
    employees = await list_employees(db)
    return [e for e in employees if q.lower() in e.name.lower()]


# ============================================
# Filter Employees (experience + joining year)
# ============================================
@router.get("/filter/", response_model=List[EmployeeResponse])
async def filter_employees(
    min_exp: int = 0,
    year: int = None,
    db: AsyncSession = Depends(get_db)
):
    employees = await list_employees(db)
    result = employees

    if min_exp:
        result = [e for e in result if (e.experience or 0) >= min_exp]

    if year:
        result = [e for e in result if e.year_of_joining == year]

    return result


# ============================================
# Sort Employees (name or experience)
# ============================================
@router.get("/sort/", response_model=List[EmployeeResponse])
async def sort_employees(
    by: str = Query("name", description="Sort by: name | experience"),
    db: AsyncSession = Depends(get_db)
):
    employees = await list_employees(db)

    if by == "experience":
        return sorted(employees, key=lambda x: x.experience or 0, reverse=True)

    return sorted(employees, key=lambda x: x.name.lower())
