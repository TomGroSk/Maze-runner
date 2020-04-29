import socket

from sekurak import SecurityDispatcher


class Client:
    socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    securityDispatcher = SecurityDispatcher()

    def __init__(self):
        self.socket.connect(('localhost', 6666))

    def receive(self):
        dataCollection = []
        content_Length = 10
        while True:
            data = self.socket.recv(1)
            dataCollection.append(data)
            if len(dataCollection) == 10:
                header = (b"".join(i for i in dataCollection))
                content_Length = int(header[2:10], 16) + 10
            if len(dataCollection) == content_Length:
                break
        header = (b"".join(i for i in dataCollection))
        decryptedHeader = self.securityDispatcher.decrypt(header[10:])
        return int(header[:2], 16), decryptedHeader

    def send(self, msgType, data):
        encryptedData = self.securityDispatcher.encrypt(data)
        msg = msgType + hex(len(encryptedData))[2:].encode().rjust(8, b'0') + encryptedData
        self.socket.send(msg)
