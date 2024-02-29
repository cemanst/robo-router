import math
import itertools
import sys

from algorithm2.alns_params import *
from algorithm2.greedy import run_greedy
from algorithm2.vns_operators import *

from postprocessing.complete_solution import create_complete_sol
from postprocessing.fixing import fix_all_inverse

def create_temperatures(M, p0, pf, delta):
    temperatures = []
    for i in range(M):
        temperatures.append(-delta / (math.log(p0 + (pf - p0) * (i + 1) / M)))
    return temperatures

def create_temperatures_2(M, Ts, Tf):
    temperatures = []
    for i in range(M):
        temperatures.append(Ts - i*(Ts-Tf)/M)
    return temperatures


def vns(init_point, collection_points, graph, D, P):

    init_sol = run_greedy(init_point, graph, D)
    # init_sol = create_best(init_point, collection_points)
    # operators = [two_opt, three_opt, opt_7, opt_9, opt_13, opt_17, opt_23,
                # shuffle_2, shuffle_3, shuffle_7, shuffle_9, shuffle_13, shuffle_17, shuffle_23]
    oper_k = [2, 3, 7]
    create_complete_sol(init_sol, D, P)
    fixed_sol = fix_all_inverse(init_sol, collection_points)
    fs, init_cost = create_complete_sol(fixed_sol, D, P)

    best_sol = init_sol
    best_cost = init_cost

    all_pairs = itertools.combinations(list(range(len(init_sol))), 2)

    for i in range(len(oper_k)):

        all_combinations = itertools.combinations(all_pairs, oper_k[i])
        candidate_sol = best_sol
        candidate_cost = best_cost

        while True:
            for comb in all_combinations:

                new_sol = k_opt(best_sol, comb)
                if new_sol is None:
                    # Inapplicable operator for this network state, repeat iteration
                    continue

                # this will determine what are the turning points
                create_complete_sol(new_sol, D, P)
                # now, manually manually reverse adjacent turning points... (Basically, a repair operator.)
                fixed_sol = fix_all_inverse(new_sol, collection_points)
                # ... and calculate the cost of the new solution
                fs, new_cost = create_complete_sol(fixed_sol, D, P)

                if new_cost < candidate_cost:
                    candidate_sol = new_sol
                    candidate_cost = new_cost

            if candidate_cost < best_cost:
                best_sol = candidate_sol
                best_cost = candidate_cost
            else:
                break


        print('Processed k: ' + str(oper_k[i]))

    create_complete_sol(best_sol, D, P)
    fixed_sol = fix_all_inverse(best_sol, collection_points)
    full_sol, best_full_cost = create_complete_sol(fixed_sol, D, P)

    return full_sol, best_full_cost, init_cost

