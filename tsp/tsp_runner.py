# tsp/tsp_runner.py
# ─────────────────────────────────────────────────────────────────────────────
# Run all algorithms on the TSP problem and display + plot results.
# All random algorithms use a fixed SEED for reproducibility.
# ─────────────────────────────────────────────────────────────────────────────

import sys, os, time
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from tsp.tsp_instance               import TSPInstance
from algorithms.greedy_deterministic    import greedy_deterministic_tsp
from algorithms.greedy_nondeterministic import greedy_nondeterministic_tsp
from algorithms.local_search_first      import local_search_first_tsp
from algorithms.local_search_best       import local_search_best_tsp
from algorithms.simulated_annealing     import simulated_annealing_tsp
from algorithms.genetic                 import genetic_tsp
from utils.helpers                      import print_header, print_result
from utils.plots import (
    plot_tsp_cities, plot_tsp_greedy, plot_tsp_local_search,
    plot_tsp_sa, plot_tsp_ga, plot_tsp_all_tours, plot_tsp_summary
)

# Fixed seed → reproducible results every run
SEED = 42


def run_all_tsp(tsp=None, plot=True):
    if tsp is None:
        tsp = TSPInstance()

    print_header(f"TSP — {tsp.name}  ({tsp.n} cities)")
    print(f"  Seed : {SEED}  (all stochastic algorithms use this seed)\n")

    results      = {}
    tours_detail = {}

    if plot:
        plot_tsp_cities(tsp)

    # ── 1. Greedy Deterministic ──────────────────────────────────────────
    # Deterministic: no seed needed, always same result
    t0 = time.time()
    gs_tour, gs_cost = greedy_deterministic_tsp(tsp)
    elapsed = time.time() - t0
    print_result("Greedy Deterministic", gs_cost, gs_tour, elapsed)
    results["Greedy Det"] = gs_cost
    tours_detail["Greedy Det"] = (gs_tour, gs_cost)

    # ── 2. Greedy Non-Deterministic ──────────────────────────────────────
    # Stochastic: fixed seed for reproducibility
    t0 = time.time()
    gnd_tour, gnd_cost = greedy_nondeterministic_tsp(tsp, k=3, seed=SEED)
    elapsed = time.time() - t0
    print_result("Greedy Non-Deterministic (k=3)", gnd_cost, gnd_tour, elapsed)
    results["Greedy NonDet"] = gnd_cost
    tours_detail["Greedy NonDet"] = (gnd_tour, gnd_cost)

    if plot:
        plot_tsp_greedy(tsp, gs_tour, gs_cost, gnd_tour, gnd_cost)

    # ── Local Search: both start from best greedy to be fair ──────────────
    # Use the better of Greedy Det and Greedy NonDet as starting point
    if gs_cost <= gnd_cost:
        initial_tour, initial_cost, initial_label = gs_tour, gs_cost, "Greedy Det"
    else:
        initial_tour, initial_cost, initial_label = gnd_tour, gnd_cost, "Greedy NonDet"
    print(f"\n  Local Search / SA start: {initial_label} (cost={initial_cost:.1f})\n")

    # ── 3. Local Search — First Improvement ──────────────────────────────
    t0 = time.time()
    fi_tour, fi_cost, fi_iters = local_search_first_tsp(tsp, initial_tour=initial_tour)
    elapsed = time.time() - t0
    print_result(f"Local Search — First Improvement ({fi_iters} iters)", fi_cost, fi_tour, elapsed)
    results["LS First"] = fi_cost
    tours_detail["LS First"] = (fi_tour, fi_cost)

    # ── 4. Local Search — Best Improvement ───────────────────────────────
    t0 = time.time()
    bi_tour, bi_cost, bi_iters = local_search_best_tsp(tsp, initial_tour=initial_tour)
    elapsed = time.time() - t0
    print_result(f"Local Search — Best Improvement ({bi_iters} iters)", bi_cost, bi_tour, elapsed)
    results["LS Best"] = bi_cost
    tours_detail["LS Best"] = (bi_tour, bi_cost)

    if plot:
        plot_tsp_local_search(tsp, initial_tour, initial_cost,
                              fi_tour, fi_cost, bi_tour, bi_cost)

    # ── 5. Simulated Annealing ────────────────────────────────────────────
    # Starts from best greedy; tuned parameters for att48
    t0 = time.time()
    sa_tour, sa_cost, sa_history = simulated_annealing_tsp(
        tsp,
        initial_tour=initial_tour,
        T_start=5000.0,     # higher start temperature → more exploration
        T_min=0.1,
        cooling_rate=0.998,  # slower cooling → more iterations
        seed=SEED
    )
    elapsed = time.time() - t0
    print_result(f"Simulated Annealing ({len(sa_history)} steps)", sa_cost, sa_tour, elapsed)
    results["SA"] = sa_cost
    tours_detail["SA"] = (sa_tour, sa_cost)

    if plot:
        plot_tsp_sa(tsp, sa_tour, sa_cost, sa_history)

    # ── 6. Genetic Algorithm ──────────────────────────────────────────────
    # Tuned for att48: larger population, more generations
    t0 = time.time()
    ga_tour, ga_cost, ga_history = genetic_tsp(
        tsp,
        pop_size=150,
        generations=500,
        mutation_rate=0.15,
        seed=SEED
    )
    elapsed = time.time() - t0
    print_result(f"Genetic Algorithm ({len(ga_history)} generations)", ga_cost, ga_tour, elapsed)
    results["Genetic"] = ga_cost
    tours_detail["Genetic"] = (ga_tour, ga_cost)

    if plot:
        plot_tsp_ga(tsp, ga_tour, ga_cost, ga_history)
        plot_tsp_all_tours(tsp, tours_detail)
        plot_tsp_summary(results)

    # ── Summary ───────────────────────────────────────────────────────────
    print("\n" + "="*60)
    print(f"  TSP SUMMARY — {tsp.name}")
    print("="*60)
    best = min(results.values())
    for name, val in results.items():
        marker = " ★ BEST" if val == best else ""
        print(f"  {name:<35} {val:.2f}{marker}")
    print("="*60)

    return results


if __name__ == "__main__":
    DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')
    tsp_file = os.path.join(DATA_DIR, 'att48.tsp')
    if os.path.exists(tsp_file):
        tsp = TSPInstance.from_tsp_file(tsp_file)
    else:
        print("  att48.tsp not found — using default 10-city instance")
        tsp = TSPInstance()
    run_all_tsp(tsp)
