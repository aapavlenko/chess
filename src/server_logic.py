import chess


class Game:
    def __init__(self, player1):
        # Players: [white,black]
        self.players = [int(player1), -1]
        # 0 — white to move, 1 — black to move
        self.playerToMove = 0
        self.board = chess.Board()

    def add_second_player(self, player2):
        self.players[1] = int(player2)

    def make_a_move(self, move, userID):
        userID = int(userID)
        
        if self.playerToMove == 1 and self.players[1] == -1:
            return "Waiting for second player"

        if self.players[self.playerToMove] != userID:
            return "Not your turn"

        try:
            move_obj = chess.Move.from_uci(move)
        except Exception:
            return "illegal move"

        # Проверяем легальность хода
        if move_obj not in self.board.legal_moves:
            return "illegal move"

        # make a move
        self.board.push(move_obj)

        self.playerToMove = 1 - self.playerToMove

        return "ok"
