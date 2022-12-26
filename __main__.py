import math
import random
import sys

import pandas as pd
import time

from algorithm2.alns import alns
from algorithm2.greedy import run_greedy
from algorithm2.prepare_reduced_graph import prepare_data, generate_graph
from algorithm2.cost_func import create_complete_sol
from data_reader import read_data, PointType
from algorithm2.operators import fix_init_point_connection, fix_all_inverse

import matplotlib.pyplot as plt


def print_sol(sol, D, P):
    res = pd.DataFrame(columns = ['x', 'y'])

    for i in range(len(sol)-1):
        res.loc[len(res)] = [sol[i].x, sol[i].y]
        path = P[sol[i].id, sol[i+1].id]
        if path is not None:
            for p in path:
                res.append([p.x, p.y])

    res.loc[len(res)] = [sol[len(sol)-1].x, sol[len(sol)-1].y]

    res.to_csv('./data/result.csv')


def check_solution(rows, collection_points, sol, fig_name):
    for r in rows:
        plt.plot([r.a.x, r.b.x], [r.a.y, r.b.y], 'ro--')

    for cp in collection_points:
        plt.plot(cp.x, cp.y, 'bo')
        if cp.upperProj is not None:
            plt.plot(cp.upperProj.x, cp.upperProj.y, 'yo')
        if cp.lowerProj is not None:
            plt.plot(cp.lowerProj.x, cp.lowerProj.y, 'yo')

        # plt.plot([cp.upperRow.a.x, cp.upperRow.b.x], [cp.upperRow.a.y, cp.upperRow.b.y], 'bo-')
        # plt.plot([cp.lowerRow.a.x, cp.lowerRow.b.x], [cp.lowerRow.a.y, cp.lowerRow.b.y], 'bo-')

    x = []
    y = []
    for sp in sol:
        x.append(sp.x)
        y.append(sp.y)

    plt.plot(x, y, 'go-')

    ind = 1
    for i in range(len(x)):
        if sol[i].type == PointType.SAMPLE or sol[i].type == PointType.UPPER:
            plt.annotate(str(ind), (x[i], y[i]))
            ind += 1

    for sp in sol:
        if sp.turning:
            plt.plot(sp.x, sp.y, 'mo')

    # plt.show()
    plt.savefig('./data/' + fig_name + '.svg', format="svg")
    plt.clf()


# main for run
def main():
    rows, sample_points, init_points = read_data()

    random.seed()
    init_point = init_points[random.randrange(len(init_points))]

    prepare_data(init_point, sample_points, rows)
    graph, D, P = generate_graph(init_point, sample_points)

    # Greedy
    start = time.process_time_ns()
    init_sol = run_greedy(init_point, graph, D)
    create_complete_sol(init_sol, D, P)
    fixed_sol = fix_all_inverse(init_sol, sample_points)
    fs, init_cost = create_complete_sol(fixed_sol, D, P)
    end = time.process_time_ns()
    init_time = (end-start)/1000000000.0
    fix_init_point_connection(fs, rows)
    check_solution(rows, sample_points, fs, 'init_sol')
    print('Initial solution found in ' + str(init_time) + ' seconds.')
    print('Initial solution cost: ' + str(init_cost))

    # ALNS
    start = time.process_time_ns()
    alns_sol, alns_cost, weights, trend = alns(init_point, sample_points, graph, D, P)
    end = time.process_time_ns()
    alns_time = (end - start) / 1000000000.0
    print('Final solution found in ' + str(alns_time) + ' seconds.')
    print('Final solution cost: ' + str(alns_cost))

    fix_init_point_connection(alns_sol, rows)

    check_solution(rows, sample_points, alns_sol, 'best_sol')
    print_sol(alns_sol, D, P)

    x = range(len(trend[1]))
    plt.plot(x, trend[1], 'g-')
    plt.plot(x, trend[2], 'b-')
    # plt.show()
    plt.savefig('./data/trend.svg', format="svg")

    # for debugging
    pass


# main for tuning and testing
def main_for_tuning():
    rows, sample_points, init_points = read_data()

    res = pd.DataFrame(columns = ['init_cost', 'init_elapsed', 'final_cost', 'final_elapsed', 'improvement'])
    best_sol = None
    best_cost = sys.float_info.max

    for init_point in init_points:
        prepare_data(init_point, sample_points, rows)
        graph, D, P = generate_graph(init_point, sample_points)

        # Greedy
        start = time.process_time_ns()
        sol = run_greedy(init_point, graph, D)
        init_sol, init_cost = create_complete_sol(sol, D, P)
        end = time.process_time_ns()
        init_time = (end-start)/1000000000.0

        # ALNS
        start = time.process_time_ns()
        sol, weights, trend = alns(init_point, sample_points, graph, D, P)
        # check_P(rows, sample_points, sol, P)
        alns_sol, alns_cost = create_complete_sol(sol, D, P)
        end = time.process_time_ns()
        alns_time = (end - start) / 1000000000.0

        if best_cost > alns_cost:
            best_cost = alns_cost
            best_sol = alns_sol

        res.loc[len(res)] = [init_cost, init_time, alns_cost, alns_time, (init_cost-alns_cost) / init_cost]

    check_solution(rows, sample_points, best_sol, 'best_sol')
    print_sol(best_sol, D, P)

    res.to_csv('./data/best_solutions.csv')

    # x = range(len(trend[1]))
    # plt.plot(x, trend[1], 'g-')
    # plt.plot(x, trend[2], 'b-')
    # # plt.show()
    # plt.savefig('./data/trend.svg', format="svg")

    # for debugging
    pass



if __name__ == '__main__':
    main()
