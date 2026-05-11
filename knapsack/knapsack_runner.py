# knapsack/knapsack_runner.py
# ─────────────────────────────────────────────────────────────────────────────
# Run all algorithms on the Knapsack problem and display + plot results.
# All random algorithms use a fixed SEED for reproducibility.
# ─────────────────────────────────────────────────────────────────────────────

import sys, os, time
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from knapsack.knapsack_instance         import KnapsackInstance
from algorithms.greedy_deterministic    import greedy_deterministic_knapsack
from algorithms.greedy_nondeterministic import greedy_nondeterministic_knapsack
from algorithms.local_search_first      import local_search_first_knapsack
from algorithms.local_search_best       import local_search_best_knapsack
from algorithms.simulated_annealing     import simulated_annealing_knapsack
from algorithms.genetic                 import genetic_knapsack
from utils.helpers                      import print_header, print_result
from utils.plots import (
    plot_knapsack_instance, plot_knapsack_greedy, plot_knapsack_local_search,
    plot_knapsack_sa, plot_knapsack_ga, plot_knapsack_summary,
    plot_knapsack_weight_vs_value
)

# Fixed seed → reproducible results every run
SEED = 42


def run_all_knapsack(knapsack=None, plot=True):
    if knapsack is None:
        knapsack = KnapsackInstance()

    print_header(f"KNAPSACK — {knapsack.name}  ({knapsack.n} items, cap={knapsack.capacity})")
    print(f"  Seed : {SEED}  (all stochastic algorithms use this seed)\n")

    results        = {}
    results_detail = {}  # {name: (value, weight)}

    if plot:
        plot_knapsack_instance(knapsack)

    # ── 1. Greedy Deterministic ──────────────────────────────────────────
    # Deterministic: no seed needed
    t0 = time.time()
    gs_sel, gs_val, gs_wt = greedy_deterministic_knapsack(knapsack)
    elapsed = time.time() - t0
    print_result("Greedy Deterministic", gs_val, f"items={gs_sel}, w={gs_wt}", elapsed)
    results["Greedy Det"] = gs_val
    results_detail["Greedy Det"] = (gs_val, gs_wt)

    # ── 2. Greedy Non-Deterministic ──────────────────────────────────────
    # Stochastic: fixed seed
    t0 = time.time()
    gnd_sel, gnd_val, gnd_wt = greedy_nondeterministic_knapsack(knapsack, k=3, seed=SEED)
    elapsed = time.time() - t0
    print_result("Greedy Non-Deterministic (k=3)", gnd_val, f"items={gnd_sel}, w={gnd_wt}", elapsed)
    results["Greedy NonDet"] = gnd_val
    results_detail["Greedy NonDet"] = (gnd_val, gnd_wt)

    if plot:
        plot_knapsack_greedy(knapsack, gs_sel, gs_val, gnd_sel, gnd_val)

    # ── Local Search: start from best greedy ─────────────────────────────
    if gs_val >= gnd_val:
        init_sel, init_val, init_label = gs_sel, gs_val, "Greedy Det"
    else:
        init_sel, init_val, init_label = gnd_sel, gnd_val, "Greedy NonDet"
    print(f"\n  Local Search / SA start: {init_label} (value={init_val})\n")

    # ── 3. Local Search — First Improvement ──────────────────────────────
    t0 = time.time()
    fi_sel, fi_val, fi_wt, fi_iters = local_search_first_knapsack(
        knapsack, initial_selection=init_sel)
    elapsed = time.time() - t0
    print_result(f"Local Search — First Improvement ({fi_iters} iters)", fi_val,
                 f"items={fi_sel}, w={fi_wt}", elapsed)
    results["LS First"] = fi_val
    results_detail["LS First"] = (fi_val, fi_wt)

    # ── 4. Local Search — Best Improvement ───────────────────────────────
    t0 = time.time()
    bi_sel, bi_val, bi_wt, bi_iters = local_search_best_knapsack(
        knapsack, initial_selection=init_sel)
    elapsed = time.time() - t0
    print_result(f"Local Search — Best Improvement ({bi_iters} iters)", bi_val,
                 f"items={bi_sel}, w={bi_wt}", elapsed)
    results["LS Best"] = bi_val
    results_detail["LS Best"] = (bi_val, bi_wt)

    if plot:
        plot_knapsack_local_search(knapsack, init_sel, init_val,
                                   fi_sel, fi_val, bi_sel, bi_val)

    # ── 5. Simulated Annealing ────────────────────────────────────────────
    # Starts from best greedy solution (not random)
    t0 = time.time()
    sa_sel, sa_val, sa_history = simulated_annealing_knapsack(
        knapsack,
        initial_selection=_to_binary(init_sel, knapsack.n),
        T_start=200.0,
        T_min=0.01,
        cooling_rate=0.997,
        seed=SEED
    )
    sa_wt = sum(knapsack.weight(i) for i in sa_sel)
    elapsed = time.time() - t0
    print_result(f"Simulated Annealing ({len(sa_history)} steps)", sa_val,
                 f"items={sa_sel}, w={sa_wt}", elapsed)
    results["SA"] = sa_val
    results_detail["SA"] = (sa_val, sa_wt)

    if plot:
        plot_knapsack_sa(knapsack, sa_sel, sa_val, sa_history)

    # ── 6. Genetic Algorithm ──────────────────────────────────────────────
    t0 = time.time()
    ga_sel, ga_val, ga_history = genetic_knapsack(
        knapsack,
        pop_size=80,
        generations=300,
        seed=SEED
    )
    ga_wt = sum(knapsack.weight(i) for i in ga_sel)
    elapsed = time.time() - t0
    print_result(f"Genetic Algorithm ({len(ga_history)} generations)", ga_val,
                 f"items={ga_sel}, w={ga_wt}", elapsed)
    results["Genetic"] = ga_val
    results_detail["Genetic"] = (ga_val, ga_wt)

    if plot:
        plot_knapsack_ga(knapsack, ga_sel, ga_val, ga_history)
        plot_knapsack_summary(results)
        plot_knapsack_weight_vs_value(knapsack, results_detail)

    # ── Summary ───────────────────────────────────────────────────────────
    print("\n" + "="*60)
    print(f"  KNAPSACK SUMMARY — {knapsack.name}")
    print("="*60)
    best = max(results.values())
    for name, val in results.items():
        marker = " ★ BEST" if val == best else ""
        print(f"  {name:<35} {val}{marker}")
    print("="*60)

    return results


def _to_binary(selected_indices, n):
    """Convert list of selected indices to binary list."""
    binary = [0] * n
    for i in selected_indices:
        binary[i] = 1
    return binary


if __name__ == "__main__":
    DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')
    ks_file = os.path.join(DATA_DIR, 'knapsack_large.txt')
    if os.path.exists(ks_file):
        knapsack = KnapsackInstance.from_file(ks_file)
    else:
        print("  Dataset not found — using default 10-item instance")
        knapsack = KnapsackInstance()
    run_all_knapsack(knapsack)
