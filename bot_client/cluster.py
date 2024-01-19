import math
from typing import List
from gameState import GameState, Location
import numpy as np

GRID_WIDTH = 27
GRID_HEIGHT = 31


class Cluster:
    def __init__(self, x: int, y: int) -> None:
        # NOTE: We are not passing a GameState here, beware not to use fn that depend on it
        self.location = Location(None)
        value = (x << 8) | y
        self.location.update(value)

        self.magnitude = 0

    def updated_magnitude(self, x_swings: int, y_swings: int, gs: GameState):
        for i in range(self.location.row - x_swings, self.location.row + x_swings):
            for j in range(self.location.col - y_swings, self.location.col + y_swings):
                if gs.pelletAt(i, j):
                    self.magnitude += 100 / ()

                    if (x := gs.pacmanLoc.distance_to(self.location)) != 0:
                        self.magnitude += 100 / (x**2)
                    else:
                        self.magnitude += 100


class Clusters:
    def __init__(self, n: int) -> None:
        self.value = int(GRID_WIDTH / self.num_clusters)

        self.x_swings = np.full(n, self.value)
        self.y_swings = np.full(n, self.value)
        
        self.clusters: List[Cluster] = list()

        x_center_multiples = int(GRID_WIDTH / (math.sqrt(n) + 1))
        y_center_multiples = int(GRID_HEIGHT / (math.sqrt(n) + 1))

        for i in range(int(math.sqrt(n))):
            for j in range(int(math.sqrt(n))):
                x = int((i + 1) * x_center_multiples)
                y = int((j + 1) * y_center_multiples)
                self.clusters.append(Cluster(x, y))
