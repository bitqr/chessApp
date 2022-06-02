import random

from tensorflow import keras

import settings
import utils
from Engine import Engine
from AlphaBetaPruningEngine import AlphaBetaPruningEngine
from NeuralNetwork import NeuralNetwork
from internal.Color import Color
from internal.Game import Game


# Self-play game via MCTS
def mcts_self_play(game, engine):
    inputs = []
    policy_outputs = []
    score_outputs = []
    color_to_play = game.board.position.color_to_move

    while not game.is_over():
        input_vector = utils.from_fen_to_input_vector(game.board.fen_position)
        # One run of MCTS, returning the move and the (p, v) vector associated to the game state
        played_move, mcts_adapted_policy_vector = engine.run_mcts(game)
        inputs.append(input_vector)
        policy_outputs.append(mcts_adapted_policy_vector)
        game.board.apply_move(played_move)
        if game.can_be_drawn():
            game.apply_draw()
            print('Draw')

    # Update the board evaluations with the expected outcomes. Variable index is
    # to denote playing color, to determine perspective for evaluation of the position
    score = game.get_score(color_to_play)
    for index in range(len(inputs)):
        score_outputs.append(score if index % 2 == 0 else -score)
    return inputs, policy_outputs, score_outputs


# Self-play game via MCTS
def play_against_greedy(game, engine, engine_color):
    inputs = []
    policy_outputs = []
    score_outputs = []
    greedy_engine = AlphaBetaPruningEngine(Color.BLACK if engine_color == Color.WHITE else Color.WHITE)
    while not game.is_over():
        if game.board.position.color_to_move == engine_color:
            # Engine to play, use MCTS
            input_vector = utils.from_fen_to_input_vector(game.board.fen_position)
            # One run of MCTS, returning the move and the (p, v) vector associated to the game state
            played_move, mcts_adapted_policy_vector = engine.run_mcts(game)
            inputs.append(input_vector)
            policy_outputs.append(mcts_adapted_policy_vector)
        else:
            # Greedy to play, use intermediate engine move
            played_move = greedy_engine.choose_move(game)
        game.board.apply_move(played_move)
        if game.can_be_drawn():
            game.apply_draw()

    print_game_status(game, engine_color)
    # Update the board evaluations with the expected outcomes. Variable index is
    # to denote playing color, to determine perspective for evaluation of the position
    score = game.get_score(engine_color)
    for _ in range(len(inputs)):
        score_outputs.append(score)
    return inputs, policy_outputs, score_outputs


def print_game_status(game, engine_color):
    if game.is_draw():
        print("Draw")
    if game.white_wins():
        if engine_color == Color.WHITE:
            print("White (NN) wins")
        else:
            print("White wins")
    if game.black_wins():
        if engine_color == Color.BLACK:
            print("Black (engine) wins")
        else:
            print("Black wins")


def train_model(neural_net, greedy=False, engine_color=Color.WHITE):
    # Load the neural network that MCTS will use to run its simulations
    test_game = Game()
    test_engine = Engine(neural_net)

    if greedy:
        ins, policy_output, score_output = play_against_greedy(test_game, test_engine, engine_color)
    else:
        ins, policy_output, score_output = mcts_self_play(test_game, test_engine)

    # (state, policy, value) data are used to train the neural network and improve its prediction
    neural_net.update(ins, policy_output, score_output)


for iteration in range(settings.NUMBER_OF_SELF_PLAY_GAMES):
    neural_net_model = keras.models.load_model('../resources/model_parameters/trained_model')
    neural_network = NeuralNetwork(neural_net_model)
    train_model(neural_network, greedy=False, engine_color=random.choice([Color.BLACK, Color.WHITE]))
    # Save the model on the disk
    neural_network.save_model('../resources/model_parameters/trained_model')
