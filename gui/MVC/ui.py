
class UI:
    def __init__(self) -> None:
        self._controller = None

    def register(self, controller):
        self._controller = controller

    def calculateAnswer(self):
        rpn = input(">>> ")
        if rpn == "q":
            return False
        rpnList = self.convert(rpn)
        # eventually call calculate sub in brain
        answer = self._controller.getResult(rpnList)
        return True 
    
    def convert(self, rpn):
        '''convert a space-seperatd string into a list of floats (operands)
        and strings (operators)
        '''
        rpnAsConvertedList = []
        for exp in rpn:
            if exp in ['+','-','*','/','^','!']:
                rpnAsConvertedList.append(exp)
            else:
                rpnAsConvertedList.append(float(exp))
        return rpnAsConvertedList

    def displayAnswer(self, exp):
        print(exp)

    def mainloop(self):
        while True:
            carryOn = self.calculateAnswer()
            if not carryOn:
                break
