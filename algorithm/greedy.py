import numpy as np
from algorithm.prepare_data import prepare_data, generate_graph


def run_greedy(init_point, collection_points):
    graph, D, P = generate_graph(init_point, collection_points)

    curr_point = init_point
    order = [init_point]
    visited = {init_point.id}

    while len(visited) < 2*len(collection_points):
        arr = list(D[curr_point.id,:])
        j = np.argmin(arr)
        while j in visited and len(arr) > 0:
            del arr[j]
            j = np.argmin(arr)

        visited.add(j)
        if j%2:
            visited.add(j-1)
        else:
            visited.add(j+1)

        order.append(graph[j])

        return order, D, P








