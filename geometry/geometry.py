import numpy as np


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