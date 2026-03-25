import chess

class Game():
    def __init__(self,player1,player2 = -1):
        self.board = chess.Board()
        self.players = [player1,player2]
        self.playerToMove = 0

    def make_a_move(self,move):
        try:
            move = chess.Move.from_uci(move)
        
            if move in self.board.legal_moves:
                self.board.push(move)  
                self.playerToMove += 1-2*self.playerToMove #reverses the player to move
                return self.board
            else:
                return 2 #illigal move error
    
        except:
            return 1 #incorrect move notation error

