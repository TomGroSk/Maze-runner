import pygame


class EndPoint:

    def __init__(self, x, y):
        self.sprite = pygame.image.load("img/endpoint.png")
        self.rect = self.sprite.get_rect()

        self.rect.x = x
        self.rect.y = y
