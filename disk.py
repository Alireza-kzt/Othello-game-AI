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

    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y

    def __hash__(self) -> int:
        return hash(self.x) + hash(self.convertor[self.y]) + hash(self.x) * hash(self.convertor[self.y]) + hash(
            self.x * self.convertor[self.y]) + hash(str(self.x) + self.convertor[self.y])

    def is_corner(self):
        corners = [(0, 0), (7, 7), (0, 7), (7, 0)]
        return (self.x, self.y) in corners
