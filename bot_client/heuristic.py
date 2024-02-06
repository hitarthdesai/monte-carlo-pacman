from gameState import GameState, Location
from cluster import Cluster

DISTANCE_THRESHOLD = 5

# This probably belongs in a constants file
NUM_CLUSTERS = 4
CLUSTER_STARTING_COORDINATES = [[7, 8], [7, 23], [20, 8], [20, 23]]


class Heuristic:
    def __init__(self, state: GameState):
        self.state = state
        self.heuristics = [
            self._manhattan_distance,
            self._avoid_too_close_to_normal_ghosts,
            self._prefer_close_to_scared_ghosts,
            self._cluster_heuristic,
        ]
        self.num_heuristics = len(self.heuristics)

        self._clusters = [
            Cluster(coords[0], coords[1], 4) for coords in CLUSTER_STARTING_COORDINATES
        ]

    def _manhattan_distance(self):
        return self.curr.distance_to(self.target)

    def _avoid_too_close_to_normal_ghosts(self):
        """
        Avoid being too close to normal ghosts
        """

        normal_ghosts = filter(lambda g: not g.isFrightened(), self.state.ghosts)
        penalties = map(
            lambda g: DISTANCE_THRESHOLD
            - min(DISTANCE_THRESHOLD, self.curr.distance_to(g.location)),
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
            lambda g: min(DISTANCE_THRESHOLD, self.curr.distance_to(g.location))
            - DISTANCE_THRESHOLD,
            scared_ghosts,
        )

        return sum(bonuses)

    def _cluster_heuristic(self, curr):
        # Bring all clusters up to date wrt current pacman location
        for cluster in self._clusters:
            cluster.update_magnitude(self.state)

        # idea: select what cluster region the pellet belongs to, then return the magnitude of that cluster.
        # This is used as a 'discount' of the distance, to incentivise staying in cluster region
        try:
            x_s, y_s = self._clusters[0].x_swings, self._clusters[0].y_swings
        except Exception as e:
            print(f"Error in swings: {e}")
            print(curr)
            return 0

        n_x, n_y = curr[0], curr[1]

        cluster_num = -1

        for i in range(len(self._clusters)):
            # idea: start in cluster region 1. If both elements of diffs negative, pellet in cluster region. If not check another region, until found
            c_x, c_y = (
                self._clusters[i].location.row + x_s,
                self._clusters[i].location.col + y_s,
            )
            diffs = n_x - c_x, n_y - c_y
            if diffs[0] < 0 and diffs[1] < 0:
                cluster_num = i
                break

        if cluster_num == -1:
            # something went wrong, dont apply heuristic
            return 0
        return self._clusters[cluster_num].magnitude

    def get_overall_heuristic(self, curr: Location, target: Location):
        self.curr = curr
        self.target = target

        best_heuristic_score = float("-inf")  # Initialize with negative infinity

        for h in self.heuristics:
            heuristic_score = 0

            if h == self._cluster_heuristic:
                curr_int = [curr.row, curr.col]
                heuristic_score = h(curr_int)

            elif h in [
                self._avoid_too_close_to_normal_ghosts,
                self._prefer_close_to_scared_ghosts,
            ]:
                heuristic_score = h() * 1000  # Experiment with weights

            else:
                heuristic_score = h()

            heuristic_score /= self.num_heuristics
            best_heuristic_score = max(best_heuristic_score, heuristic_score)

        return best_heuristic_score
