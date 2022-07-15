import copy
import random


def k_opt(k, sol, collection_points):
    lb = random.randint(1, len(sol)-1)
    if lb + k <= len(sol)-1:
        ub = lb + k
    elif lb-k >= 1:
        ub = lb
        lb = ub-k
    else:
        return None

    new_sol = sol[lb:ub+1]
    new_sol.reverse()
    new_sol = sol[:lb] + new_sol
    if ub+1 < len(sol)-1:
        new_sol = new_sol + sol[ub+1:]

    return new_sol


def one_opt(sol, collection_points):
    return k_opt(1, sol, collection_points)


def two_opt(sol, collection_points):
    return k_opt(2, sol, collection_points)


def three_opt(sol, collection_points):
    return k_opt(3, sol, collection_points)


def reverse_proj_point(sol, collection_points):
    idx = random.randint(1, len(sol)-1)
    new_sol = copy.deepcopy(sol)
    if sol[idx].id%2:
        new_sol[idx] = collection_points[idx-1].lowerProj
    else:
        new_sol[idx] = collection_points[idx-1].upperProj

    return new_sol