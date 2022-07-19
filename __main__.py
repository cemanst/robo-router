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
        res.append([sol[i].x, sol[i].y])
        path = P[sol[i].id, sol[i+1].id]
        for p in path:
            res.append([p.x, p.y])
    res.append([sol[len(sol)-1].x, sol[len(sol)-1].y])

    res.to_csv('./data/out.csv')


def check_solution(rows, collection_points, sol):
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

    plt.show()


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

        path = P[sol[i].id, sol[i+1].id]
        if path is not None:
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
    rows, sample_points, init_point = read_data()
    prepare_data(init_point, sample_points, rows)
    graph, D, P = generate_graph(init_point, sample_points)

    # Greedy
    start = time.process_time_ns()
    sol = run_greedy(init_point, graph, D)
    #check_P(rows, sample_points, sol, P)
    comp_sol, cost = create_complete_sol(sol, D, P)
    end = time.process_time_ns()
    print('Greedy solution found in ' + str((end-start)/1000000000.0) + ' secs.')
    print('Greedy solution cost: ' + str(cost))
    # check_solution(rows, sample_points, comp_sol)

    # Nikolino pametovanje
    start = time.process_time_ns()
    sol = create_best(init_point, sample_points)
    # check_P(rows, sample_points, sol, P)
    comp_sol, cost = create_complete_sol(sol, D, P)
    end = time.process_time_ns()
    print('Good solution found in ' + str((end - start) / 1000000000.0) + ' secs.')
    print('Good solution cost: ' + str(cost))
    # check_solution(rows, sample_points, comp_sol)

    # ALNS
    start = time.process_time_ns()
    sol, weights, trend = alns(init_point, sample_points, graph, D, P)
    # check_P(rows, sample_points, sol, P)
    comp_sol, cost = create_complete_sol(sol, D, P)
    end = time.process_time_ns()
    print('ALNS solution found in ' + str((end - start) / 1000000000.0) + ' secs.')
    print('ALNS solution cost: ' + str(cost))
    check_solution(rows, sample_points, comp_sol)

    x = range(len(trend[1]))
    plt.plot(x, trend[1], 'g-')
    plt.plot(x, trend[2], 'b-')
    plt.show()

    # for debugging
    pass



if __name__ == '__main__':
    main()
