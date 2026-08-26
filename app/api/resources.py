from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.database import get_db
from app.models.resource import ResourceModel
from app.schemas.resource import ResourceCreate, ResourceResponse
from typing import List

router = APIRouter(prefix="/resources", tags=["Resources"])

@router.get("/", response_model=List[ResourceResponse])
async def get_resources(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(ResourceModel))
    resources = result.scalars().all()
    return resources

@router.post("/", response_model=ResourceResponse)
async def create_resource(resource_in: ResourceCreate, db: AsyncSession = Depends(get_db)):
    db_resource = ResourceModel(
        name=resource_in.name,
        cpu_capacity=resource_in.cpu_capacity,
        ram_capacity=resource_in.ram_capacity,
        cost_per_hour=resource_in.cost_per_hour,
        status=resource_in.status
    )
    
    db.add(db_resource)
    await db.commit()
    await db.refresh(db_resource)
    
    return db_resource