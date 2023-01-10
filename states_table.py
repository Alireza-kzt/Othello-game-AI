class StatesTable:
    states = dict()

    @staticmethod
    def add_state(state):
        StatesTable.states[hash(state)] = state

    @staticmethod
    def get_state(key: int):
        StatesTable.states.get(key)


