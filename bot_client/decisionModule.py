import asyncio
import heapq
from typing import List, Tuple
from algo import Node
from heuristic import Heuristic
from util import location_to_direction, direction_to_elec_move, next_move_in_direction

from gameState import GameState, Directions, Location, GameModes
import sys

if "-elec" in sys.argv:
    from elec import move_robot

GRID_WIDTH = 31
GRID_HEIGHT = 31
DISTANCE_THRESHOLD = 5

ALL_DIRECTIONS = [
    Directions.UP,
    Directions.DOWN,
    Directions.LEFT,
    Directions.RIGHT,
]

SUPER_PELLET_POSITIONS: List[Tuple[int, int]] = [(3, 1), (3, 26), (23, 1), (23, 26)]


class DecisionModule:
    """
    Sample implementation of a decision module for high-level
    programming for Pacbot, using asyncio.
    """

    def __init__(self, state: GameState) -> None:
        """
        Construct a new decision module object
        """

        # Game state object to store the game information
        self.state = state
        self.heuristic = Heuristic(state)

    # TODO: Consider chase vs scatter mode.
    def _get_target(self) -> Location:
        try:
            return self._find_closest_safe_pellet()
        except Exception as e:
            print(f"Error in finding closest pellet: {e}")
            return self.state.pacmanLoc

    def _is_pellet_safe(self, pellet: Location) -> bool:
        if type(pellet) is not Location:
            pelletLoc = Location(self.state)
            pelletLoc.update((pellet[0] << 8) | pellet[1])
            pellet = pelletLoc

        normal_ghosts = [g for g in self.state.ghosts if not g.isFrightened()]
        return all(
            pellet.distance_to(g.location) > DISTANCE_THRESHOLD for g in normal_ghosts
        )

    def _find_closest_safe_pellet(self) -> Location:
        """
        Find the closest pellet to the current location of Pacman
        It skips any pellets that are within a CONSTANT distance of any normal ghost

        If no pellets are found, it tries to run away from all ghosts
        """

        safe_pellets = [
            (x, y)
            for x in range(GRID_WIDTH)
            for y in range(GRID_HEIGHT)
            if self.state.pelletAt(x, y) and self._is_pellet_safe((x, y))
        ]

        try:
            x, y = min(
                safe_pellets,
                key=lambda point: self.state.pacmanLoc.distance_to_overload(point)
                - self.heuristic._cluster_heuristic(point),
            )

            closest_safe_pellet = Location(self.state)
            closest_safe_pellet.update((x << 8) | y)
            return closest_safe_pellet

        except Exception as e:
            print(f"Error in _find_closest_safe_pellet: {e}")
            return self._get_away_from_ghosts_when_cant_find_pellets()

    def _get_away_from_ghosts_when_cant_find_pellets(self):
        print("No pellets found, running away from ghosts")
        ghost_plans = [
            next_move_in_direction(g.location, g.guessPlan()) for g in self.state.ghosts
        ]

        all_possible_moves = map(
            lambda d: next_move_in_direction(self.state.pacmanLoc, d), ALL_DIRECTIONS
        )
        # Remove any moves that hit a wall or a ghost is planning to move to
        valid_moves = filter(
            lambda loc: not self.state.wallAt(loc.row, loc.col)
            and loc not in ghost_plans,
            all_possible_moves,
        )

        # If there are no possible moves, stay in the current location
        if not valid_moves:
            return self.state.pacmanLoc

        normal_ghosts = [g for g in self.state.ghosts if not g.isFrightened()]
        best_move = max(
            valid_moves,
            key=lambda move: min(move.distance_to(g.location) for g in normal_ghosts),
        )

        return best_move

    def _get_next_move(self) -> Directions:
        target = self._get_target()
        start = self.state.pacmanLoc
        path = self._algo(start, target)
        if path is not None and len(path) > 0:
            _move = path[0]
            move = location_to_direction(start, _move)
            return move

        print("No path found")
        return Directions.NONE

    def _algo(self, start: Location, target: Location) -> List[Location]:
        open_list: List[Node] = list()
        closed_set = set()
        head = Node(start, None)
        head.g = 0
        head.h = self.heuristic.get_overall_heuristic(start, target)
        head.f = head.h
        heapq.heappush(open_list, head)

        while open_list:
            curr = heapq.heappop(open_list)
            if curr.position.at(target.row, target.col):
                path: List[Location] = []
                while curr.position != start:
                    try:
                        path.append(curr.position)
                        curr = curr.parent
                    except Exception as e:
                        print(f"Error: {e}")
                        break
                path.reverse()
                return path

            closed_set.add(Location.__str__(curr.position))
            all_neighbors = map(
                lambda dir: (curr.position.row + dir[0], curr.position.col + dir[1]),
                [(1, 0), (-1, 0), (0, 1), (0, -1)],
            )

            valid_neighbors = filter(
                lambda pos: not self.state.wallAt(pos[0], pos[1]),
                all_neighbors,
            )

            for neighbor in valid_neighbors:
                if str(neighbor) in closed_set:
                    continue
                loc = Location(self.state)
                loc.update((neighbor[0] << 8) | neighbor[1])
                node = Node(loc, curr)
                node.g = curr.g + 1
                node.h = self.heuristic.get_overall_heuristic(loc, target)
                node.f = node.g + node.h
                heapq.heappush(open_list, node)

        return None

    async def decisionLoop(self) -> None:
        while self.state.isConnected():
            if (
                len(self.state.writeServerBuf) > 0
                or self.state.gameMode == GameModes.PAUSED.value
            ):
                await asyncio.sleep(0.01)  # change if pacman isn't moving as expected
                continue

            self.state.lock()
            next_move = self._get_next_move()
            elec_move = direction_to_elec_move(next_move)

            if "-elec" in sys.argv:
                move_robot(1, elec_move)

            self.state.queueAction(4, next_move)
            self.state.unlock()
