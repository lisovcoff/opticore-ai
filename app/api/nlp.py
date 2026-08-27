from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.llm_service import parse_natural_language_command

router = APIRouter(prefix="/nlp", tags=["Natural Language Interface"])

class PromptRequest(BaseModel):
    prompt: str

@router.post("/process")
async def process_natural_language(request: PromptRequest):
    """
    Receives a natural language prompt from the user,
    sends it to Gemini LLM, and returns the AI's response.
    """
    if not request.prompt.strip():
        raise HTTPException(status_code=400, detail="Prompt cannot be empty.")

    ai_response = parse_natural_language_command(request.prompt)

    return {
        "status": "success",
        "prompt": request.prompt,
        "ai_response": ai_response
    }