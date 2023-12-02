import asyncio
import heapq
from typing import Optional, List

from algo import Node
from util import location_to_direction

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

        # If we are currently getting the next move
        self.getting_next_move: bool = False

    # TODO: Consider chase vs scatter mode.
    def _get_target(self) -> Optional[Location]:
        return self.state.find_closest_pellet(self.state.pacmanLoc)

    def _get_next_move(self) -> Directions:
        self.getting_next_move = True
        target = self._get_target()

        start = self.state.pacmanLoc
        path = self.algo(start, target)
        if path is not None and len(path) > 0:
            move = location_to_direction(start, path[0])
            self.getting_next_move = False
            return move

        print("No path found 🥲")
        return Directions.NONE

    def algo(self, start: Location, target: Location) -> List[Location]:
        """
        Find a path from start to target position using A*
        """
        open_list: List[Node] = list()  # Priority queue for open nodes
        closed_set = set()  # Set to store visited nodes

        # Create the start node and initialize its costs
        head = Node(start, None)
        head.g = 0
        head.h = start.distance_to(target)
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
                    path.append(curr.position)
                    curr = curr.parent

                path.reverse()
                return path

            # TODO: Needs to be made serializable
            closed_set.add(curr.position)

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
                if neighbor in closed_set:
                    continue

                loc = Location(self.state)
                loc.update((neighbor[0] << 8) | neighbor[1])
                node = Node(loc, curr)
                node.g = curr.g + 1
                node.h = loc.distance_to(target)
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
