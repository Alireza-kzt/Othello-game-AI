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
        0:"a",
        1:"b",
        2:"c",
        3:"d",
        4:"e",
        5:"f",
        6:"g",
        7:"h",
        "a":0,
        "b":1,
        "c":2,
        "d":3,
        "e":4,
        "f":5,
        "g":6,
        "h":7,
    }

    def __init__(self,x,y) -> None:
        self.x = x
        self.y = y

    def __hash__(self) -> int:
        return hash(self.x) + hash(self.convertor[self.y]) +  hash(self.x)*hash(self.convertor[self.y]) + hash(self.x*self.convertor[self.y]) + hash(str(self.x)+self.convertor[self.y])


class State:
    """
    - State
    contain location of disk white and black , depth of state , turn of player and parent state
    default usage create root state Othello - Official Board Game
    usage State(state) return copy of object state
    """
    player_white : list[Disk]  # list of position disk white
    player_black : list[Disk]  # list of position disk black
    depth : int # depth state
    turn : bool # true : white , false : black
    parent : 'State' # parent of this state

    def __init__(self) -> None:
        self.player_white = [Disk(3,3),Disk(4,4)]
        self.player_black = [Disk(3,4),Disk(4,3)]
        self.depth = 0
        self.turn = True
        self.parent = None

    def __init__(self,parent) -> None:
        self.player_white = parent.player_white
        self.player_black = parent.player_black
        self.depth = parent.depth
        self.turn = parent.turn
        self.parent = parent



    """
    disk  := new disk for player turn
        type object Disk 
    disks :=  list disk must be change
    """
    def add_disk(self, disk, disks: list[Disk])->None:
        if self.turn:
            self.player_white.append(disk)
            for disk in disks:
                self.player_black.remove(disk)
                self.player_white.append(disk)
        else:
            self.player_black.append(disk)
            for disk in disks:
                self.player_white.remove(disk)
                self.player_black.append(disk)
        self.depth += 1
        self.turn = not self.turn
        if not self.valid_move():
            self.turn = not self.turn


    def __hash__(self) -> int:
        h = 0
        for disk in self.player_white:
            h += hash(disk)*hash("white")*hash(str(self.turn))
        for disk in self.player_black:
            h += hash(disk)*hash("black")*hash(str(self.turn))
        return h

    """
    - valid_move
    return true if player turn can move
    return false if player turn can not move 
    """
    def valid_move(self)->bool:
        from successor import successor
        return successor(self) != []





