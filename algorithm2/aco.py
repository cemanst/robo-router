import numpy as np

from algorithm2.aco_utils import construct_sol
from algorithm2.route_evaluation import evaluate_route


def aco(init_point, graph, collection_points, D, P, init_sol, max_iter=3000, num_ants=50, *, on_iteration=None):
    repaired, _, init_cost = evaluate_route(init_sol, collection_points, D, P)
    best_sol = [point.id for point in repaired]
    best_cost = init_cost
    pheromone = np.full((len(graph), len(graph)), 1e-3)
    points = {point.id: point for point in graph}
    distances = D[:len(graph), :len(graph)]
    neighbors = np.argsort(distances, axis=1, kind="stable").tolist()
    visibility = np.maximum(distances, 1e-9) ** -2

    def reinforce(order, amount):
        for source, target in zip(order, order[1:] + order[:1]):
            pheromone[source, target] += amount

    reinforce(best_sol, 1e-3)
    trend = ([], [])

    for _ in range(max_iter):
        colony = []
        constructed = []
        for _ in range(num_ants):
            order = construct_sol(init_point.id, visibility, pheromone, neighbors)
            repaired, _, cost = evaluate_route([points[i] for i in order], collection_points, D, P)
            colony.append(([point.id for point in repaired], cost))
            constructed.append((order, cost))

        iteration_sol, iteration_cost = min(colony, key=lambda candidate: candidate[1])
        if iteration_cost < best_cost:
            best_sol, best_cost = iteration_sol, iteration_cost

        pheromone *= 0.5
        np.maximum(pheromone, 5e-5, out=pheromone)
        # Keep weaker tours from reinforcing a high-cost consensus.
        constructed.sort(key=lambda candidate: candidate[1])
        for order, cost in constructed[:max(1, num_ants // 4)]:
            reinforce(order, 2 / max(cost, np.finfo(float).eps))
        reinforce(best_sol, 2 / max(best_cost, np.finfo(float).eps))

        trend[0].append(iteration_cost)
        trend[1].append(best_cost)
        if on_iteration is not None:
            on_iteration(best_cost, [cost for _, cost in colony])

    return best_sol, best_cost, init_cost, trend
