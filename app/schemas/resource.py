from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import datetime

class ResourceCreate(BaseModel):
    name: str
    cpu_capacity: int
    ram_capacity: int
    cost_per_hour: float = 0.0
    status: str = "active"

class ResourceResponse(ResourceCreate):
    id: UUID
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)