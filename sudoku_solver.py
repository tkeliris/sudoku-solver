#!/usr/bin/env python

__author__ = "Tasos Keliris"
__license = "MIT"

from optparse import OptionParser
import sys

# Sudoku board size
n = 9

# Debug mode
debug = 0

def board_init():
    """
    Initializes board with all available values 1-9 for each cell
    """
    board = [[[i for i in range(1,n+1)] for j in range(n)] for k in range(n)]
    return board

def read_puzzle(board, input_puzzle):
    """
    Reads unsolved puzzle
    If the string given is a filename with .txt of .sud suffix, the puzzle
    is read from the file, otherwise a string containing the puzzle is considered
    Expected format:
    1 line, row-wise saved values where unknown cells are marked with
    anything other than numbers 1-9
    
    Example:
    829.5...7.....2....64.7.1922.87364..7135..9.........3.64..1.8....52....113..6.2..
    """
    if any(x in input_puzzle for x in [".txt", ".sud"]):
        with open(input_puzzle, "rU") as f:
            line = f.readline().rstrip()
    else:
        line = input_puzzle
    for i in range(n):
        for j in range(n):
            if (line[i*n+j] in "123456789"):
                board[i][j] = [int(line[i*n+j])]
    return 0

def write_to_file(board, output_file = "solution.sud"):
    """
    Writes solution to file
    """
    with open(output_file, "w") as f:
        for i in range(n):
            if i and i%3==0:
                f.write("------+-------+------\n")
            for j in range(n):            
                if j and j%3==0:
                    f.write("| ")
                    if len(board[i][j]) == 1:
                        f.write(str(board[i][j][0]) + " ")
                    else:
                        f.write(". ")
                elif j==8:
                    if len(board[i][j]) == 1:
                        f.write(str(board[i][j][0]) + "\n")
                    else:
                        f.write(".\n")
                else:
                    if len(board[i][j]) == 1:
                        f.write(str(board[i][j][0]) + " ")
                    else:
                        f.write(". ")
    return 0

def print_clean(item):
    """
    Helper function for print_board
    Returns "." if the element is a list
    """
    if len(item) == 1:
        print(item[0]),
    else:
        print("."),
    return 0

def print_board(board, pretty = 1):
    """
    Prints sudoku board in a 9x9 grid
    If pretty is set, a "." is printed for cells with unknown values
    
    Example:
    
    8 2 9 | . 5 . | . . 7
    . . . | . . 2 | . . .
    . 6 4 | . 7 . | 1 9 2
    ------+-------+------
    2 . 8 | 7 3 6 | 4 . .
    7 1 3 | 5 . . | 9 . .
    . . . | . . . | . 3 .
    ------+-------+------
    6 4 . | . 1 . | 8 . .
    . . 5 | 2 . . | . . 1
    1 3 . | . 6 . | 2 . .

    """
    for i in range(n):
        if i and i%3==0:
            print("------+-------+------")
        for j in range(n):            
            if j and j%3==0:
                print("|"),
                if pretty:
                    print_clean(board[i][j])
                else:
                    print("".join(str(x) for x in board[i][j])),
            elif j==8:
                if pretty:
                    print_clean(board[i][j])
                else:
                    print("".join(str(x) for x in board[i][j])),
                print
            else:
                if pretty:
                    print_clean(board[i][j])
                else:
                    print("".join(str(x) for x in board[i][j])),
    print("")
    return 0

def deepcopy(obj):
    """
    Deepcopy a nested list
    from http://stackoverflow.com/questions/7845152/deep-copy-nested-list-without-using-deepcopy-function
    """
    if isinstance(obj, dict):
        return {deepcopy(key): deepcopy(value) for key, value in obj.items()}
    if hasattr(obj, '__iter__'):
        return type(obj)(deepcopy(item) for item in obj)
    return obj

def get_length(board):
    """
    Calculates the total number of elements in cells
    including unresolved lists of possible values
    """
    length = 0
    for i in range(n):
        for j in range(n):
                length += len(board[i][j])
    return length

def eliminate(board, i, j):
    """
    Propagates the effects of fixing a cell to the affected neighbors
    within the same square and vertical and horizontal lines
    """
    value = board[i][j][0]
    # Horizontal propagation
    for k in range(n):
        if j!=k and value in board[i][k]:
            board[i][k].remove(value)
    # Vertical propagation
    for l in range(n):
        if i!=l and value in board[l][j]:
            board[l][j].remove(value)
    # Square propagation
    for k in range(i/3*3, i/3*3+3):
        for l in range(j/3*3, j/3*3+3):
            if k!=i and l!=j and (value in board[k][l]):
                board[k][l].remove(value)
    return 0

def check_single_value(board, done_cells, i, j):
    """
    Checks if a value in a row/column/square is the 
    only possible value
    """
    # Check if list element is the only possibility in its row
    for k in board[i][j]:
        count = 1
        for l in range(n):
            if k in board[i][l] and l!=j:
                count += 1
        if count == 1:
            board[i][j] = [k]
            done_cells.append((i,j))
            eliminate(board, i,j)                            
            return 0
    # Check if list element is the only possibility in its column
    for k in board[i][j]:
        count = 1
        for l in range(n):
            if k in board[l][j] and l!=i:
                count += 1
        if count == 1:
            board[i][j] = [k]
            done_cells.append((i,j))
            eliminate(board, i,j)                              
            return 0

    # Check if list element is the only possibility in its square
    for m in board[i][j]:
        count = 1
        for k in range(i/3*3, i/3*3+3):
            for l in range(j/3*3, j/3*3+3):
                if m in board[k][l] and (k,l)!=(i,j):
                    count += 1
        if count == 1:
            board[i][j] = [m]
            done_cells.append((i,j))
            eliminate(board, i,j)                              
            return 0

def min_len_options(board):
    """
    Helper function for brute force solver
    Returns the minimum length sublists of the board and their indices
    """
    min_length = 9
    best_options = []
    for i in range(n):
        for j in range(n):
            cur_length = len(board[i][j])
            if cur_length < min_length and cur_length > 1:
                min_length = cur_length
                best_options = [(board[i][j], i, j)]
            elif cur_length == min_length:
                best_options += [(board[i][j], i, j)]
    return best_options

def valid_attempt(board):
    """
    Checks if the sudoku board is a valid board
    """
    for i in range(n):
        if [] in board[i]:
            return 0
    return 1

def brute(board):
    """
    Recursive brute force solver for remaining cells
    """
    if not valid_attempt(board):
        return False
    temp_board = deepcopy(board)
    best_options = min_len_options(temp_board)
    if best_options:
        (values,i,j) = best_options[0]
        for val in values:
            temp_board[i][j] = [val]
            temp_board = simplify_puzzle(temp_board, [])
            check = brute(temp_board)
            if check is not False:
                return check
            temp_board = deepcopy(board)
        return False
    return temp_board


def solve_puzzle(board):
    """
    Wrapper for the Sudoku solver
    First propagates cell value effects and then applies 
    brute force for remaining values
    """
    # Propagate value effects
    board = simplify_puzzle(board, [])

    # Brute force remaining cells
    board = brute(board)

    # Verify that the puzzle was successfully solved
    assert get_length(board)==81
    assert valid_attempt(board)

    return board

def simplify_puzzle(board, done_cells):
    """
    Propagates cell value effects to all cells
    """
    # Initialization
    not_done = True
    # Main loop for propagation
    while not_done:
        old_length = get_length(board)
        for i in range(n):
            for j in range(n):
                # If the value is the only possibility, propagate its effects
                # Append the coordinates to a list to keep track of what has already been done_cells
                if len(board[i][j]) == 1:# and (i,j) not in done_cells:
                    done_cells.append((i,j))
                    eliminate(board, i,j)
                # If the value is the only possibility within a row/column/square
                # fix that value and propagate its effects
                elif len(board[i][j]) > 1:
                    check_single_value(board, done_cells, i, j)
        # Check if nothing changes or if the puzzle is solved
        new_length = get_length(board)
        if new_length == old_length:
            not_done = False
    return board

def demo():
    """
    If main is called without any arguments this demo is executed
    The unsolved puzzle is:

    8 2 9 | . 5 . | . . 7
    . . . | . . 2 | . . .
    . 6 4 | . 7 . | 1 9 2
    ------+-------+------
    2 . 8 | 7 3 6 | 4 . .
    7 1 3 | 5 . . | 9 . .
    . . . | . . . | . 3 .
    ------+-------+------
    6 4 . | . 1 . | 8 . .
    . . 5 | 2 . . | . . 1
    1 3 . | . 6 . | 2 . .

    and its solution:

    8 2 9 | 4 5 1 | 3 6 7
    3 7 1 | 6 9 2 | 5 8 4
    5 6 4 | 3 7 8 | 1 9 2
    ------+-------+------
    2 9 8 | 7 3 6 | 4 1 5
    7 1 3 | 5 8 4 | 9 2 6
    4 5 6 | 1 2 9 | 7 3 8
    ------+-------+------
    6 4 2 | 9 1 7 | 8 5 3
    9 8 5 | 2 4 3 | 6 7 1
    1 3 7 | 8 6 5 | 2 4 9    
    """

    # Initialize board with all cells having possible values 1..9
    board = board_init()

    # Unsolved demo puzzle
    # Hard puzzle by Arto Inkala:
    # http://abcnews.go.com/blogs/headlines/2012/06/can-you-solve-the-hardest-ever-sudoku/
    read_puzzle(board, "8..........36......7..9.2...5...7.......457.....1...3...1....68..85...1..9....4..")

    # Print unsolved puzzle
    print("Initial Sudoku board:")
    print_board(board)

    # Solve the puzzle
    board = solve_puzzle(board)

    # Print the solution
    print("Solution:")
    print_board(board)


    # Write output to file
    write_to_file(board)
    
    return 0

def main(argv):
    """
    Main function: Parses command line arguments and calls solver functions
    """
    parser = OptionParser()

    # Run demo
    demo()
    return 0

# Call main with command line arguments
if __name__ == "__main__":
    main(sys.argv[1:])