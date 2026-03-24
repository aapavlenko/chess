import tkinter as tk
import chess

board = chess.Board()
CELL = 60
root = tk.Tk()
root.title("Шахматы")

canvas = tk.Canvas(root, width=8*CELL, height=8*CELL)
canvas.pack()

selected_square = None  # выбранная клетка

pieces = {
    "P": "♙", "p": "♟",
    "R": "♖", "r": "♜",
    "N": "♘", "n": "♞",
    "B": "♗", "b": "♝",
    "Q": "♕", "q": "♛",
    "K": "♔", "k": "♚",
}

def draw():
    canvas.delete("all")
    for row in range(8):
        for col in range(8):
            color = "white" if (row + col) % 2 == 0 else "gray"
            canvas.create_rectangle(col*CELL, row*CELL,
                                    col*CELL+CELL, row*CELL+CELL,
                                    fill=color)
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            row = 7 - (square // 8)
            col = square % 8
            canvas.create_text(col*CELL+30, row*CELL+30,
                               text=pieces[piece.symbol()],
                               font=("Arial", 32))

# Окно выбора превращения пешки
def promote_pawn(move):
    promotion_window = tk.Toplevel(root)
    promotion_window.title("Выберите фигуру")

    def choose(piece_type):
        move.promotion = piece_type
        if move in board.legal_moves:
            board.push(move)  # добавляем ход после выбора фигуры
        draw()
        promotion_window.destroy()
        global selected_square
        selected_square = None  # сброс выбранной клетки

    tk.Label(promotion_window, text="Превратить пешку в:").pack(pady=5)
    tk.Button(promotion_window, text="Ферзь", command=lambda: choose(chess.QUEEN)).pack(fill="x")
    tk.Button(promotion_window, text="Ладья", command=lambda: choose(chess.ROOK)).pack(fill="x")
    tk.Button(promotion_window, text="Слон", command=lambda: choose(chess.BISHOP)).pack(fill="x")
    tk.Button(promotion_window, text="Конь", command=lambda: choose(chess.KNIGHT)).pack(fill="x")


def on_click(event):
    global selected_square

    col = int(event.x // CELL)
    row = int(event.y // CELL)
    if col < 0 or col > 7 or row < 0 or row > 7:
        return

    square = chess.square(col, 7 - row)

    if selected_square is None:
        if board.piece_at(square):
            selected_square = square
    else:
        piece = board.piece_at(selected_square)
        move = chess.Move(selected_square, square)

        # проверка превращения пешки
        if piece and piece.piece_type == chess.PAWN:
            rank = chess.square_rank(square)
            if (piece.color == chess.WHITE and rank == 7) or (piece.color == chess.BLACK and rank == 0):
                # создаем ход с временным promotion в ферзя, чтобы он был legal
                move = chess.Move(selected_square, square, promotion=chess.QUEEN)
                if move in board.legal_moves:
                    promote_pawn(move)  # покажем окно выбора
                    return

        # обычный ход без превращения
        if move in board.legal_moves:
            board.push(move)

        selected_square = None

    draw()

canvas.bind("<Button-1>", on_click)
draw()
root.mainloop()