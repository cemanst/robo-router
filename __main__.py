import math
import random
import sys

import pandas as pd
import time

from algorithm.alns import alns
from algorithm.greedy import run_greedy, create_best, create_complete_sol
from algorithm.prepare_data import prepare_data, generate_graph
from data_reader import read_data

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
        plt.plot([r.a.x, r.b.x], [r.a.y, r.b.y], 'ro-')

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

    for i in range(len(x)):
        plt.annotate(str(i+1), (x[i], y[i]))

    # plt.show()
    plt.savefig('./data/' + fig_name + '.svg', format="svg")
    plt.clf()


def check_P(rows, collection_points, sol, P):

    for i in range(len(sol)):

        for r in rows:
            plt.plot([r.a.x, r.b.x], [r.a.y, r.b.y], 'ro-')

        for cp in collection_points:
            plt.plot(cp.x, cp.y, 'bo')
            if cp.upperProj is not None:
                plt.plot(cp.upperProj.x, cp.upperProj.y, 'yo')
            if cp.lowerProj is not None:
                plt.plot(cp.lowerProj.x, cp.lowerProj.y, 'yo')

            plt.plot([cp.upperRow.a.x, cp.upperRow.b.x], [cp.upperRow.a.y, cp.upperRow.b.y], 'bo-')
            plt.plot([cp.lowerRow.a.x, cp.lowerRow.b.x], [cp.lowerRow.a.y, cp.lowerRow.b.y], 'bo-')

        x = []
        y = []
        x.append(sol[i].x)
        y.append(sol[i].y)

        if i < len(sol)-1:
            path = P[sol[i].id, sol[i+1].id]
            for p in path:
                x.append(p.x)
                y.append(p.y)

        x.append(sol[i+1].x)
        y.append(sol[i+1].y)

        plt.plot(x, y, 'go-')
        plt.show()
        pass

    plt.show()


def main():
    rows, sample_points, init_points = read_data()

    # random.seed()
    # init_point = init_points[random.randrange(len(init_points))]

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
