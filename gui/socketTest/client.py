import socket
import pickle

HOST = "ADD IP"  # The server's hostname or IP address
PORT = 65434  # The port used by the server
t = 0
turn_order = 0

def displayBoard(boardRep):
    for i in range(3):
        print(boardRep[i])

# make move should 
def makeMove():
    # 0-8
    valid = False

    index = int(input('> '))
    #print('prepping data for transfer')
    # tells the server that data is incoming, and then waits till server ready,
    # and then sends data
    s.recv(1024)
    s.send(pickle.dumps(index))
    #print('data sent')

    while not valid:
        pickledData = s.recv(1024)
        if pickle.loads(pickledData) == 'True':
            #print('data valid')
            valid = True
        elif pickle.loads(pickledData) == 'False':
            print('Invalid Move')
            index = int(input('> '))
            s.send(pickle.dumps(index))

    #print('input valid')
    s.send(b'valid')

def display():
    # tells the server that it is ready to recieve data 
    s.send(b'ready')
    pickledData = s.recv(1024)
    #print('data recieved')
    unpickledData = pickle.loads(pickledData)
    displayBoard(unpickledData)
    #print('data loaded')

    # tells the server that the data it got sent has been processed
    # and that it can now move on 
    s.send(b'loaded')

    # server checking if won 
    pickledData =  s.recv(1024)
    unpickledData = pickle.loads(pickledData)
    if unpickledData == 0:
        print('Draw')
    elif unpickledData == 1:
        print('You loose')
    elif unpickledData == 2:
        print('You won')
    

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.send(pickle.dumps(1))
    while True:
        t += 1
        pickledData = s.recv(1024)
        unpickledData = pickle.loads(pickledData)
        if unpickledData == 1:
            #print('make move')
            s.send(pickle.dumps(0))
            makeMove()
            # waits till server is ready 
            display()
            #s.recv(1024)
            #print('server jobs complete')
            #s.recv(1024)
            s.recv(1024)
            s.send(pickle.dumps(1))
            

        elif unpickledData == 0:
            #print('display board')
            display()
            s.send(b'ready')

        print(f'next round {t}')
            
        
