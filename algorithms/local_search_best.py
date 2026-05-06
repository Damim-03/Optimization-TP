# algorithms/local_search_best.py
# ─────────────────────────────────────────────────────────────────────────────
# LOCAL SEARCH — BEST IMPROVEMENT
# ─────────────────────────────────────────────────────────────────────────────
#
# Principle:
#   Starting from an initial solution, explore the ENTIRE neighborhood,
#   collect all improving moves, and then accept the BEST one (largest
#   improvement). Only then move to the new solution.
#
#   Compared to First Improvement:
#   ✓ Makes better decisions per step (greedy over the neighborhood)
#   ✗ Slower per iteration (must scan all neighbors before moving)
#
# TSP neighborhood:   2-opt moves
#   Scan ALL 2-opt swaps. Pick the one with the maximum cost reduction.
#
# Knapsack neighborhood:   Swap moves
#   Scan ALL swap pairs. Pick the swap with the best value gain.
# ─────────────────────────────────────────────────────────────────────────────

import random


def _initial_tour_random(n, seed=42):
    random.seed(seed)
    tour = list(range(n))
    random.shuffle(tour)
    return tour


def local_search_best_tsp(tsp, initial_tour=None, max_iterations=1000):
    """
    2-opt Local Search with Best Improvement for TSP.

    At each iteration, scan ALL 2-opt neighbors, then accept the BEST
    one (maximum cost reduction). Repeat until no improvement exists.

    Args:
        tsp            : TSPInstance
        initial_tour   : starting tour (random if None)
        max_iterations : safety cap

    Returns:
        tour       : improved tour
        cost       : improved cost
        iterations : number of improvement steps
    """
    n = tsp.n

    if initial_tour is None:
        tour = _initial_tour_random(n)
    else:
        tour = list(initial_tour)

    cost = tsp.tour_cost(tour)
    iterations = 0

    for _ in range(max_iterations):
        best_gain     = 0.0
        best_i        = -1
        best_j        = -1

        # Scan ALL 2-opt pairs to find the best move
        for i in range(1, n - 1):
            for j in range(i + 1, n):
                new_tour = tour[:i] + tour[i:j+1][::-1] + tour[j+1:]
                new_cost = tsp.tour_cost(new_tour)
                gain     = cost - new_cost  # positive = improvement

                if gain > best_gain:
                    best_gain = gain
                    best_i    = i
                    best_j    = j

        if best_gain <= 0:
            break  # No improving move found → local optimum

        # Apply the BEST 2-opt move found
        tour = tour[:best_i] + tour[best_i:best_j+1][::-1] + tour[best_j+1:]
        cost -= best_gain
        iterations += 1

    return tour, cost, iterations


def local_search_best_knapsack(knapsack, initial_selection=None, max_iterations=500):
    """
    Swap-based Local Search with Best Improvement for Knapsack.

    Scans ALL swap pairs (remove one, add one), then applies the BEST
    feasible swap that gives the highest value gain.

    Args:
        knapsack          : KnapsackInstance
        initial_selection : starting selection (greedy if None)
        max_iterations    : safety cap

    Returns:
        selected   : improved selection
        value      : total value
        weight     : total weight
        iterations : number of improvement steps
    """
    from algorithms.greedy_deterministic import greedy_deterministic_knapsack

    if initial_selection is None:
        selected, _, _ = greedy_deterministic_knapsack(knapsack)
    else:
        selected = list(initial_selection)

    selected = set(selected)
    n = knapsack.n

    def current_stats():
        w = sum(knapsack.weight(i) for i in selected)
        v = sum(knapsack.value(i)  for i in selected)
        return v, w

    value, weight = current_stats()
    iterations = 0

    for _ in range(max_iterations):
        best_gain    = 0
        best_out     = None
        best_in      = None
        not_selected = [i for i in range(n) if i not in selected]

        # Scan ALL swap pairs
        for out_item in selected:
            for in_item in not_selected:
                new_weight = weight - knapsack.weight(out_item) + knapsack.weight(in_item)
                new_value  = value  - knapsack.value(out_item)  + knapsack.value(in_item)
                gain       = new_value - value

                if new_weight <= knapsack.capacity and gain > best_gain:
                    best_gain = gain
                    best_out  = out_item
                    best_in   = in_item

        if best_gain <= 0:
            break  # Local optimum

        # Apply the BEST swap
        selected.remove(best_out)
        selected.add(best_in)
        value  += best_gain
        weight  = weight - knapsack.weight(best_out) + knapsack.weight(best_in)
        iterations += 1

    return list(selected), value, weight, iterations
