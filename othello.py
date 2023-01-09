from state import State


class OthelloAI:
    def action(self, state: State, level=2):
        node = self.minmax(state, state.turn, level, is_max=state.turn)

        while node.parent != state:
            node = node.parent

        return node.copy_with(not state.turn)

    def minmax(self, state: State, turn: bool, cutoff=2, current_level=0, is_max=True) -> State:
        if current_level == cutoff:
            return state

        nodes, _ = state.copy_with(turn).successor()

        if len(nodes) == 0:
            return state

        return (max if turn else min)(
            [
                self.minmax(node.copy_with(is_max), not turn, cutoff, current_level + 1, is_max) for node in nodes
            ]
        )

    def alpha_beta_minmax(self, state: State, turn: bool, cutoff=2, current_level=0, alpha=-1, beta=1):
        """
        alpha will represent the minimum score that the maximizing player is ensured.
        beta will represent the maximum score that the minimizing player is ensured.
        If beta is ever smaller than or equal to alpha, then the player can stop exploring that game tree.
        """
        if current_level == cutoff:
            return state

        nodes, _ = state.successor()

        if len(nodes) == 0:
            return state

        scores = []
        for node in nodes:
            scores.append(score := self.alpha_beta_minmax(node, not turn, cutoff, current_level, alpha, beta))

            if turn:
                alpha = max(alpha, score)
            else:
                beta = min(beta, score)
            if beta <= alpha:
                break

        return (max if turn else min)(scores)
