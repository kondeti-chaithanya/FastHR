from pydantic import BaseModel, Field
from typing import Optional


class DepartmentBase(BaseModel):
    name: str = Field(..., example="Engineering")
    description: Optional[str] = Field(None, example="Software development department")


class DepartmentCreate(DepartmentBase):
    pass


class DepartmentUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None


class DepartmentResponse(DepartmentBase):
    id: int

    class Config:
        from_attributes = True
