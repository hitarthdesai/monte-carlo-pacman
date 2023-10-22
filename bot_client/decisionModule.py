from typing import Union
from algo import algo

# Asyncio (for concurrency)
import asyncio

# Game state
from gameState import GameState


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
    def _get_target(self):
        return self.state.find_closest_pellet(self.state.pacmanLoc)

    def _get_next_move(self):
        self.getting_next_move = True
        target = self._get_target()

        path = algo(self.state, self.state.pacmanLoc, target)
        if path is not None and len(path) > 0:
            next_grid = path[0]
            self.getting_next_move = False
            return next_grid

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

        p_loc = self.state.pacmanLoc
        next_move = self._get_next_move()

        # Unlock the game state
        self.state.unlock()

        try:
            if p_loc.row == next_move.row:
                if p_loc.col < next_move.col:
                    return "d"
                else:
                    return "a"
            else:
                if p_loc.row < next_move.row:
                    return "s"
                else:
                    return "w"
        except:  # noqa: E722
            print("WHOOOOOPS")
            return ""
