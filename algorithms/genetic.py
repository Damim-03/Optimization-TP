# algorithms/genetic.py
# ─────────────────────────────────────────────────────────────────────────────
# GENETIC ALGORITHM (GA)
# ─────────────────────────────────────────────────────────────────────────────
#
# Principle:
#   Inspired by natural selection (Darwin's evolution theory).
#   Maintains a POPULATION of solutions (individuals/chromosomes).
#   Each generation:
#       1. SELECTION   — select parents (fitter = more likely selected)
#       2. CROSSOVER   — combine two parents to create offspring
#       3. MUTATION    — randomly alter offspring (diversity)
#       4. REPLACEMENT — new generation replaces old one
#
#   Over generations, the population converges toward better solutions.
#
# TSP encoding:       Permutation (order of cities)
#   Crossover:        Order Crossover (OX)
#   Mutation:         2-opt swap of two random positions
#
# Knapsack encoding:  Binary vector [0, 1, 1, 0, ...]
#   Crossover:        Single-point crossover
#   Mutation:         Bit flip
# ─────────────────────────────────────────────────────────────────────────────

import random


# ═══════════════════════════════════════════════════════════════════════════════
#  TSP — Genetic Algorithm
# ═══════════════════════════════════════════════════════════════════════════════

def _random_tour(n):
    tour = list(range(n))
    random.shuffle(tour)
    return tour


def _ox_crossover(parent1, parent2):
    """
    Order Crossover (OX) for permutation chromosomes.
    Preserves relative order of cities from parent2 while copying
    a random segment from parent1.
    """
    n = len(parent1)
    i, j = sorted(random.sample(range(n), 2))

    # Copy segment from parent1
    child = [None] * n
    child[i:j+1] = parent1[i:j+1]

    # Fill remaining positions with parent2's order
    segment = set(parent1[i:j+1])
    p2_order = [c for c in parent2 if c not in segment]

    ptr = 0
    for k in range(n):
        if child[k] is None:
            child[k] = p2_order[ptr]
            ptr += 1

    return child


def _mutate_tour(tour, mutation_rate):
    """Swap two random cities in the tour."""
    if random.random() < mutation_rate:
        i, j = random.sample(range(len(tour)), 2)
        tour[i], tour[j] = tour[j], tour[i]
    return tour


def _tournament_selection(population, fitnesses, k=3):
    """Tournament selection: pick k random, return the best."""
    candidates = random.sample(range(len(population)), k)
    best = min(candidates, key=lambda idx: fitnesses[idx])  # minimize cost
    return population[best]


def genetic_tsp(
    tsp,
    pop_size=50,
    generations=200,
    mutation_rate=0.1,
    tournament_k=3,
    elitism=True,
    seed=42
):
    """
    Genetic Algorithm for TSP.

    Args:
        tsp           : TSPInstance
        pop_size      : number of individuals in population
        generations   : number of generations to evolve
        mutation_rate : probability of mutation per offspring
        tournament_k  : tournament size for selection
        elitism       : keep best individual across generations
        seed          : random seed

    Returns:
        best_tour  : best tour found
        best_cost  : best cost found
        history    : list of best cost per generation
    """
    random.seed(seed)
    n = tsp.n

    # Initialize population with random tours
    population = [_random_tour(n) for _ in range(pop_size)]
    fitnesses  = [tsp.tour_cost(t) for t in population]

    best_idx   = min(range(pop_size), key=lambda i: fitnesses[i])
    best_tour  = list(population[best_idx])
    best_cost  = fitnesses[best_idx]
    history    = [best_cost]

    for gen in range(generations):
        new_population = []

        # Elitism: carry best individual unchanged
        if elitism:
            new_population.append(list(best_tour))

        while len(new_population) < pop_size:
            # Selection
            parent1 = _tournament_selection(population, fitnesses, tournament_k)
            parent2 = _tournament_selection(population, fitnesses, tournament_k)

            # Crossover (OX)
            child = _ox_crossover(parent1, parent2)

            # Mutation
            child = _mutate_tour(child, mutation_rate)

            new_population.append(child)

        population = new_population
        fitnesses  = [tsp.tour_cost(t) for t in population]

        # Update best
        gen_best_idx = min(range(pop_size), key=lambda i: fitnesses[i])
        if fitnesses[gen_best_idx] < best_cost:
            best_cost = fitnesses[gen_best_idx]
            best_tour = list(population[gen_best_idx])

        history.append(best_cost)

    return best_tour, best_cost, history


# ═══════════════════════════════════════════════════════════════════════════════
#  KNAPSACK — Genetic Algorithm
# ═══════════════════════════════════════════════════════════════════════════════

def _random_binary(n, knapsack):
    """Generate a random feasible binary chromosome."""
    items = list(range(n))
    random.shuffle(items)
    chrom = [0] * n
    w = 0
    for i in items:
        if w + knapsack.weight(i) <= knapsack.capacity:
            chrom[i] = 1
            w += knapsack.weight(i)
    return chrom


def _fitness_knapsack(chrom, knapsack):
    """
    Fitness = total value if feasible, penalized otherwise.
    We maximize fitness (unlike TSP where we minimize cost).
    """
    w = sum(knapsack.weight(i) for i in range(knapsack.n) if chrom[i])
    v = sum(knapsack.value(i)  for i in range(knapsack.n) if chrom[i])
    if w > knapsack.capacity:
        return 0  # heavy penalty for infeasible solutions
    return v


def _single_point_crossover(parent1, parent2):
    """Single-point crossover for binary chromosomes."""
    n = len(parent1)
    pt = random.randint(1, n - 2)
    return parent1[:pt] + parent2[pt:]


def _mutate_binary(chrom, mutation_rate):
    """Flip each bit with probability mutation_rate."""
    return [1 - b if random.random() < mutation_rate else b for b in chrom]


def _repair_knapsack(chrom, knapsack):
    """
    Repair an infeasible chromosome by randomly removing items
    until the weight constraint is satisfied.
    """
    n = knapsack.n
    chrom = list(chrom)
    w = sum(knapsack.weight(i) for i in range(n) if chrom[i])

    while w > knapsack.capacity:
        ones = [i for i in range(n) if chrom[i]]
        if not ones:
            break
        remove = random.choice(ones)
        chrom[remove] = 0
        w -= knapsack.weight(remove)

    return chrom


def _tournament_selection_knapsack(population, fitnesses, k=3):
    """Tournament selection: maximize fitness."""
    candidates = random.sample(range(len(population)), k)
    best = max(candidates, key=lambda idx: fitnesses[idx])
    return population[best]


def genetic_knapsack(
    knapsack,
    pop_size=50,
    generations=200,
    mutation_rate=0.05,
    tournament_k=3,
    elitism=True,
    seed=42
):
    """
    Genetic Algorithm for 0/1 Knapsack.

    Args:
        knapsack      : KnapsackInstance
        pop_size      : population size
        generations   : number of generations
        mutation_rate : per-bit mutation probability
        tournament_k  : tournament size
        elitism       : preserve best chromosome
        seed          : random seed

    Returns:
        best_items : list of selected item indices
        best_value : total value
        history    : list of best value per generation
    """
    random.seed(seed)
    n = knapsack.n

    # Initialize with feasible random individuals
    population = [_random_binary(n, knapsack) for _ in range(pop_size)]
    fitnesses  = [_fitness_knapsack(c, knapsack) for c in population]

    best_idx   = max(range(pop_size), key=lambda i: fitnesses[i])
    best_chrom = list(population[best_idx])
    best_value = fitnesses[best_idx]
    history    = [best_value]

    for gen in range(generations):
        new_population = []

        if elitism:
            new_population.append(list(best_chrom))

        while len(new_population) < pop_size:
            parent1 = _tournament_selection_knapsack(population, fitnesses, tournament_k)
            parent2 = _tournament_selection_knapsack(population, fitnesses, tournament_k)

            child = _single_point_crossover(parent1, parent2)
            child = _mutate_binary(child, mutation_rate)
            child = _repair_knapsack(child, knapsack)   # ensure feasibility

            new_population.append(child)

        population = new_population
        fitnesses  = [_fitness_knapsack(c, knapsack) for c in population]

        gen_best_idx = max(range(pop_size), key=lambda i: fitnesses[i])
        if fitnesses[gen_best_idx] > best_value:
            best_value = fitnesses[gen_best_idx]
            best_chrom = list(population[gen_best_idx])

        history.append(best_value)

    best_items = [i for i in range(n) if best_chrom[i]]
    return best_items, best_value, history
