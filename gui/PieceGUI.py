import pygame


class PieceGUI(pygame.sprite.Sprite):

    def __init__(self, piece, piece_size, image, location_square):
        super().__init__()
        self.piece = piece
        self.image = pygame.image.load(image).convert_alpha()
        self.image = pygame.transform.scale(self.image, [piece_size, piece_size])
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(location_square.file * piece_size, location_square.rank * piece_size)

    def move_relative(self, vector):
        self.rect.x += vector[0]
        self.rect.y += vector[1]

    def move_to_square(self, square_sprite):
        self.rect.x = square_sprite.rect.x
        self.rect.y = square_sprite.rect.y
