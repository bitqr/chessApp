from tensorflow import keras

from engine import utils
from engine.NeuralNetwork import NeuralNetwork

fen_position = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
input_vector = utils.from_fen_to_input_vector(fen_position)
print(input_vector)

# Neural network starting from scratch
neural_network = NeuralNetwork()

keras.utils.plot_model(neural_network.model, "input_and_output_model.png", show_shapes=True)

y = neural_network.evaluate(input_vector)
neural_network.model.summary()

neural_network.save_model('../../resources/model_parameters/example_model')

# Load the model in a new NN
copied_model = keras.models.load_model('../../resources/model_parameters/example_model')
other_neural_network = NeuralNetwork(copied_model)

y2 = other_neural_network.evaluate(input_vector)

# Check that both neural networks provide the same evaluation
# y and y2 both are lists of 2 tensors:
# - The policy tensor
# - The evaluation tensor
print(y)
print(y2)

other_neural_network.model.summary()
