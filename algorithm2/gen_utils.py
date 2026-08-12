import numpy as np
import random

def calculate_fitness(individual):
    filtered_signal = np.convolve(noisy_signal, individual, mode='same')
    mse = np.mean((filtered_signal - signal) ** 2)
    fitness = 1 - mse / MAX_FITNESS
    return fitness


def crossover(parent1, parent2):
    child = []
    for i in range(filter_length):
        if random.uniform(0, 1) < crossover_rate:
            child.append(parent1[i])
        else:
            child.append(parent2[i])
    return child



def mutate(individual):
    mutated_individual = []
    for i in range(filter_length):
        if random.uniform(0, 1) < mutation_rate:
            mutated_individual.append(np.random.normal(0, 1))
        else:
            mutated_individual.append(individual[i])
    return mutated_individual


def select_individuals(fitnesses):
    total_fitness = sum(fitnesses)
    probability1 = random.uniform(0, total_fitness)
    probability2 = random.uniform(0, total_fitness)
    current_probability = 0
    for i, fitness in enumerate(fitnesses):
        current_probability += fitness
        if current_probability > probability1:
            first_individual = population[i]
            break
        else:
            first_individual = population[population_size-1]
        current_probability = 0
    for i, fitness in enumerate(fitnesses):
        current_probability += fitness
        if current_probability > probability2:
            second_individual = population[i]
            break
        else:
            second_individual = population[population_size-1]

    return first_individual, second_individual


def tournament_selection(fitnesses, tournament_size):
    tournament_candidates = []
    for i in range(tournament_size):
        random_index = random.randint(0, len(fitnesses) - 1)
        tournament_candidates.append(random_index)
    tournament_candidates.sort(key=lambda x: fitnesses[x], reverse = True)
    return population[tournament_candidates[0]], population[tournament_candidates[1]]


