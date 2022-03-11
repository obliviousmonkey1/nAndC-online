import socket
import pickle
import sys

HOST = '192.168.0.182'
PORT = 6452

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

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    print('Connected')
    print('Waiting for other connection ... ')   
    s.recv(1024)
    print('Game starting')
    while True:
        a = True
        while True:
            pickledData = s.recv(1024)
            unpickledData = pickle.loads(pickledData)
            if unpickledData == 1:
                makeMove()
                s.recv(1024)
                displayBoard()

                # tells the server that its client twos go 
                s.recv(1024)
                s.send(pickle.dumps(1))
            elif unpickledData == 0:

                # wait to ready a message 
                s.recv(1024)
                displayBoard()
            
