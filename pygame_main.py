# pygame_main.py
import pygame
import sys
from board import Board

def load_images(square_size):
    """
    Loads images for all pieces from the assets folder.
    Returns a dictionary mapping piece symbols to Pygame surfaces.
    """
    images = {}
    pieces = ['king', 'queen', 'rook', 'bishop', 'knight', 'pawn', "shieldbishop"]
    for color in ['white', 'black']:
        for piece in pieces:
            filename = f"assets/{color}/{piece}.png"
            try:
                image = pygame.image.load(filename).convert_alpha()
                image = pygame.transform.scale(image, (square_size, square_size))
                # Map to the same symbol used in the piece classes.
                if color == "white":
                    symbol = {"king": "K", "queen": "Q", "rook": "R",
                              "bishop": "B", "knight": "N", "pawn": "P", "shieldbishop" : "sB" }[piece]
                else:
                    symbol = {"king": "k", "queen": "q", "rook": "r",
                              "bishop": "b", "knight": "n", "pawn": "p" , "shieldbishop" : "sb"}[piece]
                images[symbol] = image
            except Exception as e:
                print(f"Could not load image {filename}: {e}")
    return images

def draw_board(screen, board, square_size, piece_images, selected_square, valid_moves):
    """
    Draws the board and the pieces.
    Highlights the currently selected square and valid moves.
    """
    light_color = pygame.Color(232, 235, 239)
    dark_color = pygame.Color(125, 135, 150)
    
    for row in range(board.size):
        for col in range(board.size):
            # Choose square color.
            color = light_color if (row + col) % 2 == 0 else dark_color
            rect = pygame.Rect(col * square_size, row * square_size, square_size, square_size)
            pygame.draw.rect(screen, color, rect)
            
            # Highlight the selected square.
            if selected_square == (row, col):
                pygame.draw.rect(screen, pygame.Color("yellow"), rect, 3)
            
            # Highlight valid moves with a small green circle.
            if (row, col) in valid_moves:
                center = (col * square_size + square_size // 2, row * square_size + square_size // 2)
                pygame.draw.circle(screen, pygame.Color("green"), center, 10)
            
            # Draw the piece if present.
            piece = board.grid[row][col]
            if piece is not None:
                image = piece_images.get(piece.symbol)
                if image:
                    screen.blit(image, rect)
                else:
                    font = pygame.font.SysFont(None, 36)
                    text = font.render(piece.symbol, True, pygame.Color("black"))
                    screen.blit(text, (col * square_size + 10, row * square_size + 10))

def main():
    # Configuration.
    board_size = 16
    square_size = 60  # Pixel size for each square.
    window_size = board_size * square_size

    board = Board(size=board_size)
    turn = "white"
    
    pygame.init()
    screen = pygame.display.set_mode((window_size, window_size))
    pygame.display.set_caption("Chess with Check/Checkmate")
    clock = pygame.time.Clock()
    
    piece_images = load_images(square_size)
    
    selected_square = None  # Currently selected square (row, col)
    valid_moves = []        # Valid moves for the selected piece.
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break

            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                col = x // square_size
                row = y // square_size
                
                if selected_square is None:
                    # Select a piece if it belongs to the current turn.
                    piece = board.grid[row][col]
                    if piece and piece.color == turn:
                        selected_square = (row, col)
                        valid_moves = board.get_legal_moves_for_piece(piece)
                else:
                    # If a move is attempted.
                    if (row, col) in valid_moves:
                        if board.move_piece(selected_square, (row, col)):
                            # After a successful move, switch turn.
                            turn = "black" if turn == "white" else "white"
                            
                            # Check for checkmate.
                            if board.is_checkmate(turn):
                                print(f"Checkmate! { 'White' if turn == 'black' else 'Black' } wins.")
                                running = False
                            # Inform if the new turn is in check.
                            elif board.is_in_check(turn):
                                print(f"{turn.capitalize()} is in check!")
                    # Clear selection whether or not the move was made.
                    selected_square = None
                    valid_moves = []

        draw_board(screen, board, square_size, piece_images, selected_square, valid_moves)
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
