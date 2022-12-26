import math

import sys

from algorithm2.alns_params import *
from algorithm2.greedy import run_greedy
from algorithm2.operators import *
from algorithm2.cost_func import create_complete_sol

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


def alns(init_point, collection_points, graph, D, P):

    init_sol = run_greedy(init_point, graph, D)
    # init_sol = create_best(init_point, collection_points)
    # operators = [two_opt, three_opt, opt_7, opt_9, opt_13, opt_17, opt_23,
                # shuffle_2, shuffle_3, shuffle_7, shuffle_9, shuffle_13, shuffle_17, shuffle_23]
    operators = [two_opt, three_opt, opt_7]
    oper_weights = [1 / len(operators)] * len(operators)
    create_complete_sol(init_sol, D, P)
    fixed_sol = fix_all_inverse(init_sol, collection_points)
    fs, best_cost = create_complete_sol(fixed_sol, D, P)

    # create temperatures for simulated annealing
    temperatures = create_temperatures(M, p0, pf, delta)
    # temperatures = create_temperatures_2(M, Ts, Tf)

    selected_oper = random.randint(0, len(operators))

    curr_sol = init_sol
    best_sol = init_sol
    curr_cost = best_cost

    trend = ([],[],[])
    trend[0].append(temperatures[0])
    trend[1].append(curr_cost)
    trend[2].append(best_cost)

    a = 1
    for i in range(len(temperatures)):
        if temperatures[i] < Tf:
            print('Temperature ' + str(temperatures[i]) + ' is below threshold.')
            break

        for iter_cnt in range(sa_iter_num):
            prob_sum = 0
            summed_probs = []
            for j in range(len(operators)):
                prob_sum += oper_weights[j]
                summed_probs.append(prob_sum)

            r = prob_sum * random.random()

            for j in range(len(operators)):
                if r <= summed_probs[j]:
                    selected_oper = j
                    break

            new_sol = operators[selected_oper](curr_sol, collection_points)
            if new_sol is None:
                # Inapplicable operator for this network state, repeat iteration
                continue

            # this will determine what are the turning points
            create_complete_sol(new_sol, D, P)
            # now, manually manually reverse adjacent turning points... (Basically, a repair operator.)
            fixed_sol = fix_all_inverse(new_sol, collection_points)
            # ... and calculate the cost of the new solution
            fs, new_cost = create_complete_sol(fixed_sol, D, P)

            if new_cost < curr_cost:
                curr_sol = new_sol
                curr_cost = new_cost
                reward = reward_base
            else:
                reward = -reward_base
                r = random.random()
                if r < math.exp((curr_cost - new_cost) / temperatures[i]):
                    curr_sol = new_sol
                    curr_cost = new_cost

            for j in range(len(operators)):
                if j == selected_oper:
                    oper_weights[j] += reward
                    if oper_weights[j] < min_select_poss:
                        oper_weights[j] = min_select_poss
                    break

            if new_cost < best_cost:
                best_sol = new_sol
                best_cost = new_cost

            # print('Iteration no. done: ' + str(iter_cnt+1))
            sys.stdout.flush()
            trend[0].append(temperatures[i])
            trend[1].append(curr_cost)
            trend[2].append(best_cost)

        print('Processed temperature: ' + str(temperatures[i]))

    create_complete_sol(best_sol, D, P)
    fixed_sol = fix_all_inverse(best_sol, collection_points)
    full_sol, best_full_cost = create_complete_sol(fixed_sol, D, P)

    return full_sol, best_full_cost, oper_weights, trend

