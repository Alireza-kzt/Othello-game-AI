from state import State


class OthelloAI:
    def minmax(self, state: State, cutoff: int, current_level=0) -> State:
        if current_level == cutoff:
            return state

        nodes = state.successor()

        if len(nodes) == 0:
            return state

        if state.turn:
            max(
                [
                    self.minmax(node, cutoff, current_level + 1) for node in nodes
                ]
            )
        else:
            min(
                [
                    self.minmax(node, cutoff, current_level + 1) for node in nodes
                ]
            )
