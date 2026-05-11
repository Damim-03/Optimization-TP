# knapsack/knapsack_instance.py
import os


class KnapsackInstance:
    def __init__(self, items=None, capacity=None, name="Knapsack"):
        self.name = name
        if items is None:
            self.items = [
                (2,6),(3,10),(4,12),(5,13),(9,20),
                (7,15),(1,3),(6,11),(3,9),(8,18),
            ]
        else:
            self.items = items
        self.capacity = capacity if capacity is not None else 20
        self.n = len(self.items)

    @classmethod
    def from_file(cls, filepath):
        """
        Load from a text file.
        Line 1 (non-comment): n capacity
        Next n lines: weight value
        """
        items = []
        capacity = None
        n = None
        name = os.path.basename(filepath).replace(".txt","").replace(".dat","")
        with open(filepath) as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                parts = line.split()
                if n is None:
                    n, capacity = int(parts[0]), int(parts[1])
                else:
                    items.append((int(parts[0]), int(parts[1])))
                    if len(items) == n:
                        break
        instance = cls(items=items, capacity=capacity, name=name)
        print(f"  Loaded Knapsack: {name} — {n} items, capacity={capacity}")
        return instance

    def weight(self, i): return self.items[i][0]
    def value(self, i):  return self.items[i][1]
    def ratio(self, i):  return self.items[i][1] / self.items[i][0]

    def solution_value(self, selection):
        if isinstance(selection,(list,tuple)) and len(selection)==self.n and all(x in(0,1) for x in selection):
            indices = [i for i,b in enumerate(selection) if b==1]
        else:
            indices = list(selection)
        tw = sum(self.weight(i) for i in indices)
        tv = sum(self.value(i)  for i in indices)
        return tv, tw, tw <= self.capacity

    def all_items(self): return list(range(self.n))
    def __repr__(self): return f"KnapsackInstance(name={self.name}, n={self.n}, cap={self.capacity})"
