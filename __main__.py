import pandas as pd

from algorithm.greedy import run_greedy
from data_reader import read_data


def print_sol(sol, D, P):
    res = pd.DataFrame(columns = ['x', 'y'])

    for i in range(len(sol)-1):
        res.append([sol[i].x, sol[i].y])
        path = P[sol[i].id, sol[i+1].id]
        for p in path:
            res.append([p.x, p.y])
    res.append([sol[len(sol)-1].x, sol[len(sol)-1].y])

    res.to_csv('/data/out.csv')


def main():
    rows, sample_points, init_point = read_data()
    sol, D, P = run_greedy(init_point, sample_points, rows)
    print_sol(sol, D, P)


if __name__ == '__main__':
    main()
