import numpy as np
from utils import *


# THE MAIN BOARD CLASS


class Board:
    def_tiger_pos = [
        [0, 0],
        [0, 4],
        [4, 0],
        [4, 4]
    ]
    def_board = [
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0]
    ]

    legal_diagonals = [
        [1, 0, 1, 0, 1],
        [0, 1, 0, 1, 0],
        [1, 0, 1, 0, 1],
        [0, 1, 0, 1, 0],
        [1, 0, 1, 0, 1]
    ]

    GOATS_READY_TO_MOVE = True

    # 0 - EMPTY
    # 1 - TIGER
    # 2 - GOAT
    def __init__(self, no_of_goats=20, tigers_pos=None):
        self.__board__ = np.array(Board.def_board, np.int8)
        if tigers_pos is None:
            self.__tigers_pos__ = Board.def_tiger_pos
        else:
            self.__tigers_pos__ = tigers_pos
        # SET THE TIGERS ON THE BOARD
        for point in self.__tigers_pos__:
            self.__board__[point[0], point[1]] = 1
        # SET THE NUMBER OF GOATS
        self.__goats_remaining__ = no_of_goats
        # CURRENT PLAYER (USUALLY THE GOAT)
        self.__current_player__ = 2

    def __is_legal_tiger_move__(self, pos_1, pos_2):
        # ALWAYS AN INVALID MOVE IF THE DESTINATION SQUARE IS NOT EMPTY
        if self.__board__[pos_2[0], pos_2[1]] != 0:
            return False

        if pos_1 in self.__tigers_pos__:
            displacement = find_distance(pos_1, pos_2)

            # FOR NON CAPTURING MOVES
            if equal(displacement, 1) or equal(displacement, np.sqrt(2)):
                # RETURN FALSE IF INVALID DIAGONAL MOVE
                if equal(displacement, np.sqrt(2)) and not self.__movement_in_legal_diagonal__(pos_1, pos_2):
                    return False
                return True

            # FOR CAPTURING MOVES
            if equal(displacement, 2) or equal(displacement, np.sqrt(8)):
                # RETURN FALSE IF INVALID DIAGONAL MOVE
                if equal(displacement, np.sqrt(8)) and not self.__movement_in_legal_diagonal__(pos_1, pos_2):
                    return False
                # RETURN FALSE IF THERE IS NO GOAT AT THE MIDPOINT
                mid_point = get_midpoint(pos_1, pos_2)
                if self.__board__[mid_point[0], mid_point[1]] == 2:
                    return True
                else:
                    return False
        return False

    def __is_legal_goat_placement__(self, pos):
        # GOATS ONLY GO ON EMPTY SQUARES
        if self.__board__[pos[0], pos[1]] == 0:
            return True
        else:
            return False

    def __is_legal_goat_move__(self, pos_origin, pos_dest):
        # ALREADY FALSE IF THE DESTINATION POINT IS NOT VACANT
        if self.__board__[pos_dest[0], pos_dest[1]] != 0:
            return False

        # ALSO FALSE IF THERE ARE STILL GOATS THAT CAN BE PLACED
        if self.__goats_remaining__ > 0:
            return False

        # THE ONLY OTHER RESTRICTION IS THAT IT SHOULD BE AT A UNIT DISTANCE
        displacement = find_distance(pos_origin, pos_dest)
        if equal(displacement, 1):
            return True

    @staticmethod
    def __movement_in_legal_diagonal__(pos_1, pos_2):
        if Board.legal_diagonals[pos_1[0]][pos_1[1]]:
            if Board.legal_diagonals[pos_2[0]][pos_2[1]]:
                return True
        return False

    def __str__(self):
        sketch = ""
        for row in self.__board__:
            sketch += " "
            for val in row:
                if val == 0:
                    sketch += " _ "
                elif val == 1:
                    sketch += " T "
                else:
                    sketch += " G "
            sketch += "\n"
        return sketch

    def get_legal_tiger_moves(self):
        legal_moves = []
        for tiger_idx in range(len(self.__tigers_pos__)):
            tiger_pos = self.__tigers_pos__[tiger_idx]
            legal_moves_for_current_tiger = []
            for i in range(self.__board__.shape[0]):
                for j in range(self.__board__.shape[1]):
                    if self.__is_legal_tiger_move__(tiger_pos, [i, j]):
                        legal_moves_for_current_tiger.append([i, j])
            legal_moves.append(legal_moves_for_current_tiger)
        return legal_moves

    def __switch_player__(self):
        self.__current_player__ = 1 if self.__current_player__ == 2 else 2

    def get_legal_goat_moves(self):
        legal_moves = {}
        if self.__goats_remaining__ > 0:
            legal_moves["placements"] = []
            for i in range(self.__board__.shape[0]):
                for j in range(self.__board__.shape[1]):
                    if self.__is_legal_goat_placement__([i, j]):
                        legal_moves["placements"].append([i, j])
        else:

            moves_filter = lambda x: (x[0] > 0 and x[0] < self.__board__.shape[0]) and (x[1] > 0 and x[1] < self.__board__.shape[1])

            for i in range(self.__board__.shape[0]):
                for j in range(self.__board__.shape[1]):
                    if self.__board__[i, j] == 2:
                        possible_moves_for_this_goat = []
                        only_possible_dest = [[i - 1, j - 1], [i - 1, j], [i - 1, j + 1], [i, j - 1], [i, j + 1],
                                              [i + 1, j - 1], [i + 1, j + 1]]
                        only_possible_dest = list(filter(moves_filter, only_possible_dest))
                        for dest_move in only_possible_dest:
                            if self.__is_legal_goat_move__([i, j], dest_move):
                                possible_moves_for_this_goat.append(dest_move)
                        legal_moves[tuple([i, j])] = possible_moves_for_this_goat
        return legal_moves

    def move_tiger(self, pos_1, pos_2):
        if self.__is_legal_tiger_move__(pos_1, pos_2):
            for idx in range(len(self.__tigers_pos__)):
                pos = self.__tigers_pos__[idx]
                if pos == pos_1:
                    self.__tigers_pos__[idx] = pos_2
            self.__board__[pos_1[0], pos_1[1]] = 0
            self.__board__[pos_2[0], pos_2[1]] = 1

            # REMOVE THE GOAT
            displacement = find_distance(pos_1, pos_2)
            if equal(displacement, 2) or equal(displacement, np.sqrt(8)):
                midpoint = get_midpoint(pos_1, pos_2)
                self.__board__[midpoint[0], midpoint[1]] = 0
            self.__switch_player__()
            return True
        else:
            return False

    def place_goat(self, pos):
        if self.__is_legal_goat_placement__(pos) and self.__goats_remaining__ > 0:
            self.__board__[pos[0], pos[1]] = 2
            self.__goats_remaining__ -= 1

            self.__switch_player__()
            return True
        else:
            return False

    def make_goat_move(self, pos1, pos2):
        if self.__goats_remaining__ < 0:
            if self.__is_legal_goat_move__(pos1, pos2):
                self.__board__[pos1[0], pos1[1]] = 0
                self.__board__[pos2[0], pos2[1]] = 2

            self.__switch_player__()
            return True
        return False

    def goat_status(self):
        if self.__goats_remaining__ < 0:
            return self.GOATS_READY_TO_MOVE
        else:
            return not self.GOATS_READY_TO_MOVE

    def get_current_player(self):
        return self.__current_player__

    def make_move(self, arg1, arg2=None):
        """
        The function to make a tiger or goat move on the board
        The preferred method for making a move
        :param arg1: Pos1
        :param arg2: Pos2, None if it's a goat move
        :return:
        """
        if self.__current_player__ == 1:
            return self.move_tiger(arg1, arg2)
        else:
            return self.place_goat(arg1)
