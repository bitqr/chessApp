from internal.Color import Color
from internal.GameResult import GameResult
from internal.Move import Move
from internal.PieceType import PieceType

KING_FILE = 4
CHESSBOARD_FILE_NAMES = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
game_result_to_string = {
    GameResult.WHITE_WINS_BY_CHECKMATE: 'Checkmate! White wins!',
    GameResult.BLACK_WINS_BY_CHECKMATE: 'Checkmate! Black wins!',
    GameResult.WHITE_WINS_BY_RESIGNATION: 'Black resigned! White wins!',
    GameResult.BLACK_WINS_BY_RESIGNATION: 'White resigned! Black wins!',
    GameResult.DRAW_BY_MOVE_REPEAT: 'Draw by move repeat!',
    GameResult.DRAW_BY_STALEMATE: 'Draw by stalemate!',
    GameResult.DRAW_BY_MUTUAL_AGREEMENT: 'Players agreed on a draw!',
    GameResult.WHITE_WINS_ON_TIME: 'Time out for Black! White wins!',
    GameResult.BLACK_WINS_ON_TIME: 'Time out for White! Black wins!',
    GameResult.DRAW_BY_DEAD_POSITION: 'Draw by dead position!',
    GameResult.DRAW_BY_50_MOVE_RULE: 'Draw by the 50-Move rule!',
    GameResult.UNDEFINED: 'Undefined'
}


def color_to_fen(color):
    return 'w' if color == Color.WHITE else 'b'


def fen_letter_to_color(letter):
    return Color.WHITE if letter == 'w' else Color.BLACK


def piece_color_to_string(piece_color):
    return 'White' if piece_color == Color.WHITE else 'Black'


def string_to_square_coordinates(square_string):
    rank = int(square_string[1]) - 1
    file = CHESSBOARD_FILE_NAMES.index(square_string[0])
    return rank, file


def fen_letter_to_piece(letter):
    piece_type = PieceType.NONE
    piece_color = Color.WHITE if letter.isupper() else Color.BLACK
    if letter.lower() == 'p':
        piece_type = PieceType.PAWN
    if letter.lower() == 'k':
        piece_type = PieceType.KING
    if letter.lower() == 'r':
        piece_type = PieceType.ROOK
    if letter.lower() == 'n':
        piece_type = PieceType.KNIGHT
    if letter.lower() == 'b':
        piece_type = PieceType.BISHOP
    if letter.lower() == 'q':
        piece_type = PieceType.QUEEN
    return piece_type, piece_color


def compute_castling_rook_move(move, squares):
    rook_square = squares[(move.destination_square.rank, 7)] if move.destination_square.file == 6 \
        else squares[(move.destination_square.rank, 0)]
    rook_destination_file = 5 if move.destination_square.file == 6 else 3
    rook_destination_square = squares[(move.destination_square.rank, rook_destination_file)]
    return Move(rook_square, rook_destination_square, squares)


def piece_type_to_string(piece_type):
    if piece_type == PieceType.PAWN:
        return 'Pawn'
    if piece_type == PieceType.KNIGHT:
        return 'Knight'
    if piece_type == PieceType.BISHOP:
        return 'Bishop'
    if piece_type == PieceType.ROOK:
        return 'Rook'
    if piece_type == PieceType.QUEEN:
        return 'Queen'
    if piece_type == PieceType.KING:
        return 'King'
    return 'Nothing'


def is_out_of_range(rank):
    return rank < 0 or 7 < rank


def is_out_of_board(rank, file):
    return is_out_of_range(rank) or is_out_of_range(file)


def initial_piece_positions(piece):
    result = []
    base_rank = 0 if piece.is_black() else 7
    pawn_rank = 1 if piece.is_black() else 6
    if piece.is_pawn():
        for file in range(8):
            result.append((pawn_rank, file))
        return result
    if piece.is_bishop():
        result.append((base_rank, 2))
        result.append((base_rank, 5))
    if piece.is_knight():
        result.append((base_rank, 1))
        result.append((base_rank, 6))
    if piece.is_rook():
        result.append((base_rank, 0))
        result.append((base_rank, 7))
    if piece.is_queen():
        return [(base_rank, 3)]
    if piece.is_king():
        return [(base_rank, 4)]
    return result


def king_squares(king, square, all_squares, position):
    result = []
    for rank in range(max(0, square.rank - 1), min(7, square.rank + 1) + 1):
        for file in range(max(0, square.file - 1), min(7, square.file + 1) + 1):
            if not all_squares[(rank, file)].contains_friendly_piece(king):
                result.append((rank, file))
    # Look for king-side castle
    if king.never_moved \
            and square.file == KING_FILE \
            and all_squares[(square.rank, square.file + 1)].is_free() \
            and not position.is_controlled(square.rank, square.file, king.opposite_color()) \
            and not position.is_controlled(square.rank, square.file + 1, king.opposite_color()) \
            and all_squares[(square.rank, square.file + 2)].is_free() \
            and not position.is_controlled(square.rank, square.file + 2, king.opposite_color()) \
            and all_squares[(square.rank, square.file + 3)].content.is_rook() \
            and all_squares[(square.rank, square.file + 3)].content.never_moved:
        result.append((square.rank, square.file + 2))
    # Look for queen-side castle
    if king.never_moved \
            and square.file == KING_FILE \
            and all_squares[(square.rank, square.file - 1)].is_free() \
            and not position.is_controlled(square.rank, square.file, king.opposite_color()) \
            and not position.is_controlled(square.rank, square.file - 1, king.opposite_color()) \
            and all_squares[(square.rank, square.file - 2)].is_free() \
            and not position.is_controlled(square.rank, square.file - 2, king.opposite_color()) \
            and all_squares[(square.rank, square.file - 3)].is_free() \
            and all_squares[(square.rank, square.file - 4)].content.is_rook() \
            and all_squares[(square.rank, square.file - 4)].content.never_moved:
        result.append((square.rank, square.file - 2))
    return result


def king_controlled_squares(square):
    result = []
    for rank in range(max(0, square.rank - 1), min(7, square.rank + 1) + 1):
        for file in range(max(0, square.file - 1), min(7, square.file + 1) + 1):
            result.append((rank, file))
    return result


def promotion_tuple(square_coordinates):
    result = []
    if square_coordinates[0] in [0, 7]:
        # Pawn promotion
        result.append((square_coordinates[0], square_coordinates[1], PieceType.KNIGHT))
        result.append((square_coordinates[0], square_coordinates[1], PieceType.BISHOP))
        result.append((square_coordinates[0], square_coordinates[1], PieceType.ROOK))
        result.append((square_coordinates[0], square_coordinates[1], PieceType.QUEEN))
    else:
        result = [square_coordinates]
    return result


def pawn_squares(pawn, square, all_squares, latest_move):
    rank = square.rank + pawn.opponent_direction()
    if is_out_of_range(rank):
        return []
    result = []
    if all_squares[(rank, square.file)].is_free():
        result.extend(promotion_tuple((rank, square.file)))
    if pawn.never_moved and all_squares[(rank, square.file)].is_free()\
            and all_squares[(rank + pawn.opponent_direction(), square.file)].is_free():
        result.extend(promotion_tuple((rank + pawn.opponent_direction(), square.file)))
    if not is_out_of_range(square.file - 1) and all_squares[(rank, square.file - 1)].contains_opponent_piece(pawn):
        result.extend(promotion_tuple((rank, square.file - 1)))
    if not is_out_of_range(square.file + 1) and all_squares[(rank, square.file + 1)].contains_opponent_piece(pawn):
        result.extend(promotion_tuple((rank, square.file + 1)))

    # Look for En-Passant
    if latest_move:
        if not is_out_of_range(square.file + 1) \
                and latest_move.destination_square == all_squares[(square.rank, square.file + 1)] \
                and all_squares[(square.rank, square.file + 1)].contains_opponent_pawn(pawn) \
                and latest_move.is_double_pawn_move:
            result.append((rank, square.file + 1))
        if not is_out_of_range(square.file - 1) \
                and latest_move.destination_square == all_squares[(square.rank, square.file - 1)] \
                and all_squares[(square.rank, square.file - 1)].contains_opponent_pawn(pawn) \
                and latest_move.is_double_pawn_move:
            result.append((rank, square.file - 1))
    return result


def pawn_controlled_squares(pawn, square):
    rank = square.rank + pawn.opponent_direction()
    if is_out_of_range(rank):
        return []
    result = []
    if not is_out_of_range(square.file - 1):
        result.append((rank, square.file - 1))
    if not is_out_of_range(square.file + 1):
        result.append((rank, square.file + 1))
    return result


def bishop_squares(bishop, square, all_squares):
    result = []
    for delta in range(1, 8):
        coordinates = (square.rank + delta, square.file + delta)
        if is_out_of_board(coordinates[0], coordinates[1]) or not all_squares[coordinates].is_free():
            if not is_out_of_board(coordinates[0], coordinates[1]) \
                    and all_squares[coordinates].content.color != bishop.color:
                result.append(coordinates)
            break
        result.append(coordinates)
    for delta in range(1, 8):
        coordinates = (square.rank - delta, square.file - delta)
        if is_out_of_board(coordinates[0], coordinates[1]) or not all_squares[coordinates].is_free():
            if not is_out_of_board(coordinates[0], coordinates[1]) \
                    and all_squares[coordinates].content.color != bishop.color:
                result.append(coordinates)
            break
        result.append(coordinates)
    for delta in range(1, 8):
        coordinates = (square.rank - delta, square.file + delta)
        if is_out_of_board(coordinates[0], coordinates[1]) or not all_squares[coordinates].is_free():
            if not is_out_of_board(coordinates[0], coordinates[1]) \
                    and all_squares[coordinates].content.color != bishop.color:
                result.append(coordinates)
            break
        result.append(coordinates)
    for delta in range(1, 8):
        coordinates = (square.rank + delta, square.file - delta)
        if is_out_of_board(coordinates[0], coordinates[1]) or not all_squares[coordinates].is_free():
            if not is_out_of_board(coordinates[0], coordinates[1]) \
                    and all_squares[coordinates].content.color != bishop.color:
                result.append(coordinates)
            break
        result.append(coordinates)
    return result


def bishop_controlled_squares(square, all_squares):
    result = []
    for delta in range(1, 8):
        coordinates = (square.rank + delta, square.file + delta)
        if is_out_of_board(coordinates[0], coordinates[1]) or not all_squares[coordinates].is_free():
            if not is_out_of_board(coordinates[0], coordinates[1]):
                result.append(coordinates)
            break
        result.append(coordinates)
    for delta in range(1, 8):
        coordinates = (square.rank - delta, square.file - delta)
        if is_out_of_board(coordinates[0], coordinates[1]) or not all_squares[coordinates].is_free():
            if not is_out_of_board(coordinates[0], coordinates[1]):
                result.append(coordinates)
            break
        result.append(coordinates)
    for delta in range(1, 8):
        coordinates = (square.rank - delta, square.file + delta)
        if is_out_of_board(coordinates[0], coordinates[1]) or not all_squares[coordinates].is_free():
            if not is_out_of_board(coordinates[0], coordinates[1]):
                result.append(coordinates)
            break
        result.append(coordinates)
    for delta in range(1, 8):
        coordinates = (square.rank + delta, square.file - delta)
        if is_out_of_board(coordinates[0], coordinates[1]) or not all_squares[coordinates].is_free():
            if not is_out_of_board(coordinates[0], coordinates[1]):
                result.append(coordinates)
            break
        result.append(coordinates)
    return result


def rook_squares(rook, square, all_squares):
    result = []
    for rank in range(square.rank + 1, 8):
        if not all_squares[(rank, square.file)].is_free():
            if all_squares[(rank, square.file)].content.color != rook.color:
                result.append((rank, square.file))
            break
        result.append((rank, square.file))
    for rank in range(square.rank - 1, -1, -1):
        if not all_squares[(rank, square.file)].is_free():
            if all_squares[(rank, square.file)].content.color != rook.color:
                result.append((rank, square.file))
            break
        result.append((rank, square.file))
    for file in range(square.file + 1, 8):
        if not all_squares[(square.rank, file)].is_free():
            if all_squares[(square.rank, file)].content.color != rook.color:
                result.append((square.rank, file))
            break
        result.append((square.rank, file))
    for file in range(square.file - 1, -1, -1):
        if not all_squares[(square.rank, file)].is_free():
            if all_squares[(square.rank, file)].content.color != rook.color:
                result.append((square.rank, file))
            break
        result.append((square.rank, file))
    return result


def rook_controlled_squares(square, all_squares):
    result = []
    for rank in range(square.rank + 1, 8):
        result.append((rank, square.file))
        if not all_squares[(rank, square.file)].is_free():
            break
    for rank in range(square.rank - 1, -1, -1):
        result.append((rank, square.file))
        if not all_squares[(rank, square.file)].is_free():
            break
    for file in range(square.file + 1, 8):
        result.append((square.rank, file))
        if not all_squares[(square.rank, file)].is_free():
            break
    for file in range(square.file - 1, -1, -1):
        result.append((square.rank, file))
        if not all_squares[(square.rank, file)].is_free():
            break
    return result


def queen_squares(queen, square, all_squares):
    result = rook_squares(queen, square, all_squares)
    result.extend(bishop_squares(queen, square, all_squares))
    return result


def queen_controlled_squares(square, all_squares):
    result = rook_controlled_squares(square, all_squares)
    result.extend(bishop_controlled_squares(square, all_squares))
    return result


def knight_squares(knight, square, all_squares):
    result = []
    if not is_out_of_board(square.rank - 2, square.file - 1) \
            and not all_squares[(square.rank - 2, square.file - 1)].contains_friendly_piece(knight):
        result.append((square.rank - 2, square.file - 1))
    if not is_out_of_board(square.rank - 2, square.file + 1) \
            and not all_squares[(square.rank - 2, square.file + 1)].contains_friendly_piece(knight):
        result.append((square.rank - 2, square.file + 1))
    if not is_out_of_board(square.rank + 2, square.file + 1) \
            and not all_squares[(square.rank + 2, square.file + 1)].contains_friendly_piece(knight):
        result.append((square.rank + 2, square.file + 1))
    if not is_out_of_board(square.rank + 2, square.file - 1) \
            and not all_squares[(square.rank + 2, square.file - 1)].contains_friendly_piece(knight):
        result.append((square.rank + 2, square.file - 1))
    if not is_out_of_board(square.rank - 1, square.file - 2) \
            and not all_squares[(square.rank - 1, square.file - 2)].contains_friendly_piece(knight):
        result.append((square.rank - 1, square.file - 2))
    if not is_out_of_board(square.rank - 1, square.file + 2) \
            and not all_squares[(square.rank - 1, square.file + 2)].contains_friendly_piece(knight):
        result.append((square.rank - 1, square.file + 2))
    if not is_out_of_board(square.rank + 1, square.file + 2) \
            and not all_squares[(square.rank + 1, square.file + 2)].contains_friendly_piece(knight):
        result.append((square.rank + 1, square.file + 2))
    if not is_out_of_board(square.rank + 1, square.file - 2) \
            and not all_squares[(square.rank + 1, square.file - 2)].contains_friendly_piece(knight):
        result.append((square.rank + 1, square.file - 2))
    return result


def knight_controlled_squares(square):
    result = []
    if not is_out_of_board(square.rank - 2, square.file - 1):
        result.append((square.rank - 2, square.file - 1))
    if not is_out_of_board(square.rank - 2, square.file + 1):
        result.append((square.rank - 2, square.file + 1))
    if not is_out_of_board(square.rank + 2, square.file + 1):
        result.append((square.rank + 2, square.file + 1))
    if not is_out_of_board(square.rank + 2, square.file - 1):
        result.append((square.rank + 2, square.file - 1))
    if not is_out_of_board(square.rank - 1, square.file - 2):
        result.append((square.rank - 1, square.file - 2))
    if not is_out_of_board(square.rank - 1, square.file + 2):
        result.append((square.rank - 1, square.file + 2))
    if not is_out_of_board(square.rank + 1, square.file + 2):
        result.append((square.rank + 1, square.file + 2))
    if not is_out_of_board(square.rank + 1, square.file - 2):
        result.append((square.rank + 1, square.file - 2))
    return result


def dict_copy(target):
    result = dict()
    for color_key in target.keys():
        result[color_key] = dict()
        for piece_key in target[color_key].keys():
            result[color_key][piece_key] = target[color_key][piece_key]
    return result


def is_valid_fen(fen_string):
    return len(fen_string.split(' ')) == 6
