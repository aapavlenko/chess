from ServerLogic import Game

class UserManager:
    def __init__(self):
        self.users_passwords = {}  
        self.active_users = {}     
        self.amountOfUsers = 0
        self.currentGames = []
        self.amountOfGames = 0

    def start(self,logOrReg,username,password):
        if logOrReg == "login":
            return self.login(username, password)
        elif logOrReg == "reg":
            return self.register(username, password)
        else:
            return b"Invalid option, choose 'login' or 'reg'"

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
        self.amountOfUsers += 1
        self.active_users[username] = self.amountOfUsers
        print(f"{username} is now active with ID {self.amountOfUsers}")
        return self.amountOfUsers

    def PlayAGame(self,playerID,createOrJoin):
        if createOrJoin.lower() == "create":
            self.amountOfGames += 1
            self.currentGames[self.amountOfGames] = Game(player1=playerID)
            return self.amountOfGames
        elif createOrJoin.lower() == "join":
            freeGames = []
            for a in self.currentGames:
                if a.players[1] == -1:
                    freeGames += a
            return freeGames
        else:
            return 3 #incorrect input error
    def MakeAMoove(self,gameID,playerID,move):
        game = self.currentGames[gameID]
        if game.players[game.playerToMove] == playerID:
            return game.Move(move)
        else:
            return 4 #wrong game error


    def logout(self, username):
        if username in self.active_users:
            self.amountOfUsers -= 1
            self.active_users[username] = None
            print(f"{username} logged out")
        else:
            print(f"{username} is not logged in")