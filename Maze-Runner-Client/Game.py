import sys
import time
import os

import pygame
from pygame.locals import *
import math
import threading

import config
from Player import Player
from Client import Client
from Wall import Wall
from Road import Road
from EndPoint import EndPoint
from Screen import Screen


class Game:
    cameraX, cameraY = -240, -140
    lastPlayerMove = '.'
    running = False
    end = False
    iWin = False

    def __init__(self):
        pygame.init()
        pygame.key.set_repeat(20)
        self.clock = pygame.time.Clock()

        self.screen = pygame.display.set_mode(config.WINDOW_SIZE, DOUBLEBUF)
        self.screen.set_alpha(None)

        self.players = []
        self.walls = []
        self.roads = []

        self.startScreen = Screen("wait.jpg")
        self.loseScreen = Screen("lose.png")
        self.winScreen = Screen("win.png")

    def run(self):
        self.loadInitDataFromServer()

        threading.Thread(target=self.sendPosition, args=()).start()
        threading.Thread(target=self.receiveMesseges, args=()).start()

        while True:
            self.executeGameLogic()

    def loadInitDataFromServer(self):  # test
        try:
            self.client = Client()
        except:
            print("Cannot connect to server :<")
            os._exit(0x01)

        # hello
        self.draw()

        try:
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
                    self.running = True
                    break
                else:
                    raise Exception()
        except:
            print("Fail to load initial data from server")
            os._exit(0x02)

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
                y += config.SIZE_OF_WALL
            x += config.SIZE_OF_WALL
            y = 0

    def executeGameLogic(self):

        dt = self.clock.tick(config.FRAME_RATE) // 1.75

        self.handleKeyboard(dt)

        self.handleCollision(dt)

        self.draw()

    def handleKeyboard(self, dt):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                os._exit(0xDEAD)
            if event.type == pygame.KEYDOWN:
                if event.key == K_w:
                    self.lastPlayerMove = 'w'
                    self.mainPlayer.move(0, -config.PLAYER_SPEED * dt)
                    self.cameraY -= config.PLAYER_SPEED * dt
                if event.key == K_s:
                    self.lastPlayerMove = 's'
                    self.mainPlayer.move(0, config.PLAYER_SPEED * dt)
                    self.cameraY += config.PLAYER_SPEED * dt
                if event.key == K_a:
                    self.lastPlayerMove = 'a'
                    self.mainPlayer.move(-config.PLAYER_SPEED * dt, 0)
                    self.cameraX -= config.PLAYER_SPEED * dt
                if event.key == K_d:
                    self.lastPlayerMove = 'd'
                    self.mainPlayer.move(config.PLAYER_SPEED * dt, 0)
                    self.cameraX += config.PLAYER_SPEED * dt

    def handleCollision(self, dt):
        for wall in self.walls:
            if wall.collidedWith(self.mainPlayer.rect):
                if self.lastPlayerMove == 'w':
                    self.mainPlayer.move(0, config.PLAYER_SPEED * dt)
                    self.cameraY += config.PLAYER_SPEED * dt
                elif self.lastPlayerMove == 's':
                    self.mainPlayer.move(0, -config.PLAYER_SPEED * dt)
                    self.cameraY -= config.PLAYER_SPEED * dt
                elif self.lastPlayerMove == 'a':
                    self.mainPlayer.move(config.PLAYER_SPEED * dt, 0)
                    self.cameraX += config.PLAYER_SPEED * dt
                elif self.lastPlayerMove == 'd':
                    self.mainPlayer.move(-config.PLAYER_SPEED * dt, 0)
                    self.cameraX -= config.PLAYER_SPEED * dt
        if self.endpoint.rect.colliderect(self.mainPlayer.rect):
            self.client.send(b'08', hex(self.mainPlayer.id)[2:].encode().rjust(2, b'0'))

    def draw(self):
        self.screen.fill((0, 0, 0))  # clean screen
        if not self.running:
            self.screen.blit(self.startScreen.sprite, self.calculateCenter(self.startScreen.rect))
        elif not self.end:
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
            if self.iWin:
                self.screen.blit(self.winScreen.sprite, self.calculateCenter(self.winScreen.rect))
            else:
                self.screen.blit(self.loseScreen.sprite, self.calculateCenter(self.loseScreen.rect))

        pygame.display.flip()  # display on screen

    def remap(self, rect):
        return rect.x - self.cameraX, rect.y - self.cameraY

    def calculateCenter(self, rect):
        return (config.WINDOW_SIZE[0] // 2 - rect.width // 2), (config.WINDOW_SIZE[1] // 2 - rect.height // 2)

    def sendPosition(self):
        try:
            while True:
                position = hex(self.mainPlayer.id)[2:].encode().rjust(2, b'0') + \
                           hex(self.mainPlayer.rect.x)[2:].encode().rjust(4, b'0') + \
                           hex(self.mainPlayer.rect.y)[2:].encode().rjust(4, b'0')
                time.sleep(0.05)
                self.client.send(b'06', position)
        except:
            print("Cannot send position to server")
            os._exit(0x03)

    def receiveMesseges(self):
        try:
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
        except:
            print("Cannot receive message from server")
            os._exit(0x04)


game = Game()
game.run()
