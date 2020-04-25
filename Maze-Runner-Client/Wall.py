import pygame


class Wall:

    def __init__(self, x, y, sprite):
        self.sprite = sprite
        self.rect = self.sprite.get_rect()

        self.rect.x = x
        self.rect.y = y

    def collidedWith(self, rect):
        return self.rect.colliderect(rect)

