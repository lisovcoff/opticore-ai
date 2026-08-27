from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.database import get_db
from app.models.resource import ResourceModel
from app.models.task import TaskModel
from app.services.optimizer import solve_resource_allocation

router = APIRouter(prefix="/optimize", tags=["Optimization"])

@router.post("/")
async def run_optimization(db: AsyncSession = Depends(get_db)):
    res_result = await db.execute(select(ResourceModel))
    resources = res_result.scalars().all()

    task_result = await db.execute(select(TaskModel))
    tasks = task_result.scalars().all()

    if not resources:
        raise HTTPException(status_code=400, detail="No resources available for allocation.")
    if not tasks:
        raise HTTPException(status_code=400, detail="No tasks available for allocation.")

    resources_data = [
        {
            "id": str(r.id),
            "name": r.name,
            "cpu_capacity": r.cpu_capacity,
            "ram_capacity": r.ram_capacity
        }
        for r in resources if r.status == "active"
    ]

    tasks_data = [
        {
            "id": str(t.id),
            "name": t.name,
            "cpu_required": t.cpu_required,
            "ram_required": t.ram_required,
            "priority": t.priority
        }
        for t in tasks if t.status == "pending"
    ]

    if not resources_data:
        raise HTTPException(status_code=400, detail="No active resources available.")
    if not tasks_data:
        raise HTTPException(status_code=400, detail="No pending tasks available.")

    optimization_result = solve_resource_allocation(resources_data, tasks_data)

    return {
        "message": "Optimization completed successfully",
        "result": optimization_result
    }