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
    if ub+1 < len(sol):
        new_sol = new_sol + sol[ub+1:]

    return new_sol


def two_opt(sol, collection_points):
    return k_opt(2, sol, collection_points)


def three_opt(sol, collection_points):
    return k_opt(3, sol, collection_points)


def opt_7(sol, collection_points):
    return k_opt(7, sol, collection_points)


def opt_9(sol, collection_points):
    return k_opt(9, sol, collection_points)


def opt_13(sol, collection_points):
    return k_opt(13, sol, collection_points)


def opt_17(sol, collection_points):
    return k_opt(17, sol, collection_points)


def opt_23(sol, collection_points):
    return k_opt(23, sol, collection_points)


def fix_all_inverse(sol, collection_points):
    init_pos = 1
    new_sol, ub = fix_inverse_from_position(sol, init_pos)
    while ub < len(new_sol):
        new_sol, ub = fix_inverse_from_position(new_sol, ub)
    return new_sol


def fix_random_inverse(sol, collection_points):
    init_pos = random.randint(1, len(sol)-1)
    new_sol, ub = fix_inverse_from_position(sol, init_pos)
    return new_sol


def fix_inverse_from_position(sol, init_pos):
    i = init_pos
    lb = -1
    ub = -1
    while i < len(sol):
        if sol[i].turning and lb == -1:
            lb = i
        elif not sol[i].turning and lb > -1:
            ub = i
            break
        i += 1

    if lb > -1 and ub == -1:
        ub = len(sol)

    if lb > -1:
        new_sol = sol[lb:ub]
        new_sol.reverse()
        new_sol = sol[:lb] + new_sol
        if ub < len(sol):
            new_sol = new_sol + sol[ub:]
        return new_sol, ub
    else:
        return sol, len(sol)


def k_randomize(k, sol, collection_points):
    lb = random.randint(1, len(sol)-1)
    if lb + k <= len(sol)-1:
        ub = lb + k
    elif lb-k >= 1:
        ub = lb
        lb = ub-k
    else:
        return None

    new_sol = sol[lb:ub+1]
    random.shuffle(new_sol)
    new_sol = sol[:lb] + new_sol
    if ub+1 < len(sol):
        new_sol = new_sol + sol[ub+1:]

    return new_sol


def shuffle_2(sol, collection_points):
    return k_randomize(2, sol, collection_points)


def shuffle_3(sol, collection_points):
    return k_randomize(3, sol, collection_points)


def shuffle_7(sol, collection_points):
    return k_randomize(7, sol, collection_points)


def shuffle_9(sol, collection_points):
    return k_randomize(9, sol, collection_points)


def shuffle_13(sol, collection_points):
    return k_randomize(13, sol, collection_points)


def shuffle_17(sol, collection_points):
    return k_randomize(17, sol, collection_points)


def shuffle_23(sol, collection_points):
    return k_randomize(23, sol, collection_points)