import socket

HOST = '10.176.155.15'  # IP сервера
PORT = 9001             # Порт сервера

try:
    # Создаем сокет и подключаемся к серверу
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))


    while True:
        # Ввод команды пользователем
        message = input("You: ")

        # Отправляем команду серверу
        client.sendall(message.encode('utf-8'))

        # Если команда "exit", выходим
        if message.lower() == "exit":
            print("Closing connection...")
            break

        # Получаем ответ от сервера
        response = client.recv(1024).decode('utf-8')
        print(response)

except Exception as e:
    print(f"Error: {e}")
finally:
    client.close()