from socket import *
from uuid import uuid4

class Client:
    def __init__(self):
        self.__id = str(uuid4())
        self.__client = socket(AF_INET, SOCK_STREAM)
        self.__isConnected = False

    def connect(self, IP = "127.0.0.1", PORT = 4000):
        self.__client.connect((IP, PORT))
        self.__isConnected = True
        self.__client.send(self.__id.encode())

    def send(self, message):
        if self.__isConnected:
            self.__client.send(message.encode())

    def receive(self, size = 1024):
        if self.__isConnected:
            return self.__client.recv(size).decode()

    def close(self):
        self.send("close")
        self.__client.close()
        self.__isConnected = False