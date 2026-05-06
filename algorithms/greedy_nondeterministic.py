# algorithms/greedy_nondeterministic.py
# ─────────────────────────────────────────────────────────────────────────────
# GREEDY ALGORITHM — NON-DETERMINISTIC (RANDOMIZED) VERSION
# ─────────────────────────────────────────────────────────────────────────────
#
# Principle:
#   Instead of always picking the single best greedy choice, we build a
#   Restricted Candidate List (RCL) of the top-k candidates and pick
#   randomly from it. This introduces diversity and avoids getting stuck
#   in the same local optimum every run.
#
#   This is the core idea behind GRASP (Greedy Randomized Adaptive Search).
#
# TSP strategy:
#   At each step, consider the k nearest unvisited cities, pick one at random.
#
# Knapsack strategy:
#   Sort by ratio, but randomly shuffle items within the top-k tier.
# ─────────────────────────────────────────────────────────────────────────────

import random


def greedy_nondeterministic_tsp(tsp, k=3, seed=None):
    """
    Randomized Nearest Neighbor greedy for TSP.
    At each step, choose randomly from the k nearest unvisited cities.

    Args:
        tsp  : TSPInstance
        k    : size of the Restricted Candidate List (RCL)
        seed : random seed for reproducibility (None = truly random)

    Returns:
        tour : list of city indices
        cost : total tour distance
    """
    if seed is not None:
        random.seed(seed)

    n = tsp.n
    visited = [False] * n
    tour = []

    # Start from a random city (non-deterministic starting point)
    current = random.randint(0, n - 1)
    visited[current] = True
    tour.append(current)

    for _ in range(n - 1):
        # Collect all unvisited cities with their distances
        candidates = []
        for city in range(n):
            if not visited[city]:
                d = tsp.distance(current, city)
                candidates.append((d, city))

        # Sort by distance and take top-k
        candidates.sort(key=lambda x: x[0])
        rcl = candidates[:k]  # Restricted Candidate List

        # Pick randomly from RCL
        _, chosen = random.choice(rcl)

        visited[chosen] = True
        tour.append(chosen)
        current = chosen

    cost = tsp.tour_cost(tour)
    return tour, cost


def greedy_nondeterministic_knapsack(knapsack, k=3, seed=None):
    """
    Randomized ratio greedy for Knapsack.
    Build RCL from top-k items by ratio, pick one randomly, repeat.

    Args:
        knapsack : KnapsackInstance
        k        : RCL size
        seed     : random seed

    Returns:
        selected : list of selected item indices
        value    : total value
        weight   : total weight
    """
    if seed is not None:
        random.seed(seed)

    n = knapsack.n
    available = list(range(n))  # items not yet considered
    selected = []
    total_weight = 0
    total_value  = 0

    while available:
        # Filter items that still fit
        feasible = [i for i in available if total_weight + knapsack.weight(i) <= knapsack.capacity]

        if not feasible:
            break  # No more items fit

        # Sort feasible items by ratio, take top-k as RCL
        feasible.sort(key=lambda i: knapsack.ratio(i), reverse=True)
        rcl = feasible[:k]

        # Pick randomly from RCL
        chosen = random.choice(rcl)

        selected.append(chosen)
        total_weight += knapsack.weight(chosen)
        total_value  += knapsack.value(chosen)
        available.remove(chosen)

    return selected, total_value, total_weight
