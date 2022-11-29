from enum import Enum


class Direction(Enum):
    DOWN = 0
    UP = 1


TURNING_DIST = 3


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

    if len(full) >= 1:
        if full[0].y > full[1].y:
            direction = Direction.DOWN
        else:
            direction = Direction.UP

        for i in range(len(full)-1):
            if direction == Direction.DOWN and full[i + 1].y > full[i].y:
                direction = Direction.UP
                cost += TURNING_DIST
                full[i].turning = True
            elif direction == Direction.UP and full[i + 1].y < full[i].y:
                direction = Direction.DOWN
                cost += TURNING_DIST
                full[i].turning = True
            else:
                full[i].turning = False

    return full, cost