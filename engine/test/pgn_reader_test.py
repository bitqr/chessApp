from internal.Game import Game

game_entire_pgn = '1. e4 e5 2. Nf3 Nc6 3. Bc4 Bc5 4. d3 Nf6 5. c3 d6 6. Bb3 a5 7. a4 h6 8. h3 O-O 9. O-O Re8 10. Re1 ' \
                  'Bd7 11. Nbd2 Be6 12. Nc4 Qd7 13. Bd2 Rad8 14. Bc2 Qc8 15. Rc1 Bxh3 16. gxh3 Qxh3 17. Ne3 Bxe3 18. ' \
                  'Rxe3 Ng4 19. Qf1 Qxf1+ 20. Kxf1 Nxe3+ 21. Bxe3 g5 22. d4 Kg7 23. Nd2 b6 24. Bd3 Ne7 25. Bb5 Rf8 ' \
                  '26. Nc4 c6 27. Ba6 Ra8 28. Bb7 Ra7 29. Nxd6 Rb8 30. dxe5 Rbxb7 31. Nxb7 Rxb7 32. b4 Ng6 33. e6 ' \
                  'fxe6 34. Rb1 axb4 35. cxb4 Rb8 36. Ra1 Kf7 37. a5 c5 38. Rc1 Ke8 39. axb6 Rxb6 40. Bxc5 Rb7 41. ' \
                  'Rb1 Rb5 42. Ke2 Kf7 43. Ke3 h5 44. Kd4 g4 45. Bd6 Ke8 46. Kc4 Rg5 47. b5 Kd7 48. Rd1 Kc8 49. Kb4 ' \
                  'Ne5 50. Rc1+ Kd7 51. Bxe5 Rxe5 52. Rc4 Rg5 53. b6 g3 54. fxg3 Rxg3 55. Rc7+ Kd8 56. e5 h4 57. Rc4 ' \
                  'Kd7 58. b7 Rg1 59. b8=N+ Kd8 60. Kc5 Kc7 61. Na6+ Kb7 62. Nb4 Rg5 63. Kd6 h3 64. Rh4 Kb6 65. Kxe6 ' \
                  'Kc5 66. Rxh3 Kxb4 67. Kd6 Rg2 68. Rh4+ Ka3 69. e6 Rg6 70. Re4 Kb2 71. Kd7 Rg1 72. e7 Rd1+ 73. Ke6 ' \
                  'Ra1 74. e8=Q Ra6+ 75. Kd5 Ra5+ 76. Kc4 Rc5+ 77. Kxc5 Kc1 78. Re2 Kb1 79. Qa4 Kc1 80. Qc2# {Black ' \
                  'checkmated} 1-0'.split(' ')

game = Game()

move_index = 0
while not game.is_over():
    if move_index % 3 == 0:
        move_index += 1
    move = game.read_pgn_move(game_entire_pgn[move_index])
    print(move.to_string())
    game.board.apply_move(move)
    move_index += 1
