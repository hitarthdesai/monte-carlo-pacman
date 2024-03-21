import random
import math
from typing import List
from gameState import GameState, Directions
from util import get_valid_pacman_actions
from heuristic import Heuristic
from constants import SIMULATION_DEPTH, EPSILON


class MonteCarloTreeNode:
    def __init__(
        self, state: GameState, action: Directions, parent: "MonteCarloTreeNode"
    ):
        # Store the parent state and the action taken from that parent state
        self.state = state
        self.action = action
        self.parent = parent

        # Store the children of this node
        self.children: List[MonteCarloTreeNode] = []

        # Stores information for back-propagation
        self.visits = 0
        self.total_reward = 0

    def duplicate_and_perform_action(self, action: Directions) -> "MonteCarloTreeNode":
        """
        Duplicate the current state and perform the given action on the duplicate.
        """

        state = GameState()
        state.update(self.state.serialize())
        state.simulateAction(state.updatePeriod, action)

        return MonteCarloTreeNode(state, action, self)

    def calculate_ucb(self) -> float:
        """
        Calculate the Upper Confidence Bound for a node.
        """

        if self.visits == 0:
            return math.inf

        exploitation = self.total_reward / self.visits
        exploration = 0.1 * math.sqrt(
            math.log(self.parent.visits + EPSILON) / self.visits
        )

        return exploitation + exploration


class MonteCarlo:
    def __init__(self) -> None:
        self.heuristics = Heuristic()

    def init_tree(self, gs: GameState) -> None:
        self.root = MonteCarloTreeNode(gs, None, None)
        return self.root

    def select_action(self, node: MonteCarloTreeNode) -> MonteCarloTreeNode:
        """
        This is the first step of MCTS. It selects a valid action for the pacman

        For now, it performs a random valid action, and returns the corresponding node.
        """
        print(node)
        if len(node.children) == 0:
            actions = get_valid_pacman_actions(node.state)
            children = map(
                lambda action: node.duplicate_and_perform_action(action), actions
            )
            node.children = list(children)
        
        ucb_values = [child.calculate_ucb() for child in node.children]
        
        max_ucb_value = max(ucb_values, default=0)

         # Get all nodes with the maximum UCB value
        best_nodes = [child for child, ucb in zip(node.children, ucb_values) if ucb == max_ucb_value]

            # If there's only one best node, return it directly
        if len(best_nodes) == 1:
            return best_nodes[0]
        else:
            # Randomly select one of the best nodes with equal probability
            return random.choice(best_nodes)


        # best_node = max(node.children, key=lambda child: child.calculate_ucb())

        # return best_node

    def expansion(self, node: MonteCarloTreeNode) -> MonteCarloTreeNode:
        """
        This is the second step of MCTS. We check if the resulting state, after applying
        the selected action to the current state, corresponds to an unexplored node in our tree.

        If it does, we create a new node for that state and add it as a child to the selected node.
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

    def simulate_playout(self, node: MonteCarloTreeNode) -> int:
        """
        This is the third step of MCTS. Plays the game till termination or a specific depth is reached.

        For now, it simply returns a random reward. We can do better than this though.
        """
        state = GameState()
        state.update(node.state.serialize())
        final_score = 0

        for _ in range(SIMULATION_DEPTH):
            actions = get_valid_pacman_actions(state)

            scores = []
            for action in actions:
                new_state = GameState()
                new_state.update(state.serialize())
                is_safe = new_state.simulateAction(new_state.updatePeriod, action)

                # Decrease in number of lives means we reached a bad terminal state
                if not is_safe:
                    scores.append(-math.inf)

                # Increase in the level means we reached a good terminal state
                elif new_state.currLevel > state.currLevel:
                    scores.append(math.inf)

                # Otherwise, we use the heuristic to evaluate a non-terminal state
                else:
                    score = self.heuristics.get_overall_heuristic(new_state)
                    score += new_state.currScore - state.currScore
                    scores.append(score)

            max_score_index = scores.index(max(scores))
            final_score += scores[max_score_index]
            action = actions[max_score_index]
            state.simulateAction(state.updatePeriod, action)

        return final_score

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
