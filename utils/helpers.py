# utils/helpers.py
# Shared utility functions for displaying results

import time


def print_separator(char="=", length=60):
    print(char * length)


def print_header(title):
    print_separator()
    print(f"  {title}")
    print_separator()


def print_result(algorithm_name, value, solution=None, elapsed=None):
    print(f"\n{'─'*50}")
    print(f"  Algorithm : {algorithm_name}")
    print(f"  Result    : {value:.4f}" if isinstance(value, float) else f"  Result    : {value}")
    if solution is not None:
        if len(str(solution)) < 80:
            print(f"  Solution  : {solution}")
        else:
            print(f"  Solution  : {str(solution)[:80]}...")
    if elapsed is not None:
        print(f"  Time      : {elapsed:.4f}s")
    print(f"{'─'*50}")


def timeit(func):
    """Decorator to measure execution time."""
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        elapsed = time.time() - start
        return result, elapsed
    return wrapper
