from internal.Color import Color
from internal.PieceType import PieceType


def piece_type_to_string(piece_type):
    if piece_type == PieceType.PAWN:
        return 'Pawn'
    if piece_type == PieceType.KNIGHT:
        return 'Knight'
    if piece_type == PieceType.BISHOP:
        return 'Bishop'
    if piece_type == PieceType.ROOK:
        return 'Rook'
    if piece_type == PieceType.QUEEN:
        return 'Queen'
    if piece_type == PieceType.KING:
        return 'King'
    return 'Nothing'


def piece_color_to_string(piece_color):
    return 'Black' if piece_color == Color.BLACK else 'White'


def base_rank_index(piece_color):
    if piece_color == Color.WHITE:
        return 7
    return 0


castling_files = [2, 6]


class Move:

    def __init__(self, origin_square, destination_square, squares):
        self.piece = squares[(origin_square.rank, origin_square.file)].content
        self.origin_square = origin_square
        self.destination_square = destination_square
        self.is_king_side_castle = self.is_king_side_castle()
        self.is_queen_side_castle = self.is_queen_side_castle()
        self.is_castle = self.is_king_side_castle or self.is_queen_side_castle
        self.is_double_pawn_move = self.is_double_pawn_move()
        self.is_check = False
        self.is_capture = self.is_capture()
        self.is_en_passant = self.is_en_passant()
        self.is_promotion = self.is_promotion()
        self.promoted_piece_type = PieceType.NONE

    def is_capture(self):
        return not self.destination_square.is_free()

    def is_king_side_castle(self):
        return self.piece.is_king() and self.piece.never_moved \
               and self.destination_square.rank == base_rank_index(self.piece.color) \
               and self.destination_square.file == castling_files[1]

    def is_queen_side_castle(self):
        return self.piece.is_king() and self.piece.never_moved \
               and self.destination_square.rank == base_rank_index(self.piece.color) \
               and self.destination_square.file == castling_files[0]

    def is_pawn_move(self):
        return self.piece.is_pawn() or self.is_promotion

    def is_double_pawn_move(self):
        return self.piece.is_pawn() and abs(self.destination_square.rank - self.origin_square.rank) == 2

    def is_en_passant(self):
        return self.piece.is_pawn() and not self.is_capture \
               and self.origin_square.file != self.destination_square.file

    def is_promotion(self):
        return self.piece.is_pawn() \
               and ((self.piece.is_white() and self.destination_square.rank == 0)
                    or (self.piece.is_black() and self.destination_square.rank == 7))

    def to_string(self, target_piece=None):
        delimiter = 'x' if (target_piece and target_piece.type != PieceType.NONE) or self.is_en_passant else '_'
        piece_to_display = '{0}: Pawn'.format(piece_color_to_string(self.piece.color)) \
            if self.is_promotion else self.piece.to_string()
        result = \
            '{0}_{1}{2}{3}'.format(
                piece_to_display, self.origin_square.to_string(), delimiter, self.destination_square.to_string()
            )
        if self.is_promotion:
            result += '({0})'.format(piece_type_to_string(self.promoted_piece_type))
        if self.is_king_side_castle:
            return '{0}: O-O'.format(piece_color_to_string(self.piece.color))
        if self.is_queen_side_castle:
            return '{0}: O-O-O'.format(piece_color_to_string(self.piece.color))
        if self.is_check:
            result += '+'
        return result
