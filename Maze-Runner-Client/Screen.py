import pygame


class Screen:

    def __init__(self, x, y, imgName):
        self.sprite = pygame.image.load("img/" + imgName)
        self.rect = self.sprite.get_rect()

        self.rect.x = x
        self.rect.y = y
