import numpy as np

from model.model import Point
from algorithm2.distance import euclidean_dist_with_elev

def pass_all_rows(init_point, rows):
    first_row = rows[0]
    last_row = rows[-1]

    centroid = Point()
    corners = [first_row.a, first_row.b, last_row.a, last_row.b]
    for c in corners:
        centroid.x += c.x / 4
        centroid.y += c.y / 4
    
    lines = [
        (first_row.a, first_row.b),
        (last_row.a, last_row.b),
        (first_row.a, last_row.a),
        (first_row.b, last_row.b)
    ]
    reachable_corners = []
    for l in lines:
        if not is_same_side(init_point, centroid, l[0], l[1]):
            if l[0] not in reachable_corners:
                reachable_corners.append(l[0])
            if l[1] not in reachable_corners:
                reachable_corners.append(l[1])
    
    reachable_corners.sort(key = lambda x: euclidean_dist_with_elev(init_point, x))
    start_corner = reachable_corners[0]

    rows_ordered = None
    if start_corner in (first_row.a, first_row.b):
        rows_ordered = rows[::] # first to last
    elif start_corner in (last_row.a, last_row.b):
        rows_ordered = rows[::-1] # last to first
    a2b = (start_corner == rows_ordered[0].a) # zik: a->b, or zak: b->a

    solution = [init_point]
    for r in rows_ordered:
        patch = [r.a, r.b]
        if not a2b:
            patch.reverse()
        solution += patch

        a2b = not a2b
    
    return_options = []
    last_corner = solution[-1]
    same_row_corner = solution[-2]
    if last_corner == rows_ordered[-1].a:
        same_side_corner = rows_ordered[0].a
    elif last_corner == rows_ordered[-1].b:
        same_side_corner = rows_ordered[0].b

    if last_corner in reachable_corners:
        return_options.append(tuple([
            euclidean_dist_with_elev(last_corner, init_point), 
            []
        ]))
    if same_row_corner in reachable_corners:
        return_options.append(tuple([
            euclidean_dist_with_elev(last_corner, same_row_corner) + euclidean_dist_with_elev(same_row_corner, init_point),
            [same_row_corner]
        ]))
    if same_side_corner in reachable_corners:
        return_options.append(tuple([
            euclidean_dist_with_elev(last_corner, same_side_corner) + euclidean_dist_with_elev(same_side_corner, init_point),
            [same_side_corner]
        ]))
    
    return_options.sort(key= lambda x: x[0])
    solution += return_options[0][1] + [init_point]
    return solution


def is_same_side(init_point, centroid, point1, point2):
    k = (point2.y - point1.y) / (point2.x - point1.x)
    n = point1.y - k*point1.x

    side_centroid = np.sign( centroid.y - k * centroid.x - n )
    side_init = np.sign( init_point.y - k * init_point.x - n )

    return side_centroid == side_init # same or different sides of point1-point2 line

