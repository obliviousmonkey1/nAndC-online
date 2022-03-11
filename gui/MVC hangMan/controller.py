
from model import *
from view import *

class Controller:
    def __init__(self, model, view) -> None:
        self._model = model
        self._view = view
        self._view.register(self)
    
    def a(self, guess):
        a = self._model.haveGuess(guess)
        if a != None:
            self._model.guessedLetters.append(guess)

        if self._model.hasGuessedAll():
            self._view.displayEndGameInfo('won',self.getRword(), self._model.word)

        if self._model.guessesLeft == 0:
            self._view.displayEndGameInfo('better luck next time', self.getRword(), self._model.word)

    def gR(self):
        return self._model.isGameOver()

    def getLivesLeft(self) -> int:
        return self._model.guessesLeft

    def getRword(self):
        return self._model.revealedWord

    def getGl(self):
        return self._model.guessedLetters

while __name__ == '__main__':
    model = Hangman()
    view = UI()
    c = Controller(model, view)
    view.mainloop()
    break

