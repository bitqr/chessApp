from internal import util


class Position:

    def __init__(self):
        self.pieces_positions = dict()

    def update_position(self, piece, square):
        self.pieces_positions[piece] = square

    def moving_squares(self, piece, all_squares):
        origin_square = self.pieces_positions[piece]
        if piece.is_king():
            return util.king_squares(origin_square)
        if piece.is_pawn():
            return util.pawn_squares(piece, origin_square)
        if piece.is_bishop():
            return util.bishop_squares(origin_square, all_squares)
        if piece.is_rook():
            return util.rook_squares(origin_square, all_squares)
        if piece.is_queen():
            return util.queen_squares(origin_square, all_squares)
        if piece.is_knight():
            return util.knight_squares(origin_square)
        return []
