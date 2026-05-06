# algorithms/local_search_first.py
# ─────────────────────────────────────────────────────────────────────────────
# LOCAL SEARCH — FIRST IMPROVEMENT
# ─────────────────────────────────────────────────────────────────────────────
#
# Principle:
#   Starting from an initial solution, explore the neighborhood of the current
#   solution. In FIRST IMPROVEMENT, we accept the FIRST neighbor that is
#   better than the current solution, then move to it immediately (don't
#   wait to see all neighbors).
#
#   This is faster per iteration but may miss better moves found later
#   in the neighborhood.
#
# TSP neighborhood:   2-opt moves
#   Reverse a segment of the tour. If it reduces cost → accept immediately.
#
# Knapsack neighborhood:   Swap moves
#   Try swapping one selected item for one unselected item.
#   Accept the first swap that improves value.
# ─────────────────────────────────────────────────────────────────────────────

import random


def _initial_tour_random(n, seed=42):
    """Generate a random initial tour."""
    random.seed(seed)
    tour = list(range(n))
    random.shuffle(tour)
    return tour


def local_search_first_tsp(tsp, initial_tour=None, max_iterations=1000):
    """
    2-opt Local Search with First Improvement for TSP.

    At each iteration, scan 2-opt swaps and accept the FIRST one
    that reduces the tour cost. Repeat until no improvement is found.

    Args:
        tsp            : TSPInstance
        initial_tour   : starting tour (random if None)
        max_iterations : safety cap on iterations

    Returns:
        tour : improved tour
        cost : improved cost
        iterations : number of improvement steps taken
    """
    n = tsp.n

    # Start from a random tour if none provided
    if initial_tour is None:
        tour = _initial_tour_random(n)
    else:
        tour = list(initial_tour)

    cost = tsp.tour_cost(tour)
    iterations = 0

    for _ in range(max_iterations):
        improved = False

        # Scan all 2-opt pairs
        for i in range(1, n - 1):
            for j in range(i + 1, n):
                # 2-opt: reverse segment tour[i..j]
                new_tour = tour[:i] + tour[i:j+1][::-1] + tour[j+1:]
                new_cost = tsp.tour_cost(new_tour)

                if new_cost < cost:
                    # FIRST IMPROVEMENT: accept immediately
                    tour = new_tour
                    cost = new_cost
                    improved = True
                    iterations += 1
                    break  # restart scan from beginning

            if improved:
                break

        if not improved:
            break  # Local optimum reached

    return tour, cost, iterations


def local_search_first_knapsack(knapsack, initial_selection=None, max_iterations=500):
    """
    Swap-based Local Search with First Improvement for Knapsack.

    Neighborhood: swap one selected item with one unselected item.
    Accept the FIRST swap that improves total value while staying feasible.

    Args:
        knapsack          : KnapsackInstance
        initial_selection : set of selected item indices (greedy if None)
        max_iterations    : safety cap

    Returns:
        selected   : improved selection (list of indices)
        value      : total value
        weight     : total weight
        iterations : number of improvement steps
    """
    from algorithms.greedy_deterministic import greedy_deterministic_knapsack

    # Start from greedy solution if none provided
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
        improved = False
        not_selected = [i for i in range(n) if i not in selected]

        for out_item in selected:
            for in_item in not_selected:
                # Try: remove out_item, add in_item
                new_weight = weight - knapsack.weight(out_item) + knapsack.weight(in_item)
                new_value  = value  - knapsack.value(out_item)  + knapsack.value(in_item)

                if new_weight <= knapsack.capacity and new_value > value:
                    # FIRST IMPROVEMENT: accept immediately
                    selected.remove(out_item)
                    selected.add(in_item)
                    value  = new_value
                    weight = new_weight
                    improved = True
                    iterations += 1
                    break

            if improved:
                break

        if not improved:
            break  # Local optimum

    return list(selected), value, weight, iterations
