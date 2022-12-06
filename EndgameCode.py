import chess
import random

board = chess.Board()
while(board.is_checkmate() == False and board.is_stalemate() == False and board.is_insufficient_material() == False and board.can_claim_fifty_moves() == False and board.can_claim_draw() == False):
#for x in range(1,10):

    legal_moves = list(board.legal_moves)

    rand = random.randint(0,len(legal_moves)-1)
    move = str(legal_moves[rand])
    print(board)
    print("\n")
    board.push_san(move)
print("\n")
if(board.is_checkmate() == True):
    print("CHECKMATE")
elif(board.is_stalemate() == True):
    print("lmao stalemate")
elif(board.is_insufficient_material() == True):
    print("yo too small")
elif(board.can_claim_fifty_moves() == True):
    print("50")
elif(board.can_claim_draw() == True):
    print("draw dumbass")
print("\nDONE")


