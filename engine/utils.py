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


# Each move is equivalent to a vector of 8*8*73 planes
# The 8*8 component is the origin square
# The 73 planes are composed of
# - 56 planes of line-wise and diagonal-wise moves, with 7 distance possible values and 8 directions
# - 8 planes of knight moves
# - 9 under-promotion moves: for each piece (knight, bishop, rook), 3 possible directions (straight, and 2 diagonals)
# - A queen promotion move is considered in the 56 planes, as a 1-distance and one among 3 directions
def from_move_to_output(move):
    pass
