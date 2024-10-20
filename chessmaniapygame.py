import pygame
import sys
from enum import Enum
from typing import List, Tuple, Optional

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 640, 640
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH // COLS

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_BROWN = (238, 238, 210)
DARK_BROWN = (118, 150, 86)
HIGHLIGHT = (255, 255, 0, 100)  # Semi-transparent yellow
CHECK_COLOR = (255, 0, 0, 100)  # Semi-transparent red
INVALID_MOVE_COLOR = (128, 128, 128, 100)  # Semi-transparent gray

# Load images
PIECES = {
    "wP": pygame.image.load("images/wP.png"),
    "wR": pygame.image.load("images/wR.png"),
    "wN": pygame.image.load("images/wN.png"),
    "wB": pygame.image.load("images/wB.png"),
    "wQ": pygame.image.load("images/wQ.png"),
    "wK": pygame.image.load("images/wK.png"),
    "bP": pygame.image.load("images/bP.png"),
    "bR": pygame.image.load("images/bR.png"),
    "bN": pygame.image.load("images/bN.png"),
    "bB": pygame.image.load("images/bB.png"),
    "bQ": pygame.image.load("images/bQ.png"),
    "bK": pygame.image.load("images/bK.png"),
}

# Resize piece images
for piece in PIECES:
    PIECES[piece] = pygame.transform.scale(PIECES[piece], (SQUARE_SIZE, SQUARE_SIZE))

class PieceType(Enum):
    PAWN = "P"
    ROOK = "R"
    KNIGHT = "N"
    BISHOP = "B"
    QUEEN = "Q"
    KING = "K"

class Color(Enum):
    WHITE = "w"
    BLACK = "b"

class Piece:
    def __init__(self, color: Color, piece_type: PieceType):
        self.color = color
        self.type = piece_type

    def __str__(self):
        return f"{self.color.value}{self.type.value}"

    def get_legal_moves(self, board: 'Board', row: int, col: int) -> List[Tuple[int, int]]:
        if self.type == PieceType.PAWN:
            return board.get_pawn_moves(row, col)
        elif self.type == PieceType.ROOK:
            return board.get_rook_moves(row, col)
        elif self.type == PieceType.KNIGHT:
            return board.get_knight_moves(row, col)
        elif self.type == PieceType.BISHOP:
            return board.get_bishop_moves(row, col)
        elif self.type == PieceType.QUEEN:
            return board.get_queen_moves(row, col)
        elif self.type == PieceType.KING:
            return board.get_king_moves(row, col)
        return []

class Board:
    def __init__(self):
        self.reset()

    def reset(self):
        self.board = [[None for _ in range(COLS)] for _ in range(ROWS)]
        self.set_initial_position()
        self.en_passant_target = None
        self.current_player = Color.WHITE
        self.move_history = []

    def set_initial_position(self):
        # Set up the initial chess board position
        piece_order = [PieceType.ROOK, PieceType.KNIGHT, PieceType.BISHOP, PieceType.QUEEN,
                       PieceType.KING, PieceType.BISHOP, PieceType.KNIGHT, PieceType.ROOK]
        
        for col in range(COLS):
            self.board[0][col] = Piece(Color.BLACK, piece_order[col])
            self.board[1][col] = Piece(Color.BLACK, PieceType.PAWN)
            self.board[6][col] = Piece(Color.WHITE, PieceType.PAWN)
            self.board[7][col] = Piece(Color.WHITE, piece_order[col])

    def is_valid_position(self, row: int, col: int) -> bool:
        return 0 <= row < ROWS and 0 <= col < COLS

    def get_piece(self, row: int, col: int) -> Optional[Piece]:
        if self.is_valid_position(row, col):
            return self.board[row][col]
        return None

    def is_enemy(self, piece1: Piece, piece2: Piece) -> bool:
        return piece1 is not None and piece2 is not None and piece1.color != piece2.color

    def make_move(self, start: Tuple[int, int], end: Tuple[int, int]) -> None:
        start_row, start_col = start
        end_row, end_col = end
        piece = self.board[start_row][start_col]
        
        # Handle en passant capture
        if piece.type == PieceType.PAWN and (end_row, end_col) == self.en_passant_target:
            self.board[start_row][end_col] = None
        
        # Move the piece
        self.board[end_row][end_col] = piece
        self.board[start_row][start_col] = None
        
        # Handle pawn promotion (always promote to queen for simplicity)
        if piece.type == PieceType.PAWN and (end_row == 0 or end_row == 7):
            self.board[end_row][end_col] = Piece(piece.color, PieceType.QUEEN)
        
        # Update en passant target
        self.en_passant_target = None
        if piece.type == PieceType.PAWN and abs(start_row - end_row) == 2:
            self.en_passant_target = (end_row + (start_row - end_row) // 2, end_col)
        
        # Switch current player
        self.current_player = Color.BLACK if self.current_player == Color.WHITE else Color.WHITE
        
        # Add move to history
        self.move_history.append((start, end))

    def get_pawn_moves(self, row: int, col: int) -> List[Tuple[int, int]]:
        moves = []
        piece = self.get_piece(row, col)
        if piece is None:
            return moves

        direction = -1 if piece.color == Color.WHITE else 1
        start_row = 6 if piece.color == Color.WHITE else 1

        # Move forward
        if self.get_piece(row + direction, col) is None:
            moves.append((row + direction, col))
            # Double move from start position
            if row == start_row and self.get_piece(row + 2*direction, col) is None:
                moves.append((row + 2*direction, col))

        # Capture diagonally
        for dcol in [-1, 1]:
            if self.is_valid_position(row + direction, col + dcol):
                target = self.get_piece(row + direction, col + dcol)
                if self.is_enemy(piece, target) or (row + direction, col + dcol) == self.en_passant_target:
                    moves.append((row + direction, col + dcol))

        return moves

    def get_rook_moves(self, row: int, col: int) -> List[Tuple[int, int]]:
        moves = []
        piece = self.get_piece(row, col)
        if piece is None:
            return moves

        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dr, dc in directions:
            for i in range(1, 8):
                new_row, new_col = row + i*dr, col + i*dc
                if not self.is_valid_position(new_row, new_col):
                    break
                target = self.get_piece(new_row, new_col)
                if target is None:
                    moves.append((new_row, new_col))
                elif self.is_enemy(piece, target):
                    moves.append((new_row, new_col))
                    break
                else:
                    break
        return moves

    def get_knight_moves(self, row: int, col: int) -> List[Tuple[int, int]]:
        moves = []
        piece = self.get_piece(row, col)
        if piece is None:
            return moves

        knight_moves = [(-2, -1), (-2, 1), (-1, -2), (-1, 2),
                        (1, -2), (1, 2), (2, -1), (2, 1)]
        for dr, dc in knight_moves:
            new_row, new_col = row + dr, col + dc
            if self.is_valid_position(new_row, new_col):
                target = self.get_piece(new_row, new_col)
                if target is None or self.is_enemy(piece, target):
                    moves.append((new_row, new_col))
        return moves

    def get_bishop_moves(self, row: int, col: int) -> List[Tuple[int, int]]:
        moves = []
        piece = self.get_piece(row, col)
        if piece is None:
            return moves

        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        for dr, dc in directions:
            for i in range(1, 8):
                new_row, new_col = row + i*dr, col + i*dc
                if not self.is_valid_position(new_row, new_col):
                    break
                target = self.get_piece(new_row, new_col)
                if target is None:
                    moves.append((new_row, new_col))
                elif self.is_enemy(piece, target):
                    moves.append((new_row, new_col))
                    break
                else:
                    break
        return moves

    def get_queen_moves(self, row: int, col: int) -> List[Tuple[int, int]]:
        return self.get_rook_moves(row, col) + self.get_bishop_moves(row, col)

    def get_king_moves(self, row: int, col: int) -> List[Tuple[int, int]]:
        moves = []
        piece = self.get_piece(row, col)
        if piece is None:
            return moves

        king_moves = [(-1, -1), (-1, 0), (-1, 1), (0, -1),
                      (0, 1), (1, -1), (1, 0), (1, 1)]
        for dr, dc in king_moves:
            new_row, new_col = row + dr, col + dc
            if self.is_valid_position(new_row, new_col):
                target = self.get_piece(new_row, new_col)
                if target is None or self.is_enemy(piece, target):
                    moves.append((new_row, new_col))
        return moves

    def is_square_attacked(self, row: int, col: int, attacking_color: Color) -> bool:
        for r in range(ROWS):
            for c in range(COLS):
                piece = self.get_piece(r, c)
                if piece is not None and piece.color == attacking_color:
                    if (row, col) in piece.get_legal_moves(self, r, c):
                        return True
        return False

    def find_king(self, color: Color) -> Optional[Tuple[int, int]]:
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.get_piece(row, col)
                if piece is not None and piece.color == color and piece.type == PieceType.KING:
                    return row, col
        return None

    def is_in_check(self, color: Color) -> bool:
        king_pos = self.find_king(color)
        if king_pos is None:
            return False
        return self.is_square_attacked(king_pos[0], king_pos[1], Color.BLACK if color == Color.WHITE else Color.WHITE)

    def is_checkmate(self, color: Color) -> bool:
        if not self.is_in_check(color):
            return False
        
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.get_piece(row, col)
                if piece is not None and piece.color == color:
                    legal_moves = self.get_legal_moves(row, col)
                    if legal_moves:
                        return False
        return True

    def is_stalemate(self, color: Color) -> bool:
        if self.is_in_check(color):
            return False
        
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.get_piece(row, col)
                if piece is not None and piece.color == color:
                    legal_moves = self.get_legal_moves(row, col)
                    if legal_moves:
                        return False
        return True

    def get_legal_moves(self, row: int, col: int) -> List[Tuple[int, int]]:
        piece = self.get_piece(row, col)
        if piece is None:
            return []

        moves = piece.get_legal_moves(self, row, col)
        legal_moves = []
        for move in moves:
            temp_board = Board()
            temp_board.board = [row[:] for row in self.board]
            temp_board.make_move((row, col), move)
            if not temp_board.is_in_check(piece.color):
                legal_moves.append(move)
        return legal_moves

class ChessGame:
    def __init__(self):
        self.board = Board()
        self.selected_piece = None
        self.dragging_piece = None
        self.legal_moves = []
        self.game_over = False
        self.winner = None

    def handle_click(self, pos: Tuple[int, int]) -> None:
        if self.game_over:
            return

        col, row = pos[0] // SQUARE_SIZE, pos[1] // SQUARE_SIZE
        piece = self.board.get_piece(row, col)
        
        if self.selected_piece is None:
            if piece is not None and piece.color == self.board.current_player:
                self.selected_piece = (row, col)
                self.dragging_piece = (str(piece), pos)
                self.legal_moves = self.board.get_legal_moves(row, col)
        else:
            if (row, col) in self.legal_moves:
                self.board.make_move(self.selected_piece, (row, col))
                self.selected_piece = None
                self.dragging_piece = None
                self.legal_moves = []
                self.check_game_over()
            elif piece is not None and piece.color == self.board.current_player:
                self.selected_piece = (row, col)
                self.dragging_piece = (str(piece), pos)
                self.legal_moves = self.board.get_legal_moves(row, col)
            else:
                self.selected_piece = None
                self.dragging_piece = None
                self.legal_moves = []

    def handle_drag(self, pos: Tuple[int, int]) -> None:
        if self.dragging_piece:
            self.dragging_piece = (self.dragging_piece[0], pos)

    def check_game_over(self) -> None:
        if self.board.is_checkmate(self.board.current_player):
            self.game_over = True
            self.winner = Color.WHITE if self.board.current_player == Color.BLACK else Color.BLACK
        elif self.board.is_stalemate(self.board.current_player):
            self.game_over = True
            self.winner = None

    def draw(self, screen: pygame.Surface) -> None:
        self.draw_board(screen)
        self.draw_pieces(screen)
        self.draw_highlights(screen)
        self.draw_game_over(screen)

    def draw_board(self, screen: pygame.Surface) -> None:
        for row in range(ROWS):
            for col in range(COLS):
                color = LIGHT_BROWN if (row + col) % 2 == 0 else DARK_BROWN
                pygame.draw.rect(screen, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def draw_pieces(self, screen: pygame.Surface) -> None:
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board.get_piece(row, col)
                if piece is not None and (row, col) != self.selected_piece:
                    screen.blit(PIECES[str(piece)], (col * SQUARE_SIZE, row * SQUARE_SIZE))
        
        if self.dragging_piece:
            piece, pos = self.dragging_piece
            screen.blit(PIECES[piece], (pos[0] - SQUARE_SIZE // 2, pos[1] - SQUARE_SIZE // 2))

    def draw_highlights(self, screen: pygame.Surface) -> None:
        if self.selected_piece:
            row, col = self.selected_piece
            pygame.draw.rect(screen, HIGHLIGHT, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
        
        for move in self.legal_moves:
            row, col = move
            pygame.draw.circle(screen, HIGHLIGHT, 
                               (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), 
                               SQUARE_SIZE // 6)

        for color in [Color.WHITE, Color.BLACK]:
            if self.board.is_in_check(color):
                king_pos = self.board.find_king(color)
                if king_pos:
                    row, col = king_pos
                    pygame.draw.rect(screen, CHECK_COLOR, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def draw_game_over(self, screen: pygame.Surface) -> None:
        if self.game_over:
            font = pygame.font.Font(None, 74)
            if self.winner:
                text = f"{'White' if self.winner == Color.WHITE else 'Black'} wins!"
            else:
                text = "Stalemate!"
            text_surface = font.render(text, True, BLACK)
            text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            pygame.draw.rect(screen, WHITE, text_rect.inflate(20, 20))
            screen.blit(text_surface, text_rect)

def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Chess Game")
    clock = pygame.time.Clock()
    game = ChessGame()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                game.handle_click(pygame.mouse.get_pos())
            elif event.type == pygame.MOUSEMOTION:
                game.handle_drag(pygame.mouse.get_pos())
            elif event.type == pygame.MOUSEBUTTONUP:
                game.handle_click(pygame.mouse.get_pos())
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # Reset game
                    game = ChessGame()

        game.draw(screen)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()