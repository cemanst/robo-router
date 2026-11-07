import itertools
import random

from algorithm2.greedy import run_greedy
from algorithm2.route_evaluation import evaluate_route
from algorithm2.vns_operators import k_opt


def vns(init_point, collection_points, graph, D, P, *, max_evaluations=10040, on_evaluation=None):
    greedy = run_greedy(init_point, graph, D)
    best, full, baseline = evaluate_route(greedy, collection_points, D, P)
    best_cost = baseline
    pairs = list(itertools.combinations(range(1, len(best)), 2))
    neighborhoods = [size for size in (1, 2, 3, 7) if size <= len(pairs)]
    if not neighborhoods:
        return full, best_cost, baseline

    neighborhood = 0
    misses = 0
    for _ in range(max_evaluations):
        moves = random.sample(pairs, neighborhoods[neighborhood])
        order, expanded, cost = evaluate_route(k_opt(best, moves), collection_points, D, P)
        if cost < best_cost:
            best, full, best_cost = order, expanded, cost
            neighborhood = 0
            misses = 0
        else:
            misses += 1
            if misses == len(best):
                neighborhood = (neighborhood + 1) % len(neighborhoods)
                misses = 0
        if on_evaluation is not None:
            on_evaluation(best_cost)

    return full, best_cost, baseline
