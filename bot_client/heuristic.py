from gameState import GameState, Location
from cluster import Cluster, Clusters


class Heuristic:
    def __init__(self, state: GameState):
        self.state = state
        self.heuristics = [
            self._manhattan_distance,
            self._avoid_too_close_to_normal_ghosts,
            self._prefer_close_to_scared_ghosts,
            self.cluster_heuristic
        ]
        self.num_heuristics = len(self.heuristics)
        print(f"Number of Heuristics: {self.num_heuristics}")

    def _manhattan_distance(self):
        return self.curr.distance_to(self.target)

    def _avoid_too_close_to_normal_ghosts(self):
        """
        Avoid being too close to normal ghosts
        """
        distance_threshold = 5

        normal_ghosts = filter(lambda g: not g.isFrightened(), self.state.ghosts)
        distances = map(
            lambda g: min(distance_threshold, self.curr.distance_to(g.location)),
            normal_ghosts,
        )
        penalties = map(lambda d: distance_threshold - d, distances)

        return sum(penalties)

    def _prefer_close_to_scared_ghosts(self):
        """
        Prefers being close to scared ghosts
        """
        distance_threshold = 5

        scared_ghosts = filter(lambda g: g.isFrightened(), self.state.ghosts)
        distances = map(
            lambda g: min(distance_threshold, self.curr.distance_to(g.location)),
            scared_ghosts,
        )
        penalties = map(lambda d: d - distance_threshold, distances)

        return sum(penalties)
    
    def cluster_heuristic(self, state: GameState, clusters: Clusters, curr: Location):
        #idea: select what cluster region the pellet belongs to, then return the magnitude of that cluster. 
        # This is used as a 'discount' of the distance, to incentivise staying in cluster region

        x_swings, y_swings = clusters[0].x_swings, clusters[0].y_swings
        n_x,n_y = curr.row, curr.col

        cluster_num = -1

        for i in range(len(clusters)):
            #idea: start in cluster region 1. If both elements of diffs negative, pellet in cluster region. If not check another region, until found
            c_x, c_y = clusters[i].coords.x + x_swings, clusters[i].coords.y + y_swings
            diffs = n_x - c_x, n_y - c_y
            if diffs[0] < 0 and diffs[1] < 0:
                cluster_num = i
                break
            
        if cluster_num == -1:
            #something went wrong, dont apply heuristic
            return 0
        return clusters[cluster_num].magnitude

    def get_overall_heuristic(self, curr: Location, target: Location):
        self.curr = curr
        self.target = target

        score = 0.0
        for h in self.heuristics:
            score += h() / self.num_heuristics
        return score
