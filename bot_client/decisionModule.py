import asyncio
from typing import Optional

from algo import algo
from util import location_to_direction

from gameState import GameState, Location, Direction


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

    def _get_next_move(self) -> Optional[Direction]:
        self.getting_next_move = True
        target = self._get_target()

        path = algo(self.state, self.state.pacmanLoc, target)
        if path is not None and len(path) > 0:
            move = location_to_direction(self.state.pacmanLoc, path[0])
            self.getting_next_move = False
            return move

        raise Exception("No path found")

    async def decision_loop(self) -> str:
        """
        Decision loop for Pacbot
        """

        # Receive values as long as we have access
        # WARNING: 'await' statements should be routinely placed
        # to free the event loop to receive messages, or the
        # client may fall behind on updating the game state!

        await asyncio.sleep(0.2)

        # Lock the game state
        self.state.lock()

        await asyncio.sleep(0.2)
        next_move = self._get_next_move()

        # Unlock the game state
        self.state.unlock()

        if next_move is None:
            print("No move found 🤔")
            await asyncio.sleep(0.2)
        else:
            return ["w", "a", "s", "d"][next_move]
