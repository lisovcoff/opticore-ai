import os
import json
from dotenv import load_dotenv
from openai import OpenAI
from app.schemas.nlp_schemas import ParsedResourceCommand

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

def parse_natural_language_command(prompt: str) -> dict:
    """
    Parses a natural language prompt into a structured JSON 
    matching the ParsedResourceCommand schema using Gemini.
    """
    system_prompt = (
        "You are an AI assistant for OptiCore AI, an infrastructure optimization engine. "
        "Extract infrastructure commands from the user prompt and return a valid JSON object "
        "matching these fields if applicable: action ('create_resource' or 'create_task'), "
        "resource_name, cpu_capacity, ram_capacity, cost_per_hour, "
        "task_name, cpu_required, ram_required, priority."
    )

    try:
        response = client.chat.completions.create(
            model="gemini-3.6-flash",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"},
            temperature=0.1
        )
        
        content = response.choices[0].message.content
        parsed_data = json.loads(content)
        
        # Validate data against Pydantic schema
        validated_command = ParsedResourceCommand(**parsed_data)
        return validated_command.model_dump()
        
    except Exception as e:
        return {"error": f"Failed to parse command: {str(e)}"}