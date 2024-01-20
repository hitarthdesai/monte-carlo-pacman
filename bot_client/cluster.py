import math
from typing import List
from gameState import GameState, Location
import numpy as np

GRID_WIDTH = 27
GRID_HEIGHT = 31


class Cluster:
    def __init__(self, x: int, y: int, n: int, gs: GameState) -> None:
        # NOTE: We are not passing a GameState here, beware not to use fn that depend on it
        self.location = Location(None)
        value = (x << 8) | y
        self.location.update(value)
        self.num_clusters = n
        self.magnitude = 0
        self.x_swings, self.y_swings = int(GRID_WIDTH / self.num_clusters), int(GRID_HEIGHT / self.num_clusters)
        self.updated_magnitude(gs)

    # update the magnitude of each cluster.
    def updated_magnitude(self, gs: GameState):
        for i in range(self.location.row - self.x_swings, self.location.row + self.x_swings):
            for j in range(self.location.col - self.y_swings, self.location.col + self.y_swings):
                if gs.pelletAt(i, j):
                    self.magnitude += 100 / ()

                    if (x := gs.pacmanLoc.distance_to(self.location)) != 0:
                        self.magnitude += 100 / (x**2)
                    else:
                        self.magnitude += 100
