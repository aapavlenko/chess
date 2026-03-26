import tkinter as tk
import threading
from client_input_output_system import GameClient
from GUI import ChessGUI  # исправленный GUI

class App:
    def __init__(self, ip):
        self.root = tk.Tk()
        self.root.title("Authorization")
        self.root.geometry("300x200")
        self.gameClient = GameClient(ip, 9000)
        self.create_main_screen()

    # ===== Main screen =====
    def create_main_screen(self):
        self.clear_window(self.root)
        tk.Label(self.root, text="CHESS", font=("Arial", 14)).pack(pady=20)
        tk.Button(self.root, text="Login", width=20, height=2, command=lambda: self.open_auth("login")).pack(pady=5)
        tk.Button(self.root, text="Register", width=20, height=2, command=lambda: self.open_auth("register")).pack(pady=5)

    # ===== Auth window =====
    def open_auth(self, mode):
        self.mode = mode
        self.root.withdraw()
        self.auth_window = tk.Toplevel()
        self.auth_window.title(mode.capitalize())
        self.auth_window.geometry("300x200")
        self.auth_window.protocol("WM_DELETE_WINDOW", self.back_to_main)

        self.username_entry = tk.Entry(self.auth_window)
        self.username_entry.insert(0, "Enter username")
        self.username_entry.pack(pady=10)

        self.password_entry = tk.Entry(self.auth_window, show="*")
        self.password_entry.insert(0, "Enter password")
        self.password_entry.pack(pady=10)

        tk.Button(self.auth_window, text="OK", command=self.submit).pack(pady=10)
        tk.Button(self.auth_window, text="Back", command=self.back_to_main).pack(pady=5)

    def back_to_main(self):
        if hasattr(self, 'auth_window') and self.auth_window.winfo_exists():
            self.auth_window.destroy()
        self.root.deiconify()

    # ===== Login/Register =====
    def submit(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if self.mode == "login":
            self.gameClient.login(login=username, password=password)
            print("Logging in...")
        elif self.mode == "register":
            self.gameClient.register(login=username, password=password)
            print("Registering...")

        self.auth_window.destroy()
        self.open_game_menu()

    # ===== Game menu =====
    def open_game_menu(self):
        self.root.deiconify()
        self.clear_window(self.root)
        tk.Label(self.root, text="Game Menu", font=("Arial", 14)).pack(pady=20)

        tk.Button(self.root, text="Create Game", width=20, height=2, command=lambda: self.start_game("create")).pack(pady=5)
        tk.Button(self.root, text="Join Game", width=20, height=2, command=lambda: self.start_game("join")).pack(pady=5)

    # ===== Start game =====
    def start_game(self, mode):
        self.clear_window(self.root)
        
        # Создаём GUI сразу
        self.chess_gui = ChessGUI(self.root, self.gameClient)

        # Сетевые операции в фоне
        threading.Thread(target=self.handle_game_start, args=(mode,), daemon=True).start()

    # ===== Handle game in background =====
    def handle_game_start(self, mode):
        try:
            if mode == "create":
                print("Creating game...")
                self.gameClient.create_game()
            elif mode == "join":
                print("Joining game...")
                self.gameClient.join_game()
            print("Game ready!")
        except Exception as e:
            print("Network error:", e)

    # ===== Clear window =====
    def clear_window(self, window):
        for widget in window.winfo_children():
            widget.destroy()

# ===== Run app =====
if __name__ == "__main__":
    app = App('10.176.155.12')
    app.root.mainloop()