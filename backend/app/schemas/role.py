from pydantic import BaseModel, Field
from typing import Optional


class RoleBase(BaseModel):
    title: str = Field(..., example="Manager")
    level: int = Field(..., example=3)
    description: Optional[str] = Field(None, example="Manages team operations")


class RoleCreate(RoleBase):
    pass


class RoleUpdate(BaseModel):
    title: Optional[str] = None
    level: Optional[int] = None
    description: Optional[str] = None


class RoleResponse(RoleBase):
    id: int

    class Config:
        from_attributes = True
