from algorithm2.distance import objective_energy_consumption

def run_greedy(init_point, graph, D):

    curr_point = init_point
    order = [init_point]
    remaining = graph.copy()
    del remaining[0]

    while len(remaining) > 0:
        closest = remaining[0]
        closest_idx = 0
        for i in range(1, len(remaining)):
            if D[curr_point.id, remaining[i].id] < D[curr_point.id, closest.id]:
                closest = remaining[i]
                closest_idx = i

        del remaining[closest_idx]
        order.append(closest)
        curr_point = closest

    return order


def create_best(init_point, collection_points):

    if collection_points[0].upperRow.a.x < collection_points[1].upperRow.a.x:
        sorted = [collection_points[0], collection_points[1]]
    else:
        sorted = [collection_points[1], collection_points[0]]

    for i in range (2, len(collection_points)):
        cp = collection_points[i]
        if cp.upperRow.a.x < sorted[0].upperRow.a.x:
            sorted.insert(0, cp)
        elif cp.upperRow.a.x > sorted[len(sorted)-1].upperRow.a.x:
            sorted.append(cp)
        else:
            for j in range(len(sorted)-1):
                if sorted[j].upperRow.a.x < cp.upperRow.a.x < sorted[j + 1].upperRow.a.x:
                    sorted.insert(j+1, cp)
                    break

    if objective_energy_consumption(init_point, sorted[0].upperRow.a) > objective_energy_consumption(init_point, sorted[len(sorted)-1].upperRow.a):
        sorted.reverse()

    order = [init_point]
    for cp in sorted:
        order.append(cp.upperProj)

    return order








