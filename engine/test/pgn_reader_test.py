from internal.Game import Game
from internal.utils import game_result_to_string

game_entire_pgn = '1. e4 e5 2. Nf3 Nc6 3. d4 exd4 4. Nxd4 Qf6 5. c3 Bc5 6. Be3 Nge7 7. g3 d5 8. Bg2 dxe4 9. O-O Bxd4 ' \
                  '10. cxd4 O-O 11. Nc3 Rd8 12. Nxe4 Qg6 13. Re1 Nf5 14. d5 Nxe3 15. Rxe3 Nb4 16. Qd2 Nxd5 17. Nc5 c6 '\
                  '18. Rae1 f6 19. Bxd5+ cxd5 20. Nd3 b6 21. Nf4 Qf5 22. Qd1 Rb8 23. h3 Rb7 24. Re7 Rxe7 25. Rxe7 Kf8 '\
                  '26. Rxa7 g5 27. Nh5 Rd7 28. Ra3 Re7 29. g4 Qe5 30. Qf3 Kf7 31. Rb3 Re6 32. Qd3 Qe4 33. Qxe4 dxe4 ' \
                  '34. Ng3 Bb7 35. a4 Bd5 36. Rb5 Ba2 37. Nf5 Rc6 38. Kg2 Be6 39. Nd4 Rd6 40. Nxe6 Kxe6 41. Kf1 Rd3 ' \
                  '42. Rxb6+ Ke5 43. Rb5+ Kd6 44. Ke2 Rxh3 45. a5 Rh1 46. b4 Ra1 47. Ke3 Ra2 48. Kxe4 Re2+ 49. Kf3 ' \
                  'Ra2 50. Ke4 Re2+ 51. Kd4 Rd2+ 52. Kc4 Rxf2 53. a6 Rc2+ 54. Kb3 Rc8 55. Rb6+ Kd5 56. Rxf6 Rb8 57. ' \
                  'Rf5+ Ke6 58. b5 Ra8 59. Rxg5 h6 60. Rh5 Kd6 61. Kb4 Kd7 62. Rxh6 Rg8 63. Ka5 Ke7 64. a7 Kf7 65. ' \
                  'Rh5 Ra8 66. b6 Ke6 67. Kb5 Rc8 68. b7 Rc1 69. Kb6 Rb1+ 70. Rb5 Rxb5+ 71. Kxb5 Kd5 72. b8=Q Ke4 73. '\
                  'a8=Q+ Kd3 74. g5 Ke3 75. g6 Kd3 76. g7 Kd4 77. g8=Q Ke3 78. Qbe8+ Kd2 79. Qag2+ Kd1 80. Q8d5+ Kc1 ' \
                  '81. Qe3+ Kb1 82. Qge4+ Kb2 83. Qdd4+ Ka2 84. Qe2+ Ka3 85. Qe7+ Kb3 86. Qdc4# {Black checkmated} ' \
                  '1-0'.split(' ')

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
