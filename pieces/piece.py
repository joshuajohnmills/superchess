# pieces/piece.py
class Piece:
    def __init__(self, color, position):
        """
        color: 'white' or 'black'
        position: tuple (row, col)
        """
        self.color = color
        self.position = position
        self.name = "Piece"
        self.symbol = "?"
        self.has_moved = False

    def get_valid_moves(self, board):
        """
        Returns a list of valid moves for this piece.
        This method should be overridden in child classes.
        """
        return []

    def move(self, position):
        """Update the piece's position."""
        self.position = position
        self.has_moved = True
