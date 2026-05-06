# main.py
# ─────────────────────────────────────────────────────────────────────────────
# ENTRY POINT — Run all algorithms on both TSP and Knapsack
# ─────────────────────────────────────────────────────────────────────────────

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from tsp.tsp_instance        import TSPInstance
from knapsack.knapsack_instance import KnapsackInstance
from tsp.tsp_runner          import run_all_tsp
from knapsack.knapsack_runner import run_all_knapsack


def main():
    print("\n" + "█" * 60)
    print("█   OPTIMIZATION ALGORITHMS — TSP & KNAPSACK             █")
    print("█" * 60)
    print()

    # ── TSP ──────────────────────────────────────────────────────
    tsp = TSPInstance()          # default 10-city instance
    tsp_results = run_all_tsp(tsp)

    print("\n")

    # ── KNAPSACK ─────────────────────────────────────────────────
    knapsack = KnapsackInstance()  # default 10-item instance
    ks_results = run_all_knapsack(knapsack)

    print("\n\n" + "█" * 60)
    print("█   ALL DONE                                             █")
    print("█" * 60 + "\n")


if __name__ == "__main__":
    main()
