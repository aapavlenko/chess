from server_logic import Game


class UserManager:
    def __init__(self):
        self.users_passwords = {}   # username -> password
        self.active_users = {}      # username -> user_id
        self.current_games = []     # list of Game objects

    # ===== AUTH =====
    def login(self, username, password):
        if username not in self.users_passwords:
            return "No such user found"
        if self.users_passwords[username] != password:
            return "Incorrect password"
        return self.add_active_user(username)

    def register(self, username, password):
        if username in self.users_passwords:
            return "This user already exists"
        self.users_passwords[username] = password
        return self.add_active_user(username)

    def add_active_user(self, username):
        user_id = len(self.active_users) + 1
        self.active_users[username] = user_id
        return user_id

    # ===== GAME MANAGEMENT =====
    def play_a_game(self, player_id, create_game):
        player_id = int(player_id)

        if create_game:
            game = Game(player1=player_id)
            self.current_games.append(game)
            return len(self.current_games) - 1

        # список свободных игр
        return [i for i, g in enumerate(self.current_games) if g.players[1] == -1]

    def join_a_game(self, player_id, game_number):
        player_id = int(player_id)
        game_number = int(game_number)

        if game_number >= len(self.current_games):
            return "Game not found"

        game = self.current_games[game_number]

        # нельзя зайти в игру тем же user_id
        if game.players[0] == player_id:
            return "You cannot join your own game"

        if game.players[1] != -1:
            return "Game already full"

        game.add_second_player(player_id)
        return "Joined successfully"

    def make_a_move(self, game_id, player_id, move):
        game_id = int(game_id)
        if game_id >= len(self.current_games):
            return "Game not found"
        return self.current_games[game_id].make_a_move(move, player_id)

    def get_board(self, game_id):
        game_id = int(game_id)
        if game_id >= len(self.current_games):
            raise IndexError("no such game")
        return self.current_games[game_id].board

    def logout(self, username):
        if username not in self.active_users:
            return "User is not logged in"
        del self.active_users[username]
        return "Logged out successfully"
