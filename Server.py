class UserManager:
    def __init__(self):
        self.users_passwords = {}  
        self.active_users = {}     
        self.amount_of_users = 0

    def start(self,log_or_reg,username,password):
        if log_or_reg == "login":
            return self.login(username, password)
        elif log_or_reg == "reg":
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
        self.amount_of_users += 1
        self.active_users[username] = self.amount_of_users
        print(f"{username} is now active with ID {self.amount_of_users}")
        return self.amount_of_users

    def logout(self, username):
        if username in self.active_users:
            self.amount_of_users -= 1
            self.active_users[username] = None
            print(f"{username} logged out")
        else:
            print(f"{username} is not logged in")