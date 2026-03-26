from server_logic import Game


class UserManager:
    def __init__(self, users_passwords = {}, active_users = {},current_games = []):
        self.users_passwords = users_passwords   # username -> password
        self.active_users = active_users      # username -> ID
        self.current_games = current_games      # games

    def login(self, username, password):
        if username not in self.users_passwords:
            return "No such user found"

        if self.users_passwords[username] != password:
            return "Incorrect password"

        user_id = self.add_active_user(username)
        return user_id

    def register(self, username, password):
        if username in self.users_passwords:
            return "This user already exists"

        self.users_passwords[username] = password
        user_id = self.add_active_user(username)
        return user_id

    def add_active_user(self, username):
        user_id = len(self.active_users) + 1
        self.active_users[username] = user_id
        print(f"{username} is now active with ID {user_id}")
        return user_id

    def play_a_game(self, player_id, create_game):
        if create_game is True:
            self.current_games.append(Game(player1=player_id))
            game_id = len(self.current_games) - 1
            return game_id

        if create_game is False:
            free_games = []
            for i, game in enumerate(self.current_games):
                if game.players[1] == -1:
                    free_games.append(i)
            return free_games

        return "Incorrect input"

    def join_a_game(self, player_id, game_number):
        if game_number >= len(self.current_games):
            return "Game not found"

        game = self.current_games[game_number]

        if game.players[1] != -1:
            return "Game already full"

        game.players[1] = player_id
        return  "Joined successfully"

    def make_a_move(self, game_id, player_id, move):
        if game_id >= len(self.current_games):
            return "Game not found"

        game = self.current_games[game_id]

        if game.players[game.playerToMove] != player_id:
            return "Not your turn"

        result = game.MakeAMove(move)
        return result

    def logout(self, username):
        if username not in self.active_users:
            return "User is not logged in"

        del self.active_users[username]
        print(f"{username} logged out")
        return "Logged out successfully"
    
    def get_board(self, gameID):
        return self.current_games[gameID]