import numpy as np

from algorithm2.route_evaluation import evaluate_route


def ga(D, init_sol, collection_points, P, num_generations, population_size, mutation_rate, *, on_iteration=None):
    def evaluate(order):
        repaired, _, cost = evaluate_route(order, collection_points, D, P)
        return repaired, cost

    depot = init_sol[0]
    best = evaluate(init_sol)
    if len(init_sol) < 3:
        return best[0], best[1], [best[1]] * num_generations, [best[1]] * num_generations

    population = [best]

    def perturb(route):
        child = route.copy()
        # Mix short reversals with unrestricted moves between crop rows.
        left, right = sorted(np.random.choice(np.arange(1, len(child)), 2, replace=False))
        if np.random.rand() < 0.5:
            child[left:right + 1] = reversed(child[left:right + 1])
        else:
            source, destination = (left, right) if np.random.rand() < 0.5 else (right, left)
            child.insert(destination, child.pop(source))
        return child

    for _ in range(population_size - 1):
        population.append(evaluate(perturb(best[0])))

    def record():
        if on_iteration is not None:
            on_iteration(best[1], [cost for _, cost in population])

    if num_generations:
        best = min(population, key=lambda individual: individual[1])
        record()

    best_list = []
    curr_list = []
    for _ in range(num_generations):
        ranked = sorted(population, key=lambda individual: individual[1])
        elite_count = min(40, max(1, population_size // 2))
        population = ranked[:elite_count]
        # Keep room for fresh routes even when the top individuals converge.
        immigrants = min(population_size - elite_count, max(1, population_size // 10))
        weights = np.arange(len(ranked), 0, -1, dtype=float)
        weights /= weights.sum()
        while len(population) < population_size - immigrants:
            first, second = np.random.choice(len(ranked), 2, replace=False, p=weights)
            parent1, parent2 = ranked[first][0], ranked[second][0]
            left, right = sorted(np.random.choice(np.arange(1, len(parent1) + 1), 2, replace=False))
            segment = parent1[left:right]
            used = {point.id for point in segment}
            other = [point for point in parent2[1:] if point.id not in used]
            child = [depot] + other[:left - 1] + segment + other[left - 1:]
            if np.random.rand() < mutation_rate:
                child = perturb(child)
            population.append(evaluate(child))

        for _ in range(immigrants):
            population.append(evaluate(perturb(best[0])))

        current = min(population, key=lambda individual: individual[1])
        if current[1] < best[1]:
            best = current
        curr_list.append(current[1])
        best_list.append(best[1])
        record()

    return best[0], best[1], best_list, curr_list
