# tsp/tsp_instance.py
# TSP Problem Definition
# Goal: find the shortest route visiting all cities exactly once and returning to start.

import math


class TSPInstance:
    """
    Traveling Salesman Problem instance.
    Cities are represented as (x, y) coordinates.
    """

    def __init__(self, cities=None):
        if cities is None:
            # Default: 10 cities with fixed coordinates
            self.cities = [
                (0,  0),
                (2,  4),
                (5,  2),
                (8,  5),
                (6,  8),
                (3,  7),
                (1,  5),
                (4,  1),
                (7,  3),
                (9,  9),
            ]
        else:
            self.cities = cities

        self.n = len(self.cities)
        self.dist_matrix = self._build_distance_matrix()

    def _build_distance_matrix(self):
        """Precompute Euclidean distances between all city pairs."""
        n = self.n
        matrix = [[0.0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                if i != j:
                    xi, yi = self.cities[i]
                    xj, yj = self.cities[j]
                    matrix[i][j] = math.sqrt((xi - xj)**2 + (yi - yj)**2)
        return matrix

    def distance(self, i, j):
        """Return distance between city i and city j."""
        return self.dist_matrix[i][j]

    def tour_cost(self, tour):
        """
        Calculate total cost of a tour.
        tour: list of city indices, e.g. [0, 2, 5, 1, ...]
        Returns total distance including return to start.
        """
        total = 0.0
        n = len(tour)
        for i in range(n):
            total += self.distance(tour[i], tour[(i + 1) % n])
        return total

    def all_cities(self):
        """Return list of all city indices."""
        return list(range(self.n))

    def __repr__(self):
        return f"TSPInstance(n={self.n} cities)"
