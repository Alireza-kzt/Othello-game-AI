from state import State
import math


class OthelloAI:
    def __init__(self, player) -> None:
        self.player = player
        super().__init__()

    def action(self, state: State, level=2) -> State:
        node = self.alpha_beta(state, cutoff=level, is_max=state.turn)

        while node.parent != state and node != state:
            node = node.parent

        return node.copy_with(not state.turn)

    def minmax(self, state: State, turn=True, cutoff=2, current_level=0, is_max=True) -> State:
        if current_level == cutoff:
            return state

        nodes, _ = state.copy_with(is_max).successor()

        if len(nodes) == 0:
            return state

        return (max if turn else min)(
            [
                self.minmax(node.copy_with(self.player), not turn, cutoff, current_level + 1, not is_max) for node in nodes
            ]
        )

    def alpha_beta(self, state: State, turn=True, cutoff=2, current_level=0, alpha=-math.inf, beta=math.inf, is_max=True) -> State:
        """
        alpha will represent the minimum score that the maximizing player is ensured.
        beta will represent the maximum score that the minimizing player is ensured.
        If beta is ever smaller than or equal to alpha, then the player can stop exploring that game tree.
        """
        if current_level == cutoff:
            return state

        nodes, _ = state.copy_with(is_max).successor()

        if len(nodes) == 0:
            return state

        nods = []
        for node in nodes:
            nods.append(
                node := self.alpha_beta(node.copy_with(self.player), not turn, cutoff, current_level + 1, alpha, beta, not is_max)
            )

            if turn:
                alpha = max(alpha, node.heuristic())
            else:
                beta = min(beta, node.heuristic())
            if beta <= alpha:
                break

        return (max if turn else min)(nods)
