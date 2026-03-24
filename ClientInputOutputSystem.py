import socket

HOST = '10.176.155.15'  # IP сервера
PORT = 9001             # Порт сервера

userID = -1
gameID = -1
gameBoard = ""

def login(login, password):
    ask(client,"reg " + login + " " + password)
    global userID
    userID = int(getRespons(client))

def register(login, password):
    ask(client,"log " + login+ " " +password)
    global userID
    userID = int(getRespons(client))

def createGame():
    ask(client,"start " + userID +" "+"a")
    global gameID
    gameID = getRespons(client)

def joinGame():
    ask(client, "join " + userID)
    gameID =int(client,getRespons(client)[1])
    ask(client,gameID)
def MakeAMove(move):
    ask(client,"move " + userID + " " + move)
    ask(gameID)
    global gameBoard
    gameBoard = getRespons(client)



def getRespons(client):
    return client.recv(1024).decode('utf-8')
def ask(client, text):
    client.sendall(str(text).encode('utf-8'))

try:
    # Создаем сокет и подключаемся к серверу
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))

except Exception as e:
    print(f"Error: {e}")
finally:
    client.close()
