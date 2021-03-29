from internal.Game import Game


def try_checkmate(fen_position, move):
    temporary_game = Game(fen_position)
    temporary_game.board.apply_move(move, log=False)
    return temporary_game.is_over()
