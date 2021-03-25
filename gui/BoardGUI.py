from gui.SquareGUI import SquareGUI
from gui.PieceGUI import PieceGUI
from gui.utils import *
from pygame import sprite

from internal.Piece import Piece


class BoardGUI:

    def __init__(self, board, square_size):
        self.square_size = square_size
        self.board = board
        self.square_to_sprite = square_to_sprite()
        self.piece_to_sprite = piece_to_sprite()
        self.square_sprites = dict()
        self.piece_sprites = dict()
        self.promotion_piece_groups = dict()
        self.promotion_piece_sprites = dict()
        self.square_group = sprite.Group()
        self.piece_group = sprite.Group()
        self.dragging_group = sprite.Group()
        self.board_width = board.size * square_size
        self.board_height = board.size * square_size
        self.check_highlighted_square_sprite = None

    def initialize_board(self):
        for rank in range(self.board.size):
            for file in range(self.board.size):
                square = self.board.squares[(rank, file)]
                square_sprite = self.create_square(square)
                self.square_sprites[(square.rank, square.file)] = square_sprite
                self.square_group.add(square_sprite)
                if not square.is_free():
                    piece = square.content
                    piece_sprite = self.create_piece(piece, square.rank, square.file)
                    self.piece_sprites[piece] = piece_sprite
                    self.piece_group.add(piece_sprite)
        self.initialize_pawn_promotion_sprites()

    def initialize_pawn_promotion_sprites(self):
        # Add promotion sprites (4 piece sprites per color) to display only in pawn promotion position
        self.promotion_piece_groups[Color.WHITE] = pygame.sprite.Group()
        self.promotion_piece_groups[Color.BLACK] = pygame.sprite.Group()
        self.promotion_piece_sprites[Color.WHITE] = []
        self.promotion_piece_sprites[Color.BLACK] = []
        self.promotion_piece_sprites[Color.WHITE].append(self.create_piece(Piece(PieceType.KNIGHT, Color.WHITE), 8, 1))
        self.promotion_piece_sprites[Color.WHITE].append(self.create_piece(Piece(PieceType.BISHOP, Color.WHITE), 8, 3))
        self.promotion_piece_sprites[Color.WHITE].append(self.create_piece(Piece(PieceType.ROOK, Color.WHITE), 8, 5))
        self.promotion_piece_sprites[Color.WHITE].append(self.create_piece(Piece(PieceType.QUEEN, Color.WHITE), 8, 7))
        self.promotion_piece_sprites[Color.BLACK].append(self.create_piece(Piece(PieceType.KNIGHT, Color.BLACK), 9, 1))
        self.promotion_piece_sprites[Color.BLACK].append(self.create_piece(Piece(PieceType.BISHOP, Color.BLACK), 9, 3))
        self.promotion_piece_sprites[Color.BLACK].append(self.create_piece(Piece(PieceType.ROOK, Color.BLACK), 9, 5))
        self.promotion_piece_sprites[Color.BLACK].append(self.create_piece(Piece(PieceType.QUEEN, Color.BLACK), 9, 7))
        for white_piece_sprite in self.promotion_piece_sprites[Color.WHITE]:
            self.promotion_piece_groups[Color.WHITE].add(white_piece_sprite)
        for black_piece_sprite in self.promotion_piece_sprites[Color.BLACK]:
            self.promotion_piece_groups[Color.BLACK].add(black_piece_sprite)

    def draw_board(self, screen):
        # Draw squares before pieces
        self.square_group.draw(screen)
        self.piece_group.draw(screen)
        self.promotion_piece_groups[Color.WHITE].draw(screen)
        self.promotion_piece_groups[Color.BLACK].draw(screen)
        if len(self.dragging_group) > 0:
            dragged_piece = self.dragging_group.sprites()[0]
            if self.contains(dragged_piece):
                self.dragging_group.draw(screen)

    def create_square(self, square):
        return SquareGUI(
            square,
            self.square_size,
            'sprites/{0}.png'.format(self.square_to_sprite[square.get_color()])
        )

    def create_piece(self, piece, rank, file):
        return PieceGUI(
            piece,
            self.square_size,
            'sprites/{0}.png'.format(self.piece_to_sprite[(piece.type, piece.color)]),
            rank,
            file
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

    def is_captured_piece(self, piece_sprite):
        return piece_sprite.piece not in self.board.position.pieces_positions.keys()
