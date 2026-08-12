import math

import sys

from algorithm2.alns_params import *
from algorithm2.greedy import run_greedy
from algorithm2.alns_operators import *

from postprocessing.complete_solution import create_complete_sol
from postprocessing.fixing import fix_all_inverse
from algorithm2.aco_utils import construct_sol
import numpy as np

 
# dodati elitizam za bolju eksploataciju 

def aco(init_point,graph, collection_points, D, P, init_sol,max_iter=3000,num_ants=50):
    # inicijalizacija na pocetnu tacku 
    ants = initialize_ants(init_point, num_ants)

    # ovde se prosledjuje greedy 
    fixed_sol = fix_all_inverse(init_sol, collection_points)
    fs, init_cost = create_complete_sol(fixed_sol, D, P)
    best_sol = init_sol
    best_cost = init_cost
    pheromone = np.ones((len(collection_points)+1,len(collection_points)+1))*1e-3

    # max iter : 1000
    trend = ([],[])
    for iteration in range(max_iter):
        best_iter_cost = init_cost
        best_iter_sol = init_sol

        if np.mod(iteration,100)==0:
            print(f"iteracija:{iteration} od {max_iter} \n")

        #print("USAO U ITERACIJU")
        # kroz sve mrave u koloniji : 100
        for ant in ants:
            #print("USAO U MRAVA ")
            construct_sol(ant, D, P,pheromone,collection_points)
            #apdejt najboljeg resenja: 
            if ant.cost < best_iter_cost:
                best_iter_sol = ant.solution
                best_iter_cost = ant.cost
        update_pheromones(ants, pheromone)
        if best_iter_cost<best_cost:
            best_sol = best_iter_sol
            best_cost = best_iter_cost
        trend[0].append(best_iter_cost)
        trend[1].append(best_cost)
        # resenje po iteraciji i globalno najbolje resenje 
        

    return best_sol, best_cost,init_cost,trend


def initialize_ants(init_point, num_ants):
    ants = []
    for i in range(num_ants):
        ant = Ant(init_point)  
        ants.append(ant)
    return ants


def update_pheromones(ants,pheromone,ro=0.5):
    pheromone = pheromone * (1-ro)
    delta(pheromone,ants)

    return pheromone 

def delta(pheromone,ants,Q=2):
    for ant in ants:
        for i in range(len(pheromone)-1):
            pheromone[ant.solution[i],ant.solution[i+1]] += Q/ant.cost
        pheromone[ant.solution[-1],ant.solution[0]] += Q/ant.cost
    

class Ant:
    def __init__(self, current_point):
        self.current_point = current_point
        self.solution = None  
        self.cost = None