import numpy as np

import model


class Point:
    id = 0
    x = 0
    y = 0
    connected = []
    upperRow = None
    upperProj = None


class Arc:
    dist = 0
    path = []


class Row:
    a = None
    b = None
    k = 0
    n = 0


def get_projection(mypoint, line_a, line_b):

    p1 = np.array([line_a.x, line_a.y])
    p2 = np.array([line_b.x, line_b.y])
    p3 = np.array([mypoint.x, mypoint.y])

    # distance between p1 and p2
    l2 = np.sum((p1 - p2) ** 2)
    if l2 == 0:
        print('p1 and p2 are the same points')

    # The line extending the segment is parameterized as p1 + t (p2 - p1).
    # The projection falls where t = [(p3-p1) . (p2-p1)] / |p2-p1|^2

    # if you need the point to project on line extention connecting p1 and p2
    t = np.sum((p3 - p1) * (p2 - p1)) / l2

    # if you need to ignore if p3 does not project onto line segment
    if t > 1 or t < 0:
        print('p3 does not project onto p1-p2 line segment')

    # if you need the point to project on line segment between p1 and p2 or closest point of the line segment
    t = max(0, min(1, np.sum((p3 - p1) * (p2 - p1)) / l2))

    projection = p1 + t * (p2 - p1)

    ret = model.Point()
    ret.x = projection[0]
    ret.y = projection[1]
    return ret

def find_point_projections(points):
    for p in points:
        try:
            p.upperProj = get_projection(p, p.upperRow.a, p.upperRow.b)
        except:
            pass
