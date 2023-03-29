from copy import copy
from math import pi

from geometry.vector import Vector
from model.model import PointType

def assign_directions(solution):
    previous = solution[0]

    for current in solution[1:]:
        v = Vector(current, previous)
        current.orientation = v

        previous = current
    
    solution[0].orientation = solution[1].orientation
    return solution


def duplicate_rotation_points(solution):
    retval = []
    for s in solution:
        sc = copy(s)
        retval.append(sc)

        if s.turning:
            sc = copy(s)
            sc.type = PointType.DUPLICATE
            sc.orientation = sc.orientation.rotate(pi)
            retval.append(sc)
    
    return retval


