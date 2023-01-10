from typing import Set, Tuple, Dict
from disk import Disk, transfer_vector, inverse_vector
from states_table import StatesTable


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
    successor_value: tuple
    successor_opponent_value: tuple

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
        self.successor_opponent_value = None
        self.successor_value = None

    def __hash__(self) -> int:
        h = 0
        for disks in self.players.values():
            for disk in disks:
                h += hash(disk) * hash("white") * hash(str(self.turn))
        return h

    def __eq__(self, other: 'State') -> bool:
        return hash(self) == hash(other)

    def __gt__(self, other: 'State') -> bool:
        return self.heuristic() > other.heuristic()

    def __lt__(self, other: 'State') -> bool:
        return self.heuristic() < other.heuristic()

    def __ge__(self, other: 'State') -> bool:
        return self.heuristic() >= other.heuristic()

    def __le__(self, other: 'State') -> bool:
        return self.heuristic() >= other.heuristic()

    @property
    def opponent_disks(self) -> set:
        return self.players[not self.turn]

    @property
    def my_disks(self) -> set:
        return self.players[self.turn]

    def add_disk(self, disk, disks: Set[Disk]) -> None:
        """
           disk  := new disk for player turn
               type object Disk
           disks :=  list disk must be change
        """
        self.my_disks.add(disk)
        for disk in disks:
            if disk in self.opponent_disks:
                self.opponent_disks.remove(disk)
                self.my_disks.add(disk)
        self.depth += 1
        self.turn = not self.turn

    def successor_opponent(self) -> Tuple[Set['State'], Dict['State', int]]:
        if self.successor_opponent_value is None:
            self.successor_opponent_value = self.copy_with(not self.turn).successor()
        return self.successor_opponent_value

    def successor(self) -> Tuple[Set['State'], Dict['State', int]]:
        """
        :var:
             do := disk opponent
             ndo := neighbor disk opponent
             tv := transfer vector
             itv := inverse transfer vector
             dtbv := disk transfer by vector

        :return: states and stability states
        """
        state = StatesTable.get_state(hash(self))

        if state is not None:
            if state.successor_value is not None:
                self.successor_value = state.successor_value
                for state in self.successor_value[0]:
                    state.parent = self
            if state.successor_opponent_value is not None:
                self.successor_opponent_value = state.successor_opponent_value
                for state in self.successor_opponent_value[0]:
                    state.parent = self

        if self.successor_value is not None:
            return self.successor_value

        states = set()
        stability = dict()
        inserted = set()

        for do in self.opponent_disks:
            for ndo in do.neighbors():
                if ndo not in inserted:
                    if ndo not in self.get_disks():
                        itv = inverse_vector(ndo.tv)
                        disk = self.iterates(ndo, itv)

                        if disk in self.my_disks:
                            disk_must_be_change = set()

                            for vector in transfer_vector:
                                dtbv = self.iterates(ndo, vector)

                                if dtbv in self.my_disks:
                                    itv = inverse_vector(vector)
                                    while dtbv != ndo:
                                        disk_must_be_change.add(dtbv)
                                        dtbv = dtbv.get_neighbor(itv)

                            state = State(self)
                            state.add_disk(ndo, disk_must_be_change)
                            states.add(state)
                            stability[state] = len(disk_must_be_change)
                            inserted.add(ndo)
        self.successor_value = states, stability
        StatesTable.add_state(self)
        return self.successor_value

    def iterates(self, disk, vector):
        disk = disk.get_neighbor(vector)
        while disk is not None and disk in self.opponent_disks:
            disk = disk.get_neighbor(vector)
        return disk

    def heuristic(self) -> float:
        actions, flanked = self.successor()
        opp_actions, opp_flanked = self.successor_opponent()

        mobility = self.mobility(actions, opp_actions)
        stability = self.stability(flanked, opp_flanked)
        disk_parity = self.disk_parity()
        corner_captured = self.corner_captured()

        return 2 * disk_parity + corner_captured + mobility + stability

    def disk_parity(self) -> float:
        max_player_disks = len(self.my_disks)
        min_player_disks = len(self.opponent_disks)
        return 100 * max_player_disks / (max_player_disks + min_player_disks)

    def mobility(self, actions, opponent_actions) -> float:
        max_player_moves = len(actions)
        min_player_moves = len(opponent_actions)

        if max_player_moves + min_player_moves == 0:
            return 0
        else:
            return 100 * (max_player_moves - min_player_moves) / (max_player_moves + min_player_moves)

    def stability(self, flanked, opponent_flanked) -> float:
        max_player_stability = sum(opponent_flanked.values())
        min_player_stability = sum(flanked.values())

        if max_player_stability + min_player_stability == 0:
            return 0
        else:
            return 100 * (min_player_stability - max_player_stability) / (max_player_stability + min_player_stability)

    def corner_captured(self) -> float:
        max_player_corners = 0
        min_player_corners = 0

        for disk in self.my_disks:
            if disk.is_corner():
                max_player_corners += 1

        for disk in self.opponent_disks:
            if disk.is_corner():
                min_player_corners += 1

        return 100 * (max_player_corners - min_player_corners) / 4

    def valid_move(self) -> bool:
        # return true if player[turn] can move else False
        return len(self.successor()) != 0

    def get_disks(self):
        return self.my_disks.union(self.opponent_disks)

    def is_goal(self) -> bool:
        if len(self.my_disks) + len(self.opponent_disks) == 64:
            return True

        actions, _ = self.successor()
        opponent_actions, _ = self.successor_opponent()

        if len(actions) + len(opponent_actions) == 0:
            return True

        return False

    def copy_with(self, turn: bool) -> 'State':
        state = State(self)
        if turn is not None:
            state.turn = turn

        return state

    def get_scores(self):
        black_score = len(self.players[True])
        white_score = len(self.players[False])

        return black_score, white_score

    def render(self):
        for i in range(8):
            for j in range(8):
                if Disk(i, j) in self.players[True]:
                    print('O', end=' ')
                elif Disk(i, j) in self.players[False]:
                    print('X', end=' ')
                else:
                    print('.', end=' ')
            print()
        print()
