
class AdvancedEngine:

    def __init__(self, neural_network):
        self.neural_network = neural_network

    def choose_move(self, game):
        return self.neural_network.decide(game)
