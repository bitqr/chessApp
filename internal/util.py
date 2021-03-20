from internal.Color import Color
from internal.PieceType import PieceType


def piece_color_to_string(piece_color):
    return 'White' if piece_color == Color.WHITE else 'Black'


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


def king_squares(piece, square, all_squares):
    result = []
    for rank in range(max(0, square.rank - 1), min(7, square.rank + 1) + 1):
        for file in range(max(0, square.file - 1), min(7, square.file + 1) + 1):
            if not all_squares[(rank, file)].contains_friendly_piece(piece):
                result.append((rank, file))
    return result


def pawn_squares(piece, square, all_squares):
    rank = square.rank + piece.opponent_direction()
    if is_out_of_range(rank):
        return []
    result = []
    if all_squares[(rank, square.file)].is_free():
        result.append((rank, square.file))
    if piece.never_moved and all_squares[(rank + piece.opponent_direction(), square.file)].is_free():
        result.append((rank + piece.opponent_direction(), square.file))
    if not is_out_of_range(square.file - 1) and all_squares[(rank, square.file - 1)].contains_opponent_piece(piece):
        result.append((rank, square.file - 1))
    if not is_out_of_range(square.file + 1) and all_squares[(rank, square.file + 1)].contains_opponent_piece(piece):
        result.append((rank, square.file + 1))
    return result


def bishop_squares(piece, square, all_squares):
    result = []
    for delta in range(1, 8):
        coordinates = (square.rank + delta, square.file + delta)
        if is_out_of_board(coordinates[0], coordinates[1]) or not all_squares[coordinates].is_free():
            if not is_out_of_board(coordinates[0], coordinates[1]) \
                    and all_squares[coordinates].content.color != piece.color:
                result.append(coordinates)
            break
        result.append(coordinates)
    for delta in range(1, 8):
        coordinates = (square.rank - delta, square.file - delta)
        if is_out_of_board(coordinates[0], coordinates[1]) or not all_squares[coordinates].is_free():
            if not is_out_of_board(coordinates[0], coordinates[1]) \
                    and all_squares[coordinates].content.color != piece.color:
                result.append(coordinates)
            break
        result.append(coordinates)
    for delta in range(1, 8):
        coordinates = (square.rank - delta, square.file + delta)
        if is_out_of_board(coordinates[0], coordinates[1]) or not all_squares[coordinates].is_free():
            if not is_out_of_board(coordinates[0], coordinates[1]) \
                    and all_squares[coordinates].content.color != piece.color:
                result.append(coordinates)
            break
        result.append(coordinates)
    for delta in range(1, 8):
        coordinates = (square.rank + delta, square.file - delta)
        if is_out_of_board(coordinates[0], coordinates[1]) or not all_squares[coordinates].is_free():
            if not is_out_of_board(coordinates[0], coordinates[1]) \
                    and all_squares[coordinates].content.color != piece.color:
                result.append(coordinates)
            break
        result.append(coordinates)
    return result


def rook_squares(piece, square, all_squares):
    result = []
    for rank in range(square.rank + 1, 8):
        if not all_squares[(rank, square.file)].is_free():
            if all_squares[(rank, square.file)].content.color != piece.color:
                result.append((rank, square.file))
            break
        result.append((rank, square.file))
    for rank in range(square.rank - 1, -1, -1):
        if not all_squares[(rank, square.file)].is_free():
            if all_squares[(rank, square.file)].content.color != piece.color:
                result.append((rank, square.file))
            break
        result.append((rank, square.file))
    for file in range(square.file + 1, 8):
        if not all_squares[(square.rank, file)].is_free():
            if all_squares[(square.rank, file)].content.color != piece.color:
                result.append((square.rank, file))
            break
        result.append((square.rank, file))
    for file in range(square.file - 1, -1, -1):
        if not all_squares[(square.rank, file)].is_free():
            if all_squares[(square.rank, file)].content.color != piece.color:
                result.append((square.rank, file))
            break
        result.append((square.rank, file))
    return result


def queen_squares(piece, square, all_squares):
    result = rook_squares(piece, square, all_squares)
    result.extend(bishop_squares(piece, square, all_squares))
    return result


def knight_squares(piece, square, all_squares):
    result = []
    if not is_out_of_board(square.rank - 2, square.file - 1) \
            and not all_squares[(square.rank - 2, square.file - 1)].contains_friendly_piece(piece):
        result.append((square.rank - 2, square.file - 1))
    if not is_out_of_board(square.rank - 2, square.file + 1) \
            and not all_squares[(square.rank - 2, square.file + 1)].contains_friendly_piece(piece):
        result.append((square.rank - 2, square.file + 1))
    if not is_out_of_board(square.rank + 2, square.file + 1) \
            and not all_squares[(square.rank + 2, square.file + 1)].contains_friendly_piece(piece):
        result.append((square.rank + 2, square.file + 1))
    if not is_out_of_board(square.rank + 2, square.file - 1) \
            and not all_squares[(square.rank + 2, square.file - 1)].contains_friendly_piece(piece):
        result.append((square.rank + 2, square.file - 1))
    if not is_out_of_board(square.rank - 1, square.file - 2) \
            and not all_squares[(square.rank - 1, square.file - 2)].contains_friendly_piece(piece):
        result.append((square.rank - 1, square.file - 2))
    if not is_out_of_board(square.rank - 1, square.file + 2) \
            and not all_squares[(square.rank - 1, square.file + 2)].contains_friendly_piece(piece):
        result.append((square.rank - 1, square.file + 2))
    if not is_out_of_board(square.rank + 1, square.file + 2) \
            and not all_squares[(square.rank + 1, square.file + 2)].contains_friendly_piece(piece):
        result.append((square.rank + 1, square.file + 2))
    if not is_out_of_board(square.rank + 1, square.file - 2) \
            and not all_squares[(square.rank + 1, square.file - 2)].contains_friendly_piece(piece):
        result.append((square.rank + 1, square.file - 2))
    return result
