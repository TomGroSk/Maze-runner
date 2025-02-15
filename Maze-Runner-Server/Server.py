import os
import socket
import threading
import queue
import time

import config
from BacteriaSpread import BacteriaSpread
from sekurak import SecurityDispatcher

class Server:
    socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    numberOfPlayers = 0
    clientHandlerArr = []
    clientSockets = []
    positionQueue = queue.Queue()
    resetGame = False
    securityDispatcher = SecurityDispatcher()

    def __init__(self):
        self.map_Layout = BacteriaSpread.generateBooleanMaze(config.MAP_SIZE[0], config.MAP_SIZE[1])
        self.endPoint = BacteriaSpread.generateEndPoint(self.map_Layout, config.END_POINT_PERCENT)

    def start(self):
        self.socket.bind(("localhost", 6666))
        self.socket.listen()

        while True:
            try:
                client, addr = self.socket.accept()
            except:
                print("Failed to accept client")
                continue
            print("Polaczono z: " + addr[0])
            self.numberOfPlayers += 1
            self.clientSockets.append(client)
            self.clientHandlerArr.append(threading.Thread(target=self.clientHandler,
                                                          args=(client, self.numberOfPlayers)))
            if self.numberOfPlayers == config.MAX_PLAYERS:
                break
        for c in self.clientHandlerArr:
            c.start()
        threading.Thread(target=self.sendToAll, args=()).start()

    def clientHandler(self, client, playerID):
        try:
            while True:
                response = self.receive(client)
                if response[0] == 0x00:
                    self.playerInitProtocol(client, playerID)
                elif response[0] == 0x06:
                    self.positionQueue.put(response[1])
                elif response[0] == 0x08:
                    data = hex(playerID)[2:].encode().rjust(2, b'0')
                    self.sendEndGameToAll(data)
                    time.sleep(7)
                    os._exit(0xDEAD)
        except:
            print("Lost connection with client: " + str(playerID))
            self.numberOfPlayers -= 1
            client.close()

    def playerInitProtocol(self, client, playerID):
        data = hex(playerID)[2:].encode()
        position = hex(self.endPoint.x)[2:].encode().rjust(2, b'0') + \
                   hex(self.endPoint.y)[2:].encode().rjust(2, b'0')
        binaryMap = self.parseMap(self.map_Layout)
        self.send(b'01', data, client)
        self.send(b'02', binaryMap, client)
        self.send(b'03', position, client)
        self.send(b'04', hex(self.numberOfPlayers)[2:].encode(), client)
        self.send(b'05', b'', client)

    def receive(self, client):
        dataCollection = []
        content_Length = 10
        while True:
            data = client.recv(1)
            dataCollection.append(data)
            if len(dataCollection) == 10:
                header = (b"".join(i for i in dataCollection))
                content_Length = int(header[2:10], 16) + 10
            if len(dataCollection) == content_Length:
                break
        header = (b"".join(i for i in dataCollection))
        decryptedHeader = self.securityDispatcher.decrypt(header[10:])
        return int(header[:2], 16), decryptedHeader

    def send(self, msgType, data, client):
        encryptedData = self.securityDispatcher.encrypt(data)
        msg = msgType + hex(len(encryptedData))[2:].encode().rjust(8, b'0') + encryptedData
        client.send(msg)

    def sendToAll(self):
        while True:
            item = self.positionQueue.get()
            self.positionQueue.task_done()
            for i in self.clientSockets:
                try:
                    self.send(b'07', item, i)
                except:
                    print("Failed to send data to client.")
                    self.clientSockets.remove(i)

    def sendEndGameToAll(self, num_id):
        for i in self.clientSockets:
            self.send(b'09', num_id, i)

    @staticmethod
    def parseMap(mapLayout):
        binMap = b''
        for i in mapLayout:
            for j in i:
                if j:
                    binMap += b'1'
                else:
                    binMap += b'0'
        return binMap


server = Server()
server.start()
# data.decode('utf-8')[2:10]
