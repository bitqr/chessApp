from gui.SquareGUI import SquareGUI
from gui.PieceGUI import PieceGUI
from gui.util import *
from pygame import sprite


class BoardGUI:

    def __init__(self, board, square_size):
        self.square_size = square_size
        self.board = board
        self.square_to_sprite = square_to_sprite()
        self.piece_to_sprite = piece_to_sprite()
        self.square_sprites = dict()
        self.piece_sprites = dict()
        self.square_group = sprite.Group()
        self.piece_group = sprite.Group()
        self.board_width = board.size * square_size
        self.board_height = board.size * square_size

    def initialize_board(self, board, screen):
        for rank in range(board.size):
            for file in range(board.size):
                square = board.squares[(rank, file)]
                square_sprite = self.create_square(square)
                self.square_sprites[(square.rank, square.file)] = square_sprite
                self.square_group.add(square_sprite)
                if not square.is_free():
                    piece = square.content
                    piece_sprite = self.create_piece(piece, board.position.pieces_positions[piece])
                    self.piece_sprites[(square.rank, square.file)] = piece_sprite
                    self.piece_group.add(piece_sprite)
        self.square_group.draw(screen)
        self.piece_group.draw(screen)

    def draw_board(self, screen):
        # Draw squares before pieces
        self.square_group.draw(screen)
        self.piece_group.draw(screen)

    def create_square(self, square):
        return SquareGUI(
            square,
            self.square_size,
            f'sprites/{self.square_to_sprite[square.get_color()]}.png'
        )

    def create_piece(self, piece, location_square):
        return PieceGUI(
            piece,
            self.square_size,
            f'sprites/{self.piece_to_sprite[(piece.type, piece.color)]}.png',
            location_square
        )
