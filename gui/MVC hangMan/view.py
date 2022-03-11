
class UI:
    def __init__(self) -> None:
        self._controller = None
        self.gameRunning = True 

    def register(self, controller):
        self._controller = controller
    
    def displayEndGameInfo(self,message, rWord, word):
        print(message)
        print(rWord)
        print(f'The word was {word}')

    def displayGuessedLetters(self):
        gL = self._controller.getGl()
        print(gL)

    def displayReveledWord(self):
        rWord = self._controller.getRword()
        print(rWord)

    def displayGuessesLeft(self):
        print(f'Lives left {str(self._controller.getLivesLeft())}')

    def haveGuess(self):
        guess = input('Please enter a guess > ')
        self._controller.a(guess)

    def mainloop(self):
        while not self._controller.gR():
            self.displayReveledWord()
            self.displayGuessesLeft()
            self.displayGuessedLetters()
            self.haveGuess()