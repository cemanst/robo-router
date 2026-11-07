import random


def construct_sol(depot, costs, pheromone, neighbors):
    order = [depot]
    remaining = set(range(len(pheromone))) - {depot}
    exploration = min(0.10, 1 / len(pheromone))
    while remaining:
        current = order[-1]
        if random.random() < exploration:
            next_point = random.choice(sorted(remaining))
        else:
            nearest = [point for point in neighbors[current] if point in remaining][:3]
            candidates = nearest.copy()
            # A low-cost route can contain a useful edge outside the nearest three.
            reinforced = max(remaining, key=lambda point: pheromone[current, point])
            if reinforced not in nearest:
                candidates.append(reinforced)
            weights = [pheromone[current, point] * costs[current, point] for point in candidates]
            next_point = random.choices(candidates, weights=weights)[0]
        order.append(next_point)
        remaining.remove(next_point)
    return order
