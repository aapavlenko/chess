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
    sendOutput(conn,b"Welcome! Type 'exit' to quit.\n\n\n Do you want to log in or to sign up?")
    log_or_reg = getInput(conn)
    sendOutput(conn,b"username,password")
    answer = getInput(conn)
    split = answer.find(",")
    if split == -1:
        sendOutput(conn,b"Invalid format. Use username,password")
        
    username = answer[:split]
    password = answer[split + 1:]

    sendOutput(conn, userManager.start(log_or_reg,username,password))

    try:
        while True:
            data = getInput(conn)
            if not data or data.lower() == "exit":
                break
            print(f"[{addr}] {data}")  
            sendOutput(b"Server received: "+data+"\n".encode('utf-8'))  
    except Exception as e:
        print(f"Error with {addr}: {e}")
    finally:
        conn.close()
        print(f"Connection with {addr} closed")

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