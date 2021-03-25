import pygame

from gui import settings


class ButtonGUI:

    def __init__(self, top_left_x, top_left_y, width, height, text='', color=None, text_color=None):
        self.top_left_x = top_left_x
        self.top_left_y = top_left_y
        self.width = width
        self.height = height
        self.text = text
        self.color = color
        self.text_color = text_color

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.top_left_x, self.top_left_y, self.width, self.height))
        if self.text:
            font = pygame.font.SysFont(settings.TEXT_FONT, settings.TEXT_SIZE)
            text = font.render(self.text, False, self.text_color)
            screen.blit(
                text,
                (self.top_left_x + (self.width - text.get_width()) / 2,
                 self.top_left_y + (self.height - text.get_height()) / 2)
            )

    def contains_position(self, position):
        return self.top_left_x < position[0] < self.top_left_x + self.width \
               and self.top_left_y < position[1] < self.top_left_y + self.height
