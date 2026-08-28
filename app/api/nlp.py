from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from app.core.database import get_db
from app.services.llm_service import parse_natural_language_command
from app.models.resource import ResourceModel
from app.models.task import TaskModel

router = APIRouter(prefix="/nlp", tags=["Natural Language Interface"])

class PromptRequest(BaseModel):
    prompt: str

@router.post("/process")
async def process_natural_language(request: PromptRequest, db: AsyncSession = Depends(get_db)):
    """
    Receives a natural language prompt, parses it via Gemini LLM,
    and automatically creates a resource or task in the database if applicable.
    """
    if not request.prompt.strip():
        raise HTTPException(status_code=400, detail="Prompt cannot be empty.")

    # 1. Parse command via LLM
    parsed_data = parse_natural_language_command(request.prompt)

    if "error" in parsed_data:
        raise HTTPException(status_code=400, detail=parsed_data["error"])

    action = parsed_data.get("action")
    db_item = None

    # 2. Handle 'create_resource' action
    if action == "create_resource":
        name = parsed_data.get("resource_name") or "default-node"
        cpu = parsed_data.get("cpu_capacity") or 4
        ram = parsed_data.get("ram_capacity") or 16
        cost = parsed_data.get("cost_per_hour") or 1.0

        db_item = ResourceModel(
            name=name,
            cpu_capacity=cpu,
            ram_capacity=ram,
            cost_per_hour=cost,
            status="active"
        )
        db.add(db_item)
        await db.commit()
        await db.refresh(db_item)

    # 3. Handle 'create_task' action
    elif action == "create_task":
        name = parsed_data.get("task_name") or "default-task"
        cpu = parsed_data.get("cpu_required") or 2
        ram = parsed_data.get("ram_required") or 4
        priority = parsed_data.get("priority") or 5

        db_item = TaskModel(
            name=name,
            cpu_required=cpu,
            ram_required=ram,
            priority=priority,
            status="pending"
        )
        db.add(db_item)
        await db.commit()
        await db.refresh(db_item)

    return {
        "status": "success",
        "prompt": request.prompt,
        "parsed_command": parsed_data,
        "database_record_created": True if db_item else False,
        "item_id": str(db_item.id) if db_item else None
    }