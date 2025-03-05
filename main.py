from fakeEnv import dsn
from datetime import datetime
from db_manager import DbManager


class Calc():
    def __init__(self):
        self.history = []

    def calculate(self, mathString: str):
        result = eval(mathString)
        self.history.append((datetime.now(), mathString, result))
        return result


class extendetCalc(Calc):
    def __init__(self):
        super().__init__()
        self.dbManager = DbManager(dsn)

    def start(self):
        self.history.append((datetime.now(), "Start of session", None))
        self.dbManager.saveActions(self.history)
        return True

    def end(self):
        self.history.append((datetime.now(), "End of session", None))
        self.dbManager.saveActions(self.history)

    def getLogs(self):
        return self.dbManager.getLogs()

    def getHistory(self):
        return self.dbManager.getHistory()

    def calculate(self, mathString: str):
        result = super().calculate(mathString)
        self.dbManager.saveActions(self.history)
        return result


def main():
    calc = extendetCalc()

    calc.start()

    while True:
        user_input = input("Введите выражение (или 'exit' для выхода): ")

        if user_input.lower() == 'exit':
            print("Сессия завершена.")
            break

        try:
            result = calc.calculate(user_input)
            print(f"Результат: {result}")
        except Exception as e:
            print(f"Ошибка при вычислении: {e}")

    logs = calc.getLogs()
    history = calc.getHistory()

    print("\nLogs:")
    for log in logs:
        print(log)

    print("\nHistory:")
    for record in history:
        print(record)
    calc.end()
    calc.dbManager.close()


if __name__ == "__main__":
    main()
