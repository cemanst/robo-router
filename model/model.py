import numpy as np

class Point:
    id = 0
    x = 0
    y = 0
    connected = []
    upperRow = None
    lowerRow = None
    upperProj = ()
    lowerProj = ()

class Arc:
    dist = 0
    path = []

class Row:
    a = None
    b = None
    k = 0
    n = 0


def get_projection(point, line_a, line_b):
    x = np.array(point.x, point.y)
    u = np.array(line_a.x, line_a.y)
    v = np.array(line_b.x, line_b.y)
    n = v - u
    n /= np.linalg.norm(n, 2)
    P = u + n * np.dot(x - u, n)
    ret = Point()
    ret.x = P[0], ret.y = P[1]
    return ret


def find_point_projections(points):
    for p in points:
        p.upperProj = get_projection(p, p.upperRow.a, p.upperRow.b)
        p.lowerProj = get_projection(p, p.lowerRow.a, p.lowerRow.b)
