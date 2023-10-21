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

    async def decision_loop(self) -> str:
        """
        Decision loop for Pacbot
        """

        # Receive values as long as we have access
        # WARNING: 'await' statements should be routinely placed
        # to free the event loop to receive messages, or the
        # client may fall behind on updating the game state!

        # Lock the game state
        # self.state.lock()

        # Replace this with the actual decisions for Pacbot
        await asyncio.sleep(1)

        # Currently only moves right
        return "d"

        # Unlock the game state
        # # self.state.unlock()
