import psycopg2

from engine import populate
from engine.AlphaBetaPruningEngine import AlphaBetaPruningEngine
from internal.Color import Color


def choose_move_from_db(move_suggestions):
    best_ratio = -1.
    best_move = None
    for suggestion in move_suggestions:
        ratio = suggestion[3] / suggestion[2]
        if ratio > best_ratio:
            best_ratio = ratio
            best_move = suggestion[1]
    return best_move


# The data-driven engine will access the database (DB) at a given position to look for
# all the moves that have been played in that position in the database. Idea: Select the
# move that lead to most victories in that position
# If this position is not on the DB, use the AlphaBetaPruning with high depth
class DataDrivenEngine:

    def __init__(self, color=Color.WHITE):
        self.color = color
        self.connection = psycopg2.connect(
            dbname=populate.DATABASE,
            user=populate.USER,
            host=populate.HOST,
            password=populate.PASSWORD
        )
        self.cursor = self.connection.cursor()
        self.auxiliaryEngine = AlphaBetaPruningEngine(color)

    def close_db_connection(self):
        self.cursor.close()
        self.connection.close()

    def choose_move(self, game):
        fen_position = ' '.join(game.board.fen_position.split(' ')[:4])
        self.cursor.execute("SELECT * FROM Moves WHERE Position = '{0}';".format(fen_position))
        move_suggestions = self.cursor.fetchall()
        if len(move_suggestions) == 0:
            return self.auxiliaryEngine.choose_move(game)
        else:
            # There are proposed legal moves
            pgn_move = choose_move_from_db(move_suggestions)
            return game.read_pgn_move(pgn_move)
