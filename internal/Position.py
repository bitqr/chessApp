from internal import utils
from internal.Color import Color


class Position:

    def __init__(self):
        self.color_to_move = Color.WHITE
        self.pieces_positions = dict()
        self.legal_moves = dict()
        self.controlled_squares = dict()
        self.latest_move = None

    def update_legal_moves(self, all_squares):
        pieces_list = list(self.pieces_positions.keys())
        for piece in pieces_list:
            self.compute_legal_moves(piece, all_squares)

    def update_controlled_squares(self, all_squares):
        for piece in self.pieces_positions.keys():
            self.compute_controlled_squares(piece, all_squares)

    def compute_pseudo_legal_moves(self, piece, all_squares):
        origin_square = self.pieces_positions[piece]
        pseudo_legal_moves = []
        if piece.is_king():
            pseudo_legal_moves = utils.king_squares(piece, origin_square, all_squares, self)
        if piece.is_pawn():
            pseudo_legal_moves = utils.pawn_squares(piece, origin_square, all_squares, self.latest_move)
        if piece.is_bishop():
            pseudo_legal_moves = utils.bishop_squares(piece, origin_square, all_squares)
        if piece.is_rook():
            pseudo_legal_moves = utils.rook_squares(piece, origin_square, all_squares)
        if piece.is_queen():
            pseudo_legal_moves = utils.queen_squares(piece, origin_square, all_squares)
        if piece.is_knight():
            pseudo_legal_moves = utils.knight_squares(piece, origin_square, all_squares)
        return pseudo_legal_moves

    def compute_legal_moves(self, piece, all_squares):
        self.legal_moves[piece] = []
        # Pieces cannot be moved if it's not their turn
        if not piece.color == self.color_to_move:
            return self.legal_moves[piece]
        pseudo_legal_moves = self.compute_pseudo_legal_moves(piece, all_squares)
        for item in pseudo_legal_moves:
            original_controlled_squares = utils.dict_copy(self.controlled_squares)
            # Make the temporary move
            # Free the origin square
            square = self.pieces_positions[piece]
            all_squares[(square.rank, square.file)].empty_content()
            # If it's a capture, remove the captured piece
            captured_piece = None
            is_capture = not all_squares[item].is_free()
            if is_capture:
                captured_piece = all_squares[item].content
                self.pieces_positions.pop(captured_piece)
                self.controlled_squares[captured_piece.color][captured_piece] = []
            is_en_passant = piece.is_pawn() and square.file != item[1] and not is_capture
            if is_en_passant:
                captured_piece = all_squares[square.rank, item[1]].content
                self.pieces_positions.pop(captured_piece)
                self.controlled_squares[captured_piece.color][captured_piece] = []
                all_squares[square.rank, item[1]].empty_content()
            # Fill the destination square
            all_squares[item].content = piece
            self.pieces_positions[piece] = all_squares[item]
            # Update controlled squares
            self.update_controlled_squares(all_squares)
            # Find the king of the piece color and determine if it's in check
            for each_piece in self.pieces_positions.keys():
                if each_piece.color == piece.color and each_piece.is_king()\
                        and not self.is_in_check(each_piece):
                    self.legal_moves[piece].append(item)
                    break
            # Go back to previous position
            all_squares[(square.rank, square.file)].content = piece
            if is_capture:
                all_squares[item].content = captured_piece
                self.pieces_positions[captured_piece] = all_squares[item]
            else:
                all_squares[item].empty_content()
            if is_en_passant:
                all_squares[square.rank, item[1]].content = captured_piece
                self.pieces_positions[captured_piece] = all_squares[square.rank, item[1]]
            self.pieces_positions[piece] = square
            self.controlled_squares = original_controlled_squares
        return self.legal_moves[piece]

    def compute_controlled_squares(self, piece, all_squares):
        origin_square = self.pieces_positions[piece]
        if piece.color not in self.controlled_squares:
            self.controlled_squares[piece.color] = dict()
        if piece.is_pawn():
            self.controlled_squares[piece.color][piece] = \
                utils.pawn_controlled_squares(piece, self.pieces_positions[piece])
        elif piece.is_bishop():
            self.controlled_squares[piece.color][piece] =\
                utils.bishop_controlled_squares(origin_square, all_squares)
        elif piece.is_rook():
            self.controlled_squares[piece.color][piece] =\
                utils.rook_controlled_squares(origin_square, all_squares)
        elif piece.is_queen():
            self.controlled_squares[piece.color][piece] = \
                utils.queen_controlled_squares(origin_square, all_squares)
        elif piece.is_knight():
            self.controlled_squares[piece.color][piece] = \
                utils.knight_controlled_squares(origin_square)
        else:
            self.controlled_squares[piece.color][piece] = self.compute_pseudo_legal_moves(piece, all_squares)

    def update_position(self, piece, square):
        self.pieces_positions[piece] = square

    def is_controlled(self, rank, file, color):
        for piece in self.controlled_squares[color].keys():
            if (rank, file) in self.controlled_squares[color][piece]:
                return True
        return False

    def add_captured_piece(self, piece):
        self.pieces_positions.pop(piece)
        self.controlled_squares[piece.color][piece] = []

    def is_in_check(self, king):
        king_square = self.pieces_positions[king]
        return self.is_controlled(king_square.rank, king_square.file, king.opposite_color())

    def legal_moves_count(self):
        result = 0
        for piece in self.legal_moves.keys():
            if piece.color == self.color_to_move:
                result += len(self.legal_moves[piece])
        return result
