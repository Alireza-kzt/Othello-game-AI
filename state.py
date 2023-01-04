from typing import List, Set

from disk import Disk, vectors, inv_v


class State:
    """
    - State
    contain location of disk white and black , depth of state , turn of player and parent state
    default usage create root state Othello - Official Board Game
    usage State(state) return copy of object state
    """
    players: dict
    depth: int  # depth state
    turn: bool  # true : my disk , false : opponent disk
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
                self.players[player] = set()
                for disk in disks:
                    self.players[player].append(Disk(disk))
            self.depth = parent.depth
            self.turn = parent.turn
            self.parent = parent

    def add_disk(self, disk, disks: Set[Disk]) -> None:
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

    def successor(self, d=False) -> List['State']:
        if d:
            disks = self.get_opponent_disks()
        else:
            disks = self.get_my_disks()
        list_state = set()
        for disk in disks:
            for neighbor in disk.neighbors():
                if neighbor not in self.get_my_disks() and neighbor not in self.get_opponent_disks():
                    v = inv_v(neighbor.v)
                    _neighbor = neighbor.get_neighbor(v)
                    while _neighbor is not None and _neighbor in disks:
                        _neighbor = _neighbor.get_neighbor(v)
                    if _neighbor in self.players[not d]:
                        disk_must_be_change = set()
                        for vector in vectors:
                            neighbor_temp = neighbor.get_neighbor(vector)
                            while neighbor_temp is not None and neighbor_temp in disks:
                                neighbor_temp = neighbor_temp.get_neighbor(vector)
                            if neighbor_temp not in self.players[not d]:
                                continue
                            vector_inv = inv_v(vector)
                            while neighbor_temp != neighbor:
                                disk_must_be_change.add(neighbor_temp)
                                neighbor_temp = neighbor_temp.get_neighbor(vector_inv)
                        state = State(self)
                        state.add_disk(disk, disk_must_be_change)
                        list_state.add(state)

        return []

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
