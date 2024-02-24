import random
from typing import List
from gameState import GameState, Directions
from util import get_valid_pacman_actions


class MonteCarloTreeNode:
    def __init__(
        self, current: GameState, action: Directions, parent: "MonteCarloTreeNode"
    ):
        # Store the parent state and the action taken from that parent state
        self.state = current
        self.action = action
        self.parent = parent

        # Store the children of this node
        self.children: List[MonteCarloTreeNode] = []

        # Stores information for back-propagation
        self.visits = 0
        self.total_reward = 0


class MonteCarlo:
    def __init__(self) -> None:
        pass

    def init_tree(self, gs: GameState) -> None:
        self.root = MonteCarloTreeNode(gs, None, None)
        return self.root

    def select_action(self, node: MonteCarloTreeNode) -> MonteCarloTreeNode:
        """
        This is the first step of MCTS. It selects a valid action for the pacman

        For now, it performs a random valid action, and returns the corresponding node.
        """

        actions = get_valid_pacman_actions(node.state)

        # If all actions have been explored, return random node
        if len(actions) == len(node.children):
            return random.choice(node.children)
        action = random.choice(actions)

        state = GameState()
        state.update(node.state.serialize())
        state.simulateAction(state.updatePeriod, action)

        nodes = filter(
            lambda c: c.state.serialize() == state.serialize(), node.children
        )

        try:
            visited_node = next(nodes)
            return visited_node
        except StopIteration:
            new_node = MonteCarloTreeNode(state, action, node)
            node.children.append(new_node)
            return new_node

    def expansion(self, node: MonteCarloTreeNode) -> MonteCarloTreeNode:
        """
        This is the second step of MCTS. We check if the resulting state, after applying
        the selected action to the current state, corresponds to an unexplored node in our tree.

        If it does, we create a new node for that state and add it as a child to the selected node.
        """

        return self.select_action(node)

    def simulate_action(self, node: MonteCarloTreeNode) -> int:
        """
        This is the third step of MCTS. Plays the game till termination or a specific depth is reached.

        For now, it simply returns a random reward. We can do better than this though.
        """

        return random.randint(0, 100)

    def backpropagation(self, node: MonteCarloTreeNode, reward: int) -> None:
        """
        Backpropagate the reward information up the tree.
        """

        while node is not None:
            node.visits += 1
            node.total_reward += reward
            node = node.parent

    def get_best_action(self) -> Directions:
        """
        Get the best action from the current state.
        """

        # If there are no children, return a random action
        if not self.root.children:
            return random.choice(get_valid_pacman_actions(self.mcts.root.state))

        # Otherwise, select the child node with the highest average reward
        best_child = max(
            self.root.children, key=lambda child: child.total_reward / child.visits
        )

        return best_child.action
