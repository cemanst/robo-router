import sys

import model.model
import numpy as np


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
    return np.math.sqrt((a.x - b.x) ^ 2 + (a.y - b.y) ^ 2)


def find_shortest_path_from_init(init_point, point, D, P):
    a = model.Arc()
    a.dist = eucledean_dist(init_point, point.upperRow.a) + eucledean_dist(point.upperRow.a, point.upperProj)
    a.path = [point.upperRow.a]

    tmp = eucledean_dist(init_point, point.upperRow.b) + eucledean_dist(point.upperRow.b, point.upperProj)
    if tmp < a.dist:
        a.dist = tmp
        a.path = [point.upperRow.b]

    init_point.connected.append(a)
    point.upperProj.connected.append(a)
    D[0, point.upperProj.id] = a.dist
    D[point.upperProj.id, 0] = a.dist
    P[0, point.upperProj.id] = a.path
    P[point.upperProj.id, 0] = a.path

    a = model.Arc()
    a.dist = eucledean_dist(init_point, point.lowerRow.a) + eucledean_dist(point.lowerRow.a, point.lowerProj)
    a.path = [point.lowerRow.a]

    tmp = eucledean_dist(init_point, point.lowerRow.b) + eucledean_dist(point.lowerRow.b, point.lowerProj)
    if tmp < a.dist:
        a.dist = tmp
        a.path = [point.lowerRow.b]

    init_point.connected.append(a)
    point.lowerProj.connected.append(a)
    D[0, point.lowerProj.id] = a.dist
    D[point.lowerProj.id, 0] = a.dist
    P[0, point.lowerProj.id] = a.path
    P[point.lowerProj.id, 0] = a.path


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
    point2.upperProj.connected.append(a)
    D[point1.upperProj.id, point2.upperProj.id] = a.dist
    D[point2.upperProj.id, point1.upperProj.id] = a.dist
    P[point1.upperProj.id, point2.upperProj.id] = a.path
    P[point2.upperProj.id, point1.upperProj.id] = a.path

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
    point2.lowerProj.connected.append(a)
    D[point1.upperProj.id, point2.lowerProj.id] = a.dist
    D[point2.lowerProj.id, point1.upperProj.id] = a.dist
    P[point1.upperProj.id, point2.lowerProj.id] = a.path
    P[point2.lowerProj.id, point1.upperProj.id] = a.path

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
    point2.upperProj.connected.append(a)
    D[point1.lowerProj.id, point2.upperProj.id] = a.dist
    D[point2.upperProj.id, point1.lowerProj.id] = a.dist
    P[point1.lowerProj.id, point2.upperProj.id] = a.path
    P[point2.upperProj.id, point1.lowerProj.id] = a.path

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
    point2.lowerProj.connected.append(a)
    D[point1.lowerProj.id, point2.lowerProj.id] = a.dist
    D[point2.lowerProj.id, point1.lowerProj.id] = a.dist
    P[point1.lowerProj.id, point2.lowerProj.id] = a.path
    P[point2.lowerProj.id, point1.lowerProj.id] = a.path


def generate_graph(init_point, collection_points):
    D = np.zeros(2*len(collection_points)+1, 2*len(collection_points)+1)
    P = np.empty(2*len(collection_points)+1, 2*len(collection_points)+1, dtype=[])

    init_point.id = 0
    for i in range(len(collection_points)):
        collection_points[i].id = i+1
        collection_points[i].upperProj = 2*i + 1
        collection_points[i].lowerProj = 2*i + 2

    for i in range(len(collection_points)):
        find_shortest_path_from_init(init_point, collection_points[i], D, P)

        for j in i+1..len(collection_points)-1:
            find_shortest_path(collection_points[i], collection_points[j], D, P)

    all_points = [init_point]
    for cp in collection_points:
        all_points.append(cp.upperProj)
        all_points.append(cp.lowerProj)

    return all_points, D, P


def calculate_row_params(rows):
    for r in rows:
        r.k = (r.a.y-r.b.y) / (r.a.x-r.a.y)
        r.n = r.a.y-r.k*r.a.x


def prepare_data(init_point, collection_points, rows):
    calculate_row_params(rows)
    determine_rows_for_collection(collection_points, rows)
    model.find_point_projections(collection_points)




