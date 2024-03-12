#!/usr/bin/env python
#coding:utf-8

"""
Each sudoku board is represented as a dictionary with string keys and
int values.
e.g. my_board['A1'] = 8
"""
import sys
#import time
#import statistics

ROW = "ABCDEFGHI"
COL = "123456789"


def print_board(board):
    """Helper function to print board in a square."""
    print("-----------------")
    for i in ROW:
        row = ''
        for j in COL:
            row += (str(board[i + j]) + " ")
        print(row)


def board_to_string(board):
    """Helper function to convert board dictionary to string for writing."""
    #converts the board dict to str for writing
    ordered_vals = []
    for r in ROW:
        for c in COL:
            ordered_vals.append(str(board[r + c]))
    return ''.join(ordered_vals)


def get_domain(cell, board):
    unary_constraints = set()
    
    # Constraints for rows and columns
    for i in range(1, 10):
        unary_constraints.add(board[cell[0] + str(i)])
        unary_constraints.add(board[chr(64 + i) + cell[1]])
    
    # Constraints for each 3x3 
    start_row, start_col = (ord(cell[0]) - 65) // 3 * 3, (int(cell[1]) - 1) // 3 * 3
    for i in range(3):
        for j in range(3):
            unary_constraints.add(board[chr(65 + start_row + i) + str(1 + start_col + j)])
    
    return [i for i in range(1, 10) if i not in unary_constraints]


def minimum_remaining_values(zero_board, board):
    def get_degree(cell):
        #Count the num of neighbors that are alsi in zero_board
        count = 0
        for neighbor in zero_board:
            if neighbor != cell:
                same_row = neighbor[0] == cell[0]
                same_col = neighbor[1] == cell[1]
                same_block = ((ord(neighbor[0]) - 65) // 3 == (ord(cell[0]) - 65) // 3 
                              and (int(neighbor[1]) - 1) // 3 == (int(cell[1]) - 1) // 3)
                
                if same_row or same_col or same_block:
                    count += 1
                    
        return count

    # List of cells and their domains
    mrv_list = [(cell, get_domain(cell, board)) for cell in zero_board]

    # Sort by MRV and Degree heuristic
    mrv_list.sort(key=lambda x: (len(x[1]), -get_degree(x[0])))

    # No valid cell or the domain is empty returns None
    if not mrv_list or not mrv_list[0][1]:
        return None

    return mrv_list[0]


def backtracking(board):
    if all(board[cell] != 0 for cell in board):
        return board

    zero_board = [cell for cell, val in board.items() if val == 0]
    next_cell = minimum_remaining_values(zero_board, board)
    
    if not next_cell:
        return None
    
    cell, domains = next_cell

    for val in domains:
        board[cell] = val
        if backtracking(board):
            return board
        board[cell] = 0

    return None


if __name__ == '__main__':
    puzzle_times = []
    solves = 0

    if len(sys.argv) > 1:
        
        # Running sudoku solver with one board $python3 sudoku.py <input_string>.
        print(sys.argv[1])
        # Parse boards to dict representation, scanning board L to R, Up to Down
        board = { ROW[r] + COL[c]: int(sys.argv[1][9*r+c])
                  for r in range(9) for c in range(9)}

        #start_time = time.time()
        solved_board = backtracking(board)
        #end_time = time.time()
        
        #runtime = end_time - start_time
        #puzzle_times.append(runtime)
        '''
        if solved_board:
            solves += 1
        '''
        # Write board to file
        out_filename = 'output.txt'
        outfile = open(out_filename, "w")
        outfile.write(board_to_string(solved_board))
        outfile.write('\n')

    else:
        # Running sudoku solver for boards in sudokus_start.txt $python3 sudoku.py

        #  Read boards from source.
        src_filename = 'sudokus_start.txt'
        try:
            srcfile = open(src_filename, "r")
            sudoku_list = srcfile.read()
        except:
            print("Error reading the sudoku file %s" % src_filename)
            exit()

        # Setup output file
        out_filename = 'output.txt'
        outfile = open(out_filename, "w")

        # Solve each board using backtracking
        for line in sudoku_list.split("\n"):

            if len(line) < 9:
                continue

            # Parse boards to dict representation, scanning board L to R, Up to Down
            board = { ROW[r] + COL[c]: int(line[9*r+c])
                      for r in range(9) for c in range(9)}

            # Print starting board. TODO: Comment this out when timing runs.
            #print_board(board)

            #start_time = time.time()
            solved_board = backtracking(board)
            #end_time = time.time()

            #runtime = end_time - start_time
            #puzzle_times.append(runtime)
            '''
            if solved_board:
                solves += 1
            '''
            # Print solved board. TODO: Comment this out when timing runs.
            #print_board(solved_board)

            # Write board to file
            outfile.write(board_to_string(solved_board))
            outfile.write('\n')

        print("Finishing all boards in file.")
        
        
        # Reporting performance statistics
        '''
        print(
            f"Puzzles solved: {solves}/{len(puzzle_times)}, "
            f"Min runtime: {min(puzzle_times):.4f} seconds, "
            f"Max runtime: {max(puzzle_times):.4f} seconds,"
            f"Mean runtime: {statistics.mean(puzzle_times):.4f} seconds, "
            f"Standard deviation: {statistics.stdev(puzzle_times):.4f} seconds "
        )
        '''