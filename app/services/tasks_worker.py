from app.core.celery_app import celery_app
from app.services.optimizer import solve_resource_allocation

@celery_app.task(name="run_optimization_task")
def run_optimization_task(resources: list, tasks: list) -> dict:
    """
    Celery background task that accepts pre-processed lists of resources and tasks 
    and runs a heavy mathematical solver.
    """
    result = solve_resource_allocation(resources, tasks)
    return result