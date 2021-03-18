from internal.PieceColor import PieceColor


class Piece:

    def __init__(self, piece_type, color=PieceColor.WHITE):
        self.type = piece_type
        self.color = color
