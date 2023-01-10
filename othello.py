from state import State
import math
from typing import List


class OthelloAI:
    def __init__(self, player) -> None:
        self.player = player
        super().__init__()

    def action(self, state: State, level=2) -> State:
        node = self.forward(state, cutoff=level, is_max=state.turn)

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


    def forward(self, states: List[State], turn=True, cutoff=2, current_level=0, n=3, is_max=True):
        
        if type(states) is not type([]):
            states = [states]
            
        if current_level == cutoff:
            return (max if turn else min)(states)

        chileds = []
        for state in states:
            nodes, _ = state.copy_with(is_max).successor()
            for child in nodes:
                if child not in chileds:
                    chileds.append(child)
        chileds.sort(key = lambda state: -state.heuristic() if is_max else state.heuristic())
        
        chileds = chileds[:n]
        
        if len(chileds) == 0:
            return (max if turn else min)(states)

        return (max if turn else min)(
            [
                self.forward(chileds, not turn, cutoff, current_level + 1, n, not is_max)
            ]
        )

