from brain import *
from ui import *

class Controller:
    def __init__(self, model, view) -> None:
        self._model = model
        self._view = view
        self._view.register(self)

    def getResult(self, exp):
        res = self._model.calculate(exp)
        self._view.displayAnswer(res)

if __name__ == "__main__":
    cb = CalculatorBrain()
    ui = UI()
    c = Controller(cb, ui)
    ui.mainloop()