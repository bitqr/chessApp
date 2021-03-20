import pygame


class SquareGUI(pygame.sprite.Sprite):

    def __init__(self, square, square_size, image):
        super().__init__()
        self.square = square
        self.normal_image = pygame.image.load(image).convert()
        self.normal_image = pygame.transform.scale(self.normal_image, [square_size, square_size])
        self.rect = self.normal_image.get_rect()
        self.rect = self.rect.move(square.file * square_size, square.rank * square_size)
        self.highlighted_image = pygame.image.load(image).convert_alpha()
        self.image = self.normal_image
        self.alpha = self.image.get_alpha()

    def highlight(self):
        self.image = self.highlighted_image

    def un_highlight(self):
        self.image = self.normal_image

    def is_free(self):
        return self.square.is_free()
