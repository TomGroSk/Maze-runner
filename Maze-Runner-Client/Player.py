import pygame


class Player:
    id = -1

    def __init__(self, id, x, y):
        self.id = id

        self.sprite = pygame.image.load("img/win.png") #("img/player" + str(id) + ".png")
        self.rect = self.sprite.get_rect()

        self.rect.x = x
        self.rect.y = y

    def setPosition(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def move(self, x, y):
        self.rect.x += x
        self.rect.y += y
