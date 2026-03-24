import socket
import threading
from Server import UserManager 

HOST = '0.0.0.0'  
PORT = 9001      
userManager = UserManager()

def getInput(conn):
    return  conn.recv(1024).decode('utf-8').strip()

def sendOutput(conn,text):
    print(text)
    text = (str(text)+"\n\r").encode('utf-8')
    conn.sendall(text)

def handleClient(conn, addr):
    print(f"New connection from {addr}")
    answer = getInput(conn)
    print("User answered")
    command = answer[:answer.find(" ")]
    arguments = answer[answer.find(" ")+1:]
    argument1 = arguments[:arguments.find(" ")]
    argument2 = arguments[arguments.find(" ")+1:] 
    if command == "log":
        sendOutput(conn,userManager.login(username=argument1,password=argument2))
    elif command == "reg":
        sendOutput(conn,userManager.register(username=argument1,password=argument2))
    elif command == "start":
        sendOutput(conn,userManager.PlayAGame(playerID=argument1,createGame=True))
    elif command == "join": 
        sendOutput(conn,userManager.PlayAGame(playerID=argument1,createGame=False))
        gameID = int(getInput(conn))
        serverResopnse = userManager.JoinAGame(argument1,gameNumber=gameID)
        sendOutput(conn,serverResopnse)
    elif command == "move":
        sendOutput(conn, "game?")
        gameID = int(getInput(conn))
        sendOutput(conn,userManager.MakeAMoove(gameID=gameID,playerID=argument1,move=argument2))
    handleClient(conn=conn,addr=addr)


    

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(5)
print(f"Server listening on {HOST}:{PORT}")

try:
    while True:
        conn, addr = server.accept()
        client_thread = threading.Thread(target=handleClient, args=(conn, addr))
        client_thread.start()
except KeyboardInterrupt:
    print("Server shutting down")
finally:
    server.close()