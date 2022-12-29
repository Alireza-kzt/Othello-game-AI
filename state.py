from disk import Disk


class State:
    """
    - State
    contain location of disk white and black , depth of state , turn of player and parent state
    default usage create root state Othello - Official Board Game
    usage State(state) return copy of object state
    """
    white_player: list[Disk]  # list of position disk white
    black_player: list[Disk]  # list of position disk black
    depth: int  # depth state
    turn: bool  # true : white , false : black
    parent: 'State'  # parent of this state

    def __init__(self) -> None:
        self.white_player = [Disk(3, 3), Disk(4, 4)]
        self.black_player = [Disk(3, 4), Disk(4, 3)]
        self.depth = 0
        self.turn = True
        self.parent = None

    def __init__(self, parent) -> None:
        self.white_player = parent.white_player
        self.black_player = parent.black_player
        self.depth = parent.depth
        self.turn = parent.turn
        self.parent = parent

    @property
    def maximizer_disks(self):
        return self.white_player if self.turn else self.black_player

    @property
    def minimizer_disks(self):
        return self.black_player if self.turn else self.white_player

    def add_disk(self, disk, disks: list[Disk]) -> None:
        """
           disk  := new disk for player turn
               type object Disk
           disks :=  list disk must be change
        """
        if self.turn:
            self.white_player.append(disk)
            for disk in disks:
                self.black_player.remove(disk)
                self.white_player.append(disk)
        else:
            self.black_player.append(disk)
            for disk in disks:
                self.white_player.remove(disk)
                self.black_player.append(disk)
        self.depth += 1
        self.turn = not self.turn
        if not self.valid_move():
            self.turn = not self.turn

    def __hash__(self) -> int:
        h = 0
        for disk in self.white_player:
            h += hash(disk) * hash("white") * hash(str(self.turn))
        for disk in self.black_player:
            h += hash(disk) * hash("black") * hash(str(self.turn))
        return h

    def successor(self) -> list['State']:
        pass

    def heuristic(self) -> float:
        return self.disk_parity() + self.mobility() + self.stability() + self.corner_score() + self.side_score()

    def disk_parity(self) -> float:
        max_player_disks = len(self.maximizer_disks)
        min_player_disks = len(self.maximizer_disks)
        return 100 * (max_player_disks - min_player_disks) / (max_player_disks + min_player_disks)

    def mobility(self) -> int:
        pass

    def stability(self) -> int:
        pass

    def corner_score(self) -> int:
        pass

    def side_score(self) -> int:
        pass

    def valid_move(self) -> bool:
        """
            - valid_move
            return true if player turn can move
            return false if player turn can not move
        """
        return self.successor() != []
