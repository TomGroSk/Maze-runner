import sys
import pygame
from pygame.locals import *

from Player import Player
from Wall import Wall
from Road import Road

class Game:

    windowSize = width, height = 800, 600
    cameraX, cameraY = -400, -300
    lastPlayerMove = '.'

    def __init__(self):
        pygame.init()
        pygame.key.set_repeat(20)

        self.screen = pygame.display.set_mode(self.windowSize)

        self.players = []
        self.walls = []
        self.roads = []

    def run(self):
        self.loadInitDataFromServer()

        while 1:
            self.executeGameLogic()

    def loadInitDataFromServer(self):  # test
        # load init data from server
            # player id
            # other player data
            # map
        mazeArray = [[False, False, False, False], [True, False, True, False], [False, True, True, False], [True, True, False, True]]
        self.prepareMap(mazeArray)

        self.mainPlayer = Player(1, 0, 0)

    def prepareMap(self, mazeArray):
        x, y = 0, 0
        for row in mazeArray:
            for cell in row:
                if cell:
                    self.walls.append(Wall(y, x))
                self.roads.append(Road(y, x))
                y += 128
            x += 128
            y = 0

    def executeGameLogic(self):
        # load data from server

        self.handleKeyboard()

        self.handleCollision()

        # send data to server

        self.draw()

    def handleKeyboard(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == K_w:
                    self.lastPlayerMove = 'w'
                    self.mainPlayer.move(0, -10)
                    self.cameraY -= 10
                if event.key == K_s:
                    self.lastPlayerMove = 's'
                    self.mainPlayer.move(0, 10)
                    self.cameraY += 10
                if event.key == K_a:
                    self.lastPlayerMove = 'a'
                    self.mainPlayer.move(-10, 0)
                    self.cameraX -= 10
                if event.key == K_d:
                    self.lastPlayerMove = 'd'
                    self.mainPlayer.move(10, 0)
                    self.cameraX += 10

    def handleCollision(self):

        for wall in self.walls:
            if wall.collidedWith(self.mainPlayer.rect):
                if self.lastPlayerMove == 'w':
                    self.mainPlayer.move(0, 10)
                    self.cameraY += 10
                elif self.lastPlayerMove == 's':
                    self.mainPlayer.move(0, -10)
                    self.cameraY -= 10
                elif self.lastPlayerMove == 'a':
                    self.mainPlayer.move(10, 0)
                    self.cameraX += 10
                elif self.lastPlayerMove == 'd':
                    self.mainPlayer.move(-10, 0)
                    self.cameraX -= 10


    def draw(self):
        self.screen.fill((0, 0, 0))  # clean screen

        # roads
        for road in self.roads:
            self.screen.blit(road.sprite, self.remap(road.rect))

        # walls
        for wall in self.walls:
            self.screen.blit(wall.sprite, self.remap(wall.rect))

        # other players
        for player in self.players:
            self.screen.blit(player.sprite, self.remap(player.rect))

        # main player
        self.screen.blit(self.mainPlayer.sprite, self.remap(self.mainPlayer.rect))

        pygame.display.flip()  # display on screen

    def remap(self, rect):
        return rect.x - self.cameraX, rect.y - self.cameraY


game = Game()
game.run()
