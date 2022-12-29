import numpy as np

from disk import Disk
from state import State

if __name__ == '__main__':
    pass

A = np.zeros([8, 8])
state = State()
c = {
    True: 1,
    False: -1,
}
state.add_disk(Disk(2, 4), [Disk(3, 4)])

for player, disks in state.players.items():
    for disk in disks:
        A[disk.x][disk.y] = c[player]


print(A)
