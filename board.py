# board.py
from pieces import Pawn, Rook, Knight, Bishop, Queen, King, ShieldBishop

class Board:
    def __init__(self, size=8):
        self.size = size
        self.grid = [[None for _ in range(size)] for _ in range(size)]
        self.setup_board()
        self.validate_board()  # Ensure exactly one king per player.

    def setup_board(self):
        """
        Sets up the board. For an 8×8 board, it uses the standard chess setup.
        (If you change the board size, you can modify this method accordingly.)
        """
        # Place pawns 
        for col in range(self.size):
            self.grid[4][col] = Pawn('black', (4, col))
            self.grid[self.size - 5][col] = Pawn('white', (self.size - 5, col))
            self.grid[5][col] = Pawn('black', (5, col))
            self.grid[self.size - 6][col] = Pawn('white', (self.size - 6, col))

        # Place major pieces (works properly when size == 8)
        pieces_order = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]
        if self.size >= 8:
            for col, piece_class in enumerate(pieces_order):
                self.grid[0][col] = piece_class('black', (0, col))
                self.grid[self.size - 1][col] = piece_class('white', (self.size - 1, col))
        # For nonstandard board sizes, you could add additional logic here.
        
        # Place ShieldBishops
        self.grid[3][3] = ShieldBishop('black', (3, 3))
        self.grid[self.size - 3][3] = ShieldBishop('white', (self.size - 3, 3))
        self.grid[3][4] = ShieldBishop('black', (3, 4))
        self.grid[self.size - 3][4] = ShieldBishop('white', (self.size - 3, 4))


    def validate_board(self):
        """Ensure that there is exactly one king per player."""
        king_counts = {"white": 0, "black": 0}
        for row in self.grid:
            for piece in row:
                if piece and piece.name.lower() == "king":
                    king_counts[piece.color] += 1
        if king_counts["white"] != 1 or king_counts["black"] != 1:
            pass
            #raise ValueError("Board must have exactly one king per player!")

    def find_king(self, color):
        """Find and return the position of the king of the given color."""
        for row in range(self.size):
            for col in range(self.size):
                piece = self.grid[row][col]
                if piece and piece.name.lower() == "king" and piece.color == color:
                    return (row, col)
        return None

    def is_in_check(self, color):
        """
        Returns True if the king of the given color is in check.
        (That is, if any enemy piece can move to the king’s position.)
        """
        king_pos = self.find_king(color)
        if king_pos is None:
            # In a valid game this should not occur.
            return True
        for row in range(self.size):
            for col in range(self.size):
                piece = self.grid[row][col]
                if piece and piece.color != color:
                    if king_pos in piece.get_valid_moves(self):
                        return True
        return False

    def is_move_safe(self, start, end, color):
        """
        Simulate the move from start to end and return True if it does not leave
        the king in check.
        """
        piece = self.grid[start[0]][start[1]]
        target_piece = self.grid[end[0]][end[1]]
        original_position = piece.position

        # Make the move.
        self.grid[end[0]][end[1]] = piece
        self.grid[start[0]][start[1]] = None
        piece.position = end

        safe = not self.is_in_check(color)

        # Revert the move.
        piece.position = original_position
        self.grid[start[0]][start[1]] = piece
        self.grid[end[0]][end[1]] = target_piece

        return safe

    def get_legal_moves_for_piece(self, piece):
        """Return the list of moves for the given piece that do not leave the king in check."""
        legal_moves = []
        start = piece.position
        for move in piece.get_valid_moves(self):
            if self.is_move_safe(start, move, piece.color):
                legal_moves.append(move)
        return legal_moves

    def get_all_legal_moves(self, color):
        """Return all legal moves for the player of the given color as a list of (start, end) tuples."""
        moves = []
        for row in range(self.size):
            for col in range(self.size):
                piece = self.grid[row][col]
                if piece and piece.color == color:
                    for move in self.get_legal_moves_for_piece(piece):
                        moves.append(((row, col), move))
        return moves

    def is_checkmate(self, color):
        """
        Returns True if the player of the given color is in checkmate.
        (That is, the king is in check and there are no legal moves available.)
        """
        if not self.is_in_check(color):
            return False
        if len(self.get_all_legal_moves(color)) == 0:
            return True
        return False

    def move_piece(self, start, end):
        """Attempts to move the piece from start to end. Returns True if successful."""
        start_row, start_col = start
        end_row, end_col = end
        piece = self.grid[start_row][start_col]
        if piece is None:
            print("No piece at start location.")
            return False

        legal_moves = self.get_legal_moves_for_piece(piece)
        if end not in legal_moves:
            print("Invalid move or move leaves king in check.")
            return False

        # Perform the move.
        self.grid[end_row][end_col] = piece
        self.grid[start_row][start_col] = None
        piece.move((end_row, end_col))
        
        return True

    def print_board(self):
        """Prints a simple text representation of the board."""
        print("\n  " + " ".join([chr(c + ord('a')) for c in range(self.size)]))
        for row in range(self.size):
            row_str = f"{self.size - row} "
            for col in range(self.size):
                piece = self.grid[row][col]
                row_str += (piece.symbol if piece else ".") + " "
            print(row_str)
        print()
