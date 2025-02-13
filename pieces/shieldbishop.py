# pieces/bishop.py
from .piece import Piece

class ShieldBishop(Piece):
    def __init__(self, color, position):
        super().__init__(color, position)
        self.name = "ShieldBishop"
        self.symbol = "sB" if color == "white" else "sb"

    def get_valid_moves(self, board):
        moves = []
        row, col = self.position
        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        for dr, dc in directions:
            r, c = row, col
            distance = 1
            while True and distance < 4:
                distance += 1
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

        # ShieldBishop can move like a bishop or a king
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                r, c = row + dr, col + dc
                if 0 <= r < board.size and 0 <= c < board.size:
                    target = board.grid[r][c]
                    if target is None or target.color != self.color:
                        moves.append((r, c))
        #unique moves only

        return moves
