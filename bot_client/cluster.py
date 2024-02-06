from gameState import Location, GameState

GRID_WIDTH = 27
GRID_HEIGHT = 31


class Cluster:
    def __init__(self, x: int, y: int, n: int) -> None:
        self.x = x
        self.y = y
        self.location = Location(None)
        self.location.update((x << 8) | y)
        self.num_clusters = n
        self.magnitude = 0
        self.x_swings, self.y_swings = int(GRID_WIDTH / self.num_clusters), int(
            GRID_HEIGHT / self.num_clusters
        )

    def update_magnitude(self, gs: GameState):
        self.magnitude = 0
        for i in range(
            self.location.row - self.x_swings,
            self.location.row + self.x_swings,
        ):
            for j in range(
                self.location.col - self.y_swings,
                self.location.col + self.y_swings,
            ):
                if gs.pelletAt(i, j):
                    if (x := gs.pacmanLoc.distance_to(self.location)) != 0:
                        self.magnitude += 100 / (x**2)
                    else:
                        self.magnitude += 100
