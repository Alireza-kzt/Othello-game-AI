from typing import List


class Disk:
    """
    - disk
        contain location of disk in Othello Game
        x := row
        y := column
        convertor :=
            f : X -> X , function 1-1 and Onto
            X := {0,1,2,3,4,5,6,7} union {a,b,c,d,e,f,g,h}

    - hash calculation
        hash(x) + hash(f(y)) + hash(x)*hash(f(y)) + hash(x*f(y)) + hash(x+f(y))
      example
        x = 3
        y = 3 -> f(y) = 'd'
        hash(3) + hash('d') + hash(3)*hash('d') + hash('ddd') + hash('3d')
    """
    x: int
    y: int

    convertor = {
        0: "a",
        1: "b",
        2: "c",
        3: "d",
        4: "e",
        5: "f",
        6: "g",
        7: "h",
        "a": 0,
        "b": 1,
        "c": 2,
        "d": 3,
        "e": 4,
        "f": 5,
        "g": 6,
        "h": 7,
    }

    def __init__(self, *args) -> None:
        if len(args) == 1:
            disk = args[0]
            self.x = disk.x
            self.y = disk.y
        else:
            self.x = args[0]
            self.y = args[1]

    def __hash__(self) -> int:
        return hash(self.x) + hash(self.convertor[self.y]) + hash(self.x) * hash(self.convertor[self.y]) + hash(
            self.x * self.convertor[self.y]) + hash(str(self.x) + self.convertor[self.y])

    def __eq__(self, o: "Disk") -> bool:
        return o.x == self.x and o.y == self.y

    def get_neighbor(self, v) -> 'Disk':
        disk = Disk(self)
        disk.x += v[0]
        disk.y += v[1]
        disk.v = v
        if 0 <= disk.x < 8 and 0 <= disk.y < 8:
            return disk
        return None

    def neighbors(self) -> List['Disk']:
        disks = []
        for vector in vectors:
            disk = self.get_neighbor(vector)
            if disk is not None:
                disks.append(disk)
        return disks

    def __str__(self) -> str:
        return str(self.x) + " " + str(self.y)


vectors = {(1, 1), (1, -1), (1, 0), (-1, 1), (-1, -1), (-1, 0), (0, 1), (0, -1)}


def inv_v(v):
    return -v[0], -v[1]
