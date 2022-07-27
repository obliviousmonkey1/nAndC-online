import socket
import pickle
import sys

HOST = 'ADD IP'
PORT = 6454
PORT2 = 6452

RANGE = [i for i in range(9)]

board = ['_' for _ in range(9)]
t = 1

'''
naive implementation [static clients] want to eventially dynamically allicate client 1 and client 2 
'''

def sendBoard(rows):
    # recieve ready 
    conn.recv(1024)
    conn2.recv(1024)

    # send board 
    conn.send(pickle.dumps(rows))
    conn2.send(pickle.dumps(rows))

     # checking if the clients are ready to move on 
    conn.recv(1024)
    conn2.recv(1024)

    print('> Succesfully sent clients updated representation of the board')

def updateClientBoard(board):
    rows = []
    row = ''
    for i in range(9):
        if i == 3:
            rows.append(row)
            row = ''
        elif i == 6:
            rows.append(row)
            row = ''
        row += board[i]
    rows.append(row)
    sendBoard(rows)

def validateMove(board, index):
    if board[index] == '_':
        return True
    return False

def loadClientMove(board, index, client):
    valid = False
    
    while not valid:
        if index in RANGE:
            if validateMove(board, index):
                client.send(pickle.dumps('True'))
                board[index] = 'O'
                valid = True 
                print('> Loaded client 1 move to server')

        if valid == False:
            client.send(pickle.dumps('False'))
            #print('INVALID CLIENT MOVE')
            pickledData = client.recv(1024)
            index = pickle.loads(pickledData)
   
def checkWon(board):
    # check for vertical winning positions
    for offset in range(0, 6+1, 3):
        if board[0+offset] == board[1+offset] == board[2+offset] != '_':
            return True 
    # check for horizonal winning positions
    for offset in range(0, 2+1):
        if board[0+offset] == board[3+offset] == board[6+offset] != '_':
            return True 
            
    if board[0] == board[4] == board[8] != '_':
        return True 
    if board[2] == board[4] == board[6] != '_':
        return True 
    return False

def checkDraw(board):
    for i in board:
        if i == '_':
            return False
    return True 

def turn(clientGo, clientWait):
    # tell it to switch to recieving steps
    clientWait.send(pickle.dumps(0))
    # tell client 1 to switch to sending steps
    clientGo.send(pickle.dumps(1))

    # wait to recieve data from client 1
    pickledData = clientGo.recv(1024)
    print('> Recieved board move')
    unpickledData = pickle.loads(pickledData)
    # pass conn to cut down on unnesisary code
    loadClientMove(board, unpickledData, clientGo)
    clientGo.send(b'ready')
    clientWait.send(b'ready')
    print('> Sent ready conformation to clients')
    updateClientBoard(board)

    # check nothing/won/draw [normal:0, win:1, draw:2, loss:3]
    if checkWon(board):
        clientGo.send(pickle.dumps(1))
        clientWait.send(pickle.dumps(3))
        print('> Game concluded server shutting down')
        sys.exit()
    elif checkDraw(board):
        clientGo.send(pickle.dumps(2))
        clientWait.send(pickle.dumps(2))
        print('> Game concluded server shutting down')
        sys.exit()
    clientGo.send(pickle.dumps(0))
    clientWait.send(pickle.dumps(0))

    # wait for conn to send back
    clientGo.recv(1024)
    clientWait.recv(1024)
    print('> Recieved ready confimation from clients')
    print('---------------------------------------')
    clientGo.send(b'ready')

# setting up connection to clients 
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    print('> Client 1 listening')
    s.listen()
    conn, addr = s.accept()
    print(f'2 Connected by {addr}')

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s2:
    s2.bind((HOST, PORT2))
    print('> Client 2 listening')
    s2.listen()
    conn2, addr2 = s2.accept()
    print(f'2 Connected by {addr2}')

# when two are connected starts the game 
with conn, conn2:
    conn.recv(1024)
    conn2.recv(1024)
    conn.send(b'cool')
    conn2.send(b'cool')
    print('---------------------------------------')
    while True:
        # optimize and lower footprint of this code
        a = True 
        if t == 1:
            print('> Waiting for prep message from client 1')
            while a:
                pickledData = conn.recv(1024)
                print('> Recieved prep message from client 1')
                try:
                    unpickledData = pickle.loads(pickledData)
                    a = False
                except Exception as e:
                    print(e)
        elif t == 2:
            print('> Waiting for prep message from client 2')
            while a:
                pickledData = conn2.recv(1024)
                print('> Recieved prep message from client 2')

                try:
                    unpickledData = pickle.loads(pickledData)
                    a = False
                except Exception as e:
                    print(e)

        elif t == 3:
            unpickledData = 1 

        # client 1 move
        if unpickledData == 1:
            t = 1
            turn(conn, conn2)

        # client 2 move 
        elif unpickledData == 0:
            t = 2
            turn(conn, conn2)
           