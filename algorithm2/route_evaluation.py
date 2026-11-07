from postprocessing.complete_solution import create_complete_sol
from postprocessing.fixing import fix_all_inverse


def evaluate_route(order, collection_points, costs, paths):
    """Apply ALNS's turn detection, route repair, and full cost calculation."""
    create_complete_sol(order, costs, paths)
    repaired = fix_all_inverse(order, collection_points)
    expanded, cost = create_complete_sol(repaired, costs, paths)
    return repaired, expanded, cost
