# OptiCore AI

An advanced backend system designed for automated resource allocation and combinatorial optimization, bridging the gap between natural language operational intent and heavy algorithmic computation.

##  Tech Stack & Architecture

- **Language & Framework:** Python 3.11+, FastAPI, Pydantic v2
- **Asynchronous Task Queue:** Celery, Redis
- **Database & ORM:** PostgreSQL, SQLAlchemy (Async), Alembic
- **Optimization Core:** Google OR-Tools, NetworkX, SciPy
- **AI / LLM Integration:** Google Gemini API (via OpenAI-compatible client) with Structured Outputs
- **Containerization:** Docker & Docker Compose

##  Project Architecture Layers

1. **Natural Language Interface (LLM):** Parses unstructured human commands into strict operational JSON schemas.
2. **API & Workflow Layer (FastAPI + Celery):** Handles asynchronous routing and offloads heavy mathematical solvers to background workers.
3. **Core Optimization Engine:** Solves complex bin-packing and resource-knapsack allocation challenges using Google OR-Tools.
4. **Persistence Layer:** Manages infrastructure states, workloads, and audit logs via PostgreSQL.

##  Getting Started

### 1. Clone the repository & setup environment
```bash
git clone [https://github.com/lisovcoff/opticore-ai.git](https://github.com/lisovcoff/opticore-ai.git)
cd OptiCoreAI
```

### 2. Configure environment variables

Create a `.env` file in the root directory:

```env
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/opticore_db
REDIS_URL=redis://localhost:6379/0
OPENAI_API_KEY=your_google_gemini_api_key_here
```

### 3. Run with Docker Compose

```bash
docker-compose up --build
```

## API Documentation

Once the server is running, explore interactive Swagger documentation at:
`http://127.0.0.1:8000/docs`
