import tkinter as tk
from client_input_output_system import GameClient


class App:
    def __init__(self, ip):
        self.root = tk.Tk()
        self.root.title("Authorization")
        self.root.geometry("300x200")

        self.gameClient = GameClient(ip, 9002)

        self.create_main_screen()

    # ===== Main screen =====
    def create_main_screen(self):
        self.clear_window(self.root)

        tk.Label(self.root, text="CHESS", font=("Arial", 14)).pack(pady=20)

        tk.Button(
            self.root,
            text="Login",
            width=20,
            height=2,
            command=lambda: self.open_auth("login")
        ).pack(pady=5)

        tk.Button(
            self.root,
            text="Register",
            width=20,
            height=2,
            command=lambda: self.open_auth("register")
        ).pack(pady=5)

    # ===== Open auth window =====
    def open_auth(self, mode):
        self.mode = mode
        self.root.withdraw()  # скрываем главное окно

        self.auth_window = tk.Toplevel()
        self.auth_window.title(mode.capitalize())
        self.auth_window.geometry("300x200")
        self.auth_window.protocol("WM_DELETE_WINDOW", self.back_to_main)

        # Username
        self.username_entry = tk.Entry(self.auth_window)
        self.username_entry.insert(0, "Enter username")
        self.username_entry.pack(pady=10)

        # Password
        self.password_entry = tk.Entry(self.auth_window, show="*")
        self.password_entry.insert(0, "Enter password")
        self.password_entry.pack(pady=10)

        tk.Button(
            self.auth_window,
            text="OK",
            command=self.submit
        ).pack(pady=10)

        tk.Button(
            self.auth_window,
            text="Back",
            command=self.back_to_main
        ).pack(pady=5)

    # ===== Back to main =====
    def back_to_main(self):
        if hasattr(self, 'auth_window') and self.auth_window.winfo_exists():
            self.auth_window.destroy()
        self.root.deiconify()  # показать главное окно

    # ===== Handle submit =====
    def submit(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if self.mode == "login":
            result = self.gameClient.login(login=username, password=password)
            print("Logging in... Server response:", result)

        elif self.mode == "register":
            result = self.gameClient.register(login=username, password=password)
            print("Registering... Server response:", result)

        # После успешного логина/регистрации открываем меню игры
        self.auth_window.destroy()
        self.open_game_menu()

    # ===== Game menu =====
    def open_game_menu(self):
        self.root.deiconify()
        self.clear_window(self.root)

        tk.Label(self.root, text="Game Menu", font=("Arial", 14)).pack(pady=20)

        tk.Button(
            self.root,
            text="Create Game",
            width=20,
            height=2,
            command=self.create_game
        ).pack(pady=5)

        tk.Button(
            self.root,
            text="Join Game",
            width=20,
            height=2,
            command=self.join_game
        ).pack(pady=5)

        tk.Button(
            self.root,
            text="Logout",
            width=20,
            height=2,
            command=self.logout
        ).pack(pady=5)

    # ===== Game actions =====
    def create_game(self):
        print("Create Game clicked")
        # Здесь можно открыть окно или начать лобби создания игры

    def join_game(self):
        print("Join Game clicked")
        # Здесь можно открыть окно выбора доступных игр или ввод кода комнаты

    def logout(self):
        self.gameClient.logout(username=self.username_entry)
        print("Logging out")
        self.create_main_screen()

    # ===== Utility =====
    def clear_window(self, window):
        for widget in window.winfo_children():
            widget.destroy()


# ===== Run app =====
if __name__ == "__main__":
    app = App('10.176.155.11')
    app.root.mainloop()