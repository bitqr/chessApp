from gui import settings
from gui.ButtonGUI import ButtonGUI
from gui.BoardGUI import BoardGUI
import gui.utils
import pygame
import sys

from internal.Game import Game


def open_main_menu(window):
    pygame.display.init()
    background_image = pygame.sprite.Sprite()
    background_image.image = pygame.image.load("sprites/main_menu.jpeg").convert()
    background_image.image = pygame.transform.scale(background_image.image,
                                                    [settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT])
    background_image.rect = background_image.image.get_rect()
    background_group = pygame.sprite.Group()
    background_group.add(background_image)

    start_game_button = ButtonGUI(
        settings.START_BUTTON_TOP_LEFT_X,
        settings.START_BUTTON_TOP_LEFT_Y,
        settings.START_BUTTON_WIDTH,
        settings.START_BUTTON_HEIGHT,
        settings.START_BUTTON_TEXT,
        settings.START_BUTTON_COLOR,
        settings.START_BUTTON_TEXT_COLOR
    )

    run = True
    while run:
        pygame.display.flip()
        background_group.draw(window)
        start_game_button.draw(window)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if start_game_button.contains_position(event.pos):
                    screen.fill(settings.CLEAR_SCREEN_COLOR)
                    background_group.draw(window)
                    return run_game()
    pygame.quit()
    sys.exit()


def run_game():
    game = Game()
    game_info_window, game_info_group = gui.utils.create_game_info_group(game)
    chessboard = BoardGUI(game.board, settings.SQUARE_SIZE)
    chessboard.initialize_board(game.board)
    pygame.display.init()
    run = True
    selected_piece_sprite = None
    target_squares = []
    held_button = False
    drag_in_progress = False
    restart_button = ButtonGUI(
        settings.START_BUTTON_TOP_LEFT_X,
        settings.START_BUTTON_TOP_LEFT_Y,
        settings.START_BUTTON_WIDTH,
        settings.START_BUTTON_HEIGHT,
        settings.RESTART_BUTTON_TEXT,
        settings.RESTART_BUTTON_COLOR,
        settings.START_BUTTON_TEXT_COLOR
    )
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                held_button = True
                # User clicked on something
                if restart_button.contains_position(event.pos):
                    return run_game()
                if selected_piece_sprite:
                    gui.utils.cancel_highlighting_target_squares(target_squares)
                    # Clicked on potential target square
                    for square_sprite in target_squares:
                        if square_sprite.rect.collidepoint(event.pos):
                            gui.utils.perform_move_on_board(
                                game_info_window, chessboard, selected_piece_sprite, square_sprite, event.pos
                            )
                            break
                    chessboard.current_square_sprite(selected_piece_sprite).cancel_highlight()
                    selected_piece_sprite = None
                else:
                    # 1st click for a move
                    selected_piece_sprite, target_squares =\
                        gui.utils.select_piece_sprite_for_first_click_move(chessboard, event.pos, selected_piece_sprite)
            elif event.type == pygame.MOUSEMOTION:
                if held_button and selected_piece_sprite:
                    drag_in_progress = True
                    # A piece is being dragged
                    chessboard.dragging_group.add(selected_piece_sprite)
                    if chessboard.contains(selected_piece_sprite):
                        selected_piece_sprite.move_relative(event.rel)
                    else:
                        gui.utils.end_drag_and_drop_move(chessboard, selected_piece_sprite)
                        gui.utils.cancel_highlighting_target_squares(target_squares)
                        chessboard.current_square_sprite(selected_piece_sprite).cancel_highlight()
                        selected_piece_sprite = None
                        drag_in_progress = False
            elif event.type == pygame.MOUSEBUTTONUP:
                held_button = False
                # A piece is being released OR has just been selected by a left click
                if drag_in_progress:
                    gui.utils.release_piece_after_drag_and_drop(
                        game_info_window, chessboard, selected_piece_sprite, target_squares, event.pos
                    )
                    selected_piece_sprite = None
                drag_in_progress = False
        pygame.display.flip()
        restart_button.draw(screen)
        chessboard.draw_board(screen)
        game_info_group.draw(screen)
    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption("Chess App")
    screen = pygame.display.set_mode((settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT))
    open_main_menu(screen)
