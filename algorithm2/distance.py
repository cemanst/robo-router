import numpy as np
from model.params import robot_mass, energy_transition

ELEV_K = 9.81

def euclidean_dist(a, b):
    return np.math.sqrt(pow((a.x - b.x), 2) + pow((a.y - b.y), 2))

def euclidean_dist_with_elev(a, b):
    if a.elev >= 0 and b.elev >= 0:
        elev_diff = b.elev - a.elev
    else:
        elev_diff = 0
    return np.math.sqrt(pow((a.x - b.x), 2) + pow((a.y - b.y), 2)) + ELEV_K * elev_diff


def objective_energy_consumption(a, b):
    """
    Calculate total consumption of energy for trannsition from point a to point b

    Params:
        a, b - Point
    
    Returns:
        float - amount of energy required for transition
                expressed as <consumption per 1m movement> * <traveled distance> + <difference in potential energy for uphill movement>
    """
    elev_diff = b.elev - a.elev
    uphill_work = ELEV_K * robot_mass * max(0, elev_diff) # diff in potential energy should be considered only when robot is going uphill

    x_diff = a.x - b.x
    y_diff = a.y - b.y
    distance = np.math.sqrt(x_diff**2 + y_diff**2 + elev_diff**2)

    return energy_transition * distance # + uphill_work
    


