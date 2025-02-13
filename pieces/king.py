# pieces/king.py
from .piece import Piece

class King(Piece):
    def __init__(self, color, position):
        super().__init__(color, position)
        self.name = "King"
        self.symbol = "K" if color == "white" else "k"

    def get_valid_moves(self, board):
        moves = []
        row, col = self.position
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                r, c = row + dr, col + dc
                if 0 <= r < board.size and 0 <= c < board.size:
                    target = board.grid[r][c]
                    if target is None or target.color != self.color:
                        moves.append((r, c))
        return moves
