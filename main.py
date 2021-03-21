from internal.Board import Board
from gui.BoardGUI import BoardGUI
import gui.util
import pygame
import sys


def run_app(window):
    pygame.display.init()
    run = True
    selected_piece_sprite = None
    target_squares = []
    held_button = False
    drag_in_progress = False
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                held_button = True
                # User clicked on something
                if selected_piece_sprite:
                    gui.util.cancel_highlighting_target_squares(target_squares)
                    # Clicked on potential target square
                    for square_sprite in target_squares:
                        if square_sprite.rect.collidepoint(event.pos):
                            gui.util.perform_move_on_board(window, selected_piece_sprite, square_sprite, event.pos)
                            break
                    window.current_square_sprite(selected_piece_sprite).cancel_highlight()
                    selected_piece_sprite = None
                else:
                    # 1st click for a move
                    selected_piece_sprite, target_squares =\
                        gui.util.select_piece_sprite_for_first_click_move(window, event.pos, selected_piece_sprite)
            elif event.type == pygame.MOUSEMOTION:
                if held_button and selected_piece_sprite:
                    drag_in_progress = True
                    # A piece is being dragged
                    window.dragging_group.add(selected_piece_sprite)
                    selected_piece_sprite.move_relative(event.rel)
            elif event.type == pygame.MOUSEBUTTONUP:
                held_button = False
                # A piece is being released OR has just been selected by a left click
                if drag_in_progress:
                    gui.util.release_piece_after_drag_and_drop(window, selected_piece_sprite, target_squares, event.pos)
                    selected_piece_sprite = None
                drag_in_progress = False
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
