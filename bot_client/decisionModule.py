import asyncio
import heapq
from typing import Optional, List
import math
from algo import Node
from heuristic import Heuristic
from util import location_to_direction
from cluster import Cluster

from gameState import GameState, Directions, Location, GameModes
import sys

if "-elec" in sys.argv:
    from motor_control import move_robot

DISTANCE_THRESHOLD = 5


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

        self.superPellets: List[Location] = []  # Initialize as an empty list
        self._initialize_super_pellets()

    def _initialize_super_pellets(self):
        # Initialize the locations of super pellets dynamically
        super_pellet_positions = [(3, 1), (3, 26), (23, 1), (23, 26)]
        self.superPellets = [Location(self.state) for _ in super_pellet_positions]

        # Update each super pellet location
        for location, (row, col) in zip(self.superPellets, super_pellet_positions):
            location.update((row << 8) | col)

    # TODO: Consider chase vs scatter mode.
    def _get_target(self) -> Optional[Location]:
        try:
            # return self.state.find_closest_pellet(self.state.pacmanLoc)
            return self._find_closest_pellet()
        except Exception as e:
            print(f"Error in finding closest pellet: {e}")
            return self.state.pacmanLoc

    def _is_pellet_safe(self, pellet: Location, clusters: List[Cluster]) -> bool:
        if type(pellet) is not Location:
            pelletLoc = Location(self.state)
            pelletLoc.update((pellet[0] << 8) | pellet[1])
            pellet = pelletLoc

        normal_ghosts = [g for g in self.state.ghosts if not g.isFrightened()]
        return all(
            pellet.distance_to(g.location) > DISTANCE_THRESHOLD for g in normal_ghosts
        )

    def _find_closest_pellet(self) -> Optional[Location]:
        grid_width, grid_height = 31, 31
        num_clusters = 4
        cluster_starting_coords = self._calculate_cluster_starting_coords(
            grid_width, grid_height, num_clusters
        )
        clusters = [
            Cluster(coords[0], coords[1], 4) for coords in cluster_starting_coords
        ]
        self._initialize_clusters(clusters)

        pellets = self._get_pellets_coords(grid_width, grid_height)

        pellets = [
            pellet for pellet in pellets if self._is_pellet_safe(pellet, clusters)
        ]

        try:
            return min(
                pellets,
                key=lambda point: self.state.pacmanLoc.distance_to_overload(point)
                - self.heuristic.cluster_heuristic(clusters, point),
            )
        except Exception as e:
            print(f"Error in return: {e}")
            return self._get_away_from_ghosts_when_cant_find_pellets()

    def _calculate_cluster_starting_coords(self, grid_width, grid_height, num_clusters):
        x_center_multiples, y_center_multiples = int(
            grid_width / (math.sqrt(num_clusters) + 1)
        ), int(grid_height / (math.sqrt(num_clusters) + 1))
        cluster_starting_coords = [
            ((i + 1) * x_center_multiples, (j + 1) * y_center_multiples)
            for i in range(int(math.sqrt(num_clusters)))
            for j in range(int(math.sqrt(num_clusters)))
        ]
        return cluster_starting_coords

    def _initialize_clusters(self, clusters):
        for cluster in clusters:
            cluster.location = Location(None)
            value = (cluster.x << 8) | cluster.y
            cluster.location.update(value)
            self.state.updated_magnitude(cluster)

    def _get_pellets_coords(self, grid_width, grid_height):
        pellets = [
            (x, y)
            for x in range(grid_width)
            for y in range(grid_height)
            if self.state.pelletAt(x, y)
        ]
        return pellets

    def _get_new_location(self, current_location, direction):
        if direction == Directions.UP:
            return (current_location.row, current_location.col + 1)
        elif direction == Directions.DOWN:
            return (current_location.row, current_location.col - 1)
        elif direction == Directions.LEFT:
            return (current_location.row - 1, current_location.col)
        elif direction == Directions.RIGHT:
            return (current_location.row + 1, current_location.col)

    def _get_new_location_as_location(self, current_location, direction):
        target = self._get_new_location(current_location, direction)
        if type(target) is not Location:
            targetLoc = Location(self.state)
            targetLoc.update((target[0] << 8) | target[1])
            target = targetLoc

        return target

    def _get_away_from_ghosts_when_cant_find_pellets(self):
        print("No pellets found, running away from ghosts")
        ghost_plans = [g.guessPlan() for g in self.state.ghosts]
        normal_ghosts = [g for g in self.state.ghosts if not g.isFrightened()]

        possible_moves = [
            Directions.UP,
            Directions.DOWN,
            Directions.LEFT,
            Directions.RIGHT,
        ]

        possible_moves = [
            move
            for move in possible_moves
            if not self.state.wallAt(
                *self._get_new_location(self.state.pacmanLoc, move)
            )
        ]

        # Remove any moves that would lead to a location that a ghost is planning to move to
        possible_moves = [
            move
            for move in possible_moves
            if self._get_new_location(self.state.pacmanLoc, move) not in ghost_plans
        ]

        # If there are no possible moves, stay in the current location
        if not possible_moves:
            return self.state.pacmanLoc

        best_move = max(
            possible_moves,
            key=lambda move: min(
                self._get_new_location_as_location(
                    self.state.pacmanLoc, move
                ).distance_to(g.location)
                for g in normal_ghosts
            ),
        )

        # Return the new location
        return self._get_new_location(self.state.pacmanLoc, best_move)

    def _get_next_move(self) -> Directions:
        target = self._get_target()
        if type(target) is not Location:
            targetLoc = Location(self.state)
            targetLoc.update((target[0] << 8) | target[1])
            target = targetLoc
        else:
            targetLoc = target

        start = self.state.pacmanLoc
        path = self._algo(start, targetLoc)
        if path is not None and len(path) > 0:
            _move = path[0]
            self._handle_super_pellet(_move)
            move = location_to_direction(start, _move)
            return move

        print("No path found")
        return Directions.NONE

    def _algo(self, start: Location, target: Location) -> List[Location]:
        open_list: List[Node] = list()
        closed_set = set()
        head = Node(start, None)
        head.g = 0
        head.h = self._get_heuristic(start, target)
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
                node.h = self._get_heuristic(loc, target)
                node.f = node.g + node.h
                heapq.heappush(open_list, node)

        return None

    def _handle_super_pellet(self, move: Location):
        if self.state.superPelletAt(move.row, move.col):
            self.superPellets = [
                sp
                for sp in self.superPellets
                if not (sp.row == move.row and sp.col == move.col)
            ]

    def _get_heuristic(self, curr: Location, other: Location) -> int:
        cluster_starting_coords = [[7, 8], [7, 23], [20, 8], [20, 23]]
        clusters = [
            Cluster(coords[0], coords[1], 4) for coords in cluster_starting_coords
        ]
        self._initialize_clusters(clusters)
        return self.heuristic.get_overall_heuristic(curr, other, clusters)

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

            direction_map = {
                Directions.UP: "N",
                Directions.LEFT: "W",
                Directions.DOWN: "S",
                Directions.RIGHT: "E",
                Directions.NONE: "NONE",
            }
            direction_letter = direction_map[next_move]
            if "-elec" in sys.argv:
                move_robot(1, direction_letter, 4)

            self.state.queueAction(4, next_move)
            self.state.unlock()
