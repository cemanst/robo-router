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


#https://cs.nyu.edu/~yap/classes/visual/03s/hw/h2/math.pdf
def get_projection(point, line_a, line_b):
    A = np.array([[line_b.x-line_a.x, line_b.y-line_a.y], [line_a.y-line_b.y, line_b.x-line_a.x]])
    b = np.array([[-point.x*(line_b.x-line_a.x) - point.y*(line_b.y-line_a.y)]
                     ,[-line_a.x*(line_b.x-line_a.x) - line_a.y*(line_b.y-line_a.y)]])

    p = np.matmul(np.linalg.inv(A), b)
    ret = Point()
    ret.x = p[0][0]
    ret.y = p[1][0]
    return ret


def find_point_projections(points):
    for p in points:
        p.upperProj = get_projection(p, p.upperRow.a, p.upperRow.b)
        p.lowerProj = get_projection(p, p.lowerRow.a, p.lowerRow.b)
