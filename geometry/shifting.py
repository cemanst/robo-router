import numpy as np

from geometry.vector import Vector
from model.model import Point

def shift_corners(rows):
    first_row = rows[0]
    last_row = rows[-1]

    side_a = Vector(last_row.a, first_row.a)
    unit_dist = side_a.get_length() / (len(rows)-1)

    for row in rows:
        vec_b2a = Vector(row.a, row.b)
        vec_a2b = Vector(row.b, row.a)
        

        vec_b2a.set_length(unit_dist)
        vec_b2a.shift(row.a)
        
        vec_a2b.set_length(unit_dist)
        vec_a2b.shift(row.b)

def shift_out_init_point(rows, init_point):
    first_row = rows[0]
    last_row = rows[-1]
    
    side_a = Vector(last_row.a, first_row.a)
    unit_dist = side_a.get_length() / (len(rows)-1)

    corners = [first_row.a, first_row.b, last_row.a, last_row.b]
    centroid = Point()
    for c in corners:
        centroid.x += c.x / 4
        centroid.y += c.y / 4 # centroid of a field used to detect side of initial point
    
    from_vector = Vector(init_point, centroid)
    from_vector.set_length(3*unit_dist)
    from_vector.shift(init_point)
 


