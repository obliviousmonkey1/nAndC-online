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
    conn.recv(1024)
    conn2.recv(1024)

    conn.send(pickle.dumps(rows))
    conn2.send(pickle.dumps(rows))

    conn.recv(1024)
    conn2.recv(1024)

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
    pass

def loadClientMove(board, index, client):
    if index in RANGE:
        if validateMove(board, index):
            pass
    
    if client == 1:
        board[index] = 'O'
    else:
        board[index] = 'X'

    return board 

def checkWon():
    pass

def checkDraw():
    pass

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
    while True:
        a = True 
        if t == 1:
            print('client 1 waiting for prep message')
            while a:
                pickledData = conn.recv(1024)
                print('recieved prep message from client 1')
                try:
                    unpickledData = pickle.loads(pickledData)
                    a = False
                except Exception as e:
                    print(e)
        elif t == 2:
            print('client 2 waiting for prep message')
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
            updateClientBoard(board)

            conn.send(b'done')

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
            updateClientBoard(board)

            conn2.send(b'done')
