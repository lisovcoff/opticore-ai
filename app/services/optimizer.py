from ortools.linear_solver import pywraplp
from typing import List, Dict, Any

def solve_resource_allocation(resources: List[Dict[str, Any]], tasks: List[Dict[str, Any]]) -> Dict[str, Any]:
    solver = pywraplp.Solver.CreateSolver('CBC_MIXED_INTEGER_PROGRAMMING')
    if not solver:
        return {"error": "Could not create solver", "allocations": []}
    x = {}
    for task in tasks:
        for resource in resources:
            x[(task['id'], resource['id'])] = solver.BoolVar(f"task_{task['id']}_res_{resource['id']}")

    for task in tasks:
        solver.Add(solver.Sum(x[(task['id'], resource['id'])] for resource in resources) <= 1)

    for resource in resources:
        res_id = resource['id']
        solver.Add(
            solver.Sum(x[(task['id'], res_id)] * task['cpu_required'] for task in tasks) 
            <= resource['cpu_capacity']
        )
        solver.Add(
            solver.Sum(x[(task['id'], res_id)] * task['ram_required'] for task in tasks) 
            <= resource['ram_capacity']
        )

    objective_terms = []
    for task in tasks:
        priority = task.get('priority', 1)
        for resource in resources:
            objective_terms.append(x[(task['id'], resource['id'])] * priority)
    
    # Передаем сумму выражений в солвер для максимизации
    solver.Maximize(solver.Sum(objective_terms))

    status = solver.Solve()

    allocations = []
    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        for task in tasks:
            for resource in resources:
                if x[(task['id'], resource['id'])].solution_value() > 0.5:
                    allocations.append({
                        "task_id": task['id'],
                        "resource_id": resource['id'],
                        "task_name": task['name'],
                        "resource_name": resource['name']
                    })

    return {
        "status": "success" if allocations else "no_optimal_solution",
        "allocations": allocations
    }