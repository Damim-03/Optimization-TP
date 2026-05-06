# Optimization Algorithms — TSP & Knapsack

Implementation of classical optimization algorithms applied to TSP and Knapsack problems.

## Project Structure

```
optimization_algorithms/
│
├── tsp/
│   ├── tsp_instance.py          # TSP problem definition & data
│   └── tsp_runner.py            # Run all algorithms on TSP
│
├── knapsack/
│   ├── knapsack_instance.py     # Knapsack problem definition & data
│   └── knapsack_runner.py       # Run all algorithms on Knapsack
│
├── algorithms/
│   ├── greedy_deterministic.py  # Greedy (Deterministic)
│   ├── greedy_nondeterministic.py # Greedy (Non-Deterministic / Randomized)
│   ├── local_search_first.py    # Local Search — First Improvement
│   ├── local_search_best.py     # Local Search — Best Improvement
│   ├── simulated_annealing.py   # Simulated Annealing
│   └── genetic.py               # Genetic Algorithm
│
├── utils/
│   └── helpers.py               # Shared utilities & display functions
│
├── main.py                      # Entry point — run everything
└── README.md
```

## Algorithms

| Algorithm | Type | TSP | Knapsack |
|-----------|------|-----|----------|
| Greedy Deterministic | Constructive | Nearest Neighbor | Sort by ratio |
| Greedy Non-Deterministic | Constructive (Randomized) | Random greedy | Random ratio |
| Local Search First-Improvement | Improvement | 2-opt (first) | Swap (first) |
| Local Search Best-Improvement | Improvement | 2-opt (best) | Swap (best) |
| Simulated Annealing | Metaheuristic | 2-opt moves | Swap moves |
| Genetic Algorithm | Metaheuristic | Order crossover | Binary GA |

## How to Run

```bash
# Run all algorithms on both problems
python main.py

# Run only TSP
python tsp/tsp_runner.py

# Run only Knapsack
python knapsack/knapsack_runner.py
```

## Requirements

```bash
pip install matplotlib numpy
```
