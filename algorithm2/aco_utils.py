import random
import numpy as np
def construct_sol(ant, D, P,pheromone,collection_points):
    current_point = ant.current_point.id
    solution = [current_point]
    cost = 0 
    visited = [False]*(len(collection_points)+1) # visited duzine 51 - zbog inicijalne tacke koja ne spada u sampling 50 
    visited[current_point] = True
    while False in visited:
        next_point = select_next_point(ant,visited, D, current_point,pheromone)
        visited[next_point] = True
        solution.append(next_point)
        cost +=D[current_point,next_point]
        #print ( f"added cost is : {D[current_point,next_point]}")
        current_point = next_point
        #print(f"visited: {visited}")
    cost += D[solution[-1],solution[0]]
    ant.solution = solution
    #print(f"solution: {solution}")
    ant.cost = cost
    #print(f"cost : {cost}")

def select_next_point(ant, visited, D, current_point,pheromone):
    # evo je greska 
    candidate_points = get_candidate_points(current_point, D,visited)

    probabilities = calculate_probabilities(ant,current_point, candidate_points, D,pheromone)

    next_point = roulette(candidate_points, probabilities)

    return next_point

def get_candidate_points(current_point, D,visited,n=3):
    # prvih 5 najboljih, nakon cega provera da nisu vec obidjeni 
    # kad treba da se promeni sorted? kada se promeni current point? 
    #print(f"current point:{current_point}")
    sorted = np.argsort(D[current_point])
    sorted = sorted[D[current_point][sorted] != 0]
    sorted = sorted[sorted!=0]

    #print(f"sorted : {len(sorted)}")
    candidates = sorted[sorted!=current_point]
    #print(f"candidates : {candidates}")
    candidates = [point for point in candidates if not visited[point]]
    candidate_points = candidates[:n] if len(candidates)>=n else candidates
    #print(candidate_points)
    return candidate_points


def calculate_probabilities(ant,current_point, candidate_points, D,pheromone):
    probabilities = []
    total_probability = 0
    for point in candidate_points:
        probability = calculate_probability(ant, point,current_point, D,pheromone)
        probabilities.append(probability)
        total_probability += probability
    probabilities = [p / total_probability for p in probabilities]
    #print(f"total prob:{total_probability}")
    #print(f" scaled probabilities:{probabilities}")
    return probabilities

def calculate_probability(ant, point,current_point, D,pheromone,alpha=1,beta=5):

    eta = 1/(D[current_point][point])
    probability = pheromone ** alpha * eta ** beta 
    #print(f"probability : {probability[0,0]}")
    return probability[0,0]



def roulette(candidate_points, probabilities):
    #print(probabilities)
    #print(f"candidates:{candidate_points} \n probabilities: {probabilities}")
    selected_point = random.choices(candidate_points, weights=probabilities)[0]
    return selected_point
