import random
import os

import pandas as pd
import time
import json
from pyproj import Transformer

from algorithm2.alns import alns
from algorithm2.greedy import run_greedy
from algorithm2.prepare_reduced_graph import prepare_data, generate_graph

from data_reader import read_data, PointType

from postprocessing.complete_solution import create_complete_sol, extract_copies
from postprocessing.fixing import fix_init_point_connection
from postprocessing.smoothing import insert_sinuosities
from postprocessing.orientation import assign_orientation, duplicate_prepend_rotation, duplicate_postpend_direction

from watering.single_pass_watering import single_pass_watering
from watering.double_pass_watering import double_pass_watering

import matplotlib.pyplot as plt

from datetime import datetime
random.seed(datetime.now().timestamp())

def print_sol_csv(sol, D, P, casename, filename="results"):
    res = pd.DataFrame(columns = ['x', 'y'])

    for i in range(len(sol)-1):
        res.loc[len(res)] = [sol[i].x, sol[i].y]
        path = P[sol[i].id, sol[i+1].id]
        if path is not None:
            for p in path:
                res.append([p.x, p.y])

    res.loc[len(res)] = [sol[len(sol)-1].x, sol[len(sol)-1].y] # cycle back to last point

    os.makedirs(f'./data/out/paths/{casename}', exist_ok = True)
    res.to_csv(f'./data/out/paths/{casename}/{filename}.csv')


def print_sol(sol, D, P, casename, filename="results"):

    transformer = Transformer.from_crs(32634, 4326)

    res = []
    id_cnt = 0
    for i in range(len(sol)-1):
        pfp = {}
        pfp["idPoint"] = id_cnt
        tmp = transformer.transform(sol[i].x, sol[i].y)
        pfp["x"] = sol[i].x
        pfp["y"] = sol[i].y
        pfp["latitude"] = round(tmp[0], 10)
        pfp["longitude"] = round(tmp[1], 10)
        if sol[i].type == PointType.SAMPLE:
            pfp["pointType"] = 'U'  
            pfp["samplingSide"] = "RIGHT"
        else: 
            pfp["pointType"] = 'P'
            pfp["samplingSide"] = "none"
        pfp["orientation"] = sol[i].orientation_in.angle()

        res.append(pfp)
        id_cnt += 1

        # path = P[sol[i].id, sol[i+1].id]
        # if path is not None:
        #     for p in path:
        #         pfp2 = {}
        #         pfp2["idPoint"] = id_cnt
        #         tmp = transformer.transform(p.x, p.y)
        #         pfp2["latitude"] = round(tmp[0], 10)
        #         pfp2["longitude"] = round(tmp[1], 10)
        #         pfp2["pointType"] = 'P'
        #         res.append(pfp2)
        #         id_cnt += 1

    pfp3 = {}
    pfp3["idPoint"] = id_cnt
    tmp = transformer.transform(sol[-1].x, sol[-1].y)
    pfp3["x"] = sol[-1].x
    pfp3["y"] = sol[-1].y
    pfp3["latitude"] = round(tmp[0], 10)
    pfp3["longitude"] = round(tmp[1], 10)
    pfp3["pointType"] = 'H'
    pfp3["samplingSide"] = "none"
    pfp3["orientation"] = sol[-1].orientation_in.angle()

    res.append(pfp3)
    id_cnt += 1

    json_str = json.dumps(res)
    os.makedirs(f'./data/out/paths/{casename}', exist_ok = True)
    with open(f'./data/out/paths/{casename}/{filename}.json', "w") as outfile:
        outfile.write(json_str)


def check_solution(rows, collection_points, sol, casename, filename):
    for r in rows:
        plt.plot([r.a.x, r.b.x], [r.a.y, r.b.y], 'r.--')

    for cp in collection_points:
        plt.plot(cp.x, cp.y, 'bs')
        if cp.upperProj is not None:
            plt.plot(cp.upperProj.x, cp.upperProj.y, 'kx')
        # if cp.lowerProj is not None:
        #     plt.plot(cp.lowerProj.x, cp.lowerProj.y, 'kx')

        # plt.plot([cp.upperRow.a.x, cp.upperRow.b.x], [cp.upperRow.a.y, cp.upperRow.b.y], 'bo-')
        # plt.plot([cp.lowerRow.a.x, cp.lowerRow.b.x], [cp.lowerRow.a.y, cp.lowerRow.b.y], 'bo-')

    x = []
    y = []
    for sp in sol:
        x.append(sp.x)
        y.append(sp.y)

    plt.plot(x, y, 'g-')

    ind = 1
    for i in range(len(x)):
        if sol[i].type == PointType.SAMPLE:
            plt.annotate(str(ind), (x[i]-130, y[i]+50))
            if not sol[i].turning:
                plt.plot(x[i], y[i], 'go')
            ind += 1
    # for ind, sp in enumerate(sol):
    #     if sp.type in [PointType.SAMPLE, PointType.UPPER]:
    #         plt.annotate(ind, (sp.x, sp.y) )

    for sp in sol:
        if sp.turning:
            plt.plot(sp.x, sp.y, 'md')
        
        # if sp.type == PointType.SINUOSITY:
        #     plt.plot(sp.x, sp.y, 'c+')

    # plt.show()
    os.makedirs(f'./data/out/paths/{casename}', exist_ok = True)
    plt.savefig(f'./data/out/paths/{casename}/{filename}.svg', format="svg")
    plt.clf()


# main for run
def main():
    usecase = "optimize" # options: optimize, singlepass, doublepass
    casename = "with_elev_10" # test2_6mart, with_elev

    random.seed()
    rows, sample_points, init_points = read_data(casename)
    init_point = init_points[random.randrange(len(init_points))]

    # shift_corners(rows)
    # shift_out_init_point(rows, init_point)

    prepare_data(init_point, sample_points, rows)
    graph, D, P = generate_graph(init_point, sample_points)

    if usecase == "optimize":
        # Greedy
        start = time.process_time_ns()
        init_sol = run_greedy(init_point, graph, D)
        # create_complete_sol(init_sol, D, P)
        # fixed_sol = fix_all_inverse(init_sol, sample_points)
        fs, init_cost = create_complete_sol(init_sol, D, P)
        end = time.process_time_ns()
        init_time = (end-start)/1000000000.0
        fix_init_point_connection(fs, rows)
        check_solution(rows, sample_points, fs, casename, filename='init_sol')

        # ALNS
        start = time.process_time_ns()
        alns_sol, alns_cost, weights, trend, init_cost = alns(init_point, sample_points, graph, D, P)
        end = time.process_time_ns()
        alns_time = (end - start) / 1000000000.0

        print('Initial solution found in ' + str(init_time) + ' seconds.')
        print('Initial solution cost: ' + str(init_cost))
        print('Final solution found in ' + str(alns_time) + ' seconds.')
        print('Final solution cost: ' + str(alns_cost))

        fix_init_point_connection(alns_sol, rows)

        alns_sol = insert_sinuosities(alns_sol, rows)
        check_solution(rows, sample_points, alns_sol, casename, filename='best_sol')

        alns_sol = extract_copies(alns_sol)
        alns_sol = assign_orientation(alns_sol)
        alns_sol = duplicate_prepend_rotation(alns_sol)
        alns_sol = duplicate_postpend_direction(alns_sol)
        print_sol(alns_sol, D, P, casename, filename="best_sol")

        x = range(len(trend[1]))
        plt.plot(x, trend[1], 'g-')
        plt.plot(x, trend[2], 'b-')
        # plt.show()
        plt.savefig(f'./data/out/paths/{casename}/trend.svg', format="svg")

    elif usecase == "singlepass":
        # pass all rows once in zik-zak manner
        all_pass_solution = single_pass_watering(init_point, rows)
        
        all_pass_solution = insert_sinuosities(all_pass_solution, rows)
        check_solution(rows, sample_points, all_pass_solution, casename, filename="single_pass_sol")

        all_pass_solution = extract_copies(all_pass_solution)
        all_pass_solution = assign_orientation(all_pass_solution)
        print_sol(all_pass_solution, D, P, casename, filename="single_pass_sol")

    elif usecase == "doublepass":
        # pass all rows once in zik-zak manner
        all_pass_solution = double_pass_watering(init_point, rows)

        all_pass_solution = insert_sinuosities(all_pass_solution, rows)
        check_solution(rows, sample_points, all_pass_solution, casename, filename="double_pass_sol")

        all_pass_solution = extract_copies(all_pass_solution)
        all_pass_solution = assign_orientation(all_pass_solution)
        print_sol(all_pass_solution, D, P, casename, filename="double_pass_sol")

    # for debugging
    pass


# main for tuning and testing
def tuning_main():

    stats = pd.DataFrame(columns=['case', 'init cost', 'best cost', 'improvement', 'sol time'])

    casenames = ["with_elev_10", "with_elev_50", "with_elev"] #"with_elev",

    for casename in casenames:

        rows, sample_points, init_points = read_data(casename)

        for init_point in init_points:
            prepare_data(init_point, sample_points, rows)
            graph, D, P = generate_graph(init_point, sample_points)

            # Greedy
            start = time.process_time_ns()
            init_sol = run_greedy(init_point, graph, D)
            # create_complete_sol(init_sol, D, P)
            # fixed_sol = fix_all_inverse(init_sol, sample_points)
            fs, init_cost = create_complete_sol(init_sol, D, P)
            end = time.process_time_ns()
            init_time = (end - start) / 1000000000.0
            fix_init_point_connection(fs, rows)
            # check_solution(rows, sample_points, fs, casename, filename='init_sol')

            # ALNS
            start = time.process_time_ns()
            alns_sol, alns_cost, weights, trend, init_cost = alns(init_point, sample_points, graph, D, P)
            end = time.process_time_ns()
            alns_time = (end - start) / 1000000000.0

            # print('Initial solution found in ' + str(init_time) + ' seconds.')
            # print('Initial solution cost: ' + str(init_cost))
            # print('Final solution found in ' + str(alns_time) + ' seconds.')
            # print('Final solution cost: ' + str(alns_cost))

            fix_init_point_connection(alns_sol, rows)

            alns_sol = insert_sinuosities(alns_sol, rows)
            #check_solution(rows, sample_points, alns_sol, casename, filename='best_sol')

            alns_sol = extract_copies(alns_sol)
            alns_sol = assign_orientation(alns_sol)
            alns_sol = duplicate_prepend_rotation(alns_sol)
            alns_sol = duplicate_postpend_direction(alns_sol)
            #print_sol(alns_sol, D, P, casename, filename="best_sol")

            # x = range(len(trend[1]))
            # plt.plot(x, trend[1], 'g-')
            # plt.plot(x, trend[2], 'b-')
            # # plt.show()
            # plt.savefig(f'./data/out/paths/{casename}/trend.svg', format="svg")

            stats.loc[len(stats)] = [casename, init_cost, alns_cost, round(100*(init_cost - alns_cost) / init_cost, 2),  alns_time]

    os.makedirs(f'./data/out', exist_ok=True)
    stats.to_csv(f'./data/out/stats.csv')

    # for debugging
    pass



if __name__ == '__main__':
    main()
