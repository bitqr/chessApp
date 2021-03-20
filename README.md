# chessApp
Chess Application

Will contain:

- A chess app, with a GUI of the board
- A chess engine, for somme chess challenge
- And many more...

# Next Objectives:

1) GUI improvement: When click on a piece, highlight the legal destinations
A 2nd click on a target square will perform the move. Any click elsewhere will change nothing

2) Refinement of the Computation of legal moves based on chess rules
    - Add the move: Castle

3) Start playing a game
   - Notion of a Game
   - Notion of a Player
   - Turns

4) Introduce game ending notions
   - Check
   - Checkmate (no legal move left and the player's in check
   - Stalemate (no legal move left and it's the player isn't in check)

5) Advanced notions
   - Add the move: En-Passant
   - Pawn promotion
   - Pins (pieces that are pinned cannot move)
   - More generally, in legal moves computation, prevent all moves putting the king in check
       (pins, but also moving the king to a controlled square)

6) Editor:

   - FEN-notation reader
   - Tests with public resources