import numpy as np
import matplotlib.pyplot as plt
from algorithm2.distance import objective_energy_consumption
import model.model

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


def create_inv_arc(a):
    a2 = model.Arc()
    a2.dist = a.dist
    a2.path = a.path.copy()
    a2.path.reverse()
    return a2


def find_shortest_path_from_init(init_point, point, D, P):
    a = model.Arc()
    if objective_energy_consumption(init_point, point.approaching_row().a) < objective_energy_consumption(init_point, point.approaching_row().b):
        a.dist = objective_energy_consumption(init_point, point.approaching_row().a) + objective_energy_consumption(point.approaching_row().a, point.approaching_point())
        a.path = [point.approaching_row().a]
    else:
        a.dist = objective_energy_consumption(init_point, point.approaching_row().b) + objective_energy_consumption(point.approaching_row().b, point.approaching_point())
        a.path = [point.approaching_row().b]

    init_point.connected.append(a)
    D[init_point.id, point.approaching_point().id] = a.dist
    P[init_point.id, point.approaching_point().id] = a.path

    a2 = create_inv_arc(a)
    point.approaching_point().connected.append(a2)
    D[point.approaching_point().id, init_point.id] = a2.dist
    P[point.approaching_point().id, init_point.id] = a2.path


def find_shortest_path(point1, point2, D, P):
    #connect approaching_point()-approaching_point()
    a = model.Arc()
    if point1.approaching_row() == point2.approaching_row():
        a.dist = objective_energy_consumption(point1.approaching_point(), point2.approaching_point())
        a.path = []
    else:
        a.dist = objective_energy_consumption(point1.approaching_point(), point1.approaching_row().a) \
                 + objective_energy_consumption(point1.approaching_row().a, point2.approaching_row().a) \
                 + objective_energy_consumption(point2.approaching_row().a, point2.approaching_point())
        a.path = [point1.approaching_row().a, point2.approaching_row().a]

        tmp = objective_energy_consumption(point1.approaching_point(), point1.approaching_row().b) \
              + objective_energy_consumption(point1.approaching_row().b, point2.approaching_row().b) \
              + objective_energy_consumption(point2.approaching_row().b, point2.approaching_point())
        if tmp < a.dist:
            a.dist = tmp
            a.path = [point1.approaching_row().b, point2.approaching_row().b]

    point1.approaching_point().connected.append(a)
    D[point1.approaching_point().id, point2.approaching_point().id] = a.dist
    P[point1.approaching_point().id, point2.approaching_point().id] = a.path

    a2 = create_inv_arc(a)
    point2.approaching_point().connected.append(a2)
    D[point2.approaching_point().id, point1.approaching_point().id] = a2.dist
    P[point2.approaching_point().id, point1.approaching_point().id] = a2.path


def generate_graph(init_point, collection_points):
    D = np.zeros([2*len(collection_points)+1, 2*len(collection_points)+1])
    P = np.empty([2*len(collection_points)+1, 2*len(collection_points)+1], dtype=object)

    init_point.id = 0
    for i in range(len(collection_points)):
        collection_points[i].id = i+1
        collection_points[i].approaching_point().id = i + 1

    for i in range(len(collection_points)):
        find_shortest_path_from_init(init_point, collection_points[i], D, P)

        if i < len(collection_points)-1:
            for j in range(i+1, len(collection_points)):
                find_shortest_path(collection_points[i], collection_points[j], D, P)

    all_points = [init_point]
    for cp in collection_points:
        all_points.append(cp.approaching_point())

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
        if cp.approaching_point() is not None:
            plt.plot(cp.approaching_point().x, cp.approaching_point().y, 'go')

        plt.plot([cp.approaching_row().a.x, cp.approaching_row().b.x], [cp.approaching_row().a.y, cp.approaching_row().b.y], 'bo-')

    plt.show()
