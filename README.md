# chessApp
Chess Application

Will contain:

- A chess app, with a GUI of the board
- A chess engine, for some chess challenge
- Many more...

# Next Objectives:

- Refinement of the Computation of legal moves based on chess rules
    - Add the notion of Check
    - Add controlled squares for each color
    - Add the move: Castle

- Start playing a game
   - Notion of a Game
   - Notion of a Player
   - Turns

- Introduce game ending notions
   - Checkmate (no legal move left, and the player's in check)
   - Stalemate (no legal move left, and it's the player isn't in check)

- Advanced notions
   - Add the move: En-Passant
   - Pawn promotion
   - Pins (pieces that are pinned cannot move)
   - More generally, in legal moves computation, prevent all moves putting the king in check
       (pins, but also moving the king to a controlled square)

- Editor:

   - FEN-notation reader
   - Tests with public resources