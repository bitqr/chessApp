import numpy

from internal.Move import Move
from internal.PieceType import PieceType


def get_bitboard(board_pieces, piece):
    result = []
    for rank in board_pieces.split('/'):
        for item in rank:
            if item == piece:
                result.append(1)
            else:
                if item.isnumeric():
                    for i in range(int(item)):
                        result.append(0)
                else:
                    result.append(0)
    return result


def get_castling_rights_vector(fen_castling_rights):
    result = []
    for item in ['K', 'Q', 'k', 'q']:
        result.append(1 if item in fen_castling_rights else 0)
    return result


def get_en_passant_square_vector(fen_en_passant_square):
    result = []
    en_passant_binary_representation = bin(en_passant_square_to_int[fen_en_passant_square])[2:]
    for item in range(5 - len(en_passant_binary_representation)):
        result.append(0)
    for digit in en_passant_binary_representation:
        result.append(1 if digit == '1' else 0)
    return result


def get_no_progress_count(fen_no_progress_count):
    no_progress_binary_representation = bin(min(50, int(fen_no_progress_count)))[2:]
    result = []
    for item in range(6 - len(no_progress_binary_representation)):
        result.append(0)
    for digit in no_progress_binary_representation:
        result.append(1 if digit == '1' else 0)
    return result


en_passant_square_to_int = {
    '-': 0,
    'a3': 1,
    'b3': 2,
    'c3': 3,
    'd3': 4,
    'e3': 5,
    'f3': 6,
    'g3': 7,
    'h3': 8,
    'a6': 9,
    'b6': 10,
    'c6': 11,
    'd6': 12,
    'e6': 13,
    'f6': 14,
    'g6': 15,
    'h6': 16,
}


# Given a FEN string, a bitboard of each one of piece type/color is added to the vector (8*8*12 components)
# An additional value vector of 16 bits contains:
# - The color to move (1 bit)
# - The castling rights (4 bits)
# - The en-passant square (17 possible values, either 0 or one of the 16 squares in 3rd and 6ths ranks --> 5 bits)
# - The no-progress count (51 possibles values, between 0 and 50 --> 6 bits)
# Total: 8*8*12 + 16 = 784 bits
def from_fen_to_input_vector(fen_position):
    result = []
    fen_fields = fen_position.split(' ')
    board_pieces = fen_fields[0]
    # For each one of the 12 piece types, build the binary vector
    for piece in ['P', 'N', 'B', 'R', 'Q', 'K', 'p', 'n', 'b', 'r', 'q', 'k']:
        result.extend(get_bitboard(board_pieces, piece))
    # Color to move: 1 bit (0 if 'b', 1 if 'w')
    result.append(0 if fen_fields[1] == 'b' else 1)
    # Castling rights
    result.extend(get_castling_rights_vector(fen_fields[2]))
    # En-passant square: 17 possible values, hard-coded by a dict in utils
    result.extend(get_en_passant_square_vector(fen_fields[3]))
    # No-progress count: A number between 0 and 50, as its 6-bit binary representation
    result.extend(get_no_progress_count(fen_fields[4]))
    return result


# In AlphaZero network, each move is equivalent to a vector of 8*8*73 planes
# The 73 planes are composed of
# - 56 planes of line-wise and diagonal-wise moves, with 7 distance possible values and 8 directions
# - 8 planes of knight moves
# - 9 under-promotion moves: for each piece (knight, bishop, rook), 3 possible directions (straight, and 2 diagonals)
# - A queen promotion move is considered in the 56 planes, as a 1-distance and one among 3 directions
# That would make a vector of 4672 components, which is big
# Another possibility with 4164 components is the following:
# For each pair of distinct squares in the board, add a component for a non-promoting move (64 * 63 = 4032)
# Promoting moves are related to 44 pairs of squares (from rank 7 (resp.2) to rank 8 (resp. 1) in 3 possible directions)
# Each pair of squares have 3 promotion possibilities --> 3 * 44 = 132 (by default, promoted to a queen)
# Total: 4164 components
def from_move_to_output(move):
    result = []
    origin_rank, origin_file = move.origin_square.rank, move.origin_square.file
    destination_rank, destination_file = move.destination_square.rank, move.destination_square.file
    result.extend(numpy.zeros(63 * 64))
    if not move.is_promotion or move.promoted_piece_type == PieceType.QUEEN:
        result[origin_destination_couple_to_index(origin_rank, origin_file, destination_rank, destination_file)] = 1.
    # Under-promotion moves
    under_promotion_components = numpy.zeros(132)
    if move.is_promotion and move.promoted_piece_type != PieceType.QUEEN:
        output_index = promotion_to_output_index[(origin_rank, origin_file, destination_rank, destination_file)] \
            if (origin_rank, origin_file, destination_rank, destination_file) in promotion_to_output_index \
            else 22 + promotion_to_output_index[
                (7 - origin_rank, origin_file, 7 - destination_rank, destination_file)
            ]
        under_promotion_components[3 * output_index + piece_type_to_offset[move.promoted_piece_type]] = 1.
    result.extend(under_promotion_components)
    return result


def from_neural_network_output_to_move(game, output_vector):
    move_index = output_vector.index(1.)
    if move_index < 4032:
        # Not an under-promotion move
        origin_rank, origin_file, destination_rank, destination_file = index_to_origin_destination_couple(move_index)
        move = Move(
            game.board.squares[(origin_rank, origin_file)],
            game.board.squares[(destination_rank, destination_file)],
            game.board.squares
        )
        # By default, promoted to a queen
        if move.is_promotion:
            move.promoted_piece_type = PieceType.QUEEN
        return move
    # Under-promotion case
    start_index = 4032 if move_index < 4098 else 4098
    # White under-promotion
    (origin_rank, origin_file, destination_rank, destination_file) = \
        reverse_promotion_to_output_index[int((move_index - start_index) / 3)]
    if start_index == 4098:
        origin_rank = 7 - origin_rank
        destination_rank = 7 - destination_rank
    move = Move(
        game.board.squares[(origin_rank, origin_file)],
        game.board.squares[(destination_rank, destination_file)],
        game.board.squares
    )
    move.promoted_piece_type = reverse_piece_type_to_offset[(move_index - start_index) % 3]
    return move


promotion_to_output_index = {
    (1, 0, 0, 0): 0,
    (1, 0, 0, 1): 1,
    (1, 1, 0, 0): 2,
    (1, 1, 0, 1): 3,
    (1, 1, 0, 2): 4,
    (1, 2, 0, 1): 5,
    (1, 2, 0, 2): 6,
    (1, 2, 0, 3): 7,
    (1, 3, 0, 2): 8,
    (1, 3, 0, 3): 9,
    (1, 3, 0, 4): 10,
    (1, 4, 0, 3): 11,
    (1, 4, 0, 4): 12,
    (1, 4, 0, 5): 13,
    (1, 5, 0, 4): 14,
    (1, 5, 0, 5): 15,
    (1, 5, 0, 6): 16,
    (1, 6, 0, 5): 17,
    (1, 6, 0, 6): 18,
    (1, 6, 0, 7): 19,
    (1, 7, 0, 6): 20,
    (1, 7, 0, 7): 21
}

reverse_promotion_to_output_index = {
    0: (1, 0, 0, 0),
    1: (1, 0, 0, 1),
    2: (1, 1, 0, 0),
    3: (1, 1, 0, 1),
    4: (1, 1, 0, 2),
    5: (1, 2, 0, 1),
    6: (1, 2, 0, 2),
    7: (1, 2, 0, 3),
    8: (1, 3, 0, 2),
    9: (1, 3, 0, 3),
    10: (1, 3, 0, 4),
    11: (1, 4, 0, 3),
    12: (1, 4, 0, 4),
    13: (1, 4, 0, 5),
    14: (1, 5, 0, 4),
    15: (1, 5, 0, 5),
    16: (1, 5, 0, 6),
    17: (1, 6, 0, 5),
    18: (1, 6, 0, 6),
    19: (1, 6, 0, 7),
    20: (1, 7, 0, 6),
    21: (1, 7, 0, 7)
}

piece_type_to_offset = {
    PieceType.KNIGHT: 0,
    PieceType.BISHOP: 1,
    PieceType.ROOK: 2
}

reverse_piece_type_to_offset = {
    0: PieceType.KNIGHT,
    1: PieceType.BISHOP,
    2: PieceType.ROOK
}


def coordinates_to_index(rank, file):
    return rank * 8 + file


def origin_destination_couple_to_index(origin_rank, origin_file, destination_rank, destination_file):
    return coordinates_to_index(origin_rank, origin_file) * 63 \
           + coordinates_to_index(destination_rank, destination_file)


def index_to_origin_destination_couple(move_index):
    origin_index = int(move_index / 63)
    destination_index = move_index % 63
    return int(origin_index / 8), origin_index % 8, int(destination_index / 8), destination_index % 8
