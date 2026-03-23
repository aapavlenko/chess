import chess

board = chess.Board()

while True:
    print(board)  # показываем доску
    
    move = input("Введите ход (например e2e4): ")
    
    try:
        move = chess.Move.from_uci(move)
        
        if move in board.legal_moves:
            board.push(move)  # делаем ход
        else:
            print("Нелегальный ход!")
    
    except:
        print("Ошибка ввода!")