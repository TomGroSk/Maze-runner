import pygame


class Road:

    def __init__(self, x, y):
        self.sprite = pygame.image.load("img/ground.png")
        self.rect = self.sprite.get_rect()

        self.rect.x = x
        self.rect.y = y
