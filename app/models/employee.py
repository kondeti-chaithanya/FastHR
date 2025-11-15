from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)

    # Tech & work info
    tech_stack = Column(String, nullable=True)
    year_of_joining = Column(Integer, nullable=True)
    experience = Column(Integer, nullable=True)
    resignation_date = Column(Date, nullable=True)

    # ---------------------------
    # Department Relationship
    # ---------------------------
    department_id = Column(Integer, ForeignKey("departments.id", ondelete="SET NULL"))
    department = relationship("Department", back_populates="employees", lazy="selectin")

    # ---------------------------
    # Role Relationship
    # ---------------------------
    role_id = Column(Integer, ForeignKey("roles.id", ondelete="SET NULL"))
    role_details = relationship("Role", back_populates="employees", lazy="selectin")

    # ---------------------------
    # Manager / Hierarchy Setup
    # ---------------------------
    manager_id = Column(Integer, ForeignKey("employees.id", ondelete="SET NULL"))

    # Manager of this employee
    manager = relationship(
        "Employee",
        remote_side=[id],
        back_populates="subordinates",
        lazy="selectin"
    )

    # Subordinates
    subordinates = relationship(
        "Employee",
        back_populates="manager",
        lazy="selectin"
    )
