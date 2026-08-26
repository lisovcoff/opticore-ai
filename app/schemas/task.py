from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import datetime
from typing import Optional

class TaskCreate(BaseModel):
    name: str
    cpu_required : int
    ram_required : int
    priority: int
    status: str = "pending"

class TaskResponse(TaskCreate):
    id: UUID
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)