import socket
import pickle
import sys 

host = "192.168.2.197"
# Port to listen on (non-privileged ports are > 1023)
port = 65434
t = 0
RANGE = [i for i in range(9)]

def displayBoard(boardRep):
    for i in range(3):
        print(boardRep[i])

def sendBoard(board: list[str]):
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
    displayBoard(rows)
    return rows

def checkInvalidPos(board: list[str], index):
    if board[index] == '_':
        return False
    return True

def makeMove(board: list[str]):
    # 0-8
    valid = False
    while not valid:
        index = int(input('> '))
        if not checkInvalidPos(board, index) and index in RANGE:
            valid = True 
        else:
            print('INVALID POSITION')

    board[index] = 'X'
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

def loadClientMove(board, index):
    valid = False
    while not valid:
        if not checkInvalidPos(board, index) and index in RANGE:
            conn.send(pickle.dumps('True'))
            valid = True 
        else:
            conn.send(pickle.dumps('False'))
            #print('INVALID CLIENT MOVE')
            pickledData = conn.recv(1024)
            index = pickle.loads(pickledData)

    conn.recv(1024)
    board[index] = 'O'
    return board
    
board = ['_'for _ in range(9)]

# specifying the protocals that will be used for communication
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    # assigns an  address where you expect a client will join 
    s.bind((host, port))
    s.listen()    
    conn, addr = s.accept()
    with conn:
        print(f'Connected by {addr}')
        while True:
            t+=1
            # when its the servers turn
            pickledData = conn.recv(2042)
            unpickledData = pickle.loads(pickledData)
            
            # server is sending data (servers go)
            if unpickledData == 1:
                #print('server go ')
                # make a move and then load a representation of the current board
                board = makeMove(board)
                rows = sendBoard(board)

                # tells the client to expect data, waits until it is ready , 
                # and then sends the data 
                conn.send(pickle.dumps(0))
                #print('client ready to recieve')
                conn.recv(1024)
                #print('data sending')
                conn.send(pickle.dumps(rows))
                #print('data sent')

                # wait for it to verify that it has completed its job
                conn.recv(1024)
                #print('client jobs complete')

                # server checking if game won/drawn
                if checkWon(board):
                    print('You won')
                    conn.send(pickle.dumps(1))
                    sys.exit()
                elif checkDraw(board):
                    print('Draw')
                    conn.send(pickle.dumps(0))
                    sys.exit()
                conn.send(pickle.dumps(-1))
                conn.recv(1024)
                # tells the client to send data

                conn.send(pickle.dumps(1))

            # client is sending data (clients go)
            elif unpickledData == 0:
                #print('client go')
                # tells client that its ready to recieve 
                conn.send(b'ready')
                pickledData = conn.recv(1024)
                #print('data recieved')
                unpickledData = pickle.loads(pickledData)
                
                # Adds the clients move onto the board 
                # and then loads a representation of the current board
                board = loadClientMove(board, unpickledData)
                rows = sendBoard(board)

                #print('client ready to recieve')
                #conn.recv(1024)
                #print('data sending')
                conn.send(pickle.dumps(rows))
                #print('data sent')

                # wait for it to verify that it has completed its job
                conn.recv(1024)
                #print('client jobs complete')

                if checkWon(board):
                    print('You lost')
                    conn.send(pickle.dumps(2))
                    sys.exit()
                elif checkDraw(board):
                    print('Draw')
                    conn.send(pickle.dumps(0))
                    sys.exit()
                conn.send(pickle.dumps(-1))
                # tells client that its ready to move on 
                conn.send(b'ready')
                print('clients go done')

                
            print(f'next turn {t}')


