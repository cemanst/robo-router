import copy
import random

from algorithm2.distance import euclidean_dist


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


def fix_init_point_connection(alns_sol, rows):
    first_row = rows[0]
    last_row = rows[len(rows)-1]

    k1 = (last_row.a.y - first_row.a.y) / (last_row.a.x - first_row.a.x)
    n1 = last_row.a.y - k1*last_row.a.x

    k2 = (last_row.b.y - first_row.b.y) / (last_row.b.x - first_row.b.x)
    n2 = last_row.b.y - k2 * last_row.b.x

    init_p = alns_sol[0]
    if k1*init_p.x + n1 <= init_p.y <= k2*init_p.x + n2 or k1 * init_p.x + n1 >= init_p.y >= k2 * init_p.x + n2:
        if euclidean_dist(first_row.a, init_p) <= euclidean_dist(last_row.a, init_p):
            closer_row = first_row
        else:
            closer_row = last_row

        if euclidean_dist(closer_row.a, init_p) + euclidean_dist(closer_row.a, alns_sol[1]) \
                <= euclidean_dist(closer_row.b, init_p) + euclidean_dist(closer_row.b, alns_sol[1]):
            alns_sol.insert(1, closer_row.a)
        else:
            alns_sol.insert(1, closer_row.b)

        if euclidean_dist(closer_row.a, init_p) + euclidean_dist(closer_row.a, alns_sol[len(alns_sol)-1]) <= euclidean_dist(
                closer_row.b, init_p) + euclidean_dist(closer_row.b, alns_sol[len(alns_sol)-1]):
            alns_sol.insert(len(alns_sol)-1, closer_row.a)
        else:
            alns_sol.insert(len(alns_sol)-1, closer_row.b)
