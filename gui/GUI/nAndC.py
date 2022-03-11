from tkinter import BOTTOM, END, RIGHT, Tk, Text, TOP, BOTH, X, N, LEFT, RAISED, W, E, CENTER, ALL, DISABLED, NORMAL
from tkinter.ttk import Frame, Label, Entry, Style, Button

class Test(Frame):
    def __init__(self) -> None:
        super().__init__()
        self.board = ['_' for i in range(9)]
        self.turn = 1
        self.delay = 100
        self.player = 1

        self.invalidPosition = False
        self.invalidInput = False
        self.invalidPositionTracker = 0
        self.invalidInputTracker = 0

        self.won = False
        self.draw = False

        # changeable variables 
        self.zeroStartIndex = False   
        self.positionBoard = True  


        self.initUI()
    
    def initUI(self):
        self.master.title(f"Noughts and Crosses")
        self.style = Style()
        self.style.theme_use("default")

        self.frame = Frame(self, relief=RAISED, borderwidth=1)
        self.frame.pack(fill=BOTH, expand=True)

        self.frame1 = Frame(self)
        self.frame1.pack(fill=X)

        self.pack(fill=BOTH, expand=True)

        #self.frame.columnconfigure(0, pad=3)

        self.frame.columnconfigure(0, pad=20)
        self.frame.columnconfigure(1, pad=20)
        self.frame.columnconfigure(2, pad=20)

        self.frame.rowconfigure(0, pad=20)
        self.frame.rowconfigure(1, pad=20)
        self.frame.rowconfigure(2, pad=20)
      
        if self.zeroStartIndex:
            self.offset = 0
        else:
            self.offset = 1
        
        self.range = [i+self.offset for i in range(9)]

        if self.positionBoard == True:
            self.lblHolder = [Label(self.frame, text=f"{i+self.offset}", width=6) for i in range(9)]
        else:
            self.lblHolder = [Label(self.frame, text="_", width=6) for _ in range(9)]

        r = 0 
        c = 0 
        #lblHolder[1] = Label(frame, text="X", width=6)
        for label in self.lblHolder:
            if c % 3 == 0:
                r += 1
                c = 0
            label.grid(row=r, column=c)
            c += 1
       # lbl1.grid(row=0, column=0)

        self.master.title(f"Player : {self.player}")
        lbl2 = Label(self.frame1, text=f"Input [{self.offset}-{self.offset+8}] :", width=8)
        lbl2.pack(side=LEFT, padx=5, pady=5)

        self.move = Entry(self.frame1)
        self.move.pack(fill=X, padx=5, expand=True)
        #self.move.pack(side=TOP, padx=5, pady=5)
    
        self.inputButton = Button(self, text="Input :", command=lambda : self.makeMove())
        self.resetButton = Button(self, text="Reset Board", command=lambda : self.reset())
        self.resetButton['state'] = DISABLED
        self.inputButton.pack(side=LEFT, padx=5, pady=5)
        self.resetButton.pack(side=RIGHT, padx=5, pady=5)

    def isInt(self, a):
        try:
            int(a)
        except:
            return False
        return True 

    def makeMove(self):
        a = self.move.get()
        if self.isInt(a) and int(a) in self.range:
            if self.turn %2 == 0:
                if self.board[int(a)-self.offset] == '_':
                    self.lblHolder[int(a)-self.offset] = Label(self.frame, text="X", width=6, font='Helvetica 15 bold')
                    self.board[int(a)-self.offset] = 'X'
                    self.turn += 1 

                else:
                    self.invalidPosition = True 
                    self.invalidPositionTracker +=1
                    
            elif self.turn % 2 != 0:
                if self.board[int(a)-self.offset] == '_':
                    self.lblHolder[int(a)-self.offset] = Label(self.frame, text="O", width=6,font='Helvetica 15 bold')
                    self.board[int(a)-self.offset] = 'O'
                    self.turn += 1 

                else:
                    self.invalidPosition = True 
                    self.invalidPositionTracker +=1
            
            self.checkWon()
            self.checkDraw()
        else:
            self.invalidInput = True 
            self.invalidInputTracker +=1


        self.after(self.delay, self.updateWindow())

    def checkWon(self):
         # check for vertical winning positions
        for offset in range(0, 6+1, 3):
            if self.board[0+offset] == self.board[1+offset] == self.board[2+offset] != '_':
                self.won = True

        # check for horizonal winning positions
        for offset in range(0, 2+1):
            if self.board[0+offset] == self.board[3+offset] == self.board[6+offset] != '_':
                self.won = True
        if self.board[0] == self.board[4] == self.board[8] != '_':
            self.won = True 
        if self.board[2] == self.board[4] == self.board[6] != '_':
            self.won = True 

    def checkDraw(self):
        self.draw = True  
        for i in self.board:
            if i == '_':
                self.draw = False
                break
    
    def reset(self):
        self.board = ['_' for i in range(9)]
        self.turn = 1
        self.player = 2
        self.won = False
        self.draw = False     
        if self.positionBoard == True:
            self.lblHolder = [Label(self.frame, text=f"{i+self.offset}", width=6) for i in range(9)]
        else:
            self.lblHolder = [Label(self.frame, text="_", width=6) for _ in range(9)]
        self.resetButton['state'] = DISABLED
        self.inputButton['state'] = NORMAL
        self.updateWindow()


    def updateWindow(self):
        r = 0 
        c = 0 
        #lblHolder[1] = Label(frame, text="X", width=6)
        for label in self.lblHolder:
            if c % 3 == 0:
                r += 1
                c = 0
            label.grid(row=r, column=c)
            c += 1
        
        if self.won == True:
            self.master.title(f"Player : {self.player} has Won the game")
            self.resetButton['state'] = NORMAL
            self.inputButton['state'] = DISABLED

        elif self.draw == True:
            self.master.title(f'Draw')
            self.resetButton['state'] = NORMAL
            self.inputButton['state'] = DISABLED
        elif self.invalidPosition == False and self.invalidInput == False:
            if self.player == 1:
                self.player = 2
            else:
                self.player = 1

            self.master.title(f"Player : {self.player}")
            self.invalidInputTracker = 0 
            self.invalidPositionTracker = 0

        elif self.invalidPosition == True:
            self.master.title(f"Player : {self.player} Invalid Move {self.invalidPositionTracker}, Bitch")
            self.invalidPosition = False
        elif self.invalidInput == True:
            self.master.title(f"Player : {self.player} Invalid Input {self.invalidInputTracker}, Bitch")
            self.invalidInput = False
        
        self.move.delete(0, END)


       
def main():
    root = Tk()
    root.geometry("300x200+300+300") 
    app = Test()
    root.mainloop()


if __name__ == "__main__":
    main()