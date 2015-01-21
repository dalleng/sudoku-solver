import math
from itertools import product
from copy import copy


class SudokuBoard():
    """ Class for a 9x9 sudoku board"""

    def __init__(self, board=None):
        """ If board is None an empty board is initialized, else an
            initial board can be given as a single space separated
            strings of numbers.

            Example:    0 0 0 0 0 0 0 0 0
                        0 0 8 0 0 0 0 4 0
                        0 0 0 0 0 0 0 0 0
                        0 0 0 0 0 6 0 0 0
                        0 0 0 0 0 0 0 0 0
                        0 0 0 0 0 0 0 0 0
                        2 0 0 0 0 0 0 0 0
                        0 0 0 0 0 0 2 0 0
                        0 0 0 0 0 0 0 0 0
        """

        self._board = {}

        if board and isinstance(board, str):
            for x, line in enumerate(board.split('\n')):
                for y, value in enumerate(line.split(' ')):
                    try:
                        value = int(value)
                    except ValueError:
                        continue

                    if value:
                        # print x, y, value
                        self.set_cell((x + 1, y + 1), value)
        elif board and isinstance(board, dict):
            self._board = board
        elif board and isinstance(board, list):
            for i, row in enumerate(board):
                for j, value in enumerate(row):
                    if value:
                        self.set_cell((i + 1, j + 1), value)

    def set_cell(self, position, value):
        """ Sets the value for a given position in
            the board """
        x, y = position

        if x < 1 or x > 9:
            raise ValueError('Position out of range. x: %d y: %d value: %d'
                             % (x, y, value))
        if y < 1 or y > 9:
            raise ValueError('Position out of range. x: %d y: %d value: %d'
                             % (x, y, value))
        if value < 1 or value > 9:
            raise ValueError('Position out of range. x: %d y: %d value: %d'
                             % (x, y, value))

        self._board[position] = value

    def erase_cell(self, position):
        del self._board[position]

    def check_row(self, row):
        """ Returns True if there are no repeated values,
            False if there are repeated values """
        l = [self._board[(x, y)] for x, y in self._board if x == row]
        return len(l) == len(set(l))

    def check_col(self, col):
        """ Returns True if there are no repeated values,
            False if there are repeated values """
        l = [self._board[(x, y)] for x, y in self._board if y == col]
        return len(l) == len(set(l))

    def check_region(self, region):
        positions = self.get_positions(region)
        positions = [pos for pos in positions if pos in self._board]
        l = [self._board[pos] for pos in positions]

        return len(l) == len(set(l))

    def check_board(self):
        for i in range(1, 10):
            if not self.check_row(i):
                return False

            if not self.check_col(i):
                return False

        for i in range(1, 10):
            if not self.check_region(i):
                return False

        return True

    def is_complete(self):
        return len(self._board) == 81 and self.check_board()

    def get_board(self):
        return copy(self._board)

    @classmethod
    def get_region(cls, pos):
        x, y = pos

        if x <= 3:
            region = math.ceil(y / 3.0)
        elif x <= 6:
            region = math.ceil(y / 3.0) + 3
        elif x <= 9:
            region = math.ceil(y / 3.0) + 6

        return region

    @classmethod
    def get_positions(cls, region):
        if region <= 3:
            rows = (1, 2, 3)
        elif region <= 6:
            rows = (4, 5, 6)
        elif region <= 9:
            rows = (7, 8, 9)

        if region in (1, 4, 7):
            cols = (1, 2, 3)
        elif region in (2, 5, 8):
            cols = (4, 5, 6)
        elif region in (3, 6, 9):
            cols = (7, 8, 9)

        return product(rows, cols)

    def __repr__(self):
        board = ''
        for x in range(1, 10):
            line = ''
            for y in range(1, 10):
                line += str(self._board.get((x, y), 0)) + ' '
            board += line + '\n'
        return board


if __name__ == '__main__':
    sudoku = SudokuBoard()

    # Test set cell
    try:
        sudoku.set_cell((10, 5), 1)
    except ValueError:
        print 'Row out of range test: passed'

    try:
        sudoku.set_cell((1, 10), 1)
    except ValueError:
        print 'Col out of range test: passed'

    try:
        sudoku.set_cell((1, 1), 10)
    except ValueError:
        print 'Value out of range test: passed'

    # Test Row
    sudoku.set_cell((1, 1), 2)
    sudoku.set_cell((1, 2), 2)
    assert sudoku.check_row(1) is False

    # Test Col
    sudoku.set_cell((1, 9), 7)
    sudoku.set_cell((2, 9), 7)
    assert sudoku.check_col(9) is False

    # Test board string input
    board = ("0 0 8 0 0 0 0 0 0\n"
             "0 0 8 0 0 0 0 4 0\n"
             "0 0 0 0 0 0 0 0 0\n"
             "0 0 0 0 0 6 0 0 0\n"
             "0 0 0 0 0 0 0 0 0\n"
             "0 0 0 0 0 0 0 0 0\n"
             "2 0 0 0 0 0 0 0 0\n"
             "0 0 0 0 0 0 2 0 0\n"
             "0 0 0 0 0 0 0 0 0\n")

    sudoku2 = SudokuBoard(board=board)
    sudoku3 = SudokuBoard(board=repr(sudoku2))
    assert sudoku2.check_region(1) is False
    assert sudoku2.check_region(7) is True
    assert repr(sudoku2) == repr(sudoku3)

    # is_complete test
    board2 = ("3 4 5 6 7 8 9 1 2\n"
              "6 7 8 9 1 2 3 4 5\n"
              "9 1 2 3 4 5 6 7 8\n"
              "1 2 3 4 5 6 7 8 9\n"
              "4 5 6 7 8 9 1 2 3\n"
              "7 8 9 1 2 3 4 5 6\n"
              "2 3 4 5 6 7 8 9 1\n"
              "5 6 7 8 9 1 2 3 4\n"
              "8 9 1 2 3 4 5 6 7\n")
    sudoku4 = SudokuBoard(board=board2)
    assert sudoku4.is_complete() is True
