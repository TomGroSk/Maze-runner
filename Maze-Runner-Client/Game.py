import sys
import pygame
from pygame.locals import *

from Position import Position2d


class Game:

    windowSize = width, height = 800, 600
    playerPosition = Position2d(400, 300)

    # test only
    player = pygame.image.load("img/hello.png")
    playerrect = player.get_rect()
    # end test only

    def __init__(self):
        pygame.init()
        pygame.key.set_repeat(20)

        self.screen = pygame.display.set_mode(self.windowSize)

    def run(self):
        while 1:
            self.executeGameLogic()

    def executeGameLogic(self):
        # event handling
        self.handleKeyboard()
        # print("x: " + str(self.playerPosition.x) + " y:" + str(self.playerPosition.y))

        # collisions

        # drawing
        self.draw()

    def handleKeyboard(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == K_w:
                    self.playerPosition.y -= 10
                if event.key == K_s:
                    self.playerPosition.y += 10
                if event.key == K_a:
                    self.playerPosition.x -= 10
                if event.key == K_d:
                    self.playerPosition.x += 10

    def draw(self):
        self.screen.fill((0, 0, 0))  # clean screen

        # test only
        self.screen.blit(self.player, (self.playerPosition.x, self.playerPosition.y))
        # test only

        pygame.display.flip()  # display on screen


game = Game()
game.run()
