import pygame


class GameInfoGUI(pygame.sprite.Sprite):

    def __init__(self, game, top_left_x, top_left_y, width, height, color):
        super().__init__()
        self.game = game
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(top_left_x, top_left_y)
