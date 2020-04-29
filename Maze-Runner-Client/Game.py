import sys
import time
import os

import pygame
from pygame.locals import *
import math
import threading

from Player import Player
from Client import Client
from Wall import Wall
from Road import Road
from EndPoint import EndPoint
from Screen import Screen


class Game:
    windowSize = width, height = 800, 600
    cameraX, cameraY = -240, -140
    lastPlayerMove = '.'
    playerSpeed = 1
    sizeOfWall = 128
    framerate = 60
    end = False
    iWin = False

    def __init__(self):
        pygame.init()
        pygame.key.set_repeat(20)
        self.clock = pygame.time.Clock()

        self.screen = pygame.display.set_mode(self.windowSize, DOUBLEBUF)
        self.screen.set_alpha(None)

        self.players = []
        self.walls = []
        self.roads = []

    def run(self):
        self.loadInitDataFromServer()

        threading.Thread(target=self.sendPosition, args=()).start()
        threading.Thread(target=self.receiveMesseges, args=()).start()

        while True:
            self.executeGameLogic()

    def loadInitDataFromServer(self):  # test
        self.client = Client()

        # hello
        self.client.send(b'00', b'')
        while True:
            msg = self.client.receive()
            if msg[0] == 0x01:  # whoami
                self.setPlayer(msg)
            elif msg[0] == 0x02:  # map
                self.setMap(msg)
            elif msg[0] == 0x03:  # endpoint
                self.setEndPoint(msg)
            elif msg[0] == 0x04:  # players
                self.setOtherPlayers(msg)
            elif msg[0] == 0x05:  # start
                break
            else:
                raise Exception()

    def setPlayer(self, msg):
        nr = int(msg[1].decode(), 16)
        self.mainPlayer = Player(nr, 160, 160)

    def setOtherPlayers(self, msg):
        number = int(msg[1].decode(), 16)
        for i in range(1, number + 1):
            if not self.mainPlayer.id == i:
                self.players.append(Player(i, 160, 160))

    def setEndPoint(self, msg):
        posX = int(msg[1][:2].decode(), 16)
        posY = int(msg[1][2:].decode(), 16)
        self.endpoint = EndPoint(posY * 128, posX * 128)

    def setMap(self, msg):
        mazeSize = int(math.sqrt(len(msg[1])))
        booleanArray = [[True for x in range(mazeSize)] for y in range(mazeSize)]
        for i in range(mazeSize):
            for j in range(mazeSize):
                if msg[1][i * mazeSize + j] == ord('0'):
                    booleanArray[i][j] = False
        self.prepareMap(booleanArray)

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

        dt = self.clock.tick(self.framerate) // 1.75

        self.handleKeyboard(dt)

        self.handleCollision(dt)

        self.draw()

    def handleKeyboard(self, dt):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == K_w:
                    self.lastPlayerMove = 'w'
                    self.mainPlayer.move(0, -self.playerSpeed * dt)
                    self.cameraY -= self.playerSpeed * dt
                if event.key == K_s:
                    self.lastPlayerMove = 's'
                    self.mainPlayer.move(0, self.playerSpeed * dt)
                    self.cameraY += self.playerSpeed * dt
                if event.key == K_a:
                    self.lastPlayerMove = 'a'
                    self.mainPlayer.move(-self.playerSpeed * dt, 0)
                    self.cameraX -= self.playerSpeed * dt
                if event.key == K_d:
                    self.lastPlayerMove = 'd'
                    self.mainPlayer.move(self.playerSpeed * dt, 0)
                    self.cameraX += self.playerSpeed * dt

    def handleCollision(self, dt):

        for wall in self.walls:
            if wall.collidedWith(self.mainPlayer.rect):
                if self.lastPlayerMove == 'w':
                    self.mainPlayer.move(0, self.playerSpeed * dt)
                    self.cameraY += self.playerSpeed * dt
                elif self.lastPlayerMove == 's':
                    self.mainPlayer.move(0, -self.playerSpeed * dt)
                    self.cameraY -= self.playerSpeed * dt
                elif self.lastPlayerMove == 'a':
                    self.mainPlayer.move(self.playerSpeed * dt, 0)
                    self.cameraX += self.playerSpeed * dt
                elif self.lastPlayerMove == 'd':
                    self.mainPlayer.move(-self.playerSpeed * dt, 0)
                    self.cameraX -= self.playerSpeed * dt

        if self.endpoint.rect.colliderect(self.mainPlayer.rect):
            self.client.send(b'08', hex(self.mainPlayer.id)[2:].encode().rjust(2, b'0'))

    def draw(self):
        self.screen.fill((0, 0, 0))  # clean screen

        if not self.end:
            # roads
            for road in self.roads:
                self.screen.blit(road.sprite, self.remap(road.rect))

            # walls
            for wall in self.walls:
                self.screen.blit(wall.sprite, self.remap(wall.rect))

            self.screen.blit(self.endpoint.sprite, self.remap(self.endpoint.rect))

            # other players
            for player in self.players:
                self.screen.blit(player.sprite, self.remap(player.rect))

            # main player
            self.screen.blit(self.mainPlayer.sprite, self.remap(self.mainPlayer.rect))
        else:
            print(self.iWin)
            # todo print img

        pygame.display.flip()  # display on screen

    def remap(self, rect):
        return rect.x - self.cameraX, rect.y - self.cameraY

    def sendPosition(self):
        while True:
            position = hex(self.mainPlayer.id)[2:].encode().rjust(2, b'0') + \
                       hex(self.mainPlayer.rect.x)[2:].encode().rjust(4, b'0') + \
                       hex(self.mainPlayer.rect.y)[2:].encode().rjust(4, b'0')
            time.sleep(0.05)
            self.client.send(b'06', position)

    def receiveMesseges(self):
        while True:
            msg = self.client.receive()

            if msg[0] == 0x07:
                playerId = int(msg[1][:2].decode(), 16)
                posX = int(msg[1][2:6].decode(), 16)
                posY = int(msg[1][6:].decode(), 16)
                for p in self.players:
                    if p.id == playerId:
                        p.setPosition(posX, posY)
            elif msg[0] == 0x09:
                winPlayerId = int(msg[1].decode(), 16)
                if self.mainPlayer.id == winPlayerId:
                    self.iWin = True
                else:
                    self.iWin = False
                self.end = True
                time.sleep(5)
                os._exit(0xdead)


game = Game()
game.run()
