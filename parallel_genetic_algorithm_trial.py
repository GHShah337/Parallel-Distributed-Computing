from mpi4py import MPI
import numpy as np
import pandas as pd
from genetic_algorithms_functions import calculate_fitness, \
    select_in_tournament, order_crossover, mutate, \
    generate_unique_population
import sys

# --------------------------
# MPI Setup
# --------------------------
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# --------------------------
# Constants & Config
# --------------------------
distance_matrix = pd.read_csv("city_distances.csv").to_numpy()
num_nodes = distance_matrix.shape[0]
population_size = 10000
num_generations = 200  # Change to 200 for full run
mutation_rate = 0.1
stagnation_limit = 5

# --------------------------
# Feasibility check
# --------------------------
def is_feasible(route):
    for i in range(len(route) - 1):
        if distance_matrix[route[i], route[i + 1]] >= 100000:
            return False
    if distance_matrix[route[-1], route[0]] >= 100000:
        return False
    return True

# --------------------------
# Initial Population (on root)
# --------------------------
if rank == 0:
    population = generate_unique_population(population_size, num_nodes)
else:
    population = None

# Broadcast initial population to all processes
population = comm.bcast(population, root=0)

# --------------------------
# Begin Generational Loop
# --------------------------
best_fitness = int(1e6)
stagnation_counter = 0

for generation in range(num_generations):
    regenerated = False  

    counts = [len(population) // size + (1 if i < len(population) % size else 0) for i in range(size)]
    starts = [sum(counts[:i]) for i in range(size)]
    local_pop = population[starts[rank]:starts[rank] + counts[rank]]

    local_fitness = np.array([calculate_fitness(route, distance_matrix) for route in local_pop])

    all_fitness = None
    if rank == 0:
        all_fitness = np.empty(len(population), dtype=np.float64)
    recvcounts = np.array(counts, dtype=int)
    displacements = np.array(starts, dtype=int)

    comm.Gatherv(local_fitness, [all_fitness, recvcounts, displacements, MPI.DOUBLE], root=0)

    if rank == 0:
        current_best = np.max(all_fitness)

        if current_best > best_fitness or generation == 0:
            best_fitness = current_best
            stagnation_counter = 0
        else:
            stagnation_counter += 1

        if stagnation_counter >= stagnation_limit:
            print(f"Regenerating population at generation {generation} due to stagnation", flush=True)
            top_indices = np.argsort(all_fitness)[-10:]
            elites = [population[i] for i in top_indices]
            population = generate_unique_population(population_size - len(elites), num_nodes)
            population.extend(elites)
            stagnation_counter = 0
            regenerated = True  

    population = comm.bcast(population, root=0)
    regenerated = comm.bcast(regenerated if rank == 0 else None, root=0)

    if regenerated:
        continue

    # --------------------------
    # Evolution
    # --------------------------
    if rank == 0:
        selected = select_in_tournament(population, all_fitness, number_tournaments=len(population))
        np.random.shuffle(selected)

        offspring = []
        for i in range(0, len(selected), 2):
            parent1, parent2 = selected[i], selected[i + 1]
            child = order_crossover(parent1[1:], parent2[1:])
            new_route = [0] + child
            offspring.append(new_route)

        mutated_offspring = [mutate(route, mutation_rate) for route in offspring]

        population = mutated_offspring

        unique_population = set(tuple(ind) for ind in population)
        while len(unique_population) < population_size:
            individual = [0] + list(np.random.permutation(np.arange(1, num_nodes)))
            unique_population.add(tuple(individual))
        population = [list(ind) for ind in unique_population]

        print(f"Generation {generation}: Best = {current_best}, Worst = {np.min(all_fitness)}", flush=True)

    population = comm.bcast(population, root=0)

# --------------------------
# Final Output
# --------------------------
if rank == 0:
    final_fitness = np.array([calculate_fitness(route, distance_matrix) for route in population])
    best_idx = np.argmax(final_fitness)
    best_route = population[best_idx]
    print("Best Solution:", best_route, flush=True)
    print("Total Distance:", -final_fitness[best_idx], flush=True)
