from engine.Engine import Engine
from internal.Game import Game


def display_search_tree_root(search_tree):
    print('Root: ')
    print(search_tree.root.to_string())
    for move in search_tree.root.children:
        print('move [{0}, {1}] --> ({2}, {3})'.format(move.origin_square.to_string(),
                                                      move.destination_square.to_string(),
                                                      search_tree.root.children[move].value,
                                                      search_tree.root.children[move].visit_count))


engine = Engine()
engine.choose_move(Game())
display_search_tree_root(engine.search_tree)
