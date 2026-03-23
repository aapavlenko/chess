import socket

HOST = '10.176.155.16'  
PORT = 9000         

try:
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))

    
    welcome = client.recv(1024).decode('utf-8')
    print(welcome)

    while True:
        message = input("You: ")
        client.sendall(message.encode('utf-8'))
        if message.lower() == "exit":
            break
        response = client.recv(1024).decode('utf-8')
        print(response)

except Exception as e:
    print(f"Error: {e}")
finally:
    client.close()