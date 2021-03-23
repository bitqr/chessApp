import sys

import pygame

from gui import settings
from gui.GameInfoGUI import GameInfoGUI
from internal.PieceType import PieceType
from internal.Color import Color
from internal.Move import Move


def piece_to_sprite():
    result = dict()
    result[(PieceType.PAWN, Color.WHITE)] = "whitePawn"
    result[(PieceType.KNIGHT, Color.WHITE)] = "whiteKnight"
    result[(PieceType.BISHOP, Color.WHITE)] = "whiteBishop"
    result[(PieceType.ROOK, Color.WHITE)] = "whiteRook"
    result[(PieceType.QUEEN, Color.WHITE)] = "whiteQueen"
    result[(PieceType.KING, Color.WHITE)] = "whiteKing"
    result[(PieceType.PAWN, Color.BLACK)] = "blackPawn"
    result[(PieceType.KNIGHT, Color.BLACK)] = "blackKnight"
    result[(PieceType.BISHOP, Color.BLACK)] = "blackBishop"
    result[(PieceType.ROOK, Color.BLACK)] = "blackRook"
    result[(PieceType.QUEEN, Color.BLACK)] = "blackQueen"
    result[(PieceType.KING, Color.BLACK)] = "blackKing"
    return result


def square_to_sprite():
    result = dict()
    result[Color.WHITE] = "whiteSquare"
    result[Color.BLACK] = "blackSquare"
    return result


def highlight_target_squares(chessboard, selected_piece_sprite):
    squares_coordinates = chessboard.board.position.legal_moves[selected_piece_sprite.piece]
    result = []
    square_sprite = chessboard.current_square_sprite(selected_piece_sprite)
    for coordinates in squares_coordinates:
        sprite = chessboard.square_sprites[coordinates]
        result.append(sprite)
        sprite.highlight()
    if len(squares_coordinates) == 0:
        square_sprite.signal_unmovable()
    return result


def un_highlight_target_squares(square_sprites):
    for square_sprite in square_sprites:
        square_sprite.un_highlight()


def cancel_highlighting_target_squares(square_sprites):
    for square_sprite in square_sprites:
        square_sprite.cancel_highlight()


def perform_move_on_board(
        screen,
        game_info,
        chessboard,
        selected_piece_sprite,
        destination_square_sprite,
        event_position
):
    # First, remove check highlighted square
    if chessboard.check_highlighted_square_sprite:
        chessboard.check_highlighted_square_sprite.un_highlight()
        chessboard.check_highlighted_square_sprite = None
    origin_square = chessboard.current_square_sprite(selected_piece_sprite).square
    move = Move(origin_square, selected_piece_sprite.piece, destination_square_sprite.square)
    piece_type = PieceType.NONE
    if move.is_promotion:
        piece_type = run_pawn_promotion_selection(chessboard, move, screen)
        move.promoted_piece_type = piece_type
    latest_move = chessboard.board.position.latest_move
    chessboard.board.apply_move(move)
    if move.is_capture:
        # Look for the captured piece sprite and delete it
        for piece_sprite in chessboard.piece_group.sprites():
            if piece_sprite != selected_piece_sprite \
                    and piece_sprite.rect.collidepoint(event_position):
                chessboard.piece_group.remove(piece_sprite)
                break
    if move.is_castle:
        # Also move the additional rook on the board
        rook = \
            chessboard.board.squares[(move.destination_square.rank, 5)].content if move.destination_square.file == 6 \
            else chessboard.board.squares[(move.destination_square.rank, 3)].content
        rook_sprite = chessboard.piece_sprites[rook]
        rook_sprite.move_to_square(chessboard.current_square_sprite(rook_sprite))
    checked_king_current_square_sprite = chessboard.attacked_king_sprite(move.piece)
    if move.is_en_passant:
        # Remove the captured pawn, which in this case is the latest moved piece
        chessboard.piece_group.remove(chessboard.piece_sprites[latest_move.piece])
    if move.is_promotion:
        selected_piece_sprite.promote_pawn(
            piece_type, destination_square_sprite.square.file, destination_square_sprite.square.rank
        )
    if move.is_check:
        # Highlight opponent king
        checked_king_current_square_sprite.signal_check()
        chessboard.check_highlighted_square_sprite = checked_king_current_square_sprite
    game_info.update_text()
    end_drag_and_drop_move(chessboard, selected_piece_sprite)


def end_drag_and_drop_move(chessboard, selected_piece_sprite):
    selected_piece_sprite.move_to_square(chessboard.current_square_sprite(selected_piece_sprite))
    chessboard.dragging_group.remove(selected_piece_sprite)
    chessboard.piece_group.add(selected_piece_sprite)


def release_piece_after_drag_and_drop(
        screen,
        game_info,
        chessboard,
        selected_piece_sprite,
        target_squares,
        event_position
):
    found_square = False
    for square_sprite in target_squares:
        if square_sprite.rect.collidepoint(event_position):
            found_square = True
            perform_move_on_board(screen, game_info, chessboard, selected_piece_sprite, square_sprite, event_position)
            break
    if not found_square:
        end_drag_and_drop_move(chessboard, selected_piece_sprite)
        cancel_highlighting_target_squares(target_squares)
        chessboard.current_square_sprite(selected_piece_sprite).cancel_highlight()
    else:
        un_highlight_target_squares(target_squares)


def select_piece_sprite_for_first_click_move(chessboard, event_position, selected_piece_sprite):
    for piece_sprite in chessboard.piece_group.sprites():
        if piece_sprite.rect.collidepoint(event_position):
            # Drag and drop can start here only if there are target squares
            target_squares = highlight_target_squares(chessboard, piece_sprite)
            selected_piece_sprite = piece_sprite
            return selected_piece_sprite, target_squares
    return selected_piece_sprite, []


def create_game_info_group(game):
    game_info_window = GameInfoGUI(
        game,
        settings.GAME_INFO_TOP_LEFT_X,
        settings.GAME_INFO_TOP_LEFT_Y,
        settings.GAME_INFO_WIDTH,
        settings.GAME_INFO_HEIGHT,
        settings.GAME_INFO_COLOR
    )
    game_info_window_group = pygame.sprite.Group()
    game_info_window_group.add(game_info_window)
    return game_info_window, game_info_window_group


def run_pawn_promotion_selection(chessboard, move, screen):
    run = True
    while run:
        pygame.display.flip()
        promotion_piece_group = chessboard.promotion_piece_groups[move.piece.color]
        promotion_piece_group.draw(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for promotion_piece_sprite in promotion_piece_group.sprites():
                    if promotion_piece_sprite.rect.collidepoint(event.pos):
                        return promotion_piece_sprite.piece.type
