# main.py — Entry point
import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from tsp.tsp_instance           import TSPInstance
from knapsack.knapsack_instance  import KnapsackInstance
from tsp.tsp_runner              import run_all_tsp
from knapsack.knapsack_runner    import run_all_knapsack

DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')

def main():
    print("\n" + "█"*60)
    print("█   OPTIMIZATION ALGORITHMS — TSP & KNAPSACK             █")
    print("█"*60 + "\n")

    # ── TSP ──────────────────────────────────────────────────────────────
    tsp_file = os.path.join(DATA_DIR, 'att48.tsp')
    if os.path.exists(tsp_file):
        tsp = TSPInstance.from_tsp_file(tsp_file)
    else:
        print("  [WARNING] att48.tsp not found — using default 10-city instance")
        tsp = TSPInstance()
    run_all_tsp(tsp, plot=True)

    print("\n\n")

    # ── KNAPSACK ──────────────────────────────────────────────────────────
    ks_file = os.path.join(DATA_DIR, 'knapsack_large.txt')
    if os.path.exists(ks_file):
        knapsack = KnapsackInstance.from_file(ks_file)
    else:
        print("  [WARNING] knapsack_large.txt not found — using default 10-item instance")
        knapsack = KnapsackInstance()
    run_all_knapsack(knapsack, plot=True)

    print("\n\n" + "█"*60)
    print("█   ALL DONE — plots saved in ./plots/                   █")
    print("█"*60 + "\n")

if __name__ == "__main__":
    main()
