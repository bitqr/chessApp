import os.path

import keras as keras
import numpy


from engine.NeuralNetwork import NeuralNetwork
from engine.utils import from_fen_to_input_vector, from_move_to_output_index
from internal.Game import Game
from internal.utils import game_result_to_string

FILE_INDEX = 1
START_GAME_INDEX = 0
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


def pre_process_data():
    for file_name in FILES_TO_READ:
        file = open(os.path.join(PREFIX_PATH, file_name + '.pgn',), 'r')
        output_file = open(os.path.join(PREFIX_PATH, file_name + '_proc.pgn'), 'w')
        for line in file:
            if line[:2] == '1.':
                output_file.write(line)
        file.close()
        output_file.close()


# pre_process_data()

# Each line in the files is a game pgn

def train_model(neural_net, file, saving_frequency):
    game_iteration = 1
    for line in file:
        test_game = Game()
        if game_iteration > START_GAME_INDEX:
            print('Game #{0}'.format(game_iteration))
            ins, policy_output, score_output = play_database_game(test_game, line)
            # (state, policy, value) data are used to train the neural network and improve its prediction
            neural_net.update(ins, policy_output, score_output)
            # Save the model on the disk
            if game_iteration % saving_frequency == 0:
                neural_network.save_model('../resources/model_parameters/trained_model')
        game_iteration += 1
    neural_network.save_model('../resources/model_parameters/trained_model')


def read_move(game, pgn_move):
    chosen_move = game.read_pgn_move(pgn_move)
    policy_vector = numpy.zeros(4164)
    policy_vector[from_move_to_output_index(chosen_move)] = 1.
    return chosen_move, policy_vector


def play_database_game(game, game_pgn=''):
    inputs = []
    policy_outputs = []
    score_outputs = []
    color_to_play = game.board.position.color_to_move
    moves_pgn_list = game_pgn.split(' ')
    pgn_move_index = 0

    while not game.is_over():
        if moves_pgn_list[pgn_move_index][0] == '{':
            if 'ran' in moves_pgn_list[pgn_move_index:] \
                    or 'drawn' in moves_pgn_list[pgn_move_index:] or 'material}' in moves_pgn_list[pgn_move_index:]:
                game.apply_draw()
            if 'resigns}' in moves_pgn_list[pgn_move_index:] or 'forfeits' in moves_pgn_list[pgn_move_index:]:
                game.apply_resign()
            break
        if pgn_move_index % 3 == 0:
            pgn_move_index += 1
        input_vector = from_fen_to_input_vector(game.board.fen_position)
        played_move, policy_vector = read_move(game, moves_pgn_list[pgn_move_index])
        inputs.append(input_vector)
        policy_outputs.append(policy_vector)
        game.board.apply_move(played_move)
        pgn_move_index += 1
    print(game_result_to_string[game.result])

    # Update the board evaluations with the expected outcomes. Variable index is
    # to denote playing color, to determine perspective for evaluation of the position
    score = game.get_score(color_to_play)
    for index in range(len(inputs)):
        score_outputs.append(score if index % 2 == 0 else -score)
    return inputs, policy_outputs, score_outputs


file_to_read = open(os.path.join(PREFIX_PATH, FILES_TO_READ[FILE_INDEX] + '.pgn'), 'r')
neural_net_model = keras.models.load_model('../resources/model_parameters/trained_model')
neural_network = NeuralNetwork(neural_net_model)
train_model(neural_network, file_to_read, saving_frequency=1000)
file_to_read.close()
