from internal.Board import Board
from gui.BoardGUI import BoardGUI
import pygame
import sys


def run_app(window):
    pygame.display.init()
    run = True
    selected_piece_sprite = None
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # User clicked on something
                for piece_sprite in window.piece_group.sprites():
                    if piece_sprite.rect.collidepoint(event.pos):
                        # Drag and drop can start here
                        selected_piece_sprite = piece_sprite
                        break
            elif event.type == pygame.MOUSEMOTION:
                if selected_piece_sprite:
                    # A piece is being dragged
                    window.dragging_group.add(selected_piece_sprite)
                    selected_piece_sprite.move_relative(event.rel)
            elif event.type == pygame.MOUSEBUTTONUP:
                if selected_piece_sprite:
                    # A piece is being released, either on a square or somewhere else
                    for square_sprite in window.square_group.sprites():
                        if square_sprite.rect.collidepoint(event.pos):
                            is_capture = window.request_move(selected_piece_sprite, square_sprite)
                            if is_capture:
                                # Look for the captured piece sprite and delete it
                                for piece_sprite in window.piece_group.sprites():
                                    if piece_sprite != selected_piece_sprite \
                                            and piece_sprite.rect.collidepoint(event.pos):
                                        window.piece_group.remove(piece_sprite)
                                        break
                            selected_piece_sprite.move_to_square(window.current_square_sprite(selected_piece_sprite))
                            window.dragging_group.remove(selected_piece_sprite)
                            selected_piece_sprite = None
                            break
        pygame.display.flip()
        window.draw_board(screen)
    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    pygame.init()
    board = Board(8)
    chessboard = BoardGUI(board, 100)
    screen = pygame.display.set_mode((chessboard.board_width, chessboard.board_height))
    pygame.display.set_caption("Chess App")
    chessboard.initialize_board(board, screen)

    run_app(chessboard)


# -> Next Objectives:

# - Computation of legal moves based on chess rules
#   - Castle
#   - En-Passant
#   - FEN-notation reading
#   - Pins (pieces that are pinned cannot move)
#   - More generally, prevent all moves putting the king in check
#       (pins, but also moving the king to a controlled square)

# - GUI: Click & Click for moving pieces, with possible squares highlighted

# - Start playing a game
