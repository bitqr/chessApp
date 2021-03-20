from internal.PieceType import PieceType
from internal.Color import Color
from internal.Piece import Piece
from internal.Position import Position
from internal.Square import Square


class Board:

    def __init__(self, size):
        self.squares = dict()
        self.size = size
        self.position = Position()
        for rank in range(size):
            for file in range(size):
                self.squares[(rank, file)] = Square(rank, file)
        self.initialize_board()

    def initialize_board(self):
        self.initialize_side(Color.WHITE)
        self.initialize_side(Color.BLACK)

    def initialize_side(self, piece_color):
        base_rank = 0
        pawn_rank = 1
        if piece_color == Color.WHITE:
            base_rank = self.size - 1
            pawn_rank = self.size - 2
        self.put_piece_on_square(Piece(PieceType.ROOK, piece_color), base_rank, 0)
        self.put_piece_on_square(Piece(PieceType.ROOK, piece_color), base_rank, 7,)
        self.put_piece_on_square(Piece(PieceType.KNIGHT, piece_color), base_rank, 1)
        self.put_piece_on_square(Piece(PieceType.KNIGHT, piece_color), base_rank, 6)
        self.put_piece_on_square(Piece(PieceType.BISHOP, piece_color), base_rank, 2)
        self.put_piece_on_square(Piece(PieceType.BISHOP, piece_color), base_rank, 5)
        self.put_piece_on_square(Piece(PieceType.QUEEN, piece_color), base_rank, 3)
        self.put_piece_on_square(Piece(PieceType.KING, piece_color), base_rank, 4)
        for file in range(self.size):
            self.put_piece_on_square(Piece(PieceType.PAWN, piece_color), pawn_rank, file)

    def current_square(self, piece):
        return self.position.pieces_positions[piece]

    def is_move_legal(self, move):
        piece = move.piece
        destination_square = move.square
        if not destination_square.is_free():
            if destination_square.content.color != piece.color:
                square_coordinates = self.position.capturing_squares(piece, self.squares)
                capturing_squares = list(
                    map(lambda coordinates: self.squares[coordinates], square_coordinates)
                )
                return destination_square in capturing_squares
            return False
        square_coordinates = self.position.moving_squares(piece, self.squares)
        moving_squares = list(
            map(lambda coordinates: self.squares[coordinates], square_coordinates)
        )
        return destination_square in moving_squares

    # This method will tell in its return boolean value whether the move is legal AND a capture
    def request_move(self, move):
        is_legal = self.is_move_legal(move)
        is_capture = move.is_capture()
        if is_legal:
            self.apply_move(move)
            return is_capture
        return False

    def apply_move(self, move):
        self.leave_square(move.piece)
        # If the move is a capture, remove the piece on the destination square
        if move.is_capture():
            self.position.pieces_positions.pop(move.square.content)
        self.put_piece_on_square(move.piece, move.square.rank, move.square.file)
        move.piece.never_moved = False

    def leave_square(self, piece):
        current_square = self.position.pieces_positions[piece]
        current_square.empty_content()

    def put_piece_on_square(self, piece, rank, file):
        self.squares[(rank, file)].content = piece
        self.position.update_position(piece, self.squares[(rank, file)])
