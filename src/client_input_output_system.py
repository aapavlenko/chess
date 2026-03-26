import socket


class GameClient:
    def __init__(self, host, port):
        self.host = host
        self.port = int(port)
        self.client = None
        self.user_id = -1
        self.game_id = -1
        self.connect()

    def connect(self):
        if self.client is not None:
            return
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.client.connect((self.host, self.port))
        except Exception as e:
            print("no server online:", e)
            self.client = None

    def close(self):
        if self.client:
            try:
                self.client.close()
            finally:
                self.client = None

    def ask(self, text: str):
        if self.client is None:
            self.connect()
        if self.client is None:
            raise ConnectionError("No connection to server")
        msg = (str(text) + "\n").encode("utf-8")
        self.client.sendall(msg)

    def get_response(self) -> str:
        data = self.client.recv(1024)
        if not data:
            return ""
        return data.decode("utf-8").strip()

    # ===== auth =====
    def login(self, login, password):
        self.ask(f"log {login} {password}")
        resp = self.get_response()
        if resp.isdigit():
            self.user_id = int(resp)
            return True, None
        return False, resp

    def register(self, login, password):
        self.ask(f"reg {login} {password}")
        resp = self.get_response()
        if resp.isdigit():
            self.user_id = int(resp)
            return True, None
        return False, resp

    # ===== game management =====
    def create_game(self):
        self.ask(f"start {self.user_id}")
        resp = self.get_response()
        if resp.isdigit():
            self.game_id = int(resp)
            return True, None
        return False, resp

    def join_game(self):
        self.ask(f"join {self.user_id}")
        resp = self.get_response()
        if resp.isdigit():
            self.game_id = int(resp)
            return True, None
        return False, resp

    # ===== moves & board =====
    def make_move(self, move: str):
        self.ask(f"move {self.user_id} {self.game_id} {move}")
        return self.get_response()

    def get_board(self):
        self.ask(f"get_board {self.game_id}")
        return self.get_response()

    def logout(self, username):
        self.ask(f"logout {username}")
