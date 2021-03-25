import pygame
import clipboard

from gui import settings
from gui.ButtonGUI import ButtonGUI


class InputBoxGUI(ButtonGUI):

    def __init__(self, top_left_x, top_left_y, width, height, color, text_color, text=''):
        super().__init__(top_left_x, top_left_y, width, height)
        self.rect = pygame.Rect(top_left_x, top_left_y, width, height)
        self.text = text
        self.color = color
        self.text_color = text_color
        self.font = pygame.font.SysFont(settings.TEXT_FONT, settings.TEXT_SIZE)
        self.text_surface = self.font.render(self.text, True, text_color)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input box rect
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable
                self.active = not self.active
            else:
                self.active = False
            self.color = settings.INPUT_BOX_ACTIVE_COLOR if self.active else settings.INPUT_BOX_INACTIVE_COLOR
        if event.type == pygame.KEYDOWN:
            if self.active:
                keys = pygame.key.get_pressed()
                if event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    if keys[pygame.K_LCTRL] and keys[pygame.K_v]:
                        self.text = clipboard.paste()
                    else:
                        self.text += event.unicode
                # Re-render the text
                self.text_surface = self.font.render(self.text, True, self.text_color)

    def update(self):
        # Resize the box if the text is too long
        self.rect.w = min(settings.WINDOW_WIDTH,
                          max(self.rect.w, self.text_surface.get_width() + settings.INPUT_BOX_OFFSET))

    def draw(self, screen):
        pygame.draw.rect(screen, settings.CLEAR_SCREEN_COLOR, self.rect)
        screen.blit(self.text_surface,
                    (self.rect.x + settings.INPUT_BOX_OFFSET / 2, self.rect.y + settings.INPUT_BOX_OFFSET / 2))
        pygame.draw.rect(screen, self.color, self.rect, 2)
