from typing import List
from gameState import GameState, Directions, Location
from .nextMoveInDirection import next_move_in_direction

GRID_WIDTH = 31
GRID_HEIGHT = 31
ALL_DIRECTIONS = [
    Directions.UP,
    Directions.DOWN,
    Directions.LEFT,
    Directions.RIGHT,
    Directions.NONE,
]


def is_location_within_grid(loc: Location):
    """
    Check if a location is valid
    """

    row, col = loc.row, loc.col
    return row >= 0 and row < GRID_WIDTH and col >= 0 and col < GRID_HEIGHT


def get_valid_pacman_moves(gs: GameState) -> List[Location]:
    """
    Get the valid moves for the pacman
    """

    next_moves = map(lambda d: next_move_in_direction(gs.pacmanLoc, d), ALL_DIRECTIONS)
    valid_moves = filter(
        lambda loc: is_location_within_grid(loc) and not gs.wallAt(loc.row, loc.col),
        next_moves,
    )

    return list(valid_moves)