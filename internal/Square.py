from internal import utils
from internal.Piece import Piece
from internal.PieceType import PieceType
from internal.Color import Color


class Square:

    def __init__(self, rank, file):
        self.rank = rank
        self.file = file
        self.content = Piece(PieceType.NONE)

    def set_content(self, piece):
        self.content = piece

    def is_free(self):
        return self.content.type == PieceType.NONE

    def get_color(self):
        return Color.WHITE if (self.rank + self.file) % 2 == 0 else Color.BLACK

    def empty_content(self):
        self.content = Piece(PieceType.NONE)

    def contains_friendly_piece(self, piece):
        return not self.is_free() and self.content.color == piece.color

    def contains_opponent_piece(self, piece):
        return not self.is_free() and self.content.color != piece.color

    def contains_opponent_pawn(self, piece):
        return not self.is_free() and self.content.color != piece.color and self.content.is_pawn()

    def to_string(self):
        return '{0}{1}'.format(utils.CHESSBOARD_FILE_NAMES[self.file], 8 - self.rank)
