from math import pi

import numpy as np

from model.params import sinuosity_scale_width, sinuosity_scale_height
from geometry.bend import Bend
# from geometry.crown import Crown
from geometry.symmetry import symmetry
from geometry.vector import Vector

def is_same_side(init_point, centroid, point1, point2):
    """
    Determine if centroid and init_point are on the same or opposite sides of the line beteween point1 and point2.

    Params:
        init_point: Point
            Initial robot point
        centroid: Point
            Point in the middle of the field, average of field corners
        point1, point2: Point
            2 points connected by the same side of the field, 2 out of 4 field corner points
        
    Returns:
        bool
            True if centroid and init_point are on the same side of point1-point2 line, False otherwise
    """
    k = (point2.y - point1.y) / (point2.x - point1.x) # line equation: y - kx - n = 0 
    n = point1.y - k*point1.x

    side_centroid = np.sign( centroid.y - k * centroid.x - n ) # half-plane detection
    side_init = np.sign( init_point.y - k * init_point.x - n )

    return side_centroid == side_init # same or different sides of point1-point2 line


def sinuosity(point_a, point_b, centroid, row_width):
    distance = Vector(point_b, point_a).get_length()
    W = min(distance, row_width) * sinuosity_scale_width
    H = min(distance, row_width) * sinuosity_scale_height

    sa, middle, sb = symmetry(point_a, point_b)
    outer = None
    if not is_same_side(sa, centroid, point_a, point_b):
        outer = sa
    else:
        outer = sb
    
    xaxis  = Vector(point_b, middle)
    yaxis = Vector(outer, middle)
    
    xaxis.set_length(W)
    yaxis.set_length(H)

    bend_a = Bend(npoints=9, leaving=True, inner=True)
    pivot_a = xaxis.shift(point_a, inplace=False)
    pivot_a.elev = point_a.elev
    intersteps_a = bend_a.apply(xaxis, yaxis, pivot_a)

    bend_b = Bend(npoints=9, leaving=False, inner=True)
    xreverse = xaxis.rotate(pi)
    pivot_b = xreverse.shift(point_b, inplace=False)
    pivot_b.elev = point_b.elev
    intersteps_b = bend_b.apply(xaxis, yaxis, pivot_b)

    return intersteps_a + intersteps_b
    


