from internal.Color import Color
from internal.PieceType import PieceType


def piece_color_to_string(piece_color):
    return 'White' if piece_color == Color.WHITE else 'Black'


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


def is_out_of_board(rank):
    return rank < 0 or 7 < rank


def king_squares(square):
    result = []
    for rank in range(max(0, square.rank - 1), min(7, square.rank + 1) + 1):
        for file in range(max(0, square.file - 1), min(7, square.file + 1) + 1):
            result.append((rank, file))
    return result


def pawn_squares(piece, square):
    result = []
    rank = square.rank + piece.opponent_direction()
    if is_out_of_board(rank):
        return result
    for file in range(max(0, square.file - 1), min(7, square.file + 1) + 1):
        result.append((rank, file))
    if piece.never_moved:
        result.append((rank + piece.opponent_direction(), square.file))
    return result
