from socket import *

class Server:
    def __init__(self, IP = "127.0.0.1", PORT = 4000):
        self.__IP = IP
        self.__PORT = PORT
        self.__server = socket(AF_INET, SOCK_STREAM)
        self.__server.bind((self.__IP, self.__PORT))
        self.__clientConns = []
        self.__clientIDs = []
        self.__currentClient = ""

    def connect(self, quantity = 1):
        self.__server.listen(quantity)
        for i in range(quantity):
            conn, addr = self.__server.accept()
            id = conn.recv(1024).decode()
            self.__clientConns.append(conn)
            self.__clientIDs.append(id)
            self.__currentClient = id

    def send(self, message, id = 0):
        if not id:
            id = self.__currentClient
        for i in range(len(self.__clientIDs)):
            if self.__clientIDs[i] == id:
                self.__currentClient = id
                self.__clientConns[i].send(message.encode())

    def receive(self, size = 1024, id = 0):
        if not id:
            id = self.__currentClient
        for i in range(len(self.__clientIDs)):
            if self.__clientIDs[i] == id:
                self.__currentClient = id
                return self.__clientConns[i].recv(size).decode()

    def close(self):
        for conn in self.__clientConns:
            conn.close()
        self.__server.close()