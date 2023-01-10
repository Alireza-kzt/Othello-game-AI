from othello import OthelloAI
from state import State

if __name__ == '__main__':
    black_player = OthelloAI(True)
    white_player = OthelloAI(False)

    state = State()  # init state
    state.render()

    while not state.is_goal():
        state = black_player.action(state, level=1) if state.turn else white_player.action(state, level=3)
        state.render()

    black_score, white_score = state.get_scores()
    print('Black player score: ', black_score)
    print('White player score: ', white_score)
