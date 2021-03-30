from engine import utils


def display_board(vector):
    res = ''
    iteration = 1
    for element in vector:
        res += '{0} '.format(element)
        if iteration % 8 == 0:
            res += '\n'
        iteration += 1
    return res


fen_position = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'

board_pieces = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR'
print('Black Rook:')
print(display_board(utils.get_bitboard(board_pieces, 'r')))
print('White Rook:')
print(display_board(utils.get_bitboard(board_pieces, 'R')))
print('Black Pawn:')
print(display_board(utils.get_bitboard(board_pieces, 'p')))
print('White Pawn:')
print(display_board(utils.get_bitboard(board_pieces, 'P')))
print('Black Bishop:')
print(display_board(utils.get_bitboard(board_pieces, 'b')))
print('White Bishop:')
print(display_board(utils.get_bitboard(board_pieces, 'B')))
print('Black Knight:')
print(display_board(utils.get_bitboard(board_pieces, 'n')))
print('White Knight:')
print(display_board(utils.get_bitboard(board_pieces, 'N')))
print('Black Queen:')
print(display_board(utils.get_bitboard(board_pieces, 'q')))
print('White Queen:')
print(display_board(utils.get_bitboard(board_pieces, 'Q')))
print('Black King:')
print(display_board(utils.get_bitboard(board_pieces, 'k')))
print('White King:')
print(display_board(utils.get_bitboard(board_pieces, 'K')))

assert utils.get_castling_rights_vector('KQkq') == [1, 1, 1, 1]
assert utils.get_castling_rights_vector('KQ') == [1, 1, 0, 0]
assert utils.get_castling_rights_vector('KQk') == [1, 1, 1, 0]
assert utils.get_castling_rights_vector('kq') == [0, 0, 1, 1]
assert utils.get_castling_rights_vector('q') == [0, 0, 0, 1]
assert utils.get_castling_rights_vector('-') == [0, 0, 0, 0]

assert utils.get_en_passant_square_vector('-') == [0, 0, 0, 0, 0]
assert utils.get_en_passant_square_vector('a3') == [0, 0, 0, 0, 1]
assert utils.get_en_passant_square_vector('e6') == [0, 1, 1, 0, 1]
assert utils.get_en_passant_square_vector('h6') == [1, 0, 0, 0, 0]

assert utils.get_no_progress_count('0') == [0, 0, 0, 0, 0, 0]
assert utils.get_no_progress_count('10') == [0, 0, 1, 0, 1, 0]
assert utils.get_no_progress_count('15') == [0, 0, 1, 1, 1, 1]
assert utils.get_no_progress_count('50') == [1, 1, 0, 0, 1, 0]
assert utils.get_no_progress_count('60') == [1, 1, 0, 0, 1, 0]

result = utils.from_fen_to_input_vector(fen_position)

assert len(result) == 784
assert sum(result) == 37
