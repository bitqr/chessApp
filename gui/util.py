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


def highlight_target_squares(window, selected_piece_sprite):
    squares_coordinates = window.board.position.legal_moves[selected_piece_sprite.piece]
    result = []
    for coordinates in squares_coordinates:
        sprite = window.square_sprites[coordinates]
        result.append(sprite)
        sprite.highlight()
    return result


def un_highlight_target_squares(square_sprites):
    for square_sprite in square_sprites:
        square_sprite.un_highlight()


def perform_move_on_board(window, selected_piece_sprite, square_sprite, event_position):
    is_capture = not square_sprite.is_free()
    window.board.apply_move(Move(selected_piece_sprite.piece, square_sprite.square))
    if is_capture:
        # Look for the captured piece sprite and delete it
        for piece_sprite in window.piece_group.sprites():
            if piece_sprite != selected_piece_sprite \
                    and piece_sprite.rect.collidepoint(event_position):
                window.piece_group.remove(piece_sprite)
                break
    end_drag_and_drop_move(window, selected_piece_sprite)


def end_drag_and_drop_move(window, selected_piece_sprite):
    selected_piece_sprite.move_to_square(window.current_square_sprite(selected_piece_sprite))
    window.dragging_group.remove(selected_piece_sprite)


def release_piece_after_drag_and_drop(window, selected_piece_sprite, target_squares, event_position):
    found_square = False
    for square_sprite in target_squares:
        if square_sprite.rect.collidepoint(event_position):
            found_square = True
            perform_move_on_board(window, selected_piece_sprite, square_sprite, event_position)
            break
    if not found_square:
        end_drag_and_drop_move(window, selected_piece_sprite)
    un_highlight_target_squares(target_squares)


def select_piece_sprite_for_first_click_move(window, event_position, selected_piece_sprite):
    for piece_sprite in window.piece_group.sprites():
        if piece_sprite.rect.collidepoint(event_position):
            # Drag and drop can start here only if there are target squares
            target_squares = highlight_target_squares(window, piece_sprite)
            if len(target_squares) > 0:
                selected_piece_sprite = piece_sprite
            return selected_piece_sprite, target_squares
    return selected_piece_sprite, []
