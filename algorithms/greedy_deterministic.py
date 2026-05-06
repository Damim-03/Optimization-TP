# algorithms/greedy_deterministic.py
# ─────────────────────────────────────────────────────────────────────────────
# GREEDY ALGORITHM — DETERMINISTIC VERSION
# ─────────────────────────────────────────────────────────────────────────────
#
# Principle:
#   At each step, make the locally best (greedy) choice based on a fixed,
#   deterministic rule — no randomness involved.
#
# TSP strategy:   Nearest Neighbor Heuristic
#   Start from city 0, always go to the closest unvisited city.
#
# Knapsack strategy:   Sort by value/weight ratio (descending)
#   Pick items greedily by best ratio until capacity is full.
# ─────────────────────────────────────────────────────────────────────────────


def greedy_deterministic_tsp(tsp):
    """
    Nearest Neighbor greedy for TSP.
    Always chooses the nearest unvisited city from the current position.

    Returns:
        tour  : list of city indices (the route)
        cost  : total tour distance
    """
    n = tsp.n
    visited = [False] * n
    tour = []

    # Start from city 0 (deterministic starting point)
    current = 0
    visited[current] = True
    tour.append(current)

    for _ in range(n - 1):
        # Find the nearest unvisited city
        best_next = None
        best_dist = float('inf')

        for city in range(n):
            if not visited[city]:
                d = tsp.distance(current, city)
                if d < best_dist:
                    best_dist = d
                    best_next = city

        # Move to nearest city
        visited[best_next] = True
        tour.append(best_next)
        current = best_next

    cost = tsp.tour_cost(tour)
    return tour, cost


def greedy_deterministic_knapsack(knapsack):
    """
    Value/Weight ratio greedy for Knapsack.
    Sort items by ratio descending, pick greedily.

    Returns:
        selected : list of selected item indices
        value    : total value
        weight   : total weight
    """
    n = knapsack.n

    # Sort items by value/weight ratio — deterministic order
    items_sorted = sorted(range(n), key=lambda i: knapsack.ratio(i), reverse=True)

    selected = []
    total_weight = 0
    total_value  = 0

    for item in items_sorted:
        w = knapsack.weight(item)
        if total_weight + w <= knapsack.capacity:
            selected.append(item)
            total_weight += w
            total_value  += knapsack.value(item)

    return selected, total_value, total_weight
