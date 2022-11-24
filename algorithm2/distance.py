import numpy as np

ELEV_K = 9.81

def euclidean_dist(a, b):
    return np.math.sqrt(pow((a.x - b.x), 2) + pow((a.y - b.y), 2))

def euclidean_dist_with_elev(a, b):
    if a.elev >= 0 and b.elev >= 0:
        elev_diff = b.elev - a.elev
    else:
        elev_diff = 0
    return np.math.sqrt(pow((a.x - b.x), 2) + pow((a.y - b.y), 2)) + ELEV_K * elev_diff