import pygame

from gui import settings
from internal import util


class GameInfoGUI(pygame.sprite.Sprite):

    def __init__(self, game, top_left_x, top_left_y, width, height, color):
        super().__init__()
        self.color = color
        self.game = game
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(top_left_x, top_left_y)

    def update_text(self):
        self.image.fill(self.color)
        lines = self.game.to_string().split('\n')
        font = pygame.font.SysFont(settings.GAME_INFO_TEXT_FONT, settings.GAME_INFO_TEXT_SIZE)
        line_index = settings.GAME_INFO_LINE_OFFSET
        for line in lines:
            text = font.render(line, False, settings.GAME_INFO_TEXT_COLOR)
            self.image.blit(text, (settings.GAME_INFO_COLUMN_OFFSET, line_index))
            line_index += settings.GAME_INFO_LINE_INTERVAL
