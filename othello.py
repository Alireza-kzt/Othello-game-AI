from state import State


class OthelloAI:
    def minmax(self, state: State, cutoff=2, current_level=0) -> State:
        if current_level == cutoff:
            return state

        nodes = state.successor()

        if len(nodes) == 0:
            return state

        return (max if state.turn else min)(
            [
                self.minmax(node, cutoff, current_level + 1) for node in nodes
            ]
        )

    def alpha_beta_minmax(self, state: State, cutoff=2, current_level=0, alpha=-1, beta=1):
        """
        alpha will represent the minimum score that the maximizing player is ensured.
        beta will represent the maximum score that the minimizing player is ensured.
        If beta is ever smaller than or equal to alpha, then the player can stop exploring that game tree.
        """
        if current_level == cutoff:
            return state

        nodes = state.successor()

        if len(nodes) == 0:
            return state

        scores = []
        for node in nodes:
            scores.append(score := self.alpha_beta_minmax(node, cutoff, current_level, alpha, beta))

            if state.turn:
                alpha = max(alpha, score)
            else:
                beta = min(beta, score)
            if beta <= alpha:
                break

        return (max if state.turn else min)(scores)
