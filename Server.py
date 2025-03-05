from socket import *
import pyodbc

class Server:
    def __init__(self, IP="127.0.0.1", PORT=4000):
        self.__IP = IP
        self.__PORT = PORT
        self.__server = socket(AF_INET, SOCK_STREAM)
        self.__server.bind((self.__IP, self.__PORT))
        self.__clientConns = []

        self.__conn = pyodbc.connect("Driver={SQL Server};"
                                     "Server=localhost\\SQLEXPRESS;"
                                     "Database=calculator_db;"
                                     "Trusted_Connection=Yes;")
        self.__cursor = self.__conn.cursor()

    def connect(self, quantity=1):
        self.__server.listen(quantity)
        for _ in range(quantity):
            conn, _ = self.__server.accept()
            self.__clientConns.append(conn)
            self.log_action("Клиент подключился")

    def send(self, message, conn):
        self.log_action("Отправил данные на сервер")
        conn.send(message.encode())

    def receive(self, conn):
        return conn.recv(1024).decode()

    def log_action(self, action):
        self.__cursor.execute("INSERT INTO Logs (action) VALUES (?)", action)
        self.__conn.commit()

    def save_history(self, expression, result):
        self.__cursor.execute("INSERT INTO History (expression, result) VALUES (?, ?)", expression, str(result))
        self.__conn.commit()

    def run(self):
        self.connect()
        conn = self.__clientConns[0]
        while True:
            expr = self.receive(conn)
            if expr.lower() == "close":
                self.log_action("Клиент отключился")
                conn.close()
                break
            try:
                result = eval(expr)
                self.save_history(expr, result)
                self.send(str(result), conn)
            except Exception:
                self.send("Ошибка", conn)

    def close(self):
        self.__cursor.close()
        self.__conn.close()
        for conn in self.__clientConns:
            conn.close()
        self.__server.close()


server = Server()
server.run()
