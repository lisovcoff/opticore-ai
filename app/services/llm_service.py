import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

# Initialize the OpenAI client pointing to Google's Gemini API base URL
# Gemini provides an OpenAI-compatible endpoint for developers
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

def parse_natural_language_command(prompt: str) -> str:
    """
    Sends a natural language prompt to Google Gemini 
    and asks it to extract infrastructure commands or analyze tasks.
    """
    try:
        response = client.chat.completions.create(
            # Using the fast and free-tier friendly Gemini 2.5 Flash model
            model="gemini-3.6-flash",
            messages=[
                {
                    "role": "system", 
                    "content": "You are an AI assistant for OptiCore AI, an infrastructure optimization engine. "
                               "Your job is to help users manage computing resources and tasks using natural language."
                },
                {
                    "role": "user", 
                    "content": prompt
                }
            ],
            temperature=0.2
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error communicating with Gemini LLM: {str(e)}"