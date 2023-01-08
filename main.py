from othello import OthelloAI
from state import State
import datetime
import numpy as np

if __name__ == '__main__':
    black_player = OthelloAI()
    white_player = OthelloAI()

    state = State()  # init state

    while not state.is_goal():
        state.render()
        next_state = black_player.minmax(state, state.turn) if state.turn else white_player.minmax(state, state.turn)
        state = next_state if state is not None else state

    print(state.get_winner())

# A = np.zeros([8, 8])
# state = State()
# c = {
#     True: 1,
#     False: -1,
# }
# t1 = datetime.datetime.now()
# for i in range(100):
#     if len(state.successor()[0]) != 0:
#         state = state.successor()[0].pop()
#         if not state.valid_move():
#             state.turn = not state.turn
#         A = np.zeros([8, 8])
#         for player, disks in state.players.items():
#             for disk in disks:
#                 A[disk.x][disk.y] = c[player]
#         # print(state.turn)
#         # print(A)
# t2 = datetime.datetime.now()
# print(t2-t1)
# print(len(state.players[True]))
# print(len(state.players[False]))











