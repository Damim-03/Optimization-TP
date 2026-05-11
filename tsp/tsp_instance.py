# tsp/tsp_instance.py
import math
import os


class TSPInstance:
    def __init__(self, cities=None, name="TSP"):
        self.name = name
        self.edge_type = "EUC_2D"
        if cities is None:
            self.cities = [
                (0,0),(2,4),(5,2),(8,5),(6,8),
                (3,7),(1,5),(4,1),(7,3),(9,9),
            ]
        else:
            self.cities = cities
        self.n = len(self.cities)
        self.dist_matrix = self._build_distance_matrix()

    @classmethod
    def from_tsp_file(cls, filepath):
        cities = []
        edge_type = "EUC_2D"
        name = os.path.basename(filepath).replace(".tsp", "")
        with open(filepath) as f:
            reading = False
            for line in f:
                line = line.strip()
                if line.startswith("NAME"):
                    name = line.split(":")[-1].strip()
                if line.startswith("EDGE_WEIGHT_TYPE"):
                    edge_type = line.split(":")[-1].strip()
                if line == "NODE_COORD_SECTION":
                    reading = True
                    continue
                if line in ("EOF", ""):
                    continue
                if reading:
                    parts = line.split()
                    if len(parts) >= 3:
                        cities.append((float(parts[1]), float(parts[2])))
        instance = cls(cities=cities, name=name)
        instance.edge_type = edge_type
        if edge_type == "ATT":
            instance.dist_matrix = instance._build_att_distance_matrix()
        print(f"  Loaded TSP: {name} — {len(cities)} cities  [{edge_type}]")
        return instance

    def _build_distance_matrix(self):
        n = self.n
        matrix = [[0.0]*n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                if i != j:
                    xi,yi = self.cities[i]
                    xj,yj = self.cities[j]
                    matrix[i][j] = math.sqrt((xi-xj)**2+(yi-yj)**2)
        return matrix

    def _build_att_distance_matrix(self):
        n = self.n
        matrix = [[0.0]*n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                if i != j:
                    xi,yi = self.cities[i]
                    xj,yj = self.cities[j]
                    xd,yd = xi-xj, yi-yj
                    rij = math.sqrt((xd*xd+yd*yd)/10.0)
                    tij = round(rij)
                    matrix[i][j] = tij+1 if tij < rij else tij
        return matrix

    def distance(self, i, j):
        return self.dist_matrix[i][j]

    def tour_cost(self, tour):
        total = 0.0
        n = len(tour)
        for i in range(n):
            total += self.distance(tour[i], tour[(i+1)%n])
        return total

    def all_cities(self):
        return list(range(self.n))

    def __repr__(self):
        return f"TSPInstance(name={self.name}, n={self.n})"
