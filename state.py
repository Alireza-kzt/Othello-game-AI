from disk import Disk


class State:
    """
    - State
    contain location of disk white and black , depth of state , turn of player and parent state
    default usage create root state Othello - Official Board Game
    usage State(state) return copy of object state
    """
    players: dict
    depth: int  # depth state
    turn: bool  # true : white , false : black
    parent: object  # parent of this state

    def __init__(self, *args) -> None:
        if len(args) == 0:
            self.players = {True: [Disk(3, 3), Disk(4, 4)], False: [Disk(3, 4), Disk(4, 3)]}
            self.depth = 0
            self.turn = True
            self.parent = None
        else:
            parent = args[0]
            self.players = {}
            for player, disks in parent.players.items():
                self.players[player] = []
                for disk in disks:
                    self.players[player].append(Disk(disk))
            self.depth = parent.depth
            self.turn = parent.turn
            self.parent = parent

    def add_disk(self, disk, disks: list[Disk]) -> None:
        """
           disk  := new disk for player turn
               type object Disk
           disks :=  list disk must be change
        """
        self.get_my_disks().append(disk)
        for disk in disks:
            self.get_opponent_disks().remove(disk)
            self.get_my_disks().append(disk)
        self.depth += 1
        self.turn = not self.turn
        if not self.valid_move():
            self.turn = not self.turn

    def __hash__(self) -> int:
        h = 0
        for disks in self.players.values():
            for disk in disks:
                h += hash(disk) * hash("white") * hash(str(self.turn))
        return h

    def successor(self) -> list['State']:
        pass

    def heuristic(self) -> int:
        return self.disk_difference() + self.mobility() + self.stability() + self.corner_score() + self.side_score()

    def disk_difference(self) -> int:
        pass

    def mobility(self) -> int:
        pass

    def stability(self) -> int:
        pass

    def corner_score(self) -> int:
        pass

    def side_score(self) -> int:
        pass

    def get_opponent_disks(self) -> list:
        return self.players[not self.turn]

    def get_my_disks(self) -> list:
        return self.players[self.turn]

    def valid_move(self) -> bool:
        """
            - valid_move
            return true if player turn can move
            return false if player turn can not move
        """
        return self.successor() != []
