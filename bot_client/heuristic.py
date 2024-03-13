from gameState import GameState
from cluster import Cluster
from constants import CLUSTER_STARTING_COORDINATES, DISTANCE_THRESHOLD, NUM_CLUSTERS


class Heuristic:
    def __init__(self):
        self.heuristics = [
            self._avoid_too_close_to_normal_ghosts,
            self._prefer_close_to_scared_ghosts,
        ]

        self.weights = [-1000, 1000]
        self.num_heuristics = len(self.heuristics)

        self._clusters = [
            Cluster(coords[0], coords[1], NUM_CLUSTERS)
            for coords in CLUSTER_STARTING_COORDINATES
        ]

    def _avoid_too_close_to_normal_ghosts(self):
        """
        Avoid being too close to normal ghosts
        """

        normal_ghosts = filter(lambda g: not g.isFrightened(), self.state.ghosts)
        penalties = map(
            lambda g: max(0, DISTANCE_THRESHOLD - self.curr.distance_to(g.location)),
            normal_ghosts,
        )

        return sum(penalties)

    def _prefer_close_to_scared_ghosts(self):
        """
        Prefers being close to scared ghosts
        """

        scared_ghosts = filter(
            lambda g: g.isFrightened() and not g.spawning, self.state.ghosts
        )
        bonuses = map(
            lambda g: max(0, DISTANCE_THRESHOLD - self.curr.distance_to(g.location)),
            scared_ghosts,
        )

        return sum(bonuses)

    def _cluster_heuristic(self):
        # Bring all clusters up to date wrt current pacman location
        for cluster in self._clusters:
            cluster.update_magnitude(self.state)

        x_swings, y_swings = self._clusters[0].x_swings, self._clusters[0].y_swings

        cluster_num = -1
        for i in range(len(self._clusters)):
            # idea: start in cluster region 1. If both elements of diffs negative, pellet in cluster region. If not check another region, until found
            c_x, c_y = (
                self._clusters[i].location.row + x_swings,
                self._clusters[i].location.col + y_swings,
            )
            diffs = self.curr.row - c_x, self.curr.col - c_y
            if diffs[0] < 0 and diffs[1] < 0:
                cluster_num = i
                break

        if cluster_num == -1:
            # something went wrong, dont apply heuristic
            return 0
        return self._clusters[cluster_num].magnitude

    def get_overall_heuristic(self, state: GameState):
        self.state = state
        self.curr = state.pacmanLoc

        heuristic_score = 0
        for i in range(self.num_heuristics):
            heuristic_score += self.weights[i] * self.heuristics[i]()

        return heuristic_score
