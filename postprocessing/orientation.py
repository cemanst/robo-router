from copy import copy
from math import pi

from geometry.vector import Vector
from model.model import PointType


def assign_orientation(solution):
    for previous, current, following in zip(solution[:-2], solution[1:-1], solution[2:]):
        current.orientation_in = Vector(current, previous)
        current.orientation_out = Vector(following, current)

    solution[0].orientation_out = solution[1].orientation_in # propagate orientation backwards to first point
    solution[0].orientation_in = solution[0].orientation_out 

    solution[-1].orientation_in = solution[-2].orientation_out # propagate orientation forwards to last point
    solution[-1].orientation_out = solution[-1].orientation_in

    return solution


def duplicate_prepend_rotation(solution):
    retval = []
    for s in solution:
        step_original = copy(s)

        if s.turning:
            step_duplicate = copy(s)
            step_duplicate.type = PointType.DUPLICATE
            step_duplicate.orientation_out = None
            step_duplicate.turning = True
            retval.append(step_duplicate)
        
            step_original.orientation_in = step_original.orientation_in.rotate(pi)
        
        retval.append(step_original)

    return retval


def duplicate_postpend_direction(solution):
    retval  = []
    for s in solution:
        step_original = copy(s)
        step_duplicate = None

        if step_original.orientation_in.angle_between(step_original.orientation_out) > 0.9 * pi:
            step_duplicate = copy(s)
            step_duplicate.type = PointType.DUPLICATE
            step_duplicate.orientation_in = step_original.orientation_out
            step_duplicate.orientation_out = step_original.orientation_out

            step_original.orientation_out = None

        retval.append(step_original)
        if step_duplicate:
            retval.append(step_duplicate)
    
    return retval




