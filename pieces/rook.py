# pieces/rook.py
from .piece import Piece

class Rook(Piece):
    def __init__(self, color, position):
        super().__init__(color, position)
        self.name = "Rook"
        self.symbol = "R" if color == "white" else "r"

    def get_valid_moves(self, board):
        moves = []
        row, col = self.position
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        for dr, dc in directions:
            r, c = row, col
            while True:
                r += dr
                c += dc
                if r < 0 or r >= board.size or c < 0 or c >= board.size:
                    break
                if board.grid[r][c] is None:
                    moves.append((r, c))
                else:
                    if board.grid[r][c].color != self.color:
                        moves.append((r, c))
                    break
        return moves
