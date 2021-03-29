from internal.Game import Game


def positions():
    return [
        'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1',
        'r3k2r/p1ppqpb1/bn2pnp1/3PN3/1p2P3/2N2Q1p/PPPBBPPP/R3K2R w KQkq - 0 1',
        '8/2p5/3p4/KP5r/1R3p1k/8/4P1P1/8 w - - 0 1',
        'r3k2r/Pppp1ppp/1b3nbN/nP6/BBP1P3/q4N2/Pp1P2PP/R2Q1RK1 w kq - 0 1',
        'r2q1rk1/pP1p2pp/Q4n2/bbp1p3/Np6/1B3NBn/pPPP1PPP/R3K2R b KQ - 0 1',
        'rnbq1k1r/pp1Pbppp/2p5/8/2B5/8/PPP1NnPP/RNBQK2R w KQ - 1 8',
        'r4rk1/1pp1qppp/p1np1n2/2b1p1B1/2B1P1b1/P1NP1N2/1PP1QPPP/R4RK1 w - - 0 10'
        ]


def moves_count():
    return [
        20,
        48,
        14,
        6,
        6,
        44,
        46
    ]


def test_legal_moves():
    for item in list(zip(positions(), moves_count())):
        game = Game(item[0])
        legal_moves_count = len(game.board.position.legal_moves_list())
        print('count = {0} vs {1} expected'.format(legal_moves_count, item[1]))
        assert legal_moves_count == item[1]


test_legal_moves()
