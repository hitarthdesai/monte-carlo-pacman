import asyncio
from typing import List
from heuristic import Heuristic
from monteCarlo import MonteCarlo

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
        self.mcts = MonteCarlo()

    def _get_next_move(self) -> Directions:
        root = self.mcts.init_tree(self.state)
        for i in range(100):
            node = self.mcts.select_action(root)
            expanded_node = self.mcts.expansion(node)
            reward = self.mcts.simulate_playout(expanded_node)
            self.mcts.backpropagation(expanded_node, reward)

        return self.mcts.get_best_action()

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
