import pygame


class SquareGUI(pygame.sprite.Sprite):

    def __init__(self, square, square_size, image):
        super().__init__()
        self.square = square
        self.highlighted_image = pygame.Surface((square_size, square_size))
        self.highlighted_image.fill(pygame.Color("red"))
        self.image = pygame.image.load(image).convert()
        self.image = pygame.transform.scale(self.image, [square_size, square_size])
        self.normal_image = self.image
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(square.file * square_size, square.rank * square_size)

    def highlight(self):
        self.image = self.highlighted_image

    def un_highlight(self):
        self.image = self.normal_image

    def is_free(self):
        return self.square.is_free()
