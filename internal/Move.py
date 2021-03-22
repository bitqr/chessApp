from internal.Color import Color
from internal.PieceType import PieceType


def base_rank_index(piece_color):
    if piece_color == Color.WHITE:
        return 7
    return 0


castling_files = [2, 6]


class Move:

    def __init__(self, piece, square):
        self.piece = piece
        self.square = square
        self.is_king_side_castle = self.is_king_side_castle()
        self.is_queen_side_castle = self.is_queen_side_castle()
        self.is_castle = self.is_king_side_castle or self.is_queen_side_castle
        self.is_check = False

    def is_capture(self):
        return not self.square.is_free()

    def is_king_side_castle(self):
        return self.piece.is_king() and self.piece.never_moved \
               and self.square.rank == base_rank_index(self.piece.color) \
               and self.square.file == castling_files[1]

    def is_queen_side_castle(self):
        return self.piece.is_king() and self.piece.never_moved \
               and self.square.rank == base_rank_index(self.piece.color) \
               and self.square.file == castling_files[0]

    def to_string(self, origin_square, target_piece):
        delimiter = "x" if target_piece.type != PieceType.NONE else "_"
        result = \
            f'{self.piece.to_string()}_{origin_square.to_string()}{delimiter}{self.square.to_string()}'
        if self.is_king_side_castle:
            return '0-0'
        if self.is_queen_side_castle:
            return '0-0-0'
        if self.is_check:
            result += 'x'
        return result
