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


def remove_overheads(sol, P):
    found_swap = True
    while found_swap:
        found_swap = False
        for i in range(len(sol) - 1):
            path = P[sol[i].id, sol[i + 1].id]
            if path is not None and len(path) > 0:
                path.insert(0, sol[i])
                path.append(sol[i+1])
                for j in range(i):
                    if point_on_path(sol[j], path):
                        found_swap = True
                        break
            if found_swap:
                break
        if found_swap:
            swap_pt = sol[j]
            sol.remove(j)
            sol.insert(i+1, swap_pt)


def point_on_path(pt, path):

    if len(path) < 2:
        eps = 0.2
        for i in range(len(path)-1):
            k = (path[i].y - path[i+1].y) / (path[i].x - path[i+1].x)
            n = path[i].y - k * path[i].x
            if abs(k*pt.x + n - pt.y) < eps:
                return True

    return False