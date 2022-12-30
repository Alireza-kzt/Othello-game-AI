from othello import OthelloAI
from state import State

if __name__ == '__main__':
    black_player = OthelloAI()
    white_player = OthelloAI()

    state = State()  # init state

    while not state.is_goal():
        next_state = black_player.minmax(state) if state.turn else white_player.minmax(state)
        state = next_state if state is not None else state

    print(state.get_winner())
