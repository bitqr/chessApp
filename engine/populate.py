import psycopg2
import os

from internal.Color import Color
from internal.Game import Game

FILE_INDEX = 1
START_GAME_INDEX = 0
END_GAME_INDEX = 30000
FILES_TO_READ = [
    'ficsgamesdb_2017_CvC_nomovetimes_199240',
    'ficsgamesdb_2018_CvC_nomovetimes_199241',
    'ficsgamesdb_2019_CvC_nomovetimes_199242',
    'ficsgamesdb_2020_CvC_nomovetimes_199243',
    'ficsgamesdb_2018_standard2000_nomovetimes_199245',
    'ficsgamesdb_2019_standard2000_nomovetimes_199246',
    'ficsgamesdb_2020_standard2000_nomovetimes_199247'
]
PREFIX_PATH = '../resources/games_database'

USER = 'abdel'
PASSWORD = 'chessapp'
HOST = 'localhost'
PORT = '5432'
DATABASE = 'bestMoves'


def create_database():
    connection = psycopg2.connect(dbname=DATABASE, user=USER, host=HOST, password=PASSWORD)
    cursor = connection.cursor()
    cursor.execute('CREATE TABLE Moves (Position varchar(100), Move varchar(10),'
                   ' GamesCount int, WinsCount int, LossesCount int, DrawsCount int, PRIMARY KEY(Position, Move));')
    cursor.close()
    connection.commit()
    connection.close()


def populate_database(file, saving_frequency):
    connection = psycopg2.connect(dbname=DATABASE, user=USER, host=HOST, password=PASSWORD)
    cursor = connection.cursor()
    game_iteration = 1
    for line in file:
        if START_GAME_INDEX < game_iteration < END_GAME_INDEX:
            # Each line is a game
            moves_pgn_list = line.split(' ')
            # 1 -> White wins, -1 -> Black wins, 0 -> Draw
            result = 0 if '1/2-1/2' in moves_pgn_list[len(moves_pgn_list) - 1] else \
                1 if '1-0' in moves_pgn_list[len(moves_pgn_list) - 1] else -1
            print('Game #{0}'.format(game_iteration))
            game = Game()
            pgn_move_index = 0
            while not game.is_over():
                color_to_move = game.board.position.color_to_move
                if moves_pgn_list[pgn_move_index][0] == '{':
                    if 'ran' in moves_pgn_list[pgn_move_index:] \
                            or 'drawn' in moves_pgn_list[pgn_move_index:] \
                            or 'material}' in moves_pgn_list[pgn_move_index:]:
                        game.apply_draw()
                    if 'resigns}' in moves_pgn_list[pgn_move_index:] or 'forfeits' in moves_pgn_list[pgn_move_index:]:
                        game.apply_resign()
                    break
                if pgn_move_index % 3 == 0:
                    pgn_move_index += 1
                played_move = game.read_pgn_move(moves_pgn_list[pgn_move_index])
                # Here, insert this new item in the database
                field_to_update = 'DrawsCount'
                fen_position = ' '.join(game.board.fen_position.split(' ')[:4])
                inserted_row = "('{0}','{1}',1,".format(fen_position, moves_pgn_list[pgn_move_index])
                if (color_to_move == Color.WHITE and result == 1) or (color_to_move == Color.BLACK and result == -1):
                    field_to_update = 'WinsCount'
                    inserted_row += '1,0,0)'
                elif (color_to_move == Color.WHITE and result == -1) or (color_to_move == Color.BLACK and result == 1):
                    field_to_update = 'LossesCount'
                    inserted_row += '0,1,0)'
                else:
                    inserted_row += '0,0,1)'
                to_execute = 'INSERT INTO Moves VALUES {0} ON CONFLICT (Position, Move) DO UPDATE SET GamesCount = ' \
                             "Moves.GamesCount + 1, {1} = Moves.{1} + 1 WHERE Moves.Position = '{2}';"\
                    .format(inserted_row, field_to_update, fen_position)
                cursor.execute(to_execute)
                game.board.apply_move(played_move, log=False)
                pgn_move_index += 1
            if game_iteration % saving_frequency == 0:
                connection.commit()
        game_iteration += 1
    cursor.close()
    connection.commit()
    connection.close()


# create_database()
file_to_read = open(os.path.join(PREFIX_PATH, FILES_TO_READ[FILE_INDEX] + '.pgn'), 'r')
populate_database(file_to_read, saving_frequency=100)
file_to_read.close()
