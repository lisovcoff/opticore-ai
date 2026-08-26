from fastapi import FastAPI
from app.api.resources import router as resources_router
from app.api.tasks import router as tasks_router

app = FastAPI(
    title="OptiCore AI",
    description="Backend for resource and task optimization using Algorithms and AI",
    version="0.1.0"
)

# Подключаем наши роутеры с префиксом /api/v1
app.include_router(resources_router, prefix="/api/v1")
app.include_router(tasks_router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "Welcome to OptiCore AI API! Go to /docs for Swagger UI."}