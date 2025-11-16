from fastapi import FastAPI

# Routers
from app.routers import employee as employee_router
from app.routers import role as role_router
from app.routers import department as department_router

# Database
from app.database import engine, Base

# Import all models for SQLAlchemy
import app.models.employee
import app.models.role
import app.models.department

app = FastAPI(title="FastHR")

# Register Routers
app.include_router(employee_router.router)
app.include_router(role_router.router)
app.include_router(department_router.router)

# Create all tables on startup
@app.on_event("startup")
async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
