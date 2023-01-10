from othello import OthelloAI
from state import State
from datetime import datetime

if __name__ == '__main__':
    black_player = OthelloAI(True)
    white_player = OthelloAI(False)

    state = State()  # init state
    state.render()

    time_start = datetime.now()

    while not state.is_goal():
        t1 = datetime.now()
        state = black_player.action(state, level=1) if state.turn else white_player.action(state, level=10)
        state.render()
        print(datetime.now() - action_start)

    time_end = datetime.now()
    print(time_end - time_start)

    black_score, white_score = state.get_scores()
    print('Black player score: ', black_score)
    print('White player score: ', white_score)
