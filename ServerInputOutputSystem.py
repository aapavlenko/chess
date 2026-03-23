import socket
import threading
from Server import UserManager 

HOST = '0.0.0.0'  
PORT = 9000      
userManager = UserManager()

def getInput(conn):
    return conn.recv(1024).decode('utf-8').strip()

def sendOutput(conn,text):
    conn.sendall(text)

def handle_client(conn, addr):
    print(f"New connection from {addr}")
    sendOutput(conn,b"Welcome! Type 'exit' to quit.\n\n\nWhat do you want to do?\n")
    answer = getInput(conn)
    splitID = answer.find(",")
    splitGame = answer.find("/")
    if splitID == -1:
        logOrReg = answer
        sendOutput(conn,"Enter username,password")
        answer = getInput(conn)
        splitName = answer.find(",")
        if splitName == -1:
            sendOutput(conn,b"Invalid format. Use username,password")
            
        username = answer[:splitName]
        password = answer[splitName + 1:]

        sendOutput(conn, userManager.start(logOrReg,username,password))
        return handle_client(conn,addr)
    elif splitGame == -1:
        playerID = int(answer[:splitID])
        return userManager.PlayAGame(playerID=playerID, createOrJoin=answer[splitID+1:])
    else:
        playerID = int(answer[splitGame+1:splitID])
        GameID = int(answer[:splitGame])
        return userManager.MakeAMoove(playerID==playerID,gameID=GameID,move=answer[:splitID])


    

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(5)
print(f"Server listening on {HOST}:{PORT}")

try:
    while True:
        conn, addr = server.accept()
        client_thread = threading.Thread(target=handle_client, args=(conn, addr))
        client_thread.start()
except KeyboardInterrupt:
    print("Server shutting down")
finally:
    server.close()