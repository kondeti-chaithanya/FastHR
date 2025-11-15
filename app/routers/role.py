from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.database import get_db
from app.schemas.role import RoleCreate, RoleResponse, RoleUpdate
from app.schemas.employee import EmployeeResponse
from app.services.role_service import (
    create_role,
    list_roles,
    get_role,
    update_role,
    delete_role,
    get_role_employees
)

router = APIRouter(prefix="/roles", tags=["roles"])


# ======================================
# Create Role
# ======================================
@router.post("/", response_model=RoleResponse, status_code=201)
async def create_role_endpoint(payload: RoleCreate, db: AsyncSession = Depends(get_db)):
    return await create_role(db, payload)


# ======================================
# List All Roles
# ======================================
@router.get("/", response_model=List[RoleResponse])
async def get_roles(db: AsyncSession = Depends(get_db)):
    return await list_roles(db)


# ======================================
# Get Single Role by ID
# ======================================
@router.get("/{role_id}", response_model=RoleResponse)
async def get_role_endpoint(role_id: int, db: AsyncSession = Depends(get_db)):
    role = await get_role(db, role_id)
    if not role:
        raise HTTPException(404, "Role not found")
    return role


# ======================================
# Update Role
# ======================================
@router.put("/{role_id}", response_model=RoleResponse)
async def update_role_endpoint(role_id: int, payload: RoleUpdate, db: AsyncSession = Depends(get_db)):
    updated = await update_role(db, role_id, payload)
    if not updated:
        raise HTTPException(404, "Role not found")
    return updated


# ======================================
# Delete Role
# ======================================
@router.delete("/{role_id}")
async def delete_role_endpoint(role_id: int, db: AsyncSession = Depends(get_db)):
    role = await get_role(db, role_id)
    if not role:
        raise HTTPException(404, "Role not found")
    await delete_role(db, role_id)
    return {"message": "Role deleted successfully"}


# ======================================
# Employees Assigned to a Role
# ======================================
@router.get("/{role_id}/employees", response_model=List[EmployeeResponse])
async def get_role_employees_endpoint(role_id: int, db: AsyncSession = Depends(get_db)):
    return await get_role_employees(db, role_id)
