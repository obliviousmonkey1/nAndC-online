import socket
import pickle

HOST = '192.168.0.182'
PORT = 6454

def displayBoard() -> None:
    s.send(b'ready')
    pickledData = s.recv(1024)
    boardRep = pickle.loads(pickledData)
    for i in range(3):
        print(boardRep[i])
    s.send(b'complete')

    # check nothing/win/loss/draw

def makeMove() -> None:
    move = int(input('> '))
    s.send(pickle.dumps(move))

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    print('connected')
    s.send(pickle.dumps(1))
    while True:
        a = True 
        while a :
            pickledData = s.recv(1024)
            print('recieved prep messgae')
            try:
                unpickledData = pickle.loads(pickledData)
                a = False
            except Exception as e :
                print(e)
        
        if unpickledData == 1:
            makeMove()
            s.recv(1024)
            displayBoard()

            # tells the server that its client twos go 
            s.recv(1024)
            s.send(pickle.dumps(0))
        elif unpickledData == 0:

            # wait to ready a message 
            s.recv(1024)
            displayBoard()
