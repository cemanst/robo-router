import math

import sys

from algorithm2.alns_params import *
from algorithm2.greedy import run_greedy
from algorithm2.alns_operators import *

from algorithm2.route_evaluation import evaluate_route

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


def alns(init_point, collection_points, graph, D, P, *, max_evaluations=None):

    init_sol = run_greedy(init_point, graph, D)
    # init_sol = create_best(init_point, collection_points)
    # operators = [two_opt, three_opt, opt_7, opt_9, opt_13, opt_17, opt_23,
                # shuffle_2, shuffle_3, shuffle_7, shuffle_9, shuffle_13, shuffle_17, shuffle_23]
    operators = [two_opt, three_opt, opt_7]
    oper_weights = [1 / len(operators)] * len(operators)
    _, _, init_cost = evaluate_route(init_sol, collection_points, D, P)

    # create temperatures for simulated annealing
    temperatures = create_temperatures(M, p0, pf, delta)
    cooling = [temperature for temperature in temperatures if temperature >= Tf]

    selected_oper = random.randint(0, len(operators))

    curr_sol = init_sol
    curr_cost = init_cost
    best_sol = init_sol
    best_cost = init_cost

    trend = ([],[],[])
    trend[0].append(temperatures[0])
    trend[1].append(curr_cost)
    trend[2].append(best_cost)

    a = 1
    for i in range(len(temperatures)):
        if max_evaluations is not None and len(trend[2]) - 1 >= max_evaluations:
            break
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

            temperature = temperatures[i]
            if max_evaluations is not None:
                # Spread the original cooling schedule across the scored candidates.
                fraction = (len(trend[2]) - 1) / max(1, max_evaluations - 1)
                temperature = cooling[round(fraction * (len(cooling) - 1))]
            _, _, new_cost = evaluate_route(new_sol, collection_points, D, P)

            if new_cost < curr_cost:
                curr_sol = new_sol
                curr_cost = new_cost
                reward = reward_base
            else:
                reward = -reward_base
                # r = random.random()
                r = random.random() if not DEBUG else 0
                if r < math.exp((curr_cost - new_cost) / temperature):
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
            trend[0].append(temperature)
            trend[1].append(curr_cost)
            trend[2].append(best_cost)
            if max_evaluations is not None and len(trend[2]) - 1 >= max_evaluations:
                break

        print('Processed temperature: ' + str(temperatures[i]))

    _, full_sol, best_full_cost = evaluate_route(best_sol, collection_points, D, P)

    return full_sol, best_full_cost, oper_weights, trend, init_cost
