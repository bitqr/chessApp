from internal.PieceType import PieceType
from internal.Color import Color


def piece_to_sprite():
    result = dict()
    result[(PieceType.PAWN, Color.WHITE)] = "whitePawn"
    result[(PieceType.KNIGHT, Color.WHITE)] = "whiteKnight"
    result[(PieceType.BISHOP, Color.WHITE)] = "whiteBishop"
    result[(PieceType.ROOK, Color.WHITE)] = "whiteRook"
    result[(PieceType.QUEEN, Color.WHITE)] = "whiteQueen"
    result[(PieceType.KING, Color.WHITE)] = "whiteKing"
    result[(PieceType.PAWN, Color.BLACK)] = "blackPawn"
    result[(PieceType.KNIGHT, Color.BLACK)] = "blackKnight"
    result[(PieceType.BISHOP, Color.BLACK)] = "blackBishop"
    result[(PieceType.ROOK, Color.BLACK)] = "blackRook"
    result[(PieceType.QUEEN, Color.BLACK)] = "blackQueen"
    result[(PieceType.KING, Color.BLACK)] = "blackKing"
    return result


def square_to_sprite():
    result = dict()
    result[Color.WHITE] = "whiteSquare"
    result[Color.BLACK] = "blackSquare"
    return result
