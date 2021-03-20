from internal.util import *


class Piece:

    def __init__(self, piece_type, color=Color.WHITE):
        self.type = piece_type
        self.color = color
        self.never_moved = True

    def opponent_direction(self):
        return -1 if self.color == Color.WHITE else 1

    def to_string(self):
        if self.type == PieceType.NONE:
            return 'Nothing'
        return f'{piece_color_to_string(self.color)} {piece_type_to_string(self.type)}'

    def is_king(self):
        return self.type == PieceType.KING

    def is_pawn(self):
        return self.type == PieceType.PAWN

    def is_bishop(self):
        return self.type == PieceType.BISHOP

    def is_rook(self):
        return self.type == PieceType.ROOK

    def is_queen(self):
        return self.type == PieceType.QUEEN

    def is_knight(self):
        return self.type == PieceType.KNIGHT
