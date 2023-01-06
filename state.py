from typing import Set, Tuple, Dict

from disk import Disk, transfer_vector, inverse_vector


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
            self.players = {True: {Disk(3, 3), Disk(4, 4)}, False: {Disk(3, 4), Disk(4, 3)}}
            self.depth = 0
            self.turn = True
            self.parent = None
        else:
            parent = args[0]
            self.players = {}
            for player, disks in parent.players.items():
                self.players[player] = set()
                for disk in disks:
                    self.players[player].add(Disk(disk))
            self.depth = parent.depth
            self.turn = parent.turn
            self.parent = parent

    @property
    def maximizer_disks(self):
        return self.white_player if self.turn else self.black_player

    @property
    def minimizer_disks(self):
        return self.black_player if self.turn else self.white_player

    def add_disk(self, disk, disks: Set[Disk]) -> None:
        """
           disk  := new disk for player turn
               type object Disk
           disks :=  list disk must be change
        """
        self.get_my_disks().add(disk)
        for disk in disks:
            if disk in self.get_opponent_disks():
                self.get_opponent_disks().remove(disk)
                self.get_my_disks().add(disk)
        self.depth += 1
        self.turn = not self.turn

    def __hash__(self) -> int:
        h = 0
        for disks in self.players.values():
            for disk in disks:
                h += hash(disk) * hash("white") * hash(str(self.turn))
        return h

    def successor(self) -> tuple[set['State'], dict['State', int]]:
        """
        :var:
             do := disk opponent
             ndo := neighbor disk opponent
             tv := transfer vector
             itv := inverse transfer vector
             dtbv := disk transfer by vector

        :return: states and stability states
        """
        states = set()
        stability = dict()

        for do in self.get_opponent_disks():
            for ndo in do.neighbors():
                if ndo not in self.get_disks():
                    itv = inverse_vector(ndo.tv)
                    disk = self.iterates(ndo, itv)

                    if disk in self.get_my_disks():
                        disk_must_be_change = set()

                        for vector in transfer_vector:
                            dtbv = self.iterates(ndo, vector)

                            if dtbv in self.get_my_disks():
                                itv = inverse_vector(vector)
                                while dtbv != ndo:
                                    disk_must_be_change.add(dtbv)
                                    dtbv = dtbv.get_neighbor(itv)

                        state = State(self)
                        state.add_disk(ndo, disk_must_be_change)
                        states.add(state)
                        stability[state] = len(disk_must_be_change)

        return states, stability

    def iterates(self, disk, vector):
        disk = disk.get_neighbor(vector)
        while disk is not None and disk in self.get_opponent_disks():
            disk = disk.get_neighbor(vector)
        return disk

    def __eq__(self, other: 'State') -> bool:
        return self.heuristic() == other.heuristic()

    def __gt__(self, other: 'State') -> bool:
        return self.heuristic() > other.heuristic()

    def __lt__(self, other: 'State') -> bool:
        return self.heuristic() < other.heuristic()

    def __ge__(self, other: 'State') -> bool:
        return self.heuristic() >= other.heuristic()

    def __le__(self, other: 'State') -> bool:
        return self.heuristic() >= other.heuristic()

    def heuristic(self) -> float:
        return self.disk_parity() + self.mobility() + self.stability() + self.corner_captured()

    def disk_parity(self) -> float:
        max_player_disks = len(self.maximizer_disks)
        min_player_disks = len(self.maximizer_disks)
        return 100 * (max_player_disks - min_player_disks) / (max_player_disks + min_player_disks)

    def mobility(self) -> float:
        max_player_moves = len(self.successor())
        min_player_moves = 0  # Todo: number of available moves for min player
        return 100 * (max_player_moves - min_player_moves) / (max_player_moves + min_player_moves)

    def stability(self) -> float:
        max_player_stability = 0  # Todo: rate of white disk can be flank
        min_player_stability = 0  # Todo: rate of black disk can be flank
        return 100 * (max_player_stability - min_player_stability) / (max_player_stability + min_player_stability)

    def corner_captured(self) -> float:
        max_player_corners = 0
        min_player_corners = 0

        for disk in self.maximizer_disks:
            if disk.is_corner():
                max_player_corners += 1

        for disk in self.minimizer_disks:
            if disk.is_corner():
                min_player_corners += 1

        return 100 * (max_player_corners - min_player_corners) / (max_player_corners + min_player_corners)

    def get_opponent_disks(self) -> set:
        return self.players[not self.turn]

    def get_my_disks(self) -> set:
        return self.players[self.turn]

    def valid_move(self) -> bool:
        """
            - valid_move
            return true if player turn can move
            return false if player turn can not move
        """
        return len(self.successor()) != 0

    def get_disks(self):
        return self.get_my_disks().union(self.get_opponent_disks())
