from internal.Color import Color


def base_rank_index(piece_color):
    if piece_color == Color.WHITE:
        return 7
    return 0


def castling_files():
    return [2, 6]


class Move:

    def __init__(self, piece, square):
        self.piece = piece
        self.square = square
        self.is_castle = self.is_castle()

    def is_capture(self):
        return not self.square.is_free()

    def is_castle(self):
        return self.piece.is_king() and self.piece.never_moved \
               and self.square.rank == base_rank_index(self.piece.color) \
               and self.square.file in castling_files()
