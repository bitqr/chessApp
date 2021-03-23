from gui.SquareGUI import SquareGUI
from gui.PieceGUI import PieceGUI
from gui.utils import *
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
        self.dragging_group = sprite.Group()
        self.board_width = board.size * square_size
        self.board_height = board.size * square_size
        self.check_highlighted_square_sprite = None

    def initialize_board(self, board):
        for rank in range(board.size):
            for file in range(board.size):
                square = board.squares[(rank, file)]
                square_sprite = self.create_square(square)
                self.square_sprites[(square.rank, square.file)] = square_sprite
                self.square_group.add(square_sprite)
                if not square.is_free():
                    piece = square.content
                    piece_sprite = self.create_piece(piece, board.position.pieces_positions[piece])
                    self.piece_sprites[piece] = piece_sprite
                    self.piece_group.add(piece_sprite)

    def draw_board(self, screen):
        # Draw squares before pieces
        self.square_group.draw(screen)
        self.piece_group.draw(screen)
        if len(self.dragging_group) > 0:
            dragged_piece = self.dragging_group.sprites()[0]
            if self.contains(dragged_piece):
                self.dragging_group.draw(screen)

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

    def current_square_sprite(self, piece_sprite):
        square = self.board.current_square(piece_sprite.piece)
        return self.square_sprites[(square.rank, square.file)]

    def is_white_in_check(self):
        return self.board.position.is_in_check(self.board.white_king)

    def is_black_in_check(self):
        return self.board.position.is_in_check(self.board.black_king)

    def attacked_king_sprite(self, attacking_piece):
        checked_king_sprite = \
            self.piece_sprites[self.board.white_king if attacking_piece.is_black() else self.board.black_king]
        return self.current_square_sprite(checked_king_sprite)

    def contains(self, piece_sprite):
        return piece_sprite.rect.bottom <= self.board_width and piece_sprite.rect.right - 10 <= self.board_height
