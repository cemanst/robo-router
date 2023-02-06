import numpy as np

from model.model import Point
from algorithm2.distance import objective_energy_consumption
from geometry.geometry import is_same_side

def double_pass_watering(init_point, rows):
    """
    Define route passing through all rows in sequence, where each row is passed in both directions.

    Params:
        init_point - Point
        rows - list<Row>
    
    Returns:
        solution - list<Point>
            order in which robot pass through all rows twice
    
    """
    first_row = rows[0]
    last_row = rows[-1]

    
    corners = [first_row.a, first_row.b, last_row.a, last_row.b]
    centroid = Point()
    for c in corners:
        centroid.x += c.x / 4
        centroid.y += c.y / 4 # centroid of a field used to detect side of initial point
    
    lines = [
        (first_row.a, first_row.b), # field border lines
        (last_row.a, last_row.b),
        (first_row.a, last_row.a),
        (first_row.b, last_row.b)
    ]
    reachable_corners = []
    for l in lines:
        if not is_same_side(init_point, centroid, l[0], l[1]): # detection which points are directly reachable without crossing the field
            if l[0] not in reachable_corners:
                reachable_corners.append(l[0])
            if l[1] not in reachable_corners:
                reachable_corners.append(l[1])
    
    reachable_corners.sort(key = lambda x: objective_energy_consumption(init_point, x)) # start from closes reachabe point
    start_corner = reachable_corners[0]

    rows_ordered = None
    if start_corner in (first_row.a, first_row.b): # detect of order in which rows will be visited
        rows_ordered = rows[::] # first to last
    elif start_corner in (last_row.a, last_row.b):
        rows_ordered = rows[::-1] # last to first
    a2b = (start_corner == rows_ordered[0].a) # detect of pass direction through current row, zik: a->b, or zak: b->a

    solution = [init_point]
    for r in rows_ordered:
        patch = [r.a, r.b, r.a] if a2b else [r.b, r.a, r.b] # define order in which a/b points of current row will be traversed
        solution += patch
    
    last_corner = solution[-1]
    if last_corner not in reachable_corners: # better case -> direct return
        solution += [start_corner] # worse case -> via same side to starting point
    
    solution += [init_point]
    return solution

