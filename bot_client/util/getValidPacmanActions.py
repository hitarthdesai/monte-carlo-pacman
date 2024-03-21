from typing import List
from gameState import GameState, Directions, Location
from .nextMoveInDirection import next_move_in_direction
from .locationToDirection import location_to_direction

GRID_WIDTH = 31
GRID_HEIGHT = 31
ALL_DIRECTIONS = [
    Directions.UP,
    Directions.DOWN,
    Directions.LEFT,
    Directions.RIGHT,
    # Directions.NONE,
]


def is_location_within_grid(loc: Location):
    """
    Check if a location is valid
    """

    row, col = loc.row, loc.col
    return row >= 0 and row < GRID_WIDTH and col >= 0 and col < GRID_HEIGHT


def get_valid_pacman_actions(gs: GameState) -> List[Directions]:
    """
    Get the valid moves for the pacman
    """

    next_moves = map(lambda d: next_move_in_direction(gs.pacmanLoc, d), ALL_DIRECTIONS)
    valid_moves = filter(
        lambda loc: is_location_within_grid(loc) and not gs.wallAt(loc.row, loc.col),
        next_moves,
    )
    dirs = map(lambda loc: location_to_direction(gs.pacmanLoc, loc), valid_moves)
    if len(list(dirs)) == 0:
        print("No valid moves for pacman!")
    return list(dirs)
