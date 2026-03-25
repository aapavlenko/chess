import tkinter as tk

def login():

    # Проверка, какую кнопку нажали
    global btn_login 
    btn_login = True

    root.destroy()

    root_username_password = tk.Tk()
    root_username_password.title("Registration")
    root_username_password.geometry("300x200")

    def show_username():
        global username_answer
        username_answer = enter_username.get()
        return username_answer
    
    enter_username = tk.Entry(root_username_password, fg="grey")
    enter_username.insert(0, "Enter username")
    enter_username.pack(pady=20)
    

    def show_password():
        global password_answer
        password_answer = enter_password.get()
        return password_answer
    
    enter_password = tk.Entry(root_username_password, fg="grey")
    enter_password.insert(0, "Enter password")
    enter_password.pack(pady=20)

    def username_password():
        show_username()
        show_password()

    btn_password = tk.Button(root_username_password, text = "Ok", command = username_password)
    btn_password.pack(side="bottom", pady=20)
    
    

def register():

    # Проверка, какую кнопку нажали
    global btn_register
    btn_register = False
    
    root.destroy()

    root_username_password = tk.Tk()
    root_username_password.title("registration")
    root_username_password.geometry("300x200")
    







# создаём окно
root = tk.Tk()
root.title("Authorization")
root.geometry("300x200")

# заголовок
label = tk.Label(root, text="CHESS", font=("Arial", 14))
label.pack(pady=20)

# кнопка "Войти"
btn_login = tk.Button(root, text="Login", width=20, height=2, command=login)
btn_login.pack(pady=5)

# кнопка "Зарегистрироваться"
btn_register = tk.Button(root, text="Register", width=20, height=2, command=register)
btn_register.pack(pady=5)

# запуск окна
root.mainloop() 