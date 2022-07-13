import sys

import model.model
import numpy as np
import matplotlib.pyplot as plt

def determine_rows_for_collection(collection_points, rows):
    for cp in collection_points:
        for i in range(len(rows)-1):
            rowA = rows[i]
            rowB = rows[i+1]
            if cp.y <= rowA.k*cp.x + rowA.n and cp.y >= rowB.k*cp.x + rowB.n:
                cp.upperRow = rowA
                cp.lowerRow = rowB
            elif cp.y >= rowA.k*cp.x + rowA.n and cp.y <= rowB.k*cp.x + rowB.n:
                cp.upperRow = rowB
                cp.lowerRow = rowA


def eucledean_dist(a, b):
    return np.math.sqrt(pow((a.x - b.x), 2) + pow((a.y - b.y), 2))

def create_inv_arc(a):
    a2 = model.Arc()
    a2.dist = a.dist
    a2.path = a.path.copy()
    a2.path.reverse()
    return a2


def find_shortest_path_from_init(init_point, point, D, P):
    a = model.Arc()
    if eucledean_dist(init_point, point.upperRow.a) < eucledean_dist(init_point, point.upperRow.b):
        a.dist = eucledean_dist(init_point, point.upperRow.a) + eucledean_dist(point.upperRow.a, point.upperProj)
        a.path = [point.upperRow.a]
    else:
        a.dist = eucledean_dist(init_point, point.upperRow.b) + eucledean_dist(point.upperRow.b, point.upperProj)
        a.path = [point.upperRow.b]

    init_point.connected.append(a)
    D[0, point.upperProj.id] = a.dist
    P[0, point.upperProj.id] = a.path

    a2 = create_inv_arc(a)
    point.upperProj.connected.append(a2)
    D[point.upperProj.id, 0] = a2.dist
    P[point.upperProj.id, 0] = a2.path

    a = model.Arc()
    if eucledean_dist(init_point, point.lowerRow.a) < eucledean_dist(init_point, point.lowerRow.b):
        a.dist = eucledean_dist(init_point, point.lowerRow.a) + eucledean_dist(point.lowerRow.a, point.lowerProj)
        a.path = [point.lowerRow.a]
    else:
        a.dist = eucledean_dist(init_point, point.lowerRow.b) + eucledean_dist(point.lowerRow.b, point.lowerProj)
        a.path = [point.lowerRow.b]

    init_point.connected.append(a)
    D[0, point.lowerProj.id] = a.dist
    P[0, point.lowerProj.id] = a.path

    a2 = create_inv_arc(a)
    point.lowerProj.connected.append(a2)
    D[point.lowerProj.id, 0] = a2.dist
    P[point.lowerProj.id, 0] = a2.path


def find_shortest_path(point1, point2, D, P):
    #connect upperProj-upperProj
    a = model.Arc()
    a.dist = eucledean_dist(point1.upperProj, point1.upperRow.a) \
             + eucledean_dist(point1.upperRow.a, point2.upperRow.a) \
             + eucledean_dist(point2.upperRow.a, point2.upperProj)
    a.path = [point1.upperRow.a, point2.upperRow.a]

    tmp = eucledean_dist(point1.upperProj, point1.upperRow.b) \
             + eucledean_dist(point1.upperRow.b, point2.upperRow.b) \
             + eucledean_dist(point2.upperRow.b, point2.upperProj)
    if tmp < a.dist:
        a.dist = tmp
        a.path = [point1.upperRow.b, point2.upperRow.b]

    point1.upperProj.connected.append(a)
    D[point1.upperProj.id, point2.upperProj.id] = a.dist
    P[point1.upperProj.id, point2.upperProj.id] = a.path

    a2 = create_inv_arc(a)
    point2.upperProj.connected.append(a2)
    D[point2.upperProj.id, point1.upperProj.id] = a2.dist
    P[point2.upperProj.id, point1.upperProj.id] = a2.path

    # connect upperProj-lowerProj
    a = model.Arc()
    a.dist = eucledean_dist(point1.upperProj, point1.upperRow.a) \
             + eucledean_dist(point1.upperRow.a, point2.lowerRow.a) \
             + eucledean_dist(point2.lowerRow.a, point2.lowerProj)
    a.path = [point1.upperRow.a, point2.lowerRow.a]

    tmp = eucledean_dist(point1.upperProj, point1.upperRow.b) \
          + eucledean_dist(point1.upperRow.b, point2.lowerRow.b) \
          + eucledean_dist(point2.lowerRow.b, point2.lowerProj)
    if tmp < a.dist:
        a.dist = tmp
        a.path = [point1.upperRow.b, point2.lowerRow.b]

    point1.upperProj.connected.append(a)
    D[point1.upperProj.id, point2.lowerProj.id] = a.dist
    P[point1.upperProj.id, point2.lowerProj.id] = a.path

    a2 = create_inv_arc(a)
    point2.lowerProj.connected.append(a2)
    D[point2.lowerProj.id, point1.upperProj.id] = a2.dist
    P[point2.lowerProj.id, point1.upperProj.id] = a2.path

    # connect lowerProj-upperProj
    a = model.Arc()
    a.dist = eucledean_dist(point1.lowerProj, point1.lowerRow.a) \
             + eucledean_dist(point1.lowerRow.a, point2.upperRow.a) \
             + eucledean_dist(point2.upperRow.a, point2.upperProj)
    a.path = [point1.lowerRow.a, point2.upperRow.a]

    tmp = eucledean_dist(point1.lowerProj, point1.lowerRow.b) \
          + eucledean_dist(point1.lowerRow.b, point2.upperRow.b) \
          + eucledean_dist(point2.upperRow.b, point2.upperProj)
    if tmp < a.dist:
        a.dist = tmp
        a.path = [point1.lowerRow.b, point2.upperRow.b]

    point1.lowerProj.connected.append(a)
    D[point1.lowerProj.id, point2.upperProj.id] = a.dist
    P[point1.lowerProj.id, point2.upperProj.id] = a.path

    a2 = create_inv_arc(a)
    point2.upperProj.connected.append(a2)
    D[point2.upperProj.id, point1.lowerProj.id] = a2.dist
    P[point2.upperProj.id, point1.lowerProj.id] = a2.path

    # connect lowerProj-lowerProj
    a = model.Arc()
    a.dist = eucledean_dist(point1.lowerProj, point1.lowerRow.a) \
             + eucledean_dist(point1.lowerRow.a, point2.lowerRow.a) \
             + eucledean_dist(point2.lowerRow.a, point2.lowerProj)
    a.path = [point1.lowerRow.a, point2.lowerRow.a]

    tmp = eucledean_dist(point1.lowerProj, point1.lowerRow.b) \
          + eucledean_dist(point1.lowerRow.b, point2.lowerRow.b) \
          + eucledean_dist(point2.lowerRow.b, point2.lowerProj)
    if tmp < a.dist:
        a.dist = tmp
        a.path = [point1.lowerRow.b, point2.lowerRow.b]

    point1.lowerProj.connected.append(a)
    D[point1.lowerProj.id, point2.lowerProj.id] = a.dist
    P[point1.lowerProj.id, point2.lowerProj.id] = a.path

    a2 = create_inv_arc(a)
    point2.lowerProj.connected.append(a2)
    D[point2.lowerProj.id, point1.lowerProj.id] = a2.dist
    P[point2.lowerProj.id, point1.lowerProj.id] = a2.path


def generate_graph(init_point, collection_points):
    D = np.zeros([2*len(collection_points)+1, 2*len(collection_points)+1])
    P = np.empty([2*len(collection_points)+1, 2*len(collection_points)+1], dtype=object)

    init_point.id = 0
    for i in range(len(collection_points)):
        collection_points[i].id = i+1
        collection_points[i].upperProj.id = 2*i + 1
        collection_points[i].lowerProj.id = 2*i + 2

    for i in range(len(collection_points)):
        find_shortest_path_from_init(init_point, collection_points[i], D, P)

        if i < len(collection_points)-1:
            for j in range(i+1, len(collection_points)):
                find_shortest_path(collection_points[i], collection_points[j], D, P)

    all_points = [init_point]
    for cp in collection_points:
        all_points.append(cp.upperProj)
        all_points.append(cp.lowerProj)

    return all_points, D, P


def calculate_row_params(rows):
    for r in rows:
        r.k = (r.a.y-r.b.y) / (r.a.x-r.b.x)
        r.n = r.a.y-r.k*r.a.x


def prepare_data(init_point, collection_points, rows):
    calculate_row_params(rows)
    determine_rows_for_collection(collection_points, rows)
    model.find_point_projections(collection_points)
    #check_data(rows, collection_points)
    pass


def check_data(rows, collection_points):
    for r in rows:
        plt.plot([r.a.x, r.b.x], [r.a.y, r.b.y], 'ro-')

    # for r in rows:
    #     plt.plot([r.a.x, r.b.x], [r.k*r.a.x+r.n, r.k*r.b.x+r.n], 'bo-')

    for cp in collection_points:
        plt.plot(cp.x, cp.y, 'bo')
        if cp.upperProj is not None:
            plt.plot(cp.upperProj.x, cp.upperProj.y, 'go')
        if cp.lowerProj is not None:
            plt.plot(cp.lowerProj.x, cp.lowerProj.y, 'yo')

        plt.plot([cp.upperRow.a.x, cp.upperRow.b.x], [cp.upperRow.a.y, cp.upperRow.b.y], 'bo-')
        plt.plot([cp.lowerRow.a.x, cp.lowerRow.b.x], [cp.lowerRow.a.y, cp.lowerRow.b.y], 'bo-')

    plt.show()
