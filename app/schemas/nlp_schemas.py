from pydantic import BaseModel, Field
from typing import Optional

class ParsedResourceCommand(BaseModel):
    action: str = Field(description="Action type, e.g., 'create_resource' or 'create_task'")
    resource_name: Optional[str] = Field(None, description="Name of the server or resource node")
    cpu_capacity: Optional[int] = Field(None, description="Total available CPU units or cores")
    ram_capacity: Optional[int] = Field(None, description="Total available RAM in GB")
    cost_per_hour: Optional[float] = Field(None, description="Cost per hour factor")
    
    task_name: Optional[str] = Field(None, description="Name of the task to execute")
    cpu_required: Optional[int] = Field(None, description="Required CPU for the task")
    ram_required: Optional[int] = Field(None, description="Required RAM for the task")
    priority: Optional[int] = Field(None, description="Task priority from 1 to 10")