import numpy as np
from algorithm.prepare_data import prepare_data, generate_graph

def eucledean_dist(a, b):
    return np.math.sqrt(pow((a.x - b.x), 2) + pow((a.y - b.y), 2))

def run_greedy(init_point, collection_points):
    graph, D, P = generate_graph(init_point, collection_points)

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

        if closest_idx%2 == 0:
            del remaining[closest_idx+1]
            del remaining[closest_idx]
        else:
            del remaining[closest_idx]
            del remaining[closest_idx-1]

        order.append(closest)
        curr_point = closest

    return order, D, P

def create_best(init_point, collection_points):
    graph, D, P = generate_graph(init_point, collection_points)

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

    if eucledean_dist(init_point, sorted[0].upperRow.a) > eucledean_dist(init_point, sorted[len(sorted)-1].upperRow.a):
        sorted.reverse()

    curr_point = init_point
    order = [init_point]

    for cp in sorted:
        if eucledean_dist(curr_point, cp.upperProj) < eucledean_dist(curr_point, cp.lowerProj):
            order.append(cp.upperProj)
            curr_point = cp.upperProj
        else:
            order.append(cp.lowerProj)
            curr_point = cp.lowerProj

    return order, D, P








