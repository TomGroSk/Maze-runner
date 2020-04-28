import socket
import threading

from BacteriaSpread import BacteriaSpread
from Cell import Position


class Server:
    socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    numberOfPlayers = 0
    clientHandlerArr = []

    def __init__(self):
        self.map_Layout = BacteriaSpread.generateBooleanMaze(25, 25)
        self.endPoint = BacteriaSpread.generateEndPoint(self.map_Layout, 25)

    def start(self):
        self.socket.bind(("localhost", 6666))
        self.socket.listen()

        while True:
            client, addr = self.socket.accept()
            print("Polaczono z: " + addr[0])
            self.numberOfPlayers += 1
            self.clientHandlerArr.append(threading.Thread(target=self.clientHandler, args=(client, self.numberOfPlayers)))
            if self.numberOfPlayers == 2:
                break
        for c in self.clientHandlerArr:
            c.start()

    def clientHandler(self, client, numberOfPlayers):
        while True:
            response = self.receive(client)
            if response[0] == 0x00:
                data = hex(numberOfPlayers)[2:].encode()
                position = hex(self.endPoint.x)[2:].encode().rjust(2, b'0') + \
                           hex(self.endPoint.y)[2:].encode().rjust(2, b'0')
                self.send(b'01', data, client)
                map = self.parseMap(self.map_Layout)
                self.send(b'02', map, client)
                self.send(b'03', position, client)
                self.send(b'04', hex(self.numberOfPlayers)[2:].encode(), client)
                self.send(b'05', b'', client)

    @staticmethod
    def receive(client):
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
        return int(header[:2], 16), header[10:]

    def send(self, type, data, client):
        msg = type + hex(len(data))[2:].encode().rjust(8, b'0') + data
        client.send(msg)

    def parseMap(self, map):
        bin = b''
        for i in map:
            for j in i:
                if j:
                    bin += b'1'
                else:
                    bin += b'0'
        return bin


server = Server()
server.start()
# data.decode('utf-8')[2:10]
