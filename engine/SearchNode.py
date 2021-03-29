import math


class SearchNode:

    # Constructor takes the current chessboard position and the move that generated the state
    # (for root node, this field is None)
    def __init__(self, game, generating_move=None, parent=None):
        self.game = game
        self.generating_move = generating_move
        # For each legal move, there is an entry in the children dict: (key, value) = (move, resulting position)
        self.children = dict()
        self.visit_count = 0
        self.parent = parent
        # Reward expectation
        self.value = 0

    # Tells whether node is terminal: If it leads to the end of the game
    def is_terminal(self):
        return self.game.is_over()

    # Tells whether node is a leaf
    def is_leaf(self):
        return len(self.children) == 0

    # Upper confidence bound is the main criteria for the select() method
    # One big challenge in Monte-Carlo Tree Search methods is the trade-off between
    # exploitation (deeply exploit winning or promising positions) and
    # exploration (explore rarely visited positions)
    def upper_confidence_bound(self, move, exploration_parameter):
        child_node = self.children[move]
        return child_node.value / (1 + child_node.visit_count) + \
            exploration_parameter * math.sqrt(math.log(self.visit_count) / (1 + child_node.visit_count))

    def to_string(self):
        result = 'Node {0}: ([\n'.format(self.game.board.fen_position)
        for child in self.children:
            result += '{0},\n'.format(self.children[child].game.board.fen_position)
        result += '], {0}, {1})'.format(self.value, self.visit_count)
        return result
