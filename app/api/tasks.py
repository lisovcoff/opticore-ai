from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.database import get_db
from app.models.task import TaskModel
from app.schemas.task import TaskCreate, TaskResponse
from typing import List

router = APIRouter(prefix="/tasks", tags=["Tasks"])

@router.get("/", response_model=List[TaskResponse])
async def get_tasks(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(TaskModel))
    tasks = result.scalars().all()
    return tasks

@router.post("/", response_model=TaskResponse)
async def create_task(task_in: TaskCreate, db: AsyncSession = Depends(get_db)):
    db_task = TaskModel(
        name=task_in.name,
        cpu_required =task_in.cpu_required,
        ram_required =task_in.ram_required,
        priority=task_in.priority,
        status=task_in.status
    )
    
    db.add(db_task)
    await db.commit()
    await db.refresh(db_task)
    
    return db_task