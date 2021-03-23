import pygame

from gui import utils


class PieceGUI(pygame.sprite.Sprite):

    def __init__(self, piece, piece_size, image, rank, file):
        super().__init__()
        self.piece = piece
        self.piece_size = piece_size
        self.image = pygame.image.load(image).convert_alpha()
        self.image = pygame.transform.scale(self.image, [piece_size, piece_size])
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(file * piece_size, rank * piece_size)

    def move_relative(self, vector):
        self.rect.x += vector[0]
        self.rect.y += vector[1]

    def move_to_square(self, square_sprite):
        self.rect.x = square_sprite.rect.x
        self.rect.y = square_sprite.rect.y

    def promote_pawn(self, piece_type, file, rank):
        self.image = pygame.image.load(
            'sprites/{0}.png'.format(utils.piece_to_sprite()[(piece_type, self.piece.color)])
        ).convert_alpha()
        self.image = pygame.transform.scale(self.image, [self.piece_size, self.piece_size])
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(file * self.piece_size, rank * self.piece_size)
