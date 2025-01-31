import pygame
import chess
import chess.engine

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 600
BOARD_SIZE = 8
SQUARE_SIZE = WIDTH // BOARD_SIZE
WHITE = (240, 217, 181)
BROWN = (181, 136, 99)
HIGHLIGHT = (186, 202, 68)

PIECE_NAMES = {
    'p': "black_pawn.png",
    'r': "black_rook.png",
    'n': "black_knight.png",
    'b': "black_bishop.png",
    'q': "black_queen.png",
    'k': "black_king.png",
    'P': "white_pawn.png",
    'R': "white_rook.png",
    'N': "white_knight.png",
    'B': "white_bishop.png",
    'Q': "white_queen.png",
    'K': "white_king.png"
}

# Load piece images
PIECES = {}
for piece, filename in PIECE_NAMES.items():
    try:
        PIECES[piece] = pygame.transform.scale(
            pygame.image.load(f"assets/{filename}"), (SQUARE_SIZE, SQUARE_SIZE)
        )
    except FileNotFoundError:
        print(f"Error: Missing file 'assets/{filename}'.")
        exit()

print("Loaded pieces:", PIECES.keys())  # Debugging output

# Initialize board
board = chess.Board()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess Game")
selected_square = None

# Draw chessboard
def draw_board():
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            color = WHITE if (row + col) % 2 == 0 else BROWN
            pygame.draw.rect(screen, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

# Draw pieces
def draw_pieces():
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            piece = board.piece_at(chess.square(col, 7 - row))
            if piece:
                screen.blit(PIECES[piece.symbol()], (col * SQUARE_SIZE, row * SQUARE_SIZE))

# Convert click position to board square
def get_square_from_mouse(pos):
    x, y = pos
    col = x // SQUARE_SIZE
    row = y // SQUARE_SIZE
    return chess.square(col, 7 - row)

running = True
while running:
    draw_board()
    draw_pieces()
    pygame.display.flip()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            square = get_square_from_mouse(event.pos)
            if selected_square is None:
                if board.piece_at(square):
                    selected_square = square
            else:
                move = chess.Move(selected_square, square)
                if move in board.legal_moves:
                    board.push(move)
                selected_square = None

pygame.quit()
