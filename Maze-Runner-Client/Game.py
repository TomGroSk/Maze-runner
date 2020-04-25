import sys
import pygame
from pygame.locals import *

from Player import Player
from Wall import Wall
from Road import Road

sys.path.insert(0, '../Maze-Runner-Server')
from BacteriaSpread import BacteriaSpread


class Game:
    windowSize = width, height = 800, 600
    cameraX, cameraY = -240, -140
    lastPlayerMove = '.'
    playerSpeed = 10
    sizeOfWall = 128
    framerate = 60

    def __init__(self):
        self.mainPlayer = Player(1, 160, 160)
        pygame.init()
        pygame.key.set_repeat(20)
        self.clock = pygame.time.Clock()

        self.screen = pygame.display.set_mode(self.windowSize, DOUBLEBUF)

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

        mazeArray = BacteriaSpread.generateBooleanMaze(25, 25)
        self.prepareMap(mazeArray)

    def prepareMap(self, mazeArray):
        x, y = 0, 0
        spriteWall = pygame.image.load("img/wall.png")
        spriteRoad = pygame.image.load("img/ground.png")
        for row in mazeArray:
            for cell in row:
                if cell:
                    self.walls.append(Wall(y, x, spriteWall))
                self.roads.append(Road(y, x, spriteRoad))
                y += self.sizeOfWall
            x += self.sizeOfWall
            y = 0

    def executeGameLogic(self):
        # load data from server

        self.handleKeyboard()

        self.handleCollision()

        # send data to server

        self.clock.tick(self.framerate)

        self.draw()

    def handleKeyboard(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == K_w:
                    self.lastPlayerMove = 'w'
                    self.mainPlayer.move(0, -self.playerSpeed)
                    self.cameraY -= self.playerSpeed
                if event.key == K_s:
                    self.lastPlayerMove = 's'
                    self.mainPlayer.move(0, self.playerSpeed)
                    self.cameraY += self.playerSpeed
                if event.key == K_a:
                    self.lastPlayerMove = 'a'
                    self.mainPlayer.move(-self.playerSpeed, 0)
                    self.cameraX -= self.playerSpeed
                if event.key == K_d:
                    self.lastPlayerMove = 'd'
                    self.mainPlayer.move(self.playerSpeed, 0)
                    self.cameraX += self.playerSpeed

    def handleCollision(self):

        for wall in self.walls:
            if wall.collidedWith(self.mainPlayer.rect):
                if self.lastPlayerMove == 'w':
                    self.mainPlayer.move(0, self.playerSpeed)
                    self.cameraY += self.playerSpeed
                elif self.lastPlayerMove == 's':
                    self.mainPlayer.move(0, -self.playerSpeed)
                    self.cameraY -= self.playerSpeed
                elif self.lastPlayerMove == 'a':
                    self.mainPlayer.move(self.playerSpeed, 0)
                    self.cameraX += self.playerSpeed
                elif self.lastPlayerMove == 'd':
                    self.mainPlayer.move(-self.playerSpeed, 0)
                    self.cameraX -= self.playerSpeed

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
