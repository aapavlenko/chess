import socket
import threading
from Server import UserManager

HOST = "0.0.0.0"
PORT = int(input("port: "))

userManager = UserManager()


def get_input(conn):
    data = conn.recv(1024)
    if not data:
        return ""
    return data.decode("utf-8").strip()


def send_output(conn, text):
    conn.sendall((str(text) + "\n").encode("utf-8"))


def handle_client(conn, addr):
    print(f"New connection from {addr}")

    try:
        while True:
            msg = get_input(conn)
            if not msg:
                break

            parts = msg.split()
            cmd = parts[0]

            if cmd == "log":
                send_output(conn, userManager.login(parts[1], parts[2]))

            elif cmd == "reg":
                send_output(conn, userManager.register(parts[1], parts[2]))

            elif cmd == "start":
                game_id = userManager.play_a_game(parts[1], True)
                send_output(conn, game_id)

            elif cmd == "join":
                free = userManager.play_a_game(parts[1], False)
                if free:
                    gid = free[0]
                    res = userManager.join_a_game(parts[1], gid)
                    if res == "Joined successfully":
                        send_output(conn, gid)
                    else:
                        send_output(conn, res)
                else:
                    send_output(conn, "No free games")

            elif cmd == "move":
                if len(parts) < 4:
                    send_output(conn, "invalid move format")
                else:
                    user_id = parts[1]
                    game_id = parts[2]
                    move = parts[3]
                    res = userManager.make_a_move(game_id, user_id, move)
                    send_output(conn, res)

            elif cmd == "get_board":
                try:
                    board = userManager.get_board(parts[1])
                    send_output(conn, board.fen())
                except IndexError:
                    send_output(conn, "no such game")

            elif cmd == "logout":
                send_output(conn, userManager.logout(parts[1]))

            else:
                send_output(conn, "unknown command")

    finally:
        conn.close()
        print(f"Connection closed {addr}")


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)
    print(f"Server listening on {HOST}:{PORT}")

    while True:
        conn, addr = server.accept()
        threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()


if __name__ == "__main__":
    main()
