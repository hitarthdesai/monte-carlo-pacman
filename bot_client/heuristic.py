from gameState import GameState, Location


class Heuristic:
    def __init__(self, state: GameState):
        self.state = state
        self.heuristics = [
            self._manhattan_distance,
            self._avoid_too_close_to_normal_ghosts,
            self._prefer_close_to_scared_ghosts,
        ]
        self.num_heuristics = len(self.heuristics)
        print(f"Number of Heursitics: {self.num_heuristics}")

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

    def get_overall_heuristic(self, curr: Location, target: Location):
        self.curr = curr
        self.target = target

        score = 0.0
        for h in self.heuristics:
            score += h() / self.num_heuristics
        return score
