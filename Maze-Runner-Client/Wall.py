import pygame


class Wall:

    def __init__(self, x, y):
        self.sprite = pygame.image.load("img/wall.png")
        self.rect = self.sprite.get_rect()

        self.rect.x = x
        self.rect.y = y

    def collidedWith(self, rect):
        return self.rect.colliderect(rect)

