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
