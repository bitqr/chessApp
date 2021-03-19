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

    def to_string(self):
        return f'({self.rank}, {self.file}) --> {self.content.to_string()}'
