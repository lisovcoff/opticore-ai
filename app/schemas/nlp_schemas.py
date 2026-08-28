from pydantic import BaseModel, Field, field_validator
from typing import Optional, Union

class ParsedResourceCommand(BaseModel):
    action: str = Field(description="Action type, e.g., 'create_resource' or 'create_task'")
    resource_name: Optional[str] = Field(None, description="Name of the server or resource node")
    cpu_capacity: Optional[Union[int, str]] = Field(None, description="Total available CPU units or cores")
    ram_capacity: Optional[Union[int, str]] = Field(None, description="Total available RAM in GB")
    cost_per_hour: Optional[float] = Field(None, description="Cost per hour factor")
    
    task_name: Optional[str] = Field(None, description="Name of the task to execute")
    cpu_required: Optional[Union[int, str]] = Field(None, description="Required CPU for the task")
    ram_required: Optional[Union[int, str]] = Field(None, description="Required RAM for the task")
    priority: Optional[int] = Field(None, description="Task priority from 1 to 10")

    @field_validator('cpu_capacity', 'ram_capacity', 'cpu_required', 'ram_required', mode='before')
    @classmethod
    def extract_integer(cls, v):
        if v is None:
            return None
        if isinstance(v, int):
            return v
        # Extract digits from string like '64GB' or '16 cores'
        import re
        numbers = re.findall(r'\d+', str(v))
        return int(numbers[0]) if numbers else None