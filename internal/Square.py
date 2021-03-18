from internal.Piece import Piece
from internal.PieceType import PieceType


class Square:

    def __init__(self, rank, file):
        self.rank = rank
        self.file = file
        self.content = Piece(PieceType.NONE)

    def set_content(self, piece):
        self.content = piece

    def is_free(self):
        return self.content.type == PieceType.NONE
