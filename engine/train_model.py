from tensorflow import keras

from engine import utils, settings
from engine.Engine import Engine
from engine.NeuralNetwork import NeuralNetwork
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


def train_model(file_path):
    # Load the neural network that MCTS will use to run its simulations
    model = keras.models.load_model(file_path)
    neural_net = NeuralNetwork(model)
    test_game = Game()
    test_engine = Engine(neural_net)

    ins, policy_output, score_output = mcts_self_play(test_game, test_engine)

    # (state, policy, value) data are used to train the neural network and improve its prediction
    neural_net.update(ins, policy_output, score_output)
    # Save the model on the disk
    neural_net.save_model(file_path)


for iteration in range(settings.NUMBER_OF_SELF_PLAY_GAMES):
    train_model('../../resources/model_parameters/trained_model')
