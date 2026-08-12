# genetski algoritam 

import numpy as np


import math

import sys

from algorithm2.alns_params import *
from algorithm2.greedy import run_greedy
from algorithm2.alns_operators import *

from postprocessing.complete_solution import create_complete_sol
from postprocessing.fixing import fix_all_inverse
from algorithm2.aco_utils import construct_sol
import numpy as np



class Individual:
    def __init__(self, chromosome,fitness=0):
        self.chromosome = chromosome
        self.fitness = fitness

def create_individual(chromosome,fitness=0):
    return Individual(chromosome,fitness)

def crossover(parent1, parent2,D):
    crossover_point = np.random.randint(1, len(parent1.chromosome))
    child1 = np.concatenate((parent1.chromosome[:crossover_point], [city for city in parent2.chromosome if city not in parent1.chromosome[:crossover_point]]))
    child2 = np.concatenate((parent2.chromosome[:crossover_point], [city for city in parent1.chromosome if city not in parent2.chromosome[:crossover_point]]))

    # pokusaj resenja problema list/np.ndarray nesuglasice
    child1 = child1.tolist()
    child2 = child2.tolist()


    c1 = Individual(child1)
    c2 = Individual(child2)
    f1 = calculate_fitness(c1,D)
    f2 = calculate_fitness(c2,D)
    return Individual(child1,f1), Individual(child2,f2)
    # ovde je greska, np.concat pravi numpy array umesto da nastavi da prosledjuje listu klase point

def mutate(individual, mutation_rate,D):
    if np.random.rand() < mutation_rate:
        mutation_point1, mutation_point2 = np.random.choice(len(individual.chromosome), 2, replace=False)
        
        individual.chromosome[mutation_point1], individual.chromosome[mutation_point2] = individual.chromosome[mutation_point2], individual.chromosome[mutation_point1]
        calculate_fitness(individual,D)

def calculate_fitness(individual, D):
    fitness = 0
    for i in range(len(individual.chromosome) - 1):
        fitness += D[individual.chromosome[i].id, individual.chromosome[i+1].id]
    fitness += D[individual.chromosome[-1].id, individual.chromosome[0].id] 
    individual.fitness = fitness
    return fitness

def select_parents(population):
    total_fitness = sum(individual.fitness for individual in population)
    
    selection_probs = [individual.fitness / total_fitness for individual in population]
    
    parents = np.random.choice(population, 2, p=selection_probs, replace=False)
    
    return parents

def create_new_population(population, population_size, mutation_rate, D,n_best = 40):
    # Sort the population based on fitness
    sorted_population = sorted(population, key=lambda x: x.fitness)
    
    # Keep the best n_best individuals
    new_population = sorted_population[:n_best].copy()
    
    # Fill the rest of the new population with offspring
    while len(new_population) < population_size:
        parent1, parent2 = select_parents(sorted_population[:n_best])
        child1, child2 = crossover(parent1, parent2,D)
        mutate(child1, mutation_rate,D)
        mutate(child2, mutation_rate,D)
        new_population.extend([child1, child2])
    
    # Trim the new population to the desired population size
    return new_population[:population_size]


def ga(D,init_sol,collection_points,P, num_generations, population_size, mutation_rate):
    fixed_sol = fix_all_inverse(init_sol, collection_points)
    fs, init_cost = create_complete_sol(fixed_sol, D, P)
    best_sol = init_sol
    best_cost = init_cost

    ###
    # ovde je greska: jako je glupavo da se pravi cela populacija od identicne jedinke. moraju se stvarati na random nazalost
    population = [create_individual(init_sol,init_cost) for _ in range(population_size)]
    ###
    print (f"types of best sol and init sol : {type(best_sol), type(init_sol[1]), type(population[1].chromosome[1])}")

    best_list = []
    curr_list = []
    for generation in range(num_generations):
       # print(f"GEN {generation}")
        for individual in population:
            calculate_fitness(individual, D)

        new_population = create_new_population(population,population_size,mutation_rate,D)

        population = new_population

        best_curr_individual = min(population, key=lambda x: x.fitness)
        curr_list.append(best_curr_individual.fitness)

        if best_curr_individual.fitness<best_cost:
            best_sol = best_curr_individual.chromosome
            best_cost = best_curr_individual.fitness
        best_list.append(best_cost)

    print(f"type of best sol: {type(best_sol)}")
    create_complete_sol(best_sol, D, P)
    print(f"type of best sol: {type(best_sol)}")
    fixed_sol = fix_all_inverse(best_sol, collection_points)
    full_sol, best_full_cost = create_complete_sol(fixed_sol, D, P)


   # return best_sol, best_cost, best_list,curr_list
    return best_sol, best_cost, best_list,curr_list



