import chess

class Game():
    def __init__(self,player1,player2 = -1):
        self.board = chess.Board()
        self.players = [player1,player2]
        self.playerToMove = 0

    def make_a_move(self,move,userID):
        if (self.board.turn == chess.WHITE and userID == self.players[0]) or (self.board.turn == chess.BLACK and userID == self.players[1]):
            try:
                move = chess.Move.from_uci(move)
            
                if move in self.board.legal_moves:
                    self.board.push(move)  
                    self.playerToMove += 1-2*self.playerToMove #reverses the player to move
                    return self.board
                else:
                    return "incorrect move" #illigal move error
        
            except:
                return "incorrect move notation" #incorrect move notation error
        else:
            return "not your move"

