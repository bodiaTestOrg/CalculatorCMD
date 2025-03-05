from fakeEnv import dsn
from datetime import datetime
from db_manager import DbManager


class Calc():
    def __init__(self):
        self.history = []

    def calculate(self, mathString: str):
        result = eval(mathString)
        self.history.append((datetime.now(), result))
        return result


class extendetCalc(Calc):
    def __init__(self):
        super().__init__()
        self.dsn = dsn
        self.dbManager = DbManager()

    def start(self):
        self.history.append((datetime.now(), "Start of session"))
        return True

    def end(self):
        self.history.append((datetime.now(), "End of session"))
        self.dbManager.saveActions(self.dsn, self.history)
        return True

    def getLogs(self):
        return self.dbManager.getLogs(self.dsn)
