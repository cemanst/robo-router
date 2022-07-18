import math

import random
import sys

from algorithm.alns_params import *
from algorithm.greedy import run_greedy, create_complete_sol, create_best
from algorithm.operators import *


def create_temperatures(M, p0, pf, delta):
    temperatures = []
    for i in range(M):
        temperatures.append(-delta / (math.log(p0 + (pf - p0) * (i + 1) / M)))
    return temperatures


def alns(init_point, collection_points, graph, D, P):

    # init_sol = run_greedy(init_point, graph, D)
    init_sol = create_best(init_point, collection_points)
    operators = [one_opt, two_opt, three_opt, reverse_proj_point]
    oper_weights = [1 / len(operators)] * len(operators)
    best_sol = init_sol
    fs, best_cost = create_complete_sol(init_sol, D, P)

    # create temperatures for simulated annealing
    temperatures = create_temperatures(M, p0, pf, delta)

    selected_oper = random.randint(0, len(operators))

    curr_sol = init_sol
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

            fs, new_cost = create_complete_sol(new_sol, D, P)

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

    return best_sol, oper_weights, trend

