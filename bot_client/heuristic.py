from gameState import GameState, Location
from cluster import Cluster

DISTANCE_THRESHOLD = 5


class Heuristic:
    def __init__(self, state: GameState):
        self.state = state
        self.heuristics = [
            self._manhattan_distance,
            self._avoid_too_close_to_normal_ghosts,
            self._prefer_close_to_scared_ghosts,
            self.cluster_heuristic,
        ]
        self.num_heuristics = len(self.heuristics)

    def _manhattan_distance(self):
        return self.curr.distance_to(self.target)

    def _avoid_too_close_to_normal_ghosts(self):
        """
        Avoid being too close to normal ghosts
        """

        normal_ghosts = [g for g in self.state.ghosts if not g.isFrightened()]
        distances = [
            min(DISTANCE_THRESHOLD, self.curr.distance_to(g.location))
            for g in normal_ghosts
        ]

        penalties = [DISTANCE_THRESHOLD - d for d in distances]

        return sum(penalties)

    def _prefer_close_to_scared_ghosts(self):
        """
        Prefers being close to scared ghosts
        """
        scared_ghosts = [g for g in self.state.ghosts if g.isFrightened()]
        distances = [
            min(DISTANCE_THRESHOLD, self.curr.distance_to(g.location))
            for g in scared_ghosts
        ]
        bonuses = [DISTANCE_THRESHOLD - d for d in distances]
        return sum(bonuses)

    def cluster_heuristic(self, clusters: list[Cluster], curr):
        # idea: select what cluster region the pellet belongs to, then return the magnitude of that cluster.
        # This is used as a 'discount' of the distance, to incentivise staying in cluster region
        try:
            x_s, y_s = clusters[0].x_swings, clusters[0].y_swings
        except Exception as e:
            print(f"Error in swings: {e}")
            print(curr)
            return 0

        n_x, n_y = curr[0], curr[1]

        cluster_num = -1

        for i in range(len(clusters)):
            # idea: start in cluster region 1. If both elements of diffs negative, pellet in cluster region. If not check another region, until found
            c_x, c_y = clusters[i].location.row + x_s, clusters[i].location.col + y_s
            diffs = n_x - c_x, n_y - c_y
            if diffs[0] < 0 and diffs[1] < 0:
                cluster_num = i
                break

        if cluster_num == -1:
            # something went wrong, dont apply heuristic
            return 0
        return clusters[cluster_num].magnitude

    def get_overall_heuristic(self, curr: Location, target: Location, clusters=None):
        self.curr = curr
        self.target = target

        best_heuristic_score = float("-inf")  # Initialize with negative infinity

        for h in self.heuristics:
            heuristic_score = 0

            if h == self.cluster_heuristic:
                curr_int = [curr.row, curr.col]
                heuristic_score = h(clusters, curr_int)

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
