from internal import utils
from internal.Color import Color
from internal.Move import Move
from internal.PieceType import PieceType


class Position:

    def __init__(self, squares):
        self.color_to_move = Color.WHITE
        self.pieces_positions = dict()
        self.legal_moves = dict()
        self.controlled_squares = dict()
        self.latest_move = None
        self.squares = squares

    def left_pieces_on_board(self):
        return self.pieces_positions.keys()

    def is_dead_position(self):
        pieces = self.left_pieces_on_board()
        # King vs King
        if len(pieces) == 2:
            return True
        # King & bishop vs King / King & Knight vs King
        if len(pieces) == 3:
            for piece in pieces:
                if piece.is_bishop() or piece.is_knight():
                    return True
        # King & bishop vs King & bishop of same color
        bishops_count = 0
        first_bishop_square_color = None
        if len(pieces) == 4:
            for piece in pieces:
                if piece.is_bishop() and bishops_count == 0:
                    bishops_count = 1
                    first_bishop_square_color = self.pieces_positions[piece].get_color()
                elif piece.is_bishop and bishops_count == 1 \
                        and self.pieces_positions[piece].get_color() == first_bishop_square_color:
                    return True
        return False

    def update_legal_moves(self):
        pieces_list = list(self.pieces_positions.keys())
        for piece in pieces_list:
            self.compute_legal_moves(piece)

    def update_controlled_squares(self):
        for piece in self.pieces_positions.keys():
            self.compute_controlled_squares(piece)

    def compute_pseudo_legal_moves(self, piece):
        origin_square = self.pieces_positions[piece]
        pseudo_legal_moves = []
        if piece.is_king():
            pseudo_legal_moves = utils.king_squares(piece, origin_square, self.squares, self)
        if piece.is_pawn():
            pseudo_legal_moves = utils.pawn_squares(piece, origin_square, self.squares, self.latest_move)
        if piece.is_bishop():
            pseudo_legal_moves = utils.bishop_squares(piece, origin_square, self.squares)
        if piece.is_rook():
            pseudo_legal_moves = utils.rook_squares(piece, origin_square, self.squares)
        if piece.is_queen():
            pseudo_legal_moves = utils.queen_squares(piece, origin_square, self.squares)
        if piece.is_knight():
            pseudo_legal_moves = utils.knight_squares(piece, origin_square, self.squares)
        return pseudo_legal_moves

    def compute_legal_moves(self, piece):
        self.legal_moves[piece] = []
        # Pieces cannot be moved if it's not their turn
        if not piece.color == self.color_to_move:
            return self.legal_moves[piece]
        pseudo_legal_moves = self.compute_pseudo_legal_moves(piece)
        for item in pseudo_legal_moves:
            destination_square_coordinates = item[:2]
            original_controlled_squares = utils.dict_copy(self.controlled_squares)
            # Make the temporary move
            # Free the origin square
            square = self.pieces_positions[piece]
            self.squares[(square.rank, square.file)].empty_content()
            # If it's a capture, remove the captured piece
            captured_piece = None
            is_capture = not self.squares[destination_square_coordinates].is_free()
            if is_capture:
                captured_piece = self.squares[destination_square_coordinates].content
                self.pieces_positions.pop(captured_piece)
                self.controlled_squares[captured_piece.color][captured_piece] = []
            is_en_passant = piece.is_pawn() and square.file != item[1] and not is_capture
            if is_en_passant:
                captured_piece = self.squares[square.rank, item[1]].content
                self.pieces_positions.pop(captured_piece)
                self.controlled_squares[captured_piece.color][captured_piece] = []
                self.squares[square.rank, item[1]].empty_content()
            is_pawn_promotion = len(item) == 3
            if is_pawn_promotion:
                piece.promote(item[2])
            # Fill the destination square
            self.squares[destination_square_coordinates].content = piece
            self.pieces_positions[piece] = self.squares[destination_square_coordinates]
            # Update controlled squares
            self.update_controlled_squares()
            # Find the king of the piece color and determine if it's in check
            for each_piece in self.pieces_positions.keys():
                if each_piece.color == piece.color and each_piece.is_king()\
                        and not self.is_in_check(each_piece):
                    self.legal_moves[piece].append(item)
                    break
            # Go back to previous position
            self.squares[(square.rank, square.file)].content = piece
            if is_capture:
                self.squares[destination_square_coordinates].content = captured_piece
                self.pieces_positions[captured_piece] = self.squares[destination_square_coordinates]
            else:
                self.squares[destination_square_coordinates].empty_content()
            if is_en_passant:
                self.squares[square.rank, item[1]].content = captured_piece
                self.pieces_positions[captured_piece] = self.squares[square.rank, item[1]]
            if is_pawn_promotion:
                piece.type = PieceType.PAWN
            self.pieces_positions[piece] = square
            self.controlled_squares = original_controlled_squares
        return self.legal_moves[piece]

    def compute_controlled_squares(self, piece):
        origin_square = self.pieces_positions[piece]
        if piece.color not in self.controlled_squares:
            self.controlled_squares[piece.color] = dict()
        if piece.is_pawn():
            self.controlled_squares[piece.color][piece] = \
                utils.pawn_controlled_squares(piece, self.pieces_positions[piece])
        elif piece.is_bishop():
            self.controlled_squares[piece.color][piece] =\
                utils.bishop_controlled_squares(origin_square, self.squares)
        elif piece.is_rook():
            self.controlled_squares[piece.color][piece] =\
                utils.rook_controlled_squares(origin_square, self.squares)
        elif piece.is_queen():
            self.controlled_squares[piece.color][piece] = \
                utils.queen_controlled_squares(origin_square, self.squares)
        elif piece.is_knight():
            self.controlled_squares[piece.color][piece] = \
                utils.knight_controlled_squares(origin_square)
        else:
            self.controlled_squares[piece.color][piece] = utils.king_controlled_squares(origin_square)

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

    def legal_moves_list(self):
        result = []
        for piece in self.legal_moves.keys():
            if piece.color == self.color_to_move:
                for item in self.legal_moves[piece]:
                    result.append(Move(self.pieces_positions[piece], piece, self.squares[item[:2]]))
        return result
