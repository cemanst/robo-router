from copy import deepcopy

from model.model import PointType, Direction
from model.params import energy_rotation, TURNING_DIST



def create_complete_sol(sol, D, P):

    full = []
    cost = 0
    for i in range(len(sol)):
        full.append(sol[i])
        if i < len(sol) - 1 and P[sol[i].id, sol[i + 1].id] is not None:
            full = full + P[sol[i].id, sol[i + 1].id]
            cost = cost + D[sol[i].id, sol[i + 1].id]
        elif P[sol[i].id, 0] is not None:
            full = full + P[sol[i].id, 0]
            cost = cost + D[sol[i].id, 0]

    full.append(sol[0])

    direction = Direction.NA
    for i in range(len(full)-1):

        if full[i].type == PointType.SAMPLE and direction == Direction.UP:
            cost += TURNING_DIST * energy_rotation

            full[i].turning = True
        else:
            full[i].turning = False

        if full[i].type == PointType.LOWER and full[i+1].type == PointType.SAMPLE:
            direction = Direction.UP
        elif full[i].type == PointType.UPPER and full[i+1].type == PointType.SAMPLE:
            direction = Direction.DOWN
        elif full[i].type == PointType.SAMPLE and full[i+1].type == PointType.SAMPLE:
            if full[i + 1].y > full[i].y:
                direction = Direction.UP
            else:
                direction = Direction.DOWN

    return full, cost

def extract_copies(solution):
    retval = []
    for s in solution:
        retval.append( deepcopy(s) ) # resolved pointing to same auxiliray point issue
    return retval