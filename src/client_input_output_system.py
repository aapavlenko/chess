import socket


class GameClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.client = None

        self.user_id = -1
        self.game_id = -1
        self.game_board = ""
        self.connect()

    def connect(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.client.connect((self.host, self.port)) 
        except:
            print("no server online")

    def close(self):
        if self.client:
            self.client.close()

    def ask(self, text):
        self.client.sendall(str(text).encode('utf-8'))

    def get_response(self):
        return self.client.recv(1024).decode('utf-8')

    def login(self, login, password):
        self.ask(f"log {login} {password}")
        self.user_id = int(self.get_response())

    def register(self, login, password):
        self.ask(f"reg {login} {password}")
        self.user_id = int(self.get_response())

    def create_game(self):
        self.ask(f"start {self.user_id} a")
        self.game_id = int(self.get_response())

    def join_game(self):
        self.ask(f"join {self.user_id}")
        response = self.get_response()
        self.game_id = int(response)

    def make_move(self, move):
        self.ask(f"move {self.user_id} {move}")
        self.game_board = self.get_response()
        return self.game_board
    def logout(self,username):
        self.ask(f"logout {username} a")
