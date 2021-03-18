from internal.PieceType import PieceType
from internal.PieceColor import PieceColor


def piece_to_sprite():
    result = dict()
    result[(PieceType.PAWN, PieceColor.WHITE)] = "whitePawn"
    result[(PieceType.KNIGHT, PieceColor.WHITE)] = "whiteKnight"
    result[(PieceType.BISHOP, PieceColor.WHITE)] = "whiteBishop"
    result[(PieceType.ROOK, PieceColor.WHITE)] = "whiteRook"
    result[(PieceType.QUEEN, PieceColor.WHITE)] = "whiteQueen"
    result[(PieceType.KING, PieceColor.WHITE)] = "whiteKing"
    result[(PieceType.PAWN, PieceColor.BLACK)] = "blackPawn"
    result[(PieceType.KNIGHT, PieceColor.BLACK)] = "blackKnight"
    result[(PieceType.BISHOP, PieceColor.BLACK)] = "blackBishop"
    result[(PieceType.ROOK, PieceColor.BLACK)] = "blackRook"
    result[(PieceType.QUEEN, PieceColor.BLACK)] = "blackQueen"
    result[(PieceType.KING, PieceColor.BLACK)] = "blackKing"
    return result
