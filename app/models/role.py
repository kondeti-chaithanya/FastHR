from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from app.database import Base


class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), unique=True, nullable=False)
    level = Column(Integer, nullable=False)
    description = Column(Text, nullable=True)

    # Relationship → Employees
    employees = relationship(
        "Employee",
        back_populates="role_details",
        lazy="selectin"
    )
