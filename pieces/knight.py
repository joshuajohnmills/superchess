# pieces/knight.py
from .piece import Piece

class Knight(Piece):
    def __init__(self, color, position):
        super().__init__(color, position)
        self.name = "Knight"
        self.symbol = "N" if color == "white" else "n"

    def get_valid_moves(self, board):
        moves = []
        row, col = self.position
        offsets = [
            (2, 1), (2, -1), (-2, 1), (-2, -1),
            (1, 2), (1, -2), (-1, 2), (-1, -2)
        ]
        for dr, dc in offsets:
            r, c = row + dr, col + dc
            if 0 <= r < board.size and 0 <= c < board.size:
                target = board.grid[r][c]
                if target is None or target.color != self.color:
                    moves.append((r, c))
        return moves
