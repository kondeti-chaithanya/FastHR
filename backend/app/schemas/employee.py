from pydantic import BaseModel, Field
from typing import Optional
from datetime import date


class EmployeeBase(BaseModel):
    name: str = Field(..., example="John Doe")
    tech_stack: Optional[str] = Field(None, example="Python, FastAPI")
    year_of_joining: Optional[int] = Field(None, example=2022)
    experience: Optional[int] = Field(None, example=3)
    resignation_date: Optional[date] = None

    role_id: Optional[int] = Field(None, example=3)
    department_id: Optional[int] = Field(None, example=1)
    manager_id: Optional[int] = Field(None, example=5)


class EmployeeCreate(EmployeeBase):
    name: str


class EmployeeUpdate(BaseModel):
    name: Optional[str] = None
    tech_stack: Optional[str] = None
    year_of_joining: Optional[int] = None
    experience: Optional[int] = None
    resignation_date: Optional[date] = None
    role_id: Optional[int] = None
    department_id: Optional[int] = None
    manager_id: Optional[int] = None


class EmployeeResponse(EmployeeBase):
    id: int

    class Config:
        from_attributes = True
    