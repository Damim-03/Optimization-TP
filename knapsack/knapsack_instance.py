# knapsack/knapsack_instance.py
# 0/1 Knapsack Problem Definition
# Goal: select items to maximize total value without exceeding capacity.


class KnapsackInstance:
    """
    0/1 Knapsack Problem instance.
    Each item has a weight and a value.
    We want to maximize total value without exceeding capacity.
    """

    def __init__(self, items=None, capacity=None):
        if items is None:
            # Default: 10 items (weight, value)
            self.items = [
                (2, 6),   # item 0
                (3, 10),  # item 1
                (4, 12),  # item 2
                (5, 13),  # item 3
                (9, 20),  # item 4
                (7, 15),  # item 5
                (1, 3),   # item 6
                (6, 11),  # item 7
                (3, 9),   # item 8
                (8, 18),  # item 9
            ]
        else:
            self.items = items

        self.capacity = capacity if capacity is not None else 20
        self.n = len(self.items)

    def weight(self, i):
        return self.items[i][0]

    def value(self, i):
        return self.items[i][1]

    def ratio(self, i):
        """Value-to-weight ratio for item i."""
        return self.items[i][1] / self.items[i][0]

    def solution_value(self, selection):
        """
        Calculate total value of a selection.
        selection: list/set of item indices OR binary list [0,1,0,1,...]
        Returns (total_value, total_weight, is_feasible)
        """
        if isinstance(selection, (list, tuple)) and len(selection) == self.n and all(x in (0, 1) for x in selection):
            # Binary encoding
            indices = [i for i, bit in enumerate(selection) if bit == 1]
        else:
            indices = list(selection)

        total_weight = sum(self.weight(i) for i in indices)
        total_value  = sum(self.value(i)  for i in indices)
        feasible     = total_weight <= self.capacity

        return total_value, total_weight, feasible

    def all_items(self):
        return list(range(self.n))

    def __repr__(self):
        return f"KnapsackInstance(n={self.n} items, capacity={self.capacity})"
