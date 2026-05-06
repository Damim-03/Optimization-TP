# knapsack/knapsack_runner.py
# Run all algorithms on the Knapsack problem and display results.

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from knapsack.knapsack_instance         import KnapsackInstance
from algorithms.greedy_deterministic    import greedy_deterministic_knapsack
from algorithms.greedy_nondeterministic import greedy_nondeterministic_knapsack
from algorithms.local_search_first      import local_search_first_knapsack
from algorithms.local_search_best       import local_search_best_knapsack
from algorithms.simulated_annealing     import simulated_annealing_knapsack
from algorithms.genetic                 import genetic_knapsack
from utils.helpers                      import print_header, print_result
import time


def run_all_knapsack(knapsack=None):
    if knapsack is None:
        knapsack = KnapsackInstance()

    print_header("KNAPSACK — 0/1 Knapsack Problem")
    print(f"  Items    : {knapsack.n}")
    print(f"  Capacity : {knapsack.capacity}")
    print(f"  Items (weight, value): {knapsack.items}\n")

    results = {}

    # 1. Greedy Deterministic
    t0 = time.time()
    selected, value, weight = greedy_deterministic_knapsack(knapsack)
    elapsed = time.time() - t0
    print_result("Greedy Deterministic", value,
                 f"items={selected}, w={weight}", elapsed)
    results["Greedy Det"] = value

    # 2. Greedy Non-Deterministic
    t0 = time.time()
    selected, value, weight = greedy_nondeterministic_knapsack(knapsack, k=3)
    elapsed = time.time() - t0
    print_result("Greedy Non-Deterministic (k=3)", value,
                 f"items={selected}, w={weight}", elapsed)
    results["Greedy NonDet"] = value

    # 3. Local Search First Improvement
    t0 = time.time()
    selected, value, weight, iters = local_search_first_knapsack(knapsack)
    elapsed = time.time() - t0
    print_result(f"Local Search — First Improvement ({iters} iters)", value,
                 f"items={selected}, w={weight}", elapsed)
    results["LS First"] = value

    # 4. Local Search Best Improvement
    t0 = time.time()
    selected, value, weight, iters = local_search_best_knapsack(knapsack)
    elapsed = time.time() - t0
    print_result(f"Local Search — Best Improvement ({iters} iters)", value,
                 f"items={selected}, w={weight}", elapsed)
    results["LS Best"] = value

    # 5. Simulated Annealing
    t0 = time.time()
    selected, value, history = simulated_annealing_knapsack(knapsack)
    elapsed = time.time() - t0
    print_result(f"Simulated Annealing ({len(history)} steps)", value,
                 f"items={selected}", elapsed)
    results["SA"] = value

    # 6. Genetic Algorithm
    t0 = time.time()
    selected, value, history = genetic_knapsack(knapsack)
    elapsed = time.time() - t0
    print_result(f"Genetic Algorithm ({len(history)} generations)", value,
                 f"items={selected}", elapsed)
    results["Genetic"] = value

    # Summary
    print("\n" + "=" * 60)
    print("  KNAPSACK SUMMARY — Best Value per Algorithm")
    print("=" * 60)
    best = max(results.values())
    for name, val in results.items():
        marker = " ★ BEST" if val == best else ""
        print(f"  {name:<35} {val}{marker}")
    print("=" * 60)

    return results


if __name__ == "__main__":
    run_all_knapsack()
