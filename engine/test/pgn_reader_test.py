from internal.Game import Game
from internal.utils import game_result_to_string

game_entire_pgn = '1. e3 e5 2. d4 e4 3. c4 Nf6 4. Nc3 Bb4 5. Ne2 b6 6. Bd2 Bb7 7. a3 Bd6 8. Nb5 O-O 9. Nxd6 cxd6 10. ' \
                  'd5 Na6 11. Nd4 Nc7 12. a4 Qe7 13. g4 Qe5 14. Bc3 Qg5 15. Be2 Rae8 16. Nf5 Na6 17. h4 Qg6 18. h5 ' \
                  'Qg5 19. h6 Re5 20. hxg7 Rb8 21. Nxd6 Nc5 22. b4 Nd3+ 23. Bxd3 exd3 24. Qxd3 Ba6 25. O-O-O Rxd5 26. '\
                  'Bxf6 Rxd3 27. Bxg5 Rxd1+ 28. Kxd1 Kxg7 29. Bh6+ Kg6 30. Bf4 Rd8 31. g5 Ra8 32. Rh6+ Kg7 33. b5 ' \
                  'Bxb5 34. cxb5 a6 35. Be5+ Kg8 36. Rf6 Kg7 37. Rxf7+ Kg6 38. Rf6+ Kxg5 39. f3 h5 40. Ne4+ Kh4 41. ' \
                  'Rg6 axb5 42. Nf2 Ra5 43. Bf6# {Black checkmated} 1-0'.split(' ')

FILE_TO_READ = '../../resources/games_database/ficsgamesdb_2017_CvC_nomovetimes_199240.pgn'


def play_pgn_game(pgn_string):
    game = Game()
    move_index = 0
    while not game.is_over():
        if pgn_string[move_index][0] == '{':
            if 'ran' in pgn_string[move_index:] \
                    or 'drawn' in pgn_string[move_index:] or 'material}' in pgn_string[move_index:]:
                game.apply_draw()
                break
            if 'resigns}' in pgn_string[move_index:] or 'forfeits' in pgn_string[move_index:]:
                game.apply_resign()
                break
        if move_index % 3 == 0:
            move_index += 1
        move = game.read_pgn_move(pgn_string[move_index])
        game.board.apply_move(move)
        move_index += 1
    print(game_result_to_string[game.result])


play_pgn_game(game_entire_pgn)
starting_point = 0

game_index = 1
for line in open(FILE_TO_READ, 'r'):
    print('Game #{0}'.format(game_index))
    if game_index > starting_point:
        pgn_game = line.split(' ')
        play_pgn_game(pgn_game)
    game_index += 1
