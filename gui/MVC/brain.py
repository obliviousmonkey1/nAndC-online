import pstats

from numpy import exp2, stack

OPERATORS = ['+','-','*','/','^','!']

class CalculatorBrain:
    def __init__(self) -> None:
        self._stack = []
    
    def calculate(self, expression) -> float:
        '''Takes a list of numbers and operators (as strings) 
        as an input and evaluates the expression
        
        Example input: [3, 2, '+', 6, '*'].'''
        # evaluate expression
        # TODO refactor to avoid repetitive code 
        for op in expression:
           if op in OPERATORS:
               self.apply(op)
           else:
               self.push(op)
        # return result
        return self._pop()

    def push(self, value):
        self._stack.append(value)
    
    def _pop(self):
       return self._stack.pop()
    
    def factorial(self):
        pass

    def apply(self, operator) -> None:
        operand2 = self._pop()
        operand1 = self._pop()
        if operator == '+':
            result = operand1 + operand2
        elif operator == '-':
            result = operand1 - operand2
        elif operator == '*':
            result = operand1 * operand2
        elif operator == '/':
            result = operand1 / operand2
        elif operator == '^':
            result = operand1 ** operand2
        elif operator == '!':
            result = self.factorial()

        self.push(result)



# Should write unittest first
#def unittest():
 #   cb = CalculatorBrain()
#    res = cb.calculate([3,2,'**'])
##    assert res == 9.0, "Failure on compilation"


#unittest()