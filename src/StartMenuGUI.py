import tkinter as tk
import threading
from client_input_output_system import GameClient
from GUI import ChessGUI  # import your chess UI


class App:
    def __init__(self, ip):
        # Create main window
        self.root = tk.Tk()
        self.root.title("Authorization")
        self.root.geometry("300x200")
        
        self.gameClient = GameClient(ip, 9002)

        # Load main screen
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

    # ===== Open login/register window =====
    def open_auth(self, mode):
        self.mode = mode

        # Hide main window
        self.root.withdraw()

        # Create new window
        self.auth_window = tk.Toplevel()
        self.auth_window.title(mode.capitalize())
        self.auth_window.geometry("300x200")

        # Handle closing window
        self.auth_window.protocol("WM_DELETE_WINDOW", self.back_to_main)

        # Username input
        self.username_entry = tk.Entry(self.auth_window)
        self.username_entry.insert(0, "Enter username")
        self.username_entry.pack(pady=10)

        # Password input
        self.password_entry = tk.Entry(self.auth_window, show="*")
        self.password_entry.insert(0, "Enter password")
        self.password_entry.pack(pady=10)

        # Submit button
        tk.Button(
            self.auth_window,
            text="OK",
            command=self.submit
        ).pack(pady=10)

        # Back button
        tk.Button(
            self.auth_window,
            text="Back",
            command=self.back_to_main
        ).pack(pady=5)

    # ===== Return to main screen =====
    def back_to_main(self):
        if hasattr(self, 'auth_window') and self.auth_window.winfo_exists():
            self.auth_window.destroy()

        self.root.deiconify()

    # ===== Handle login/register =====
    def submit(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if self.mode == "login":
            self.gameClient.login(login=username, password=password)
            print("Logging in... Server response:")

        elif self.mode == "register":
            self.gameClient.register(login=username, password=password)
            print("Registering... Server response:")

        # Close auth window and open game menu
        self.auth_window.destroy()
        self.open_game_menu()

    # ===== Game menu =====
    def open_game_menu(self):
        self.root.deiconify()
        self.clear_window(self.root)

        tk.Label(self.root, text="Game Menu", font=("Arial", 14)).pack(pady=20)

        # Create game button
        tk.Button(
            self.root,
            text="Create Game",
            width=20,
            height=2,
            command=lambda: self.start_game("create")
        ).pack(pady=5)

        tk.Button(
            self.root,
            text="Join Game",
            width=20,
            height=2,
            command=lambda: self.start_game("join")
        ).pack(pady=5)

    # ===== Start chess GUI =====
    def start_game(self, mode):
        # Clear menu UI
        self.clear_window(self.root)

        # Запускаем сетевую операцию в отдельном потоке
        threading.Thread(target=self.handle_game_start, args=(mode,), daemon=True).start()

    # ===== Handle game creation/join in background =====
    def handle_game_start(self, mode):
        if mode == "create":
            print("Creating game...")
            self.gameClient.create_game()  # блокирующий сетевой запрос

        elif mode == "join":
            print("Joining game...")
            self.gameClient.join_game()  # блокирующий сетевой запрос

        # После завершения запроса запускаем GUI в главном потоке
        self.root.after(0, self.launch_chess_gui)

    # ===== Launch Chess GUI safely =====
    def launch_chess_gui(self):
        self.chess_gui = ChessGUI(self.root, self.gameClient)

    # ===== Logout =====
    def logout(self):
        print("Logging out")
        self.gameClient.logout(username=self.username_entry)
        # Optional: send logout request
        # self.gameClient.logout(...)

        self.create_main_screen()

    # ===== Utility: clear window =====
    def clear_window(self, window):
        for widget in window.winfo_children():
            widget.destroy()


# ===== Run app =====
if __name__ == "__main__":
    app = App('10.176.155.12')
    app.root.mainloop()