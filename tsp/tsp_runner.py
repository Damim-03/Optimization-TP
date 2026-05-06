# tsp/tsp_runner.py
# Run all algorithms on the TSP problem and display results.

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from tsp.tsp_instance import TSPInstance
from algorithms.greedy_deterministic    import greedy_deterministic_tsp
from algorithms.greedy_nondeterministic import greedy_nondeterministic_tsp
from algorithms.local_search_first      import local_search_first_tsp
from algorithms.local_search_best       import local_search_best_tsp
from algorithms.simulated_annealing     import simulated_annealing_tsp
from algorithms.genetic                 import genetic_tsp
from utils.helpers                      import print_header, print_result
import time


def run_all_tsp(tsp=None):
    if tsp is None:
        tsp = TSPInstance()

    print_header("TSP — Traveling Salesman Problem")
    print(f"  Cities : {tsp.n}")
    print(f"  Coords : {tsp.cities}\n")

    results = {}

    # 1. Greedy Deterministic
    t0 = time.time()
    tour, cost = greedy_deterministic_tsp(tsp)
    elapsed = time.time() - t0
    print_result("Greedy Deterministic", cost, tour, elapsed)
    results["Greedy Det"] = cost

    # 2. Greedy Non-Deterministic
    t0 = time.time()
    tour, cost = greedy_nondeterministic_tsp(tsp, k=3)
    elapsed = time.time() - t0
    print_result("Greedy Non-Deterministic (k=3)", cost, tour, elapsed)
    results["Greedy NonDet"] = cost

    # 3. Local Search First Improvement
    t0 = time.time()
    tour, cost, iters = local_search_first_tsp(tsp)
    elapsed = time.time() - t0
    print_result(f"Local Search — First Improvement ({iters} iters)", cost, tour, elapsed)
    results["LS First"] = cost

    # 4. Local Search Best Improvement
    t0 = time.time()
    tour, cost, iters = local_search_best_tsp(tsp)
    elapsed = time.time() - t0
    print_result(f"Local Search — Best Improvement ({iters} iters)", cost, tour, elapsed)
    results["LS Best"] = cost

    # 5. Simulated Annealing
    t0 = time.time()
    tour, cost, history = simulated_annealing_tsp(tsp)
    elapsed = time.time() - t0
    print_result(f"Simulated Annealing ({len(history)} steps)", cost, tour, elapsed)
    results["SA"] = cost

    # 6. Genetic Algorithm
    t0 = time.time()
    tour, cost, history = genetic_tsp(tsp)
    elapsed = time.time() - t0
    print_result(f"Genetic Algorithm ({len(history)} generations)", cost, tour, elapsed)
    results["Genetic"] = cost

    # Summary
    print("\n" + "=" * 60)
    print("  TSP SUMMARY — Best Cost per Algorithm")
    print("=" * 60)
    best = min(results.values())
    for name, val in results.items():
        marker = " ★ BEST" if val == best else ""
        print(f"  {name:<35} {val:.4f}{marker}")
    print("=" * 60)

    return results


if __name__ == "__main__":
    run_all_tsp()
