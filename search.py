from itertools import product
from sudoku import SudokuBoard
from copy import deepcopy


def search(sudoku, assignments):
    # import pdb; pdb.set_trace()
    if sudoku.is_complete():
        return repr(sudoku)
    else:
        unassigned = [pos for pos in assignments
                      if isinstance(assignments[pos], list)]

        var = sorted(unassigned, key=lambda x: len(assignments[x]))[0]

        for value in assignments[var]:
            sudoku.set_cell(var, value)

            if sudoku.check_board():
                new_sudoku = SudokuBoard(board=repr(sudoku))
                new_assignments = deepcopy(assignments)
                new_assignments[var] = value
                forward_checking(new_assignments)
                result = search(new_sudoku, new_assignments)
            else:
                sudoku.erase_cell(var)
                continue

            if isinstance(result, str):
                return result

            sudoku.erase_cell(var)
    return None


def forward_checking(assignments):
    assigned = [i for i in assignments if isinstance(assignments[i], int)]

    for x, y in assigned:
        for pos in assignments:
            if pos in assigned:
                continue

            if pos[0] == x:
                try:
                    assignments[pos].remove(assignments[(x, y)])
                except ValueError:
                    pass

            if pos[1] == y:
                try:
                    assignments[pos].remove(assignments[(x, y)])
                except ValueError:
                    pass

            region = SudokuBoard.get_region((x, y))
            if pos in SudokuBoard.get_positions(region):
                try:
                    assignments[pos].remove(assignments[(x, y)])
                except ValueError:
                    pass


if __name__ == '__main__':
    board = ("0 7 0 4 0 0 3 0 0\n"
             "0 0 0 0 9 0 1 2 0\n"
             "0 0 0 7 0 0 0 0 5\n"
             "0 0 9 2 0 0 0 0 8\n"
             "8 0 0 6 0 9 0 0 4\n"
             "7 0 0 0 0 8 9 0 0\n"
             "3 0 0 0 0 5 0 0 0\n"
             "0 2 5 0 4 0 0 0 0\n"
             "0 0 7 0 0 3 0 6 0\n")

    sudoku = SudokuBoard(board)
    assignments = sudoku.get_board()

    for i in product(range(1, 10), range(1, 10)):
        if i not in assignments:
            assignments[i] = range(1, 10)
    forward_checking(assignments)

    result = search(sudoku, assignments)

    if result is None:
        print ''
    else:
        print result
