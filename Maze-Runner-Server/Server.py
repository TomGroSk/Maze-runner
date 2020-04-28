import socket
import threading


class Server:
    socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start(self):
        self.socket.bind(("localhost", 6666))
        self.socket.listen()
        while True:
            client, addr = self.socket.accept()
            print("Polaczono z: " + addr[0])
            x = threading.Thread(target=self.clientHandler, args=(client,))
            x.start()

    def clientHandler(self, client):
        pass

    @staticmethod
    def receive(client):
        dataCollection = []
        content_Length = 10
        while True:
            data = client.recv(1)
            dataCollection.append(data)
            if len(dataCollection) == 10:
                header = (b"".join(i for i in dataCollection))
                content_Length = int(header[2:10], 16)+10
            if len(dataCollection) == content_Length:
                break
        header = (b"".join(i for i in dataCollection))
        return int(header[:2], 16), header[10:]


server = Server()
server.start()
#data.decode('utf-8')[2:10]