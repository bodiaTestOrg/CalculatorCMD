import pyodbc
from datetime import datetime

class DbManager:
    def __init__(self, dsn):
        self.dsn = dsn
        self.conn = pyodbc.connect(self.dsn)
        self.cursor = self.conn.cursor()

    def saveActions(self, history):
        for action in history:
            action_time, action_expression, action_result = action
            if action_expression == "Start of session" or action_expression == "End of session":
                self.saveLog(action_expression, action_time)
            else:
                self.saveHistory(action_expression, action_result, action_time)

    def saveLog(self, action, action_time):
        query = "INSERT INTO Logs (ACTION, TIME) VALUES (?, ?)"
        self.cursor.execute(query, (action, action_time))
        self.conn.commit()

    def saveHistory(self, expression, result, action_time):
        query = "INSERT INTO History (EXPRESSION, RESULT, TIME) VALUES (?, ?, ?)"
        self.cursor.execute(query, (expression, result, action_time))
        self.conn.commit()

    def getLogs(self):
        self.cursor.execute("SELECT * FROM Logs")
        return self.cursor.fetchall()

    def getHistory(self):
        self.cursor.execute("SELECT * FROM History")
        return self.cursor.fetchall()

    def close(self):
        self.conn.close()
