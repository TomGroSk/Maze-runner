import pygame
import Position


class Wall:

    def __init__(self):
        self.sprite = pygame.image.load("img/wall.png")
        self.rect = self.sprite.get_rect()

    def draw(self, screen, playerPosition):
        screen.blit(self.sprite, (self.rect.x - playerPosition.x, self.rect.y - playerPosition.y))

