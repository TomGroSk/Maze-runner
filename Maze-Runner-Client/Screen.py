import pygame


class Screen:

    def __init__(self, imgName):
        self.sprite = pygame.image.load("img/" + imgName)
        self.rect = self.sprite.get_rect()
