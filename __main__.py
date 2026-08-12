import random
import os

import pandas as pd
import time
import json
from pyproj import Transformer

from algorithm2.alns import alns
from algorithm2.greedy import run_greedy
from algorithm2.prepare_reduced_graph import prepare_data, generate_graph
from algorithm2.vns import vns
from algorithm2.aco import aco
from algorithm2.ga import ga
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

def run_alns(casename, init_point, sample_points, rows):
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

    return alns_cost, init_cost, alns_time


def run_vns(casename, init_point, sample_points, rows):
    prepare_data(init_point, sample_points, rows)
    graph, D, P = generate_graph(init_point, sample_points)

    start = time.process_time_ns()
    init_sol = run_greedy(init_point, graph, D)
    # create_complete_sol(init_sol, D, P)
    # fixed_sol = fix_all_inverse(init_sol, sample_points)
    fs, init_cost = create_complete_sol(init_sol, D, P)
    end = time.process_time_ns()
    init_time = (end - start) / 1000000000.0
    fix_init_point_connection(fs, rows)
    check_solution(rows, sample_points, fs, casename, filename='init_sol')

    # VNS
    start = time.process_time_ns()
    vns_sol, vns_cost, init_cost = vns(init_point, sample_points, graph, D, P)
    end = time.process_time_ns()
    vns_time = (end - start) / 1000000000.0

    print('Initial solution found in ' + str(init_time) + ' seconds.')
    print('Initial solution cost: ' + str(init_cost))
    print('Final solution found in ' + str(vns_time) + ' seconds.')
    print('Final solution cost: ' + str(vns_cost))

    fix_init_point_connection(vns_sol, rows)

    vns_sol = insert_sinuosities(vns_sol, rows)
    check_solution(rows, sample_points, vns_sol, casename, filename='best_sol')

    vns_sol = extract_copies(vns_sol)
    vns_sol = assign_orientation(vns_sol)
    vns_sol = duplicate_prepend_rotation(vns_sol)
    vns_sol = duplicate_postpend_direction(vns_sol)
    print_sol(vns_sol, D, P, casename, filename="best_sol")

    return vns_cost, init_cost, vns_time

# ACO 
def run_aco(casename,init_point,sample_points,rows):
    prepare_data(init_point, sample_points, rows)
    graph, D, P = generate_graph(init_point, sample_points)

    start = time.process_time_ns()
    init_sol = run_greedy(init_point, graph, D)
    fs, init_cost = create_complete_sol(init_sol, D, P)
    end = time.process_time_ns()
    init_time = (end - start) / 1000000000.0
    fix_init_point_connection(fs, rows)
    check_solution(rows, sample_points, fs, casename, filename='init_sol')


    start = time.process_time_ns()
    aco_sol,aco_cost,init_cost,trend = aco(init_point,graph,sample_points,D,P,init_sol)
    end = time.process_time_ns()
    aco_time = (end-start)/1000000000.0

    print(f'solution: {aco_sol}')

    aco_sol = sorted(sample_points, key=lambda x: aco_sol.index(x.id))
    
    fix_init_point_connection(aco_sol, rows)

    aco_sol = insert_sinuosities(aco_sol, rows)
    check_solution(rows, sample_points, aco_sol, casename, filename='best_sol')

    aco_sol = extract_copies(aco_sol)
    aco_sol = assign_orientation(aco_sol)
    aco_sol = duplicate_prepend_rotation(aco_sol)
    aco_sol = duplicate_postpend_direction(aco_sol)
    print_sol(aco_sol, D, P, casename, filename="best_sol")


    x = range(len(trend[1]))
    plt.plot(x, trend[0], 'g-')
    plt.plot(x, trend[1], 'b-')
    plt.xlabel('iteracija')
    plt.ylabel('cost funkcija')
    plt.legend(['trenutna ','najbolja'])
    plt.show()

    return aco_cost,init_cost,aco_time,init_time
# Genetic Algorithm 
def run_ga(casename,init_point,sample_points,rows):
    prepare_data(init_point, sample_points, rows)
    graph, D, P = generate_graph(init_point, sample_points)

    start = time.process_time_ns()
    init_sol = run_greedy(init_point, graph, D)
    fs, init_cost = create_complete_sol(init_sol, D, P)
    print(f"init cost : {init_cost}")
    init_sol_list = list(point.id for point in init_sol)
    #init_sol_list = sorted(sample_points,key = lambda x: init_sol.index(x.id))

    print (f"init sol : {init_sol_list}")
    end = time.process_time_ns()
    init_time = (end - start) / 1000000000.0
    fix_init_point_connection(fs, rows)
    check_solution(rows, sample_points, fs, casename, filename='init_sol')


    start = time.process_time_ns()
    ga_sol,ga_cost,best_list,curr_list = ga(D,init_sol,sample_points,P,num_generations=1000,population_size=100,mutation_rate=0.1)
    print(ga_cost)
    end = time.process_time_ns()
    ga_time = (end-start)/1000000000.0
    ga_sol = list(point.id for point in ga_sol)
    print(ga_sol)
    ga_sol = sorted(sample_points, key=lambda x: ga_sol.index(x.id))
    
    fix_init_point_connection(ga_sol, rows)

    ga_sol = insert_sinuosities(ga_sol, rows)
    check_solution(rows, sample_points, ga_sol, casename, filename='best_sol')

    ga_sol = extract_copies(ga_sol)
    ga_sol = assign_orientation(ga_sol)
    ga_sol = duplicate_prepend_rotation(ga_sol)
    ga_sol = duplicate_postpend_direction(ga_sol)
    print_sol(ga_sol, D, P, casename, filename="best_sol")

    x = range(len(best_list))

    plt.plot(x, curr_list, 'g-')
    plt.plot(x, best_list, 'b-')
    plt.xlabel('iteracija')
    plt.ylabel('cost funkcija')
    plt.legend(['trenutna ','najbolja'])
    plt.show()

    return ga_cost,init_cost,ga_time,init_time


# main for run
def main():
    usecase = "optimizeACO" # options: optimizeACO, optimizeALNS, optimizeVNS, singlepass, doublepass
    casename = "with_elev_50" # test2_6mart, with_elev, with_elev_10, with_elev_50

    random.seed()
    rows, sample_points, init_points = read_data(casename)
    init_point = init_points[random.randrange(len(init_points))]

    # shift_corners(rows)
    # shift_out_init_point(rows, init_point)

    prepare_data(init_point, sample_points, rows)
    graph, D, P = generate_graph(init_point, sample_points)

    if usecase == "optimizeGA":
        acs,ics,ats = [],[],[]
        for init_point in init_points:
            ga_cost,init_cost,ga_time,init_time = run_ga(casename,init_point,sample_points,rows)
            acs.append(ga_cost)
            ics.append(init_cost)
            ats.append(ga_time)
            df_out= pd.DataFrame()
            df_out['GA cost'] = acs
            df_out['Init cost'] = ics
            df_out['GA time'] = ats
            print(f"ga cost: {ga_cost }\ninit cost :{init_cost}")
           # df_out.to_csv(f'.data/out/paths/{casename}/ga_results.csv')

    elif usecase== "optimizeACO":
        acs,ics,ats = [],[],[]
        for init_point in init_points:
            aco_cost,init_cost,aco_time,init_time = run_aco(casename,init_point,sample_points,rows)
            acs.append(aco_cost)
            ics.append(init_cost)
            ats.append(aco_time)
            df_out = pd.DataFrame()
            df_out['ACO cost'] = acs
            df_out['Init cost'] = ics
            df_out['ACO time'] = ats
            print(f"aco cost : {aco_cost} \ninit cost : {init_cost}")
            df_out.to_csv(f'./data/out/paths/{casename}/aco_results.csv')
    elif usecase == "optimizeALNS":
        vcs, ics, vts = [], [], []
        for init_point in init_points:
            alns_cost, init_cost, alns_time = run_alns(casename, init_point, sample_points, rows)
            vcs.append(alns_cost)
            ics.append(init_cost)
            vts.append(alns_time)
        df_out = pd.DataFrame()
        df_out['VNS cost'] = vcs
        df_out['Init cost'] = ics
        df_out['VNS time'] = vts
        df_out.to_csv(f'./data/out/paths/{casename}/alns_results.csv')

    elif usecase == "optimizeVNS":
        vcs, ics, vts = [], [], []
        for init_point in init_points:
            vns_cost, init_cost, vns_time = run_vns(casename, init_point, sample_points, rows)
            vcs.append(vns_cost)
            ics.append(init_cost)
            vts.append(vns_time)
        df_out = pd.DataFrame()
        df_out['VNS cost'] = vcs
        df_out['Init cost'] = ics
        df_out['VNS time'] = vts
        df_out.to_csv(f'./data/out/paths/{casename}/vns_results.csv')



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

        for iter, init_point in enumerate(init_points):
            print(f"{casename}, iteration {iter}")
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
