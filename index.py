import pygame

# Initialize Pygame
pygame.init()

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (128, 128, 128)

# Define the dimensions of the board
BOARD_WIDTH = 800
BOARD_HEIGHT = 800

# Create the Pygame window
screen = pygame.display.set_mode((BOARD_WIDTH, BOARD_HEIGHT))

# Set the title of the window
pygame.display.set_caption("Python Chess")

# Load the image that contains all the pieces
pieces_img = pygame.image.load("pieces/pieces.png")

# Define the size of each square on the board
SQUARE_SIZE = 100

# Define the positions of the pieces in the image
piece_positions = {
    "wK": (0, 0),
    "wQ": (SQUARE_SIZE, 0),
    "wB": (2 * SQUARE_SIZE, 0),
    "wN": (3 * SQUARE_SIZE, 0),
    "wR": (4 * SQUARE_SIZE, 0),
    "wP": (5 * SQUARE_SIZE, 0),
    "bK": (0, SQUARE_SIZE),
    "bQ": (SQUARE_SIZE, SQUARE_SIZE),
    "bB": (2 * SQUARE_SIZE, SQUARE_SIZE),
    "bN": (3 * SQUARE_SIZE, SQUARE_SIZE),
    "bR": (4 * SQUARE_SIZE, SQUARE_SIZE),
    "bP": (5 * SQUARE_SIZE, SQUARE_SIZE),
}

# Create a dictionary to store the individual piece images
pieces = {}

# Extract each piece image from the original image
for piece_name, position in piece_positions.items():
    piece_surf = pieces_img.subsurface(pygame.Rect(position[0], position[1], SQUARE_SIZE, SQUARE_SIZE))
    pieces[piece_name] = piece_surf

# Define the initial chess board
board = [
    ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
    ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
    ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
    ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
    ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
    ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
    ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
    ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
]

# Define a function to draw the chess board
def draw_board():
    for row in range(8):
        for col in range(8):
            x = col * SQUARE_SIZE
            y = row * SQUARE_SIZE
            color = WHITE if (row + col) % 2 == 0 else GREY
            pygame.draw.rect(screen, color, [x, y, SQUARE_SIZE, SQUARE_SIZE])
            piece = pieces.get(board[row][col])
            if piece:
                screen.blit(piece, (x, y))
def is_valid_move(piece, start_row, start_col, end_row, end_col, board, player, last_move):
    """
    Check whether a move is valid based on the piece being moved and the destination square.

    Parameters:
    - piece: the piece being moved (e.g. "wP", "bR", etc.)
    - start_row, start_col: the starting position of the piece
    - end_row, end_col: the destination position of the piece
    - board: the current state of the chess board

    Returns:
    - True if the move is valid, False otherwise
    """
    # Check if the start and end positions are within the bounds of the board
    if start_row < 0 or start_row > 7 or start_col < 0 or start_col > 7:
        return False
    if end_row < 0 or end_row > 7 or end_col < 0 or end_col > 7:
        return False
    
    # Check if the piece being moved is the correct color
    if piece.startswith("w") and player == "b":
        return False
    if piece.startswith("b") and player == "w":
        return False
    if piece == "  " or piece[0] != player:
        return False
    
    # Check if the destination square is occupied by a friendly piece
    if board[end_row][end_col] != "  " and board[start_row][start_col][0] == board[end_row][end_col][0]:
        return False

    # Check if the move is valid for the piece being moved
    if piece.endswith("P"):  # Pawn
        # Check for a normal pawn move
        if start_col == end_col and board[end_row][end_col] == "  ":
            if piece.startswith("w"):
                if start_row == 6 and end_row == 4 and board[5][end_col] == "  ":
                    return True
                elif start_row - end_row == 1:
                    return True
            else:
                if start_row == 1 and end_row == 3 and board[2][end_col] == "  ":
                    return True
                elif end_row - start_row == 1:
                    return True
        # Check for a pawn capture
        elif abs(start_col - end_col) == 1 and abs(start_row - end_row) == 1:
            if piece.startswith("w") and end_row == start_row - 1 and board[end_row][end_col].startswith("b"):
                return True
            elif piece.startswith("b") and end_row == start_row + 1 and board[end_row][end_col].startswith("w"):
                return True
        # Check for en passant capture
        elif abs(start_col - end_col) == 1 and abs(start_row - end_row) == 1 and board[end_row][end_col] == "  ":
            if piece.startswith("w") and start_row == 3 and board[start_row][end_col].startswith("b"):
                if last_move == (start_row + 1, end_col, "bP"):
                    return True
            elif piece.startswith("b") and start_row == 4 and board[start_row][end_col].startswith("w"):
                if last_move == (start_row - 1, end_col, "wP"):
                    return True


    elif piece.endswith("R"):  # Rook
        # Check if the move is vertical or horizontal
        if start_row != end_row and start_col != end_col:
            return False
        # Check if there are any pieces in the way
        if start_row == end_row:
            # Check horizontal moves to the right
            if start_col < end_col:
                for col in range(start_col + 1, end_col):
                    if board[start_row][col] != "  ":
                        return False
            # Check horizontal moves to the left
            else:
                for col in range(start_col - 1, end_col, -1):
                    if board[start_row][col] != "  ":
                        return False
        else:
            # Check vertical moves downwards
            if start_row < end_row:
                for row in range(start_row + 1, end_row):
                    if board[row][start_col] != "  ":
                        return False
            # Check vertical moves upwards
            else:
                for row in range(start_row - 1, end_row, -1):
                    if board[row][start_col] != "  ":
                        return False
        return True
    elif piece.endswith("N"):  # Knight
    # Check if the move is an L-shape
        if abs(start_row - end_row) == 2 and abs(start_col - end_col) == 1:
            return True
        elif abs(start_row - end_row) == 1 and abs(start_col - end_col) == 2:
            return True
        else:
            return False    
    elif piece.endswith("B"):  # Bishop
    # Check if the move is diagonal
        if abs(start_row - end_row) != abs(start_col - end_col):
            return False
    # Check if there are any pieces in the way
        row_step = 1 if start_row < end_row else -1
        col_step = 1 if start_col < end_col else -1
        row, col = start_row + row_step, start_col + col_step
        piece_color = board[start_row][start_col][0]
        enemy_color = "b" if piece_color == "w" else "w"
        while row != end_row and col != end_col:
            p2 = board[row][col][0]
            if board[row][col][0] != " ":
                if board[row][col][0] == piece_color:
                    return False
                # check if the piece is an enemy piece
                elif p2 == enemy_color:
                    if row == end_row and col == end_col:
                        return True
                    else:
                        return False
                else:
                    return True
            row += row_step
            col += col_step
        return True

    elif piece.endswith("Q"):  # Queen
        if start_row == end_row or start_col == end_col:
            # Check if there are any pieces in the way
            if start_row == end_row:
                for col in range(min(start_col, end_col) + 1, max(start_col, end_col)):
                    if board[start_row][col] != "  ":
                        return False
            else:
                for row in range(min(start_row, end_row) + 1, max(start_row, end_row)):
                    if board[row][start_col] != "  ":
                        return False
            return True
        if abs(start_row - end_row) != abs(start_col - end_col):
            return False
        row_step = 1 if start_row < end_row else -1
        col_step = 1 if start_col < end_col else -1
        row, col = start_row + row_step, start_col + col_step
        piece_color = board[start_row][start_col][0]
        enemy_color = "b" if piece_color == "w" else "w"
        while row != end_row and col != end_col:
            p2 = board[row][col][0]
            if board[row][col][0] != " ":
                if board[row][col][0] == piece_color:
                    return False
                # check if the piece is an enemy piece
                elif p2 == enemy_color:
                    if row == end_row and col == end_col:
                        return True
                    else:
                        return False
                else:
                    return True
            row += row_step
            col += col_step
        return True

    elif piece.endswith("K"):  # King
        if abs(start_row - end_row) <= 1 and abs(start_col - end_col) <= 1:
            return True
        # Check for castling
        elif start_row == end_row and abs(start_col - end_col) == 2:
            # Check if the king and rook have not moved
            if piece[0] == "w" and start_row == 7 and start_col == 4 and \
               (end_row, end_col) == (7, 6) and board[7][7] == "wR ":
                # Check if the squares between the king and rook are empty
                if board[7][5] == " " and board[7][6] == " ":
                    return True
            elif piece[0] == "b" and start_row == 0 and start_col == 4 and \
               (end_row, end_col) == (0, 6) and board[0][7] == "bR ":
                # Check if the squares between the king and rook are empty
                if board[0][5] == " " and board[0][6] == " ":
                    return True
    else:             
        return False


# Define the main game loop
def main():
    selected_piece = None
    last_move = None
    current_player = "w"
    highlighted_squares = []
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Get the position of the mouse click
                pos = pygame.mouse.get_pos()
                # Calculate the row and column of the clicked square
                row = pos[1] // SQUARE_SIZE
                col = pos[0] // SQUARE_SIZE
                if selected_piece is None:
                    # If no piece is currently selected, select the clicked piece (if it exists)
                    piece = board[row][col]
                    if piece != "  " and piece[0] == current_player:
                        selected_piece = (row, col)
                        highlighted_squares = [(i, j) for i in range(8) for j in range(8) if is_valid_move(piece, row, col, i, j, board, current_player, last_move)]
                else:
                    for i in range(8):
                        for j in range(8):
                            if is_valid_move(board[selected_piece[0]][selected_piece[1]], selected_piece[0], selected_piece[1], i, j, board, current_player, last_move):
                                highlighted_squares.append((i, j))
                    
                    if is_valid_move(piece, selected_piece[0], selected_piece[1], row, col, board, current_player, last_move):
                        # Move the selected piece to the clicked square if the move is valid
                        last_move = (selected_piece[0], selected_piece[1], piece)
                        board[row][col] = board[selected_piece[0]][selected_piece[1]]
                        
                        board[selected_piece[0]][selected_piece[1]] = "  "
                        selected_piece = None
                        highlighted_squares = []
                        # Switch to the other player's turn
                        if current_player == "w":
                            current_player = "b"
                        else:
                            current_player = "w"
                    else:
                        # Deselect the piece if the move is not valid
                        selected_piece = None
                        highlighted_squares = []
                                
        draw_board()
        draw_highlighted_squares(highlighted_squares)
        if selected_piece is not None:
            x = selected_piece[1] * SQUARE_SIZE + SQUARE_SIZE // 2
            y = selected_piece[0] * SQUARE_SIZE + SQUARE_SIZE // 2
            pygame.draw.circle(screen, (255, 255, 0, 128), (x, y), SQUARE_SIZE // 2, 3)
        pygame.display.flip()
        
def draw_highlighted_squares(highlighted_squares):
    for square in highlighted_squares:
        x = square[1] * SQUARE_SIZE + SQUARE_SIZE // 2
        y = square[0] * SQUARE_SIZE + SQUARE_SIZE // 2
        pygame.draw.circle(screen, (255, 0, 0, 128), (x, y), SQUARE_SIZE // 4)


# Call the main game loop
main()

