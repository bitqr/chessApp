from tensorflow import keras

from engine import utils
from engine.Engine import Engine
from engine.NeuralNetwork import NeuralNetwork
from internal.Color import Color
from internal.Game import Game


# Self-play game via MCTS
def mcts_self_play(game, engine):
    inputs = []
    outputs = []

    while not game.is_over():
        input_vector = utils.from_fen_to_input_vector(game.board.fen_position)
        # One run of MCTS, returning the move and the (p, v) vector associated to the game state
        played_move, probability_vector = engine.run_mcts(game)
        inputs.append(input_vector)
        outputs.append(probability_vector)
        game.board.apply_move(played_move)
        if game.can_be_drawn():
            game.apply_draw()
            print('Draw')

    # Update the board evaluations with the expected outcomes
    score = game.get_score(Color.WHITE)
    index = 0
    for probability_vector in outputs:
        probability_vector[len(probability_vector)-1] = score if index % 2 == 0 else - score
        index += 1
    return inputs, outputs


# Load the neural network that MCTS will use to run its simulations
model = keras.models.load_model('../../resources/model_parameters/example_model')
neural_net = NeuralNetwork(model)
test_game = Game()
test_engine = Engine(neural_net)

ins, outs = mcts_self_play(test_game, test_engine)

# Update the neural network with the batch
neural_net.update(ins, outs)

neural_net.save_model('../../resources/model_parameters/trained_model')
