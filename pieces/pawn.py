# pieces/pawn.py
from .piece import Piece

class Pawn(Piece):
    def __init__(self, color, position):
        super().__init__(color, position)
        self.name = "Pawn"
        # Use uppercase for white, lowercase for black.
        self.symbol = "P" if color == "white" else "p"

    def get_valid_moves(self, board):
        moves = []
        row, col = self.position
        # Determine direction: white moves up (decreasing row), black moves down.
        next_row = row - 1 if self.color == "white" else row + 1

        # Move forward one square if it is empty.
        if 0 <= next_row < board.size and board.grid[next_row][col] is None:
            moves.append((next_row, col))

        if self.has_moved is False:
            # Move forward two squares if it is empty.
            next_row = row - 2 if self.color == "white" else row + 2
            if 0 <= next_row < board.size and board.grid[next_row][col] is None:
                moves.append((next_row, col))


        # Diagonal captures.
        for dcol in [-1, 1]:
            new_col = col + dcol
            if 0 <= new_col < board.size and 0 <= next_row < board.size:
                target = board.grid[next_row][new_col]
                if target is not None and target.color != self.color:
                    moves.append((next_row, new_col))
        return moves
