from internal import util


class Position:

    def __init__(self):
        self.pieces_positions = dict()
        self.legal_moves = dict()

    def update_legal_moves(self, all_squares):
        for piece in self.pieces_positions.keys():
            self.compute_legal_moves(piece, all_squares)

    def compute_legal_moves(self, piece, all_squares):
        origin_square = self.pieces_positions[piece]
        if piece.is_king():
            self.legal_moves[piece] = util.king_squares(piece, origin_square, all_squares)
        if piece.is_pawn():
            self.legal_moves[piece] = util.pawn_squares(piece, origin_square, all_squares)
        if piece.is_bishop():
            self.legal_moves[piece] = util.bishop_squares(piece, origin_square, all_squares)
        if piece.is_rook():
            self.legal_moves[piece] = util.rook_squares(piece, origin_square, all_squares)
        if piece.is_queen():
            self.legal_moves[piece] = util.queen_squares(piece, origin_square, all_squares)
        if piece.is_knight():
            self.legal_moves[piece] = util.knight_squares(piece, origin_square, all_squares)

    def update_position(self, piece, square):
        self.pieces_positions[piece] = square
