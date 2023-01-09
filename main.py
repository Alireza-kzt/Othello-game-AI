from othello import OthelloAI
from state import State

if __name__ == '__main__':
    black_player = OthelloAI()
    white_player = OthelloAI()

    state = State()  # init state

    while not state.is_goal():
        state.render()
        state = black_player.action(state, level=3) if state.turn else white_player.action(state, level=1)

    black_score, white_score = state.get_scores()
    print(r'Black player score: ', black_score)
    print(r'White player score: ', white_score)
