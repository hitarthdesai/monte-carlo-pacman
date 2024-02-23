import asyncio
from typing import List, Tuple
from heuristic import Heuristic
from util import location_to_direction

from gameState import GameState, Directions, Location, GameModes


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

    def _algo(self, start: Location) -> List[Location]:
        return start

    def _get_next_move(self) -> Directions:
        start = self.state.pacmanLoc
        move = self._algo(start)
        return location_to_direction(start, move)

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

            self.state.queueAction(4, next_move)
            self.state.unlock()
