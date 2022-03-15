from cgi import print_arguments
import socket
import pickle
import sys 

HOST = '192.168.0.182'

def displayBoard() -> None:
    s.send(b'ready')
    pickledData = s.recv(1024)
    boardRep = pickle.loads(pickledData)
    print('\n')
    for i in range(3):
        print(boardRep[i])
    s.send(b'complete')

    pickledData = s.recv(1024)
    gameCondition = pickle.loads(pickledData)
    if gameCondition == 1:
        print('Won')
        sys.exit()
    elif gameCondition == 2:
        print('Draw')
        sys.exit()
    elif gameCondition == 3:
        print('Loss')
        sys.exit()

    s.send(b'ready')

def makeMove() -> None:
    valid = False
    move = int(input('> '))
    s.send(pickle.dumps(move))
    while not valid:
        pickledData = s.recv(1024)
        if pickle.loads(pickledData) == 'True':
            valid = True
        elif pickle.loads(pickledData) == 'False':
            print('Invalid Move')
            index = int(input('> '))
            s.send(pickle.dumps(index))


# port logic code
class Port:
    def __init__(self, iP:str, lowerBound=6450, upperBound=6456) -> None:
        self._iP = iP
        self._lowerBound = lowerBound
        self._upperBound = upperBound
   
    def scanForPorts(self):
        port = 0
        for i in range(self._lowerBound, self._upperBound):
            check, client = self.isPortOpen(i)
            if check == 0:
                break

        return client 

    def isPortOpen(self, port):
        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            connection = client.connect_ex((self._iP, port))
            port_opened = connection
            return port_opened, client
        except socket.error as e:
            print(e)

if __name__ == '__main__':
    ports = Port(HOST)
    s = ports.scanForPorts()
    
    print('Connected')
    print('Waiting for other connection ... ')
    print('Game starting')
    with s:
        s.send(b'ready')
        while True:
            a = True 
            while a :
                pickledData = s.recv(1024)
                try:
                    unpickledData = pickle.loads(pickledData)
                    a = False
                except Exception as e :
                    pass
            
            if unpickledData == 1:
                s.send(b'ready')
                makeMove()
                s.recv(1024)
                displayBoard()

                # tells the server that its client twos go 
                s.recv(1024)
                s.send(pickle.dumps(0))
            elif unpickledData == 0:
                s.send(b'ready')

                # wait to ready a message 
                s.recv(1024)
                displayBoard()
