from typing import List

GRID_WIDTH = 27
GRID_HEIGHT = 31


class Cluster:
    def __init__(self, x: int, y: int, n: int) -> None:
        # NOTE: We are not passing a GameState here, beware not to use fn that depend on it
        self.x = x
        self.y = y
        self.location = None
        # value = (x << 8) | y
        # self.location.update(value)
        self.num_clusters = n
        self.magnitude = 0
        self.x_swings, self.y_swings = int(GRID_WIDTH / self.num_clusters), int(GRID_HEIGHT / self.num_clusters)
