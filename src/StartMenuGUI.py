import tkinter as tk
import threading

from client_input_output_system import GameClient
from GUI import ChessGUI  # fixed GUI


class App:
    def __init__(self, ip, port):
        self.root = tk.Tk()
        self.root.title("Authorization")
        self.root.geometry("300x200")

        self.gameClient = GameClient(ip, port)

        self.mode = None
        self.auth_window = None
        self.username_entry = None
        self.password_entry = None

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
            command=lambda: self.open_auth("login"),
        ).pack(pady=5)
        tk.Button(
            self.root,
            text="Register",
            width=20,
            height=2,
            command=lambda: self.open_auth("register"),
        ).pack(pady=5)

    # ===== Auth window =====
    def open_auth(self, mode):
        self.mode = mode
        self.root.withdraw()
        self.auth_window = tk.Toplevel(self.root)
        self.auth_window.title(mode.capitalize())
        self.auth_window.geometry("300x200")
        self.auth_window.protocol("WM_DELETE_WINDOW", self.back_to_main)

        self.username_entry = tk.Entry(self.auth_window)
        self.username_entry.pack(pady=10)
        self.username_entry.focus_set()

        self.password_entry = tk.Entry(self.auth_window, show="*")
        self.password_entry.pack(pady=10)

        tk.Button(self.auth_window, text="OK", command=self.submit).pack(pady=10)
        tk.Button(self.auth_window, text="Back", command=self.back_to_main).pack(pady=5)

    def back_to_main(self):
        if self.auth_window is not None and self.auth_window.winfo_exists():
            self.auth_window.destroy()
        self.root.deiconify()

    # ===== Login/Register =====
    def submit(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not username or not password:
            print("Empty username or password")
            return

        threading.Thread(
            target=self._submit_worker,
            args=(self.mode, username, password),
            daemon=True,
        ).start()

    def _submit_worker(self, mode, username, password):
        try:
            if mode == "login":
                ok, err = self.gameClient.login(username, password)
            else:
                ok, err = self.gameClient.register(username, password)
        except Exception as e:
            print("Auth error:", e)
            return

        if not ok:
            print("Auth failed:", err)
            return

        self.root.after(0, self._after_auth_success)

    def _after_auth_success(self):
        if self.auth_window is not None and self.auth_window.winfo_exists():
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
            command=lambda: self.start_game("create"),
        ).pack(pady=5)
        tk.Button(
            self.root,
            text="Join Game",
            width=20,
            height=2,
            command=lambda: self.start_game("join"),
        ).pack(pady=5)

    # ===== Start game =====
    def start_game(self, mode):
        self.clear_window(self.root)
        self.chess_gui = ChessGUI(self.root, self.gameClient)
        threading.Thread(
            target=self.handle_game_start,
            args=(mode,),
            daemon=True,
        ).start()

    def handle_game_start(self, mode):
        try:
            if mode == "create":
                print("Creating game...")
                ok, err = self.gameClient.create_game()
            else:
                print("Joining game...")
                ok, err = self.gameClient.join_game()
            if not ok:
                print("Game start failed:", err)
            else:
                print("Game ready!")
        except Exception as e:
            print("Network error:", e)

    # ===== Clear window =====
    def clear_window(self, window):
        for widget in window.winfo_children():
            widget.destroy()


if __name__ == "__main__":
    ip = input("ip: ")
    port = input("port: ")
    app = App(ip, port)
    app.root.mainloop()
