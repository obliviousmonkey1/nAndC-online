from random import randint

class Hangman:
    def __init__(self):
        self.setWord()
        self.revealedWord = '*' * len(self.word)
        self.guessesLeft = 10
        self.guessedLetters = []

    def setWord(self):
        chance = 0.05
        with open('/Users/parzavel/Documents/alevel/graphical user interface/MVC hangMan/wordList.txt') as file:
            lines = file.readlines()
            for line in lines:
                if (randint(0, 851)/851) < chance:
                    self.word = line
                    break

    def haveGuess(self, letter):
        if letter in self.guessedLetters:
            return None
       
        self.guessesLeft -= 1
        inWord = False
        for idx, ch in enumerate(self.word):
            if ch == letter:
                inWord = True
                self.revealedWord = self.revealedWord[:idx] + ch + self.revealedWord[idx+1:]
        
        return inWord

    def isGameOver(self):
        return self.guessesLeft == 0 or self.hasGuessedAll()

    def hasGuessedAll(self):
        return not '*' in self.revealedWord
