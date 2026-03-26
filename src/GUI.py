import tkinter as tk
import chess

CELL = 60

class ChessGUI:
    def __init__(self, root, gameClient):
        self.root = root
        self.gameClient = gameClient
        self.board = chess.Board()
        self.selected_square = None

        self.canvas = tk.Canvas(root, width=8*CELL, height=8*CELL)
        self.canvas.pack()

        self.canvas.bind("<Button-1>", self.on_click)

        self.pieces = {
            "P": "♙", "p": "♟",
            "R": "♖", "r": "♜",
            "N": "♘", "n": "♞",
            "B": "♗", "b": "♝",
            "Q": "♕", "q": "♛",
            "K": "♔", "k": "♚",
        }

        self.draw()

    # ===== Draw board =====
    def draw(self):
        self.canvas.delete("all")

        for row in range(8):
            for col in range(8):
                color = "white" if (row + col) % 2 == 0 else "gray"
                self.canvas.create_rectangle(
                    col*CELL, row*CELL,
                    col*CELL+CELL, row*CELL+CELL,
                    fill=color
                )

        for square in chess.SQUARES:
            piece = self.board.piece_at(square)
            if piece:
                row = 7 - (square // 8)
                col = square % 8
                self.canvas.create_text(
                    col*CELL+30, row*CELL+30,
                    text=self.pieces[piece.symbol()],
                    font=("Arial", 32)
                )

    # ===== Pawn promotion window =====
    def promote_pawn(self, move):
        window = tk.Toplevel(self.root)
        window.title("Choose piece")

        def choose(piece_type):
            move.promotion = piece_type

            if move in self.board.legal_moves:
                self.board.push(move)
                self.gameClient.make_move(move)

            self.draw()
            window.destroy()
            self.selected_square = None

        tk.Label(window, text="Promote pawn to:").pack()

        tk.Button(window, text="♛", command=lambda: choose(chess.QUEEN)).pack(fill="x")
        tk.Button(window, text="♜", command=lambda: choose(chess.ROOK)).pack(fill="x")
        tk.Button(window, text="♝", command=lambda: choose(chess.BISHOP)).pack(fill="x")
        tk.Button(window, text="♞", command=lambda: choose(chess.KNIGHT)).pack(fill="x")

    # ===== Mouse click =====
    def on_click(self, event):
        col = int(event.x // CELL)
        row = int(event.y // CELL)

        if col < 0 or col > 7 or row < 0 or row > 7:
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
                self.board.push(move)
                self.gameClient.make_move(move)

            self.selected_square = None

        self.draw()