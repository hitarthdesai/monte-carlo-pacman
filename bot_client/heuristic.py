from typing import List
from gameState import GameState, Location, Ghost
from cluster import Cluster
from constants import (
    CLUSTER_STARTING_COORDINATES,
    NUM_CLUSTERS,
    NORMAL_GHOST_DISTANCE_THRESHOLD,
    SCARED_GHOST_DISTANCE_THRESHOLD,
    SUPER_PELLET_LOCATIONS,
    SP_AGG_GHOST_DISTANCE_THRESHOLD,
)


def create_super_pellet_location(x: int, y: int) -> Location:
    location = Location(None)
    location.update((x << 8) | y)
    return location


class Heuristic:
    def __init__(self):
        self.heuristics = [
            self._avoid_too_close_to_normal_ghosts,
            self._prefer_close_to_scared_ghosts,
            self._try_to_stay_away_from_normal_ghosts,
            self._try_to_chase_scared_ghosts,
            self._target_super_pellets,
        ]

        self.weights = [-1000, 1000, 1, 1000, 1000]
        self.num_heuristics = len(self.heuristics)

        self._clusters = [
            Cluster(coords[0], coords[1], NUM_CLUSTERS)
            for coords in CLUSTER_STARTING_COORDINATES
        ]

        self.super_pellet_locations = list(
            map(
                lambda loc: create_super_pellet_location(loc[0], loc[1]),
                SUPER_PELLET_LOCATIONS,
            )
        )

    def _avoid_too_close_to_normal_ghosts(self):
        """
        Avoid being too close to normal ghosts

        Add negative amount to heuristic score to avoid this behavior
        """

        normal_ghosts = filter(lambda g: not g.isFrightened(), self.state.ghosts)
        penalties = map(
            lambda g: max(
                0, NORMAL_GHOST_DISTANCE_THRESHOLD - self.curr.distance_to(g.location)
            ),
            normal_ghosts,
        )

        return sum(penalties)

    def _prefer_close_to_scared_ghosts(self):
        """
        Prefers being close to scared ghosts

        Add positive amount to heuristic score to encourage this behavior
        """

        scared_ghosts = filter(
            lambda g: g.isFrightened() and not g.spawning, self.state.ghosts
        )
        bonuses = map(
            lambda g: max(
                0, SCARED_GHOST_DISTANCE_THRESHOLD - self.curr.distance_to(g.location)
            ),
            scared_ghosts,
        )

        return sum(bonuses)

    def _try_to_stay_away_from_normal_ghosts(self):
        """
        Tries to stay away from normal ghosts

        Farther the ghosts, better the situation
        """

        normal_ghosts = filter(lambda g: not g.isFrightened(), self.state.ghosts)
        penalties = map(
            lambda g: self.curr.distance_to(g.location),
            normal_ghosts,
        )

        return sum(penalties)

    def _try_to_chase_scared_ghosts(self):
        """
        Tries to chase scared ghosts
        """

        scared_ghosts = filter(lambda g: g.isFrightened(), self.state.ghosts)
        bonuses = map(
            lambda g: (1 / (1 + self.curr.distance_to(g.location))),
            scared_ghosts,
        )

        # TODO: We need a better way to figure out if the ghost has been actually eaten.
        # Why: Misleading score in the beginning phase of the game.
        # Possible ways: check how many super pellets are present on board.
        ghosts_eaten = self.state.ghosts.count(lambda g: g.spawning)

        return sum(bonuses) + ghosts_eaten * 10

    def _target_super_pellets(self):
        if any(ghost.isFrightened() for ghost in self.state.ghosts):
            return 0

        super_pellets = list(
            filter(
                lambda p: self.state.pelletAt(p.row, p.col), self.super_pellet_locations
            )
        )
        if len(super_pellets) == 0:
            return 0

        super_pellets.sort(key=lambda p: self.curr.distance_to(p))
        closest_super_pellet = super_pellets[0]

        ghosts: List[Ghost] = sorted(
            filter(lambda g: not g.spawning, self.state.ghosts),
            key=lambda g: g.location.distance_to(closest_super_pellet),
        )

        aggregate_fright_distance = 0
        pellet_score = 0.0

        for i, ghost in enumerate(ghosts):
            aggregate_fright_distance += ghost.location.distance_to(
                closest_super_pellet
            )
            raw_ghost_score = max(
                (SP_AGG_GHOST_DISTANCE_THRESHOLD - aggregate_fright_distance)
                / SP_AGG_GHOST_DISTANCE_THRESHOLD,
                0,
            )
            pellet_score += raw_ghost_score * 2**i

        h_score = (
            pellet_score
            * (64 - self.state.pacmanLoc.distance_to(closest_super_pellet))
            / 64
        )

        return h_score

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
