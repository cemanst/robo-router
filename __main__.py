import pandas as pd

from algorithm.greedy import run_greedy
from algorithm.prepare_data import prepare_data
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

        plt.plot([cp.upperRow.a.x, cp.upperRow.b.x], [cp.upperRow.a.y, cp.upperRow.b.y], 'bo-')
        plt.plot([cp.lowerRow.a.x, cp.lowerRow.b.x], [cp.lowerRow.a.y, cp.lowerRow.b.y], 'bo-')

    x = []
    y = []
    for sp in sol:
        x.append(sp.x)
        y.append(sp.y)

    plt.plot(x, y, 'go-')

    plt.show()


def main():
    rows, sample_points, init_point = read_data()
    prepare_data(init_point, sample_points, rows)
    sol, D, P = run_greedy(init_point, sample_points)
    check_solution(rows, sample_points, sol)
    print_sol(sol, D, P)


if __name__ == '__main__':
    main()
