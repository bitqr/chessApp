from internal.Color import Color
from internal.util import *


class Piece:

    def __init__(self, piece_type, color=Color.WHITE):
        self.type = piece_type
        self.color = color

    def to_string(self):
        if self.type == PieceType.NONE:
            return 'Nothing'
        return f'{piece_color_to_string(self.color)} {piece_type_to_string(self.type)}'
