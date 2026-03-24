from ServerLogic import Game

class UserManager:
    def __init__(self):
        self.users_passwords = {}  #username ->password
        self.active_users = {}  #username->ID 
        self.currentGames = [] #games

    def login(self, username, password):
        if username in self.users_passwords:
            if self.users_passwords[username] == password:
                return self.add_active_user(username)
            else:
                return b"Incorrect password"
        else:
            return b"No such user found"

    def register(self, username, password):
        if username not in self.users_passwords:
            self.users_passwords[username] = password
            return self.add_active_user(username)
        else:
            return b"This user already exists"
    def add_active_user(self, username):
        self.active_users[username] = len(self.active_users)+1
        print(f"{username} is now active with ID {len(self.active_users)}")
        return len(self.active_users)

    def PlayAGame(self,playerID,createGame):
        if createGame == True:
            self.currentGames.append(Game(player1=playerID))
            return len(self.currentGames) -1 
        elif createGame == False:
            freeGamesIndexes = []
            b = 0
            for a in self.currentGames:
                b+= 1
                if a.players[1] == -1:
                    freeGamesIndexes.append(b-1)
            return freeGamesIndexes
        else:
            return 3 #incorrect input error
    def JoinAGame(self,playerID,gameNumber):    
        self.currentGames[gameNumber].players[1] = playerID
        return "You successfully joined the game"

    def MakeAMoove(self,gameID,playerID,move):
        game = self.currentGames[gameID]
        if game.players[game.playerToMove] == playerID:
            return game. MakeAMove(move)
        else:
            return 4 #wrong game error


    def logout(self, username):
        if username in self.active_users:
            del self.active_users[username]
            print(f"{username} logged out")
        else:
            print(f"{username} is not logged in")