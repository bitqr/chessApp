import pygame

from gui import settings


class SquareGUI(pygame.sprite.Sprite):

    def __init__(self, square, square_size, image):
        super().__init__()
        self.square = square
        self.normal_image = pygame.image.load(image).convert_alpha()
        self.normal_image = pygame.transform.scale(self.normal_image, [square_size, square_size])
        self.normal_rect = self.normal_image.get_rect()
        self.normal_rect = self.normal_rect.move(square.file * square_size, square.rank * square_size)
        self.highlighted_image = pygame.Surface((square_size, square_size))
        self.image = self.normal_image
        self.rect = self.normal_rect
        self.is_in_check = False

    def highlight(self):
        if not self.is_in_check:
            self.highlighted_image.fill(settings.HIGHLIGHTED_SQUARES_COLOR)
            self.image = self.highlighted_image

    def cancel_highlight(self):
        if not self.is_in_check:
            self.image = self.normal_image

    def un_highlight(self):
        self.image = self.normal_image
        self.is_in_check = False

    def is_free(self):
        return self.square.is_free()

    def signal_unmovable(self):
        if not self.is_in_check:
            self.highlighted_image.fill(settings.UNMOVABLE_PIECES_COLOR)
            self.image = self.highlighted_image

    def signal_check(self):
        self.highlighted_image.fill(settings.CHECKED_KING_COLOR)
        self.image = self.highlighted_image
        self.is_in_check = True
