import asyncio
import heapq
from typing import Optional, List
import math
from algo import Node
from heuristic import Heuristic
from util import location_to_direction
from cluster import Cluster

from gameState import GameState, Directions, Location, GameModes


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

        # Locations of super pellets
        # TODO: There has to be a better way of doing this
        self.superPellets: List[Location] = [None] * 4
        self.superPellets[0] = Location(self.state)
        self.superPellets[0].update((3 << 8) | 1)
        self.superPellets[1] = Location(self.state)
        self.superPellets[1].update((3 << 8) | 26)
        self.superPellets[2] = Location(self.state)
        self.superPellets[2].update((23 << 8) | 1)
        self.superPellets[3] = Location(self.state)
        self.superPellets[3].update((23 << 8) | 26)

    # TODO: Consider chase vs scatter mode.
    def _get_target(self) -> Optional[Location]:
        try:
            # return self.state.find_closest_pellet(self.state.pacmanLoc)
            return self.find_closest_pellet()
        except Exception as e:
            print(f"Error in finding closest pellet: {e}")
            return self.state.pacmanLoc

    def _get_next_move(self) -> Directions:
        target = self._get_target()
        if type(target) is not Location:
            targetLoc = Location(self.state)
            targetLoc.update((target[0] << 8) | target[1])
            target = targetLoc
        else:
            targetLoc = target

        start = self.state.pacmanLoc
        path = self.algo(start, targetLoc)
        if path is not None and len(path) > 0:
            _move = path[0]

            # Remove super pellet if we're on it
            if self.state.superPelletAt(_move.row, _move.col):
                self.superPellets = list(
                    filter(
                        lambda sp: not (sp.row == _move.row and sp.col == _move.col),
                        self.superPellets,
                    )
                )

            move = location_to_direction(start, _move)
            return move

        print("No path found 🥲")
        return Directions.NONE

    def _get_heuristic(self, curr: Location, other: Location) -> int:
        cluster_starting_coords = [[7, 8], [7, 23], [20, 8], [20, 23]]
        clusters = [
            Cluster(coords[0], coords[1], 4) for coords in cluster_starting_coords
        ]

        for cluster in clusters:
            cluster.location = Location(None)
            value = (cluster.x << 8) | cluster.y
            cluster.location.update(value)
            self.state.updated_magnitude(cluster)

        return self.heuristic.get_overall_heuristic(curr, other, clusters)

    def find_closest_pellet(self) -> Optional[Location]:
        grid_width, grid_height = (31, 31)
        num_clusters = 4  # must be a perfect square
        # cluster_starting_coords = [[7, 8], [7, 23], [20, 8], [20, 23]]
        cluster_starting_coords = list()

        # center multiples determine cluster coords. ex if num_clusters = 4, want 2 clusters across, 2 down; divide grid_width into 1/(sqrt(2)+1) = 3 equal sections
        x_center_multiples, y_center_multiples = int(
            grid_width / (math.sqrt(num_clusters) + 1)
        ), int(grid_height / (math.sqrt(num_clusters) + 1))
        # compute the coords of the center of each cluster
        for i in range(int(math.sqrt(num_clusters))):
            for j in range(int(math.sqrt(num_clusters))):
                coords = [(i + 1) * x_center_multiples, (j + 1) * y_center_multiples]
                cluster_starting_coords.append(coords)

        # Create cluster objects
        clusters = [
            Cluster(coords[0], coords[1], 4) for coords in cluster_starting_coords
        ]

        for cluster in clusters:
            cluster.location = Location(None)
            value = (cluster.x << 8) | cluster.y
            cluster.location.update(value)
            self.state.updated_magnitude(cluster)

        pellets: list[int] = list()
        for x in range(grid_width):
            for y in range(grid_height):
                if self.state.pelletAt(x, y):
                    pellets.append((x, y))

        try:
            # Metric for closeness: Manhattan distance
            return min(
                pellets,
                key=lambda point: self.state.pacmanLoc.distance_to_overload(point)
                - self.heuristic.cluster_heuristic(clusters, point),
            )
        except Exception as e:
            print(f"Error in return: {e}")
            return self.state.pacmanLoc

    def algo(self, start: Location, target: Location) -> List[Location]:
        """
        Find a path from start to target position using A*
        """
        open_list: List[Node] = list()  # Priority queue for open nodes
        closed_set = set()  # Set to store visited nodes
        # Create the start node and initialize its costs
        head = Node(start, None)
        head.g = 0
        head.h = self._get_heuristic(start, target)
        head.f = head.h

        # Add the start node to open list
        heapq.heappush(open_list, head)

        while open_list:
            curr = heapq.heappop(open_list)
            # Check if the current node is the target node
            if curr.position.at(target.row, target.col):
                path: List[Location] = []
                # Reconstruct the path by following parent pointers
                while curr.position != start:
                    try:
                        path.append(curr.position)
                        curr = curr.parent
                    except Exception as e:
                        print(f"EEEEEE {e}")
                path.reverse()
                return path

            # TODO: Needs to be made serializable
            closed_set.add(Location.__str__(curr.position))

            all_neighbors = map(
                lambda dir: (curr.position.row + dir[0], curr.position.col + dir[1]),
                [
                    (1, 0),
                    (-1, 0),
                    (0, 1),
                    (0, -1),
                ],
            )

            valid_neighbors = filter(
                lambda pos: not self.state.wallAt(pos[0], pos[1]),
                all_neighbors,
            )

            for neighbor in valid_neighbors:
                if str(neighbor) in closed_set:
                    continue

                print(f"neighbor: {neighbor}")

                loc = Location(self.state)
                loc.update((neighbor[0] << 8) | neighbor[1])
                node = Node(loc, curr)
                node.g = curr.g + 1
                node.h = self._get_heuristic(loc, target)
                node.f = node.g + node.h

                heapq.heappush(open_list, node)

        return None

    async def decisionLoop(self) -> None:
        """
        Decision loop for Pacbot
        """

        # Receive values as long as we have access
        while self.state.isConnected():
            """
            WARNING: 'await' statements should be routinely placed
            to free the event loop to receive messages, or the
            client may fall behind on updating the game state!
            """

            # If the current messages haven't been sent out yet, skip this iteration
            if (
                len(self.state.writeServerBuf) > 0
                or self.state.gameMode == GameModes.PAUSED.value
            ):
                await asyncio.sleep(0.01)
                continue

            # Lock the game state
            self.state.lock()

            # Get the next move
            next_move = self._get_next_move()

            # Write back to the server
            self.state.queueAction(4, next_move)

            # Unlock the game state
            self.state.unlock()
