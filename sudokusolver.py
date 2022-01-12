import copy
import numpy as np

class SudokuSolver(object):
    def __init__(self, myinput):
        self.sudoku = myinput
        self.backup = []

    def print_sudoku(self):
        print(self.sudoku)

    def gen_index(self):
        for i in range(9):
            for j in range(9):
                yield (i, j)

    def gen_square_index(self, square):
        row = square // 3
        col = square % 3
        row_start = row * 3
        row_end = row_start + 3
        col_start = col * 3
        col_end = col_start + 3
        for i in range(row_start, row_end):
            for j in range(col_start, col_end):
                yield (i, j)

    def is_solved(self):
        return 0 not in self.sudoku

    def build_candidates(self):
        candidate_ele = {}
        # Plain base candidate list
        for i, j in self.gen_index():
            candidate_ele[(i, j)] = set([1, 2, 3, 4, 5, 6, 7, 8, 9])
        self.candidate_ele = candidate_ele

        # Based on existing status update the candidate
        for i, j in self.gen_index():
            ele = self.sudoku[i, j]
            if ele != 0:
                self.update_candidate(i, j, ele)
        
    def update_candidate(self, i, j, ele):
        self.sudoku[i, j] = ele
        self.candidate_ele[(i, j)] = set([ele])
        for col in range(9):
            self.candidate_ele[(i, col)].discard(ele)
        for row in range(9):
            self.candidate_ele[(row, j)].discard(ele)
        square = (i // 3) * 3 + j // 3
        for idxi, idxj in self.gen_square_index(square):
            self.candidate_ele[(idxi, idxj)].discard(ele)

    def check_consistency(self, verbose=False):
        consistent = True
        for i in range(9):
            for j in range(9):
                ele = self.sudoku[i, j]
                if ele != 0:
                    y_start = (i // 3) * 3
                    y_end = y_start + 3
                    x_start = (j // 3) * 3
                    x_end = x_start + 3
                    if len(np.where(self.sudoku[i, :] == ele)[0]) > 1 \
                        or len(np.where(self.sudoku[:, j] == ele)[0]) > 1 \
                        or len(np.where(self.sudoku[y_start:y_end, x_start:x_end] == ele)[0]) > 1:
                        consistent = False
                        if verbose:
                            print("Found inconsistency at index {}, {}".format(i, j))
        if verbose and consistent:
            print("Sudoku is consistent")
        return consistent

    def _fill_single(self):
        # If only one possible value fill it
        updated = False
        for i, j in self.gen_index():
            if len(self.candidate_ele[(i, j)]) == 1:
                updated = True
                ele = next(iter(self.candidate_ele[(i, j)]))
                print("Updating {} at {}, {}".format(ele, i, j))
                self.update_candidate(i, j, ele)
        return updated
    
    def _row_scan(self, ele):
        # Row Scan
        updated = False
        for row in range(9):
            position = -1
            count = 0
            for col in range(9):
                if ele in self.candidate_ele[(row, col)]:
                    position = col
                    count += 1
            if count == 1:
                updated = True
                print("Updating {} at {}, {}".format(ele, row, position))
                self.update_candidate(row, position, ele)
        return updated
    
    def _col_scan(self, ele):
        # Column Scan
        updated = False
        for col in range(9):
            position = -1
            count = 0
            for row in range(9):
                if ele in self.candidate_ele[(row, col)]:
                    position = row
                    count += 1
            if count == 1:
                updated = True
                print("Updating {} at {}, {}".format(ele, position, col))
                self.update_candidate(position, col, ele)
        return updated

    def _square_scan(self, ele):
        # Square Scan
        updated = False
        for square in range(9):
            positionx = -1
            positiony = -1
            count = 0
            for idxi, idxj in self.gen_square_index(square):
                if ele in self.candidate_ele[(idxi, idxj)]:
                    positionx = idxi
                    positiony = idxj
                    count += 1
            if count == 1:
                updated = True
                print("Updating {} at {}, {}".format(ele, positionx, positiony))
                self.update_candidate(positionx, positiony, ele)
        return updated

    def fill_numbers(self):
        while True:
            updated = False
            updated = updated or self._fill_single()
            for ele in range(1, 10):
                updated = updated or self._row_scan(ele)
                updated = updated or self._col_scan(ele)
                updated = updated or self._square_scan(ele)
            if not updated:
                break
        if self.is_solved():
            print("Solved the sudoku problem completely")
        else:
            print("Unable to solve the problem")
        return self.is_solved()

    def solveit(self):
        self.print_sudoku()
        self.backup.append(copy.deepcopy(self.sudoku))
        self.build_candidates()
        self.check_consistency(verbose=True)
        self.fill_numbers()
        self.print_sudoku()
        # if not solved yet try guessing
        if not self.is_solved():
            for i, j in self.gen_index():
                if len(self.candidate_ele[(i, j)]) == 2:
                    guess_x = i
                    guess_y = j
                    print(self.candidate_ele[(i, j)])
                    for ele in self.candidate_ele[(i, j)]:
                        self.print_sudoku()
                        self.backup.append(copy.deepcopy(self.sudoku))
                        print("Guessing {} at {}, {}".format(ele, guess_x, guess_y))
                        self.update_candidate(guess_x, guess_y, ele)
                        self.fill_numbers()
                        if not self.is_solved():
                            self.sudoku = self.backup.pop()
                            self.build_candidates()
                        else:
                            break
                if self.is_solved():
                    break

        print("Final solution")
        self.print_sudoku()


if __name__ == '__main__':
    
    sudoku = np.zeros((10, 10), dtype=int)
    sudoku[1, [4, 5]] = [1, 7]
    sudoku[2, [7]] = [7]
    sudoku[3, [3, 5, 9]] = [3, 5, 6]
    sudoku[4, [1, 3, 7]] = [8, 6, 9]
    sudoku[5, [6, 9]] = [9, 1]
    sudoku[6, [2, 6]] = [2, 8]
    sudoku[7, [1, 3, 4, 7]] = [5, 2, 9, 8]
    sudoku[8, [2, 3]] = [4, 1]
    sudoku[9, [2, 6, 7]] = [6, 4, 3]
    sudoku = sudoku[1:, 1:]

    mysolver = SudokuSolver(sudoku)
    mysolver.solveit()
    
