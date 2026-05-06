# algorithms/simulated_annealing.py
# ─────────────────────────────────────────────────────────────────────────────
# SIMULATED ANNEALING (SA)
# ─────────────────────────────────────────────────────────────────────────────
#
# Principle:
#   Inspired by the annealing process in metallurgy (slowly cooling metal).
#   Like Local Search, but can ACCEPT WORSE solutions with a probability
#   that depends on:
#       - How much worse the new solution is (Δ = new_cost - current_cost)
#       - The current "temperature" T
#
#   Acceptance probability:  P(accept) = exp(-Δ / T)
#
#   - High T (start): almost any move accepted → exploration
#   - Low T (end):    only improvements accepted → exploitation
#
#   Temperature decreases over time via a cooling schedule:
#       T = T * cooling_rate   (geometric cooling)
#
# TSP:      2-opt neighbor moves
# Knapsack: swap / add / remove moves
# ─────────────────────────────────────────────────────────────────────────────

import math
import random


# ─────────────────────────────── TSP ─────────────────────────────────────────

def simulated_annealing_tsp(
    tsp,
    initial_tour=None,
    T_start=1000.0,
    T_min=0.01,
    cooling_rate=0.995,
    seed=42
):
    """
    Simulated Annealing for TSP using 2-opt neighborhood moves.

    Args:
        tsp          : TSPInstance
        initial_tour : starting tour (random if None)
        T_start      : initial temperature
        T_min        : stopping temperature
        cooling_rate : geometric cooling factor (0 < α < 1)
        seed         : random seed

    Returns:
        best_tour  : best tour found
        best_cost  : best cost found
        history    : list of (temperature, cost) for plotting
    """
    random.seed(seed)
    n = tsp.n

    # Initial solution
    if initial_tour is None:
        tour = list(range(n))
        random.shuffle(tour)
    else:
        tour = list(initial_tour)

    cost = tsp.tour_cost(tour)

    # Track global best
    best_tour = list(tour)
    best_cost = cost

    T = T_start
    history = [(T, cost)]

    while T > T_min:
        # Generate a random 2-opt neighbor
        i = random.randint(1, n - 2)
        j = random.randint(i + 1, n - 1)

        # Reverse segment i..j
        new_tour = tour[:i] + tour[i:j+1][::-1] + tour[j+1:]
        new_cost = tsp.tour_cost(new_tour)

        delta = new_cost - cost  # positive → worse

        # Accept if better, or with probability exp(-delta/T) if worse
        if delta < 0 or random.random() < math.exp(-delta / T):
            tour = new_tour
            cost = new_cost

            # Update global best
            if cost < best_cost:
                best_tour = list(tour)
                best_cost = cost

        # Cool down
        T *= cooling_rate
        history.append((T, cost))

    return best_tour, best_cost, history


# ─────────────────────────────── KNAPSACK ────────────────────────────────────

def simulated_annealing_knapsack(
    knapsack,
    initial_selection=None,
    T_start=500.0,
    T_min=0.01,
    cooling_rate=0.995,
    seed=42
):
    """
    Simulated Annealing for Knapsack.

    Neighborhood moves:
        1. Flip: toggle one item (add if not selected, remove if selected)
        2. Swap: swap one selected ↔ one not selected

    Args:
        knapsack          : KnapsackInstance
        initial_selection : starting selection as binary list (random if None)
        T_start           : initial temperature
        T_min             : stopping temperature
        cooling_rate      : geometric cooling factor
        seed              : random seed

    Returns:
        best_selection : binary list [0/1] of best solution
        best_value     : total value of best solution
        history        : list of (temperature, value) for plotting
    """
    random.seed(seed)
    n = knapsack.n

    # Initial solution: random binary vector
    if initial_selection is None:
        selection = [random.randint(0, 1) for _ in range(n)]
        # Repair: remove items until feasible
        while sum(knapsack.weight(i) for i in range(n) if selection[i]) > knapsack.capacity:
            ones = [i for i in range(n) if selection[i]]
            if not ones:
                break
            selection[random.choice(ones)] = 0
    else:
        selection = list(initial_selection)

    def total_value(sel):
        return sum(knapsack.value(i) for i in range(n) if sel[i])

    def total_weight(sel):
        return sum(knapsack.weight(i) for i in range(n) if sel[i])

    value  = total_value(selection)
    weight = total_weight(selection)

    best_selection = list(selection)
    best_value     = value

    T = T_start
    history = [(T, value)]

    while T > T_min:
        # Choose a random move type
        move = random.choice(['flip', 'swap'])
        new_sel = list(selection)

        if move == 'flip':
            # Toggle a random item
            idx = random.randint(0, n - 1)
            new_sel[idx] = 1 - new_sel[idx]

        else:  # swap
            ones  = [i for i in range(n) if selection[i]]
            zeros = [i for i in range(n) if not selection[i]]
            if ones and zeros:
                out = random.choice(ones)
                inp = random.choice(zeros)
                new_sel[out] = 0
                new_sel[inp] = 1
            else:
                continue

        new_weight = total_weight(new_sel)
        new_value  = total_value(new_sel)

        # Only consider feasible moves (hard constraint)
        if new_weight > knapsack.capacity:
            T *= cooling_rate
            continue

        delta = value - new_value  # positive → new is worse (we maximize)

        # Accept if better, or probabilistically if worse
        if delta < 0 or random.random() < math.exp(-delta / T):
            selection = new_sel
            value     = new_value
            weight    = new_weight

            if value > best_value:
                best_selection = list(selection)
                best_value     = value

        T *= cooling_rate
        history.append((T, value))

    best_items = [i for i in range(n) if best_selection[i]]
    return best_items, best_value, history
