import pygame


class Road:

    def __init__(self, x, y, sprite):
        self.sprite = sprite
        self.rect = self.sprite.get_rect()

        self.rect.x = x
        self.rect.y = y
