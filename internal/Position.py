from internal import util


class Position:

    def __init__(self):
        self.pieces_positions = dict()

    def update_position(self, piece, square):
        self.pieces_positions[piece] = square

    def controlled_squares(self, piece):
        origin_square = self.pieces_positions[piece]
        if piece.is_king():
            return util.king_squares(origin_square)
        if piece.is_pawn():
            return util.pawn_squares(piece, origin_square)
        return []
