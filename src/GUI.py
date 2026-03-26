import tkinter as tk
import chess
import threading
import time

CELL = 60


class ChessGUI:
    def __init__(self, root, gameClient):
        self.root = root
        self.gameClient = gameClient
        self.board = chess.Board()
        self.selected_square = None

        self.canvas = tk.Canvas(root, width=8 * CELL, height=8 * CELL)
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.on_click)

        self.pieces = {
            "P": "♙",
            "p": "♟",
            "R": "♖",
            "r": "♜",
            "N": "♘",
            "n": "♞",
            "B": "♗",
            "b": "♝",
            "Q": "♕",
            "q": "♛",
            "K": "♔",
            "k": "♚",
        }

        self.draw()

        threading.Thread(target=self.poll_server_board, daemon=True).start()

    # ===== Draw the board and pieces =====
    def draw(self):
        self.canvas.delete("all")

        for row in range(8):
            for col in range(8):
                color = "white" if (row + col) % 2 == 0 else "gray"
                self.canvas.create_rectangle(
                    col * CELL,
                    row * CELL,
                    col * CELL + CELL,
                    row * CELL + CELL,
                    fill=color,
                )

        for square in chess.SQUARES:
            piece = self.board.piece_at(square)
            if piece:
                row = 7 - (square // 8)
                col = square % 8
                self.canvas.create_text(
                    col * CELL + CELL // 2,
                    row * CELL + CELL // 2,
                    text=self.pieces[piece.symbol()],
                    font=("Arial", 32),
                )

    # ===== Pawn promotion =====
    def promote_pawn(self, move):
        window = tk.Toplevel(self.root)
        window.title("Choose piece")

        def choose(piece_type):
            move.promotion = piece_type
            if move in self.board.legal_moves:
                self.try_make_move(move)
            window.destroy()
            self.selected_square = None

        tk.Label(window, text="Promote pawn to:").pack()
        tk.Button(window, text="♛", command=lambda: choose(chess.QUEEN)).pack(fill="x")
        tk.Button(window, text="♜", command=lambda: choose(chess.ROOK)).pack(fill="x")
        tk.Button(window, text="♝", command=lambda: choose(chess.BISHOP)).pack(fill="x")
        tk.Button(window, text="♞", command=lambda: choose(chess.KNIGHT)).pack(fill="x")

    # ===== Attempt to make a move =====
    def try_make_move(self, move):
        def worker():
            try:
                result = self.gameClient.make_move(move)
            except Exception as e:
                print("make_move error:", e)
                return

            if result != "illegal move":
                self.board.push(move)
                self.root.after(0, self.draw)
            else:
                print("Server rejected move:", move)

        threading.Thread(target=worker, daemon=True).start()

    # ===== Mouse click handler =====
    def on_click(self, event):
        col = int(event.x // CELL)
        row = int(event.y // CELL)

        if not (0 <= col <= 7 and 0 <= row <= 7):
            return

        square = chess.square(col, 7 - row)

        if self.selected_square is None:
            if self.board.piece_at(square):
                self.selected_square = square
        else:
            piece = self.board.piece_at(self.selected_square)
            move = chess.Move(self.selected_square, square)

            # Pawn promotion check
            if piece and piece.piece_type == chess.PAWN:
                rank = chess.square_rank(square)
                if (piece.color and rank == 7) or (not piece.color and rank == 0):
                    move = chess.Move(self.selected_square, square, promotion=chess.QUEEN)
                    if move in self.board.legal_moves:
                        self.promote_pawn(move)
                        return

            if move in self.board.legal_moves:
                self.try_make_move(move)

            self.selected_square = None
            self.draw()

    # ===== Wait for board updates from the server =====
    def poll_server_board(self):
        last_fen = None
        while True:
            try:
                server_fen = self.gameClient.get_board()
            except Exception as e:
                # сервер недоступен / ошибка — просто подождём и попробуем снова
                # чтобы не заспамить консоль
                time.sleep(0.3)
                continue

            if not server_fen or server_fen == last_fen:
                time.sleep(0.3)
                continue

            last_fen = server_fen
            try:
                self.board = chess.Board(server_fen)
            except Exception as e:
                time.sleep(0.3)
                continue

            self.root.after(0, self.draw)
            time.sleep(0.3)
