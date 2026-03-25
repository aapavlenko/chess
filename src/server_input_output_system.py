import socket
import threading
from src.Server import UserManager 

HOST = '0.0.0.0'  
PORT = 9001      
userManager = UserManager()

def get_input(conn):
    return  conn.recv(1024).decode('utf-8').strip()

def send_output(conn,text):
    print(text)
    text = (str(text)+"\n\r").encode('utf-8')
    conn.sendall(text)

def handle_client(conn, addr):
    print(f"New connection from {addr}")
    answer = get_input(conn)
    print("User answered")
    parts = answer.split()
    command = parts[0] if len(parts) > 0 else None
    argument1 = parts[1] if len(parts) > 1 else None
    argument2 = parts[2] if len(parts) > 2 else None
    if command == "log":
        send_output(conn,userManager.login(username=argument1,password=argument2))
    elif command == "reg":
        send_output(conn,userManager.register(username=argument1,password=argument2))
    elif command == "start":
        send_output(conn,userManager.PlayAGame(playerID=argument1,createGame=True))
    elif command == "join": 
        gameID = int(get_input(conn))
        serverResopnse = userManager.JoinAGame(argument1,gameNumber=gameID)
        send_output(conn,serverResopnse)
    elif command == "serverList":
        send_output(conn,userManager.PlayAGame(playerID=argument1,createGame=False))
    elif command == "move":
        send_output(conn, "game?")
        gameID = int(get_input(conn))
        send_output(conn,userManager.MakeAMoove(gameID=gameID,playerID=argument1,move=argument2))
    handle_client(conn=conn,addr=addr)


    

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
