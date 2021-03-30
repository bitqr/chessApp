from engine import utils
from internal.Game import Game
from internal.PieceType import PieceType

fen_position = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
game = Game(fen_position)
moves = game.board.position.legal_moves_list()

output_vector = utils.from_move_to_output(moves[0])
assert len(output_vector) == 4164
assert sum(output_vector) == 1.
move_index = utils.origin_destination_couple_to_index(
    moves[0].origin_square.rank,
    moves[0].origin_square.file,
    moves[0].destination_square.rank,
    moves[0].destination_square.file
)
assert output_vector[move_index] == 1.
obtained_move = utils.from_neural_network_output_to_move(game, output_vector)
assert (obtained_move.origin_square.rank, obtained_move.origin_square.file) == (6, 0)
assert (obtained_move.destination_square.rank, obtained_move.destination_square.file) == (5, 0)
assert not obtained_move.is_promotion

fen_position = '8/P3pk1p/3p2p1/r4p2/8/4b2B/4P1KP/1R6 w - - 0 34'
game = Game(fen_position)
moves = game.board.position.legal_moves_list()

# moves[0] is a promotion to a Knight ((1,0) --> (0,0))
output_vector = utils.from_move_to_output(moves[0])
assert len(output_vector) == 4164
assert sum(output_vector) == 1.
assert output_vector[4032] == 1.
obtained_move = utils.from_neural_network_output_to_move(game, output_vector)
assert (obtained_move.origin_square.rank, obtained_move.origin_square.file) == (1, 0)
assert (obtained_move.destination_square.rank, obtained_move.destination_square.file) == (0, 0)
assert obtained_move.is_promotion
assert obtained_move.promoted_piece_type == PieceType.KNIGHT

# moves[1] is a promotion to a Bishop ((1,0) --> (0,0))
output_vector = utils.from_move_to_output(moves[1])
assert len(output_vector) == 4164
assert sum(output_vector) == 1.
assert output_vector[4033] == 1.
obtained_move = utils.from_neural_network_output_to_move(game, output_vector)
assert (obtained_move.origin_square.rank, obtained_move.origin_square.file) == (1, 0)
assert (obtained_move.destination_square.rank, obtained_move.destination_square.file) == (0, 0)
assert obtained_move.is_promotion
assert obtained_move.promoted_piece_type == PieceType.BISHOP

# moves[2] is a promotion to a Rook ((1,0) --> (0,0))
output_vector = utils.from_move_to_output(moves[2])
assert len(output_vector) == 4164
assert sum(output_vector) == 1.
assert output_vector[4034] == 1.
obtained_move = utils.from_neural_network_output_to_move(game, output_vector)
assert (obtained_move.origin_square.rank, obtained_move.origin_square.file) == (1, 0)
assert (obtained_move.destination_square.rank, obtained_move.destination_square.file) == (0, 0)
assert obtained_move.is_promotion
assert obtained_move.promoted_piece_type == PieceType.ROOK


# moves[3] is a promotion to a Queen ((1,0) --> (0,0)), it is then the default move, based on the squares coordinates
output_vector = utils.from_move_to_output(moves[3])
assert len(output_vector) == 4164
assert sum(output_vector) == 1.
move_index = utils.origin_destination_couple_to_index(
    moves[3].origin_square.rank,
    moves[3].origin_square.file,
    moves[3].destination_square.rank,
    moves[3].destination_square.file
)
assert output_vector[move_index] == 1.
obtained_move = utils.from_neural_network_output_to_move(game, output_vector)
assert (obtained_move.origin_square.rank, obtained_move.origin_square.file) == (1, 0)
assert (obtained_move.destination_square.rank, obtained_move.destination_square.file) == (0, 0)
assert obtained_move.is_promotion
assert obtained_move.promoted_piece_type == PieceType.QUEEN


# Test with black pawn promotion
fen_position = '8/P3pk1p/3p2p1/5p2/8/4b2B/4p1KP/1R6 b - - 0 34'
game = Game(fen_position)
moves = game.board.position.legal_moves_list()

# moves[24] is a promotion to a Knight ((6,4) --> (7,4))
output_vector = utils.from_move_to_output(moves[24])
assert len(output_vector) == 4164
assert sum(output_vector) == 1.
assert output_vector[4032+3*(22+12)] == 1.
obtained_move = utils.from_neural_network_output_to_move(game, output_vector)
assert (obtained_move.origin_square.rank, obtained_move.origin_square.file) == (6, 4)
assert (obtained_move.destination_square.rank, obtained_move.destination_square.file) == (7, 4)
assert obtained_move.is_promotion
assert obtained_move.promoted_piece_type == PieceType.KNIGHT


# moves[25] is a promotion to a Bishop ((6,4) --> (7,4))
output_vector = utils.from_move_to_output(moves[25])
assert len(output_vector) == 4164
assert sum(output_vector) == 1.
assert output_vector[4032+3*(22+12)+1] == 1.
obtained_move = utils.from_neural_network_output_to_move(game, output_vector)
assert (obtained_move.origin_square.rank, obtained_move.origin_square.file) == (6, 4)
assert (obtained_move.destination_square.rank, obtained_move.destination_square.file) == (7, 4)
assert obtained_move.is_promotion
assert obtained_move.promoted_piece_type == PieceType.BISHOP

# moves[26] is a promotion to a Rook ((6,4) --> (7,4))
output_vector = utils.from_move_to_output(moves[26])
assert len(output_vector) == 4164
assert sum(output_vector) == 1.
assert output_vector[4032+3*(22+12)+2] == 1.
obtained_move = utils.from_neural_network_output_to_move(game, output_vector)
assert (obtained_move.origin_square.rank, obtained_move.origin_square.file) == (6, 4)
assert (obtained_move.destination_square.rank, obtained_move.destination_square.file) == (7, 4)
assert obtained_move.is_promotion
assert obtained_move.promoted_piece_type == PieceType.ROOK

# moves[27] is a promotion to a Queen ((6,4) --> (7,4))
output_vector = utils.from_move_to_output(moves[27])
assert len(output_vector) == 4164
assert sum(output_vector) == 1.
move_index = utils.origin_destination_couple_to_index(
    moves[27].origin_square.rank,
    moves[27].origin_square.file,
    moves[27].destination_square.rank,
    moves[27].destination_square.file
)
assert output_vector[move_index] == 1.
obtained_move = utils.from_neural_network_output_to_move(game, output_vector)
assert (obtained_move.origin_square.rank, obtained_move.origin_square.file) == (6, 4)
assert (obtained_move.destination_square.rank, obtained_move.destination_square.file) == (7, 4)
assert obtained_move.is_promotion
assert obtained_move.promoted_piece_type == PieceType.QUEEN

fen_position = '8/P3pk1p/3p2p1/5p2/8/4b2B/4p1KP/1R3Q2 b - - 0 34'
game = Game(fen_position)
moves = game.board.position.legal_moves_list()

# moves[30] is an under-promotion move: (6,4) --> (7,5) promoted to a Rook
output_vector = utils.from_move_to_output(moves[30])
assert len(output_vector) == 4164
assert sum(output_vector) == 1.
assert output_vector[4032+3*(22+13)+2] == 1.
obtained_move = utils.from_neural_network_output_to_move(game, output_vector)
assert (obtained_move.origin_square.rank, obtained_move.origin_square.file) == (6, 4)
assert (obtained_move.destination_square.rank, obtained_move.destination_square.file) == (7, 5)
assert obtained_move.is_promotion
assert obtained_move.promoted_piece_type == PieceType.ROOK

# moves[18] is a bishop slide from (5,4) to (1,0)
output_vector = utils.from_move_to_output(moves[18])
assert len(output_vector) == 4164
assert sum(output_vector) == 1.
move_index = utils.origin_destination_couple_to_index(
    moves[18].origin_square.rank,
    moves[18].origin_square.file,
    moves[18].destination_square.rank,
    moves[18].destination_square.file
)
assert output_vector[move_index] == 1.
obtained_move = utils.from_neural_network_output_to_move(game, output_vector)
assert (obtained_move.origin_square.rank, obtained_move.origin_square.file) == (5, 4)
assert (obtained_move.destination_square.rank, obtained_move.destination_square.file) == (1, 0)
assert not obtained_move.is_promotion
