import pygame


class SquareGUI(pygame.sprite.Sprite):

    def __init__(self, square, square_size, image):
        super().__init__()
        self.square = square
        self.image = pygame.image.load(image).convert()
        self.image = pygame.transform.scale(self.image, [square_size, square_size])
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(square.file * square_size, square.rank * square_size)
