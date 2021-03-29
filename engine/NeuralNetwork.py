
class NeuralNetwork:

    def __init__(self, parameters=None):
        self.parameters = parameters

    def evaluate(self, board_position: str, actions: list) -> (list, float):
        # Receives an input (a FEN string or a Position object) along with a list of actions and returns
        # - a list of probabilities associated to each actions
        # - a float value giving the expected outcome of the game
        pass
