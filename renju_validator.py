import sys
from typing import List, Tuple, Optional

# Constants
BOARD_SIZE = 19
CELL_EMPTY = 0
CELL_BLACK = 1
CELL_WHITE = 2
WIN_STRIKE = 5

class Direction:
    def __init__(self, dx: int, dy: int):
        self.dx = dx
        self.dy = dy
    
    def win_impossible(self, x: int, y: int) -> bool:
        return (x + (WIN_STRIKE - 1) * self.dx >= BOARD_SIZE or
                y + (WIN_STRIKE - 1) * self.dy >= BOARD_SIZE or
                x + (WIN_STRIKE - 1) * self.dx < 0 or
                y + (WIN_STRIKE - 1) * self.dy < 0)
    
    def left_most(self, x: int, y: int) -> Tuple[int, int]:
        return (x, y)

DIRECTIONS = [
    Direction(0, 1),
    Direction(1, 0),
    Direction(1, 1),
    Direction(1, -1),
]

def read_all_test_cases(file_path: str) -> List[List[List[int]]]:
    """Read multiple Renju boards from file"""
    boards = []
    with open(file_path, 'r') as file:
        lines = [line.strip() for line in file if line.strip() and not line.startswith('#')]

    try:
        num_tests = int(lines[0])
    except ValueError:
        raise ValueError("First line must contain an integer (number of test cases).")

    line_index = 1
    for test_case in range(num_tests):
        if line_index + BOARD_SIZE > len(lines):
            raise ValueError(f"Not enough lines for test case {test_case + 1}")

        board = []
        for i in range(BOARD_SIZE):
            row = list(map(int, lines[line_index + i].split()))
            if len(row) != BOARD_SIZE:
                raise ValueError(f"Test case {test_case + 1}, line {i + 1} does not have {BOARD_SIZE} values.")
            board.append(row)

        boards.append(board)
        line_index += BOARD_SIZE

    return boards

def within_the_board(x: int, y: int) -> bool:
    return 0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE

def is_win_strike(board, x, y, direction):
    cell = board[x][y]
    dx, dy = direction.dx, direction.dy
    
    prev_x, prev_y = x - dx, y - dy
    if within_the_board(prev_x, prev_y) and board[prev_x][prev_y] == cell:
        return False
    
    for i in range(1, WIN_STRIKE):
        next_x, next_y = x + i * dx, y + i * dy
        if not within_the_board(next_x, next_y) or board[next_x][next_y] != cell:
            return False

    next_x, next_y = x + WIN_STRIKE * dx, y + WIN_STRIKE * dy
    if within_the_board(next_x, next_y) and board[next_x][next_y] == cell:
        return False
    
    return True

def check_renju_winner(board: List[List[int]]) -> Tuple[int, Optional[int], Optional[int]]:
    for x in range(BOARD_SIZE):
        for y in range(BOARD_SIZE):
            cell = board[x][y]
            if cell == CELL_EMPTY:
                continue
            
            for direction in DIRECTIONS:
                if direction.win_impossible(x, y) or not is_win_strike(board, x, y, direction):
                    continue
                left_most_x, left_most_y = direction.left_most(x, y)
                return cell, left_most_x + 1, left_most_y + 1

    return CELL_EMPTY, None, None

def main():
    if len(sys.argv) != 2:
        print("Please provide a file path to the board configuration")
        return

    try:
        boards = read_all_test_cases(sys.argv[1])
        for i, board in enumerate(boards):
            winner, row, col = check_renju_winner(board)
            if winner == CELL_EMPTY:
                print("No winner")
            else:
                print(f"{winner}")
                print(f"{row} {col}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
