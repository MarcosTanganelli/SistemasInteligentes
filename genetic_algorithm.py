#!/usr/bin/env python
# coding: utf-8

# In[3]:


import random
import numpy as np
def generate_knapsack_problem(num_items, weight_range, value_range, capacity_range):
    """
    Generates a random instance of the 0/1 Knapsack problem.
    
    Parameters:
    - num_items: Number of items to generate
    - weight_range: Tuple (min_weight, max_weight) defining the range of item weights
    - value_range: Tuple (min_value, max_value) defining the range of item values
    - capacity_range: Tuple (min_capacity, max_capacity) defining the range for knapsack capacity
    
    Returns:
    - values: List of item values
    - weights: List of item weights
    - capacity: The capacity of the knapsack
    """
    values = [random.randint(*value_range) for _ in range(num_items)]
    weights = [random.randint(*weight_range) for _ in range(num_items)]
    capacity = random.randint(*capacity_range)
    
    return values, weights, capacity

# Example usage
num_items = 10  # Number of items
weight_range = (1, 20)  # Weights will be between 1 and 20
value_range = (10, 100)  # Values will be between 10 and 100
capacity_range = (50, 100)  # Knapsack capacity will be between 50 and 100

# Generate the problem
values, weights, capacity = generate_knapsack_problem(num_items, weight_range, value_range, capacity_range)


def reproduce(parent_1, parent_2):
    # Convert to lists before extending
    value = random.randint(0,len(parent_1))
    kid_1 = list(parent_1[0:value])
    kid_1.extend(list(parent_2[value:]))

    kid_2 = list(parent_2[0:value])
    kid_2.extend(list(parent_1[value:]))

    return kid_1, kid_2


def fitness_coeficient(zeroUm, values, pesos, capacity):
    coeficient = 0
    weight = 0
    for i, j in enumerate(zeroUm):
        if j == 1:
            weight += pesos[i]
            coeficient += values[i]
            if weight > capacity: 
                return 0
    return coeficient


def mutate(individual):
    idx = random.randint(0,len(individual)-1)
    if individual[idx] == 0:
        individual[idx] = 1
    else:
        individual[idx] = 0
    return individual

def generate_random_vector(num_items):
    # Generate a random vector of 0s and 1s
    random_vector = np.random.choice([0, 1], size=num_items)
    return random_vector

def generate_random_population(size, num_items):
    population = []
    for i in range(size):
        population.append(generate_random_vector(num_items))
    return population


def roulette_wheel_selection(fitness_values, num_selections):
    # Calculate the total fitness
    total_fitness = sum(fitness_values)
    
    # Calculate selection probabilities for each individual
    probabilities = [f / total_fitness for f in fitness_values]
    
    # Perform roulette wheel selection (with repeated sampling allowed)
    selected_individuals = np.random.choice(
        len(fitness_values), size=num_selections, p=probabilities
    ).tolist()
    
    return selected_individuals

def genetic_algorithm(values, weights, capacity, population_size, mutation_probability):
    population = generate_random_population(population_size, len(values))
    i = 0
    j = 0
    pop_fitness = []
    for indv in population:
        pop_fitness.append(fitness_coeficient(indv, values, weights, capacity))
    while (i < 1000): 
        parents = roulette_wheel_selection(pop_fitness, len(population))
        new_population = []
        
        for parent in range(int(len(parents)/2)):
            
            kid_1, kid_2 = reproduce(population[parents[parent]], population[parents[len(parents) - 1 - parent]])
            new_population.append(kid_1)
            new_population.append(kid_2)
        
        new_pop_fitness = []
        for new_indv in new_population:
            probs = random.random()
            if probs < mutation_probability:
                new_indv = mutate(new_indv)          
            new_pop_fitness.append(fitness_coeficient(new_indv, values, weights, capacity))

        pop_fitness = new_pop_fitness
        population = new_population.copy()
        i += 1

    best_fitness = 0
    best_idx = -1
    for i, j in enumerate(pop_fitness):
        if best_fitness <= j:
            best_fitness = j
            best_idx = i
    return population[best_idx], best_fitness


# In[4]:


solution, valor = genetic_algorithm(values, weights, capacity, 32, 0.01)
print(solution)
print(valor)
print(values)
print(weights)
print(capacity)


# In[ ]:


#loop that will generate the results
def simulate(trials, num_items, weight_range, value_range, capacity_range):
    for i in range(trials):
        # Generate the problem
        values, weights, capacity = generate_knapsack_problem(num_items, weight_range, value_range, capacity_range)
        

