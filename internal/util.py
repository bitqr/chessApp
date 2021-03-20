from internal.Color import Color
from internal.Move import Move
from internal.PieceType import PieceType


def piece_color_to_string(piece_color):
    return 'White' if piece_color == Color.WHITE else 'Black'


def compute_castling_rook_move(move, squares):
    rook = squares[(move.square.rank, 7)].content if move.square.file == 6 \
        else squares[(move.square.rank, 0)].content
    rook_destination_file = 5 if move.square.file == 6 else 3
    rook_destination_square = squares[(move.square.rank, rook_destination_file)]
    return Move(rook, rook_destination_square)


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


def king_squares(king, square, all_squares):
    result = []
    for rank in range(max(0, square.rank - 1), min(7, square.rank + 1) + 1):
        for file in range(max(0, square.file - 1), min(7, square.file + 1) + 1):
            if not all_squares[(rank, file)].contains_friendly_piece(king):
                result.append((rank, file))
    # Look for king-side castle
    if king.never_moved \
            and all_squares[(square.rank, square.file + 1)].is_free() \
            and all_squares[(square.rank, square.file + 2)].is_free()\
            and all_squares[(square.rank, square.file + 3)].content.is_rook() \
            and all_squares[(square.rank, square.file + 3)].content.never_moved:
        result.append((square.rank, square.file + 2))
        pass
    # Look for queen-side castle
    if king.never_moved \
            and all_squares[(square.rank, square.file - 1)].is_free() \
            and all_squares[(square.rank, square.file - 2)].is_free() \
            and all_squares[(square.rank, square.file - 3)].is_free() \
            and all_squares[(square.rank, square.file - 4)].content.is_rook() \
            and all_squares[(square.rank, square.file - 4)].content.never_moved:
        result.append((square.rank, square.file - 2))
    return result


def pawn_squares(pawn, square, all_squares):
    rank = square.rank + pawn.opponent_direction()
    if is_out_of_range(rank):
        return []
    result = []
    if all_squares[(rank, square.file)].is_free():
        result.append((rank, square.file))
    if pawn.never_moved and all_squares[(rank + pawn.opponent_direction(), square.file)].is_free():
        result.append((rank + pawn.opponent_direction(), square.file))
    if not is_out_of_range(square.file - 1) and all_squares[(rank, square.file - 1)].contains_opponent_piece(pawn):
        result.append((rank, square.file - 1))
    if not is_out_of_range(square.file + 1) and all_squares[(rank, square.file + 1)].contains_opponent_piece(pawn):
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


def queen_squares(queen, square, all_squares):
    result = rook_squares(queen, square, all_squares)
    result.extend(bishop_squares(queen, square, all_squares))
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
