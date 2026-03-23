usersPaswords = {}
users = {}
amountOfUsers = 0
def Start():
    logOrReg = input("login/reg")
    answer = input("username,password")
    split = answer.find(",")
    username = answer[:split]
    password = answer[split:]
    if logOrReg == "login":
        if username in users:
                if usersPaswords[username] == password:
                    return AddActiveUser(username)
        else:
            print("No such user found")
            return Start()
    elif logOrReg == "reg":
        if not username in users:
            usersPaswords [username] = password
            return AddActiveUser(username)
        else:
            print("this user already exists")
            return Start()

def AddActiveUser(username = "Default"):
    global amountOfUsers
    amountOfUsers += 1
    users[username] = amountOfUsers
    return amountOfUsers
def LogOut(username):
    global amountOfUsers
    amountOfUsers -= 1
    users[username] = None