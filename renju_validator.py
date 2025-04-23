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
        """Check if win is impossible in this direction from (x,y)"""
        return (x + (WIN_STRIKE - 1) * self.dx >= BOARD_SIZE or
                y + (WIN_STRIKE - 1) * self.dy >= BOARD_SIZE or
                x + (WIN_STRIKE - 1) * self.dx < 0 or
                y + (WIN_STRIKE - 1) * self.dy < 0)
    
    def left_most(self, x: int, y: int) -> Tuple[int, int]:
        """Return leftmost (or uppermost) position of the winning line"""
        return (x, y)

# All possible directions to check for a win
DIRECTIONS = [
    Direction(0, 1),   # Horizontal
    Direction(1, 0),   # Vertical
    Direction(1, 1),   # Diagonal down-right
    Direction(1, -1),  # Diagonal down-left
]

def read_renju_board(file_path: str) -> List[List[int]]:
    """Read the board configuration from a file"""
    board = []
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if not line or line.startswith('#'):
                continue  # Skip empty lines and comments
            
            values = list(map(int, line.split()))
            if len(values) != BOARD_SIZE:
                raise ValueError(f"Line contains {len(values)} values, expected {BOARD_SIZE}")
            
            for value in values:
                if value not in {CELL_EMPTY, CELL_BLACK, CELL_WHITE}:
                    raise ValueError(f"Invalid cell value: {value} (must be 0, 1, or 2)")
            
            board.append(values)
    
    if len(board) != BOARD_SIZE:
        raise ValueError(f"File contains {len(board)} lines, expected {BOARD_SIZE}")
    
    return board

def within_the_board(x: int, y: int) -> bool:
    """Check if coordinates are within the board"""
    return 0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE

def is_win_strike(board, x, y, direction):
    cell = board[x][y]
    dx, dy = direction.dx, direction.dy
    
    # Check previous cell isn't same color
    prev_x, prev_y = x - dx, y - dy
    if within_the_board(prev_x, prev_y) and board[prev_x][prev_y] == cell:
        return False
    
    # Check next 4 cells
    for i in range(1, 5):
        next_x, next_y = x + i*dx, y + i*dy
        if not within_the_board(next_x, next_y) or board[next_x][next_y] != cell:
            return False
    
    # Check 6th cell isn't same color
    next_x, next_y = x + 5*dx, y + 5*dy
    if within_the_board(next_x, next_y) and board[next_x][next_y] == cell:
        return False
    
    return True

def check_renju_winner(board: List[List[int]]) -> Tuple[int, Optional[int], Optional[int]]:
    """Check for a winner on the Renju board"""
    for x in range(BOARD_SIZE):
        for y in range(BOARD_SIZE):
            cell = board[x][y]
            if cell == CELL_EMPTY:
                continue
            
            for direction in DIRECTIONS:
                if direction.win_impossible(x, y):
                    continue
                
                if not is_win_strike(board, x, y, direction):
                    continue
                
                left_most_x, left_most_y = direction.left_most(x, y)
                # Return 1-based coordinates
                return cell, left_most_x + 1, left_most_y + 1
    
    return CELL_EMPTY, None, None

def main():
    if len(sys.argv) != 2:
        print("Please provide a file path to the board configuration")
        return
    
    try:
        board = read_renju_board(sys.argv[1])
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