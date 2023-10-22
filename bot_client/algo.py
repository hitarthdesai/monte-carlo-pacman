from typing import List
from gameState import GameState, Location
import heapq


# Define a class to represent nodes in the grid
class Node:
    def __init__(self, position: Location, parent=None):
        self.position = position
        self.parent = parent
        self.g = 0  # Cost from start node to current node
        self.h = 0  # Heuristic cost (estimated cost to reach goal)
        self.f = 0  # Total cost: g + h

    # heap sorting based on 'f' values
    def __lt__(self, other):
        return self.f < other.f


# Calculate the Manhattan distance heuristic between two positions
#  |x2 - x1| + |y2 - y1|
def calc_heuristic(current: Location, target: Location) -> int:
    return current.distance_to(target.row, target.col)


# Find a path from start to target position using A* algorithm
def algo(state: GameState, start: Location, target: Location) -> List[Location]:
    # print("Start", start.row, start.col)
    # print("Target", target.row, target.col)
    open_list: List[Node] = list()  # Priority queue for open nodes
    closed_set = set()  # Set to store visited nodes

    # Create the start node and initialize its costs
    head = Node(start, None)
    head.g = 0
    head.h = calc_heuristic(start, target)
    head.f = head.h

    # Add the start node to open list
    heapq.heappush(open_list, head)

    while open_list:
        curr = heapq.heappop(open_list)
        # Get the node with the lowest f value

        # Check if the current node is the target node
        if curr.position.at(target.row, target.col):
            path: List[Location] = []
            # Reconstruct the path by following parent pointers
            while curr.position != start:
                path.append(curr.position)
                curr = curr.parent

            path.reverse()
            return path

        # Needs to be made serializable
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
            lambda pos: not state.wallAt(pos[0], pos[1]),
            all_neighbors,
        )

        for neighbor in valid_neighbors:
            if neighbor in closed_set:
                continue

            loc = Location()
            loc.update((neighbor[0] << 8) | neighbor[1])
            node = Node(loc, curr)
            node.g = curr.g + 1
            node.h = calc_heuristic(loc, target)
            node.f = node.g + node.h

            heapq.heappush(open_list, node)

    return None
