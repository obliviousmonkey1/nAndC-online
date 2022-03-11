import socket
import pickle
import sys 

HOST = '192.168.0.182'
PORT = 6454
PORT2 = 6451

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

    print('succesfully sent clients updated representation of the board')

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
    if client == 1:
        while not valid:
            if index in RANGE:
                if validateMove(board, index):
                    conn.send(pickle.dumps('True'))
                    board[index] = 'O'
                    valid = True 
                    print('loaded client 1 move to server board')

                else:
                    conn.send(pickle.dumps('False'))
                    #print('INVALID CLIENT MOVE')
                    pickledData = conn.recv(1024)
                    index = pickle.loads(pickledData)
            else:
                conn.send(pickle.dumps('False'))
                #print('INVALID CLIENT MOVE')
                pickledData = conn.recv(1024)
                index = pickle.loads(pickledData)
    else:
        while not valid:
            if index in RANGE:
                if validateMove(board, index):
                    conn2.send(pickle.dumps('True'))
                    board[index] = 'X'
                    valid = True 
                    print('loaded client 2 move to server board')
                else:
                    conn2.send(pickle.dumps('False'))
                    #print('INVALID CLIENT MOVE')
                    pickledData = conn2.recv(1024)
                    index = pickle.loads(pickledData)
            else:
                conn2.send(pickle.dumps('False'))
                #print('INVALID CLIENT MOVE')
                pickledData = conn2.recv(1024)
                index = pickle.loads(pickledData)
    
    return board 



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

# setting up connection to clients 
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    print(f'1 Connected by {addr}')

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s2:
    s2.bind((HOST, PORT2))
    s2.listen()
    conn2, addr2 = s2.accept()
    print(f'2 Connected by {addr2}')

# when two are connected starts the game 
with conn, conn2:
    conn2.send(b'ready')
    while True:
        a = True 
        if t == 1:
            print('waiting for prep message from client 1')
            while a:
                pickledData = conn.recv(1024)
                print('recieved prep message from client 1')
                try:
                    unpickledData = pickle.loads(pickledData)
                    a = False
                except Exception as e:
                    print(e)
        elif t == 2:
            print('waiting for prep message from client 2')
            while a:
                pickledData = conn2.recv(1024)
                print('recieved prep message from client 2')

                try:
                    unpickledData = pickle.loads(pickledData)
                    a = False
                except Exception as e:
                    print(e)
        # client 1 move
        if unpickledData == 1:
            t = 1
            # tell it to switch to recieving steps
            conn2.send(pickle.dumps(0))
            # tell client 1 to switch to sending steps
            conn.send(pickle.dumps(1))

            # wait to recieve data from client 1
            pickledData = conn.recv(1024)
            unpickledData = pickle.loads(pickledData)
            board = loadClientMove(board, unpickledData, 1)
            conn.send(b'ready')
            conn2.send(b'ready')
            print('sent ready conformation')
            updateClientBoard(board)

            # check nothing/won/draw [normal:0, win:1, draw:2, loss:3]
            if checkWon(board):
                conn.send(pickle.dumps(1))
                conn2.send(pickle.dumps(3))
                print('game concluded server shutting down')
                sys.exit()
            elif checkDraw(board):
                conn.send(pickle.dumps(2))
                conn2.send(pickle.dumps(2))
                print('game concluded server shutting down')
                sys.exit()
            conn.send(pickle.dumps(0))
            conn2.send(pickle.dumps(0))

            # wait for conn to send back
            conn.recv(1024)
            conn2.recv(1024)
            print('ready conformation recieved')

            conn.send(b'ready')

        # client 2 move 
        elif unpickledData == 0:
            t = 2
            # tell it to switch to recieving steps
            conn.send(pickle.dumps(0))
            # tell client 1 to switch to sending steps
            conn2.send(pickle.dumps(1))

            # wait to recieve data from client 1
            pickledData = conn2.recv(1024)
            unpickledData = pickle.loads(pickledData)
            board = loadClientMove(board, unpickledData, 0)
            conn.send(b'ready')
            conn2.send(b'ready')
            print('sent ready conformation')
            updateClientBoard(board)
            # checking if the clients are ready to move on 
            #conn.recv(1024)
            #conn2.recv(1024)

            # check nothing/won/draw [normal:0, win:1, draw:2, loss:3]
            if checkWon(board):
                conn.send(pickle.dumps(3))
                conn2.send(pickle.dumps(1))
                print('game concluded server shutting down')
                sys.exit()
            elif checkDraw(board):
                conn.send(pickle.dumps(2))
                conn2.send(pickle.dumps(2))
                print('game concluded server shutting down')
                sys.exit()
            conn.send(pickle.dumps(0))
            conn2.send(pickle.dumps(0))


            conn.recv(1024)
            conn2.recv(1024)
            print('ready recieved confimation')

            conn2.send(b'ready')
