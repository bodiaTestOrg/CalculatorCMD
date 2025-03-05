class Calc():
    def __init__(self):
        self.history = []

    def calculate(self, mathString: str):
        try:
            result = eval(mathString)
            self.history.append(result)
            return result
        except Exception:
            return 'Ошибка'

calc = Calc()

while True:
    expr = input('Введите выражение (или "exit" для выхода): ')
    if expr.lower() == 'exit':
        break
    print('Результат:', calc.calculate(expr))
