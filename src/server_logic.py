import chess


class Game:
    def __init__(self, player1):
        # Игроки: [белые, чёрные]
        self.players = [int(player1), -1]
        # 0 — ход белых, 1 — ход чёрных
        self.playerToMove = 0
        self.board = chess.Board()

    def add_second_player(self, player2):
        self.players[1] = int(player2)

    def make_a_move(self, move, userID):
        userID = int(userID)

        # Нельзя ходить чёрными, если второго игрока нет
        if self.playerToMove == 1 and self.players[1] == -1:
            return "Waiting for second player"

        # Проверяем, что ход делает тот, чей сейчас ход
        if self.players[self.playerToMove] != userID:
            return "Not your turn"

        # Преобразуем строку хода в объект python-chess
        try:
            move_obj = chess.Move.from_uci(move)
        except Exception:
            return "illegal move"

        # Проверяем легальность хода
        if move_obj not in self.board.legal_moves:
            return "illegal move"

        # Делаем ход
        self.board.push(move_obj)

        # Меняем очередь хода
        self.playerToMove = 1 - self.playerToMove

        return "ok"
