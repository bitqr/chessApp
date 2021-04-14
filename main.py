from engine import settings
from engine.Engine import Engine
from gui import utils
from internal.utils import *
from gui.ButtonGUI import ButtonGUI
from gui.BoardGUI import BoardGUI, settings
import pygame
import sys

from gui.InputBoxGUI import InputBoxGUI
from internal.Game import Game


def open_main_menu(window, engine_to_use=None):
    pygame.display.init()
    background_image = pygame.sprite.Sprite()
    background_image.image = pygame.image.load("sprites/background.jpeg").convert()
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
    editor_mode_button = ButtonGUI(
        settings.EDITOR_BUTTON_TOP_LEFT_X,
        settings.EDITOR_BUTTON_TOP_LEFT_Y,
        settings.EDITOR_BUTTON_WIDTH,
        settings.EDITOR_BUTTON_HEIGHT,
        settings.EDITOR_BUTTON_TEXT,
        settings.EDITOR_BUTTON_COLOR,
        settings.EDITOR_BUTTON_TEXT_COLOR
    )
    fen_string_input_box = InputBoxGUI(
        settings.INPUT_BOX_TOP_LEFT_X,
        settings.INPUT_BOX_TOP_LEFT_Y,
        settings.INPUT_BOX_WIDTH,
        settings.INPUT_BOX_HEIGHT,
        settings.INPUT_BOX_COLOR,
        settings.INPUT_BOX_TEXT_COLOR
    )
    input_box_intro_text = ButtonGUI(
        settings.INPUT_BOX_INTRO_TEXT_TOP_LEFT_X,
        settings.INPUT_BOX_INTRO_TEXT_TOP_LEFT_Y,
        settings.INPUT_BOX_INTRO_TEXT_WIDTH,
        settings.INPUT_BOX_INTRO_TEXT_HEIGHT,
        "Enter FEN-String to start with",
        settings.INPUT_BOX_INTRO_TEXT_COLOR,
        settings.INPUT_BOX_INTRO_TEXT_TEXT_COLOR
    )

    run = True
    while run:
        pygame.display.flip()
        background_group.draw(window)
        start_game_button.draw(window)
        editor_mode_button.draw(window)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if start_game_button.contains_position(event.pos):
                    return run_color_choice(window, background_group, engine_to_use)
                if editor_mode_button.contains_position(event.pos):
                    screen.fill(settings.CLEAR_SCREEN_COLOR)
                    background_group.draw(window)
                    input_box_intro_text.draw(window)
                    fen_string_input_box.draw(window)
                    initial_fen_position = utils.enter_fen_string(window, fen_string_input_box)
                    screen.fill(settings.CLEAR_SCREEN_COLOR)
                    if not is_valid_fen(initial_fen_position):
                        initial_fen_position = ''
                    background_group.draw(window)
                    player_color = None
                    if engine_to_use:
                        player_color = Color.WHITE if engine_to_use.color == Color.BLACK else Color.BLACK
                    return run_game(Game(initial_fen_position), player_color, engine_to_use)
    pygame.quit()
    sys.exit()


def run_color_choice(window, background_group, engine_to_use):
    play_with_white_button = ButtonGUI(
        settings.PLAY_WITH_WHITE_BUTTON_TOP_LEFT_X,
        settings.PLAY_WITH_WHITE_BUTTON_TOP_LEFT_Y,
        settings.PLAY_WITH_WHITE_BUTTON_WIDTH,
        settings.PLAY_WITH_WHITE_BUTTON_HEIGHT,
        settings.PLAY_WITH_WHITE_BUTTON_TEXT,
        settings.PLAY_WITH_WHITE_BUTTON_COLOR,
        settings.PLAY_WITH_WHITE_BUTTON_TEXT_COLOR
    )
    play_with_black_button = ButtonGUI(
        settings.PLAY_WITH_BLACK_BUTTON_TOP_LEFT_X,
        settings.PLAY_WITH_BLACK_BUTTON_TOP_LEFT_Y,
        settings.PLAY_WITH_BLACK_BUTTON_WIDTH,
        settings.PLAY_WITH_BLACK_BUTTON_HEIGHT,
        settings.PLAY_WITH_BLACK_BUTTON_TEXT,
        settings.PLAY_WITH_BLACK_BUTTON_COLOR,
        settings.PLAY_WITH_BLACK_BUTTON_TEXT_COLOR
    )
    screen.fill(settings.CLEAR_SCREEN_COLOR)
    background_group.draw(window)
    play_with_white_button.draw(window)
    play_with_black_button.draw(window)
    while True:
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                game = Game()
                if play_with_white_button.contains_position(event.pos):
                    screen.fill(settings.CLEAR_SCREEN_COLOR)
                    background_group.draw(window)
                    return run_game(game, Color.WHITE, engine_to_use)
                if play_with_black_button.contains_position(event.pos):
                    screen.fill(settings.CLEAR_SCREEN_COLOR)
                    background_group.draw(window)
                    return run_game(game, Color.BLACK, engine_to_use)


def run_game(game, player_color=None, engine_to_use=None):
    game_info_window, game_info_group = utils.create_game_info_group(game)
    chessboard = BoardGUI(game.board, settings.SQUARE_SIZE)
    chessboard.initialize_board()
    pygame.display.init()
    # If no engine provided, play against myself
    run = True
    restart_button = ButtonGUI(
        settings.START_BUTTON_TOP_LEFT_X,
        settings.START_BUTTON_TOP_LEFT_Y,
        settings.START_BUTTON_WIDTH,
        settings.START_BUTTON_HEIGHT,
        settings.RESTART_BUTTON_TEXT,
        settings.RESTART_BUTTON_COLOR,
        settings.START_BUTTON_TEXT_COLOR
    )
    resign_button = ButtonGUI(
        settings.RESIGN_BUTTON_TOP_LEFT_X,
        settings.RESIGN_BUTTON_TOP_LEFT_Y,
        settings.RESIGN_BUTTON_WIDTH,
        settings.RESIGN_BUTTON_HEIGHT,
        settings.RESIGN_BUTTON_TEXT,
        settings.RESIGN_BUTTON_COLOR,
        settings.RESIGN_BUTTON_TEXT_COLOR
    )
    draw_button = ButtonGUI(
        settings.DRAW_BUTTON_TOP_LEFT_X,
        settings.DRAW_BUTTON_TOP_LEFT_Y,
        settings.DRAW_BUTTON_WIDTH,
        settings.DRAW_BUTTON_HEIGHT,
        settings.DRAW_BUTTON_TEXT,
        settings.DRAW_BUTTON_COLOR,
        settings.DRAW_BUTTON_TEXT_COLOR
    )
    selected_piece_sprite = None
    target_squares = []
    held_button = False
    drag_in_progress = False
    if player_color == Color.BLACK:
        engine_move = engine_to_use.choose_move(chessboard.board.game)
        utils.perform_engine_move(engine_move, chessboard, game_info_window, player_color)
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                held_button = True
                # User clicked on something
                if draw_button.contains_position(event.pos):
                    if chessboard.board.game.can_be_drawn():
                        utils.draw_game(game_info_window, chessboard)
                if restart_button.contains_position(event.pos):
                    return run_game(Game(), player_color, engine_to_use)
                if resign_button.contains_position(event.pos):
                    if not chessboard.board.game.is_over():
                        utils.resign(game_info_window, chessboard)
                if selected_piece_sprite:
                    utils.cancel_highlighting_target_squares(target_squares)
                    # Clicked on potential target square
                    for square_sprite in target_squares:
                        if square_sprite.rect.collidepoint(event.pos):
                            utils.perform_move_on_board(
                                game_info_window,
                                chessboard,
                                selected_piece_sprite,
                                square_sprite,
                                player_color,
                                chessboard.board.position.latest_move
                            )
                            break
                    # Re-capture: When playing an engine, the responding move may have re-captured the piece
                    if not chessboard.is_captured_piece(selected_piece_sprite):
                        chessboard.current_square_sprite(selected_piece_sprite).cancel_highlight()
                    selected_piece_sprite = None
                else:
                    # 1st click for a move
                    selected_piece_sprite, target_squares = \
                        utils.select_piece_sprite_for_first_click_move(chessboard, event.pos, selected_piece_sprite)
            elif event.type == pygame.MOUSEMOTION:
                if held_button and selected_piece_sprite:
                    drag_in_progress = True
                    # A piece is being dragged
                    chessboard.dragging_group.add(selected_piece_sprite)
                    if chessboard.contains(selected_piece_sprite):
                        selected_piece_sprite.move_relative(event.rel)
                    else:
                        utils.end_drag_and_drop_move(chessboard, selected_piece_sprite)
                        utils.cancel_highlighting_target_squares(target_squares)
                        chessboard.current_square_sprite(selected_piece_sprite).cancel_highlight()
                        selected_piece_sprite = None
                        drag_in_progress = False
            elif event.type == pygame.MOUSEBUTTONUP:
                held_button = False
                # A piece is being released OR has just been selected by a left click
                if drag_in_progress:
                    utils.release_piece_after_drag_and_drop(
                        game_info_window,
                        chessboard,
                        selected_piece_sprite,
                        target_squares,
                        event.pos,
                        player_color,
                        engine_to_use
                    )
                    selected_piece_sprite = None
                drag_in_progress = False
        pygame.display.flip()
        restart_button.draw(screen)
        resign_button.draw(screen)
        draw_button.draw(screen)
        chessboard.draw_board(screen)
        game_info_group.draw(screen)
        pygame.display.flip()
        # Perform engine move
        if engine_to_use:
            if not chessboard.board.game.is_over() \
                    and chessboard.board.position.color_to_move != player_color:
                engine_move = engine_to_use.choose_move(chessboard.board.game)
                utils.perform_engine_move(engine_move, chessboard, game_info_window, player_color)
                restart_button.draw(screen)
                resign_button.draw(screen)
                draw_button.draw(screen)
                chessboard.draw_board(screen)
                game_info_group.draw(screen)
    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    pygame.init()
    engine = Engine(saved_model='resources/model_parameters/trained_model')
    pygame.display.set_caption("Chess App")
    screen = pygame.display.set_mode((settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT))
    open_main_menu(screen, engine)
