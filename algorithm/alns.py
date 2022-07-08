import copy
import math

import random
import sys

from algorithm.alns_params import *
from algorithm.greedy import run_greedy


def add_new_solution(non_dominated_sols, new_sol):
    for sol in non_dominated_sols:
        the_same = True
        for i in range(len(sol.harvest_week)):
            if sol.harvest_week[i] != new_sol.harvest_week[i]:
                the_same = False
                break
            if new_sol.scenario == 2 and sol.silo_capacity != new_sol.silo_capacity:
                the_same = False
        if the_same:
            return
    non_dominated_sols.append(new_sol)


def alns(init_point, collection_points, rows):

    init_sol = run_greedy(init_point, collection_points, rows)
    operators = []
    oper_weights = [1 / len(operators)] * len(operators)
    non_dominated_sols = [init_sol]

    # create temperatures for simulated annealing
    temperatures = create_temperatures(M, p0, pf, delta)

    selected_oper = random.randint(0, len(operators))

    curr_sol = init_sol

    a = 1
    for i in range(len(temperatures)):
        if temperatures[i] < Tf:
            print('Temperature ' + str(temperatures[i]) + ' is below threshold.')
            break

        print('Processed temperature: ' + str(temperatures[i]))
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

            new_sol = copy.deepcopy(curr_sol)
            operators[selected_oper](new_sol)
            if new_sol is None:
                # Inapplicable operator for this network state, repeat iteration
                continue

            non_dominated = True
            for sol in non_dominated_sols:
                if sol.dominates(new_sol):
                    non_dominated = False
                    break

            reward = reward_base
            if non_dominated:
                non_dominated_sols = [old_sol for old_sol in non_dominated_sols if not new_sol.dominates(old_sol)]
                add_new_solution(non_dominated_sols, new_sol)
                curr_sol = new_sol
            else:
                r = random.random()
                reward = -reward_base
                if selected_oper == len(operators)-1:   #Operator changing capacity
                    if r < 0.1:
                        #print('   Accept capacity change')
                        curr_sol = new_sol
                else:                                   #All other operators
                    #print('   Accept probability ' + str(round(math.exp(-Solution.calc_increase(new_sol, curr_sol) / temperatures[i]), 3)))
                    if r < math.exp(-Solution.calc_increase(new_sol, curr_sol) / temperatures[i]):
                        curr_sol = new_sol

            for j in range(len(operators)):
                if j == selected_oper:
                    oper_weights[j] += reward
                    if oper_weights[j] < min_select_poss:
                        oper_weights[j] = min_select_poss
                    break

            print('Iteration no. done: ' + str(iter_cnt+1))
            sys.stdout.flush()

    return init_sol, non_dominated_sols, oper_weights


def create_temperatures(M, p0, pf, delta):
    temperatures = []
    for i in range(M):
        temperatures.append(-delta / (math.log(p0 + (pf - p0) * (i + 1) / M)))
    return temperatures
