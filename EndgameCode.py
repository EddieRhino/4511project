import chess
import random

# board = chess.Board()
# while(board.is_checkmate() == False and board.is_stalemate() == False and board.is_insufficient_material() == False and board.can_claim_fifty_moves() == False and board.can_claim_draw() == False):
# #for x in range(1,10):

#     legal_moves = list(board.legal_moves)

#     rand = random.randint(0,len(legal_moves)-1)
#     move = str(legal_moves[rand])
#     print(board)
#     print("\n")
#     board.push_san(move)
# print("\n")
# if(board.is_checkmate() == True):
#     print("CHECKMATE")
# elif(board.is_stalemate() == True):
#     print("lmao stalemate")
# elif(board.is_insufficient_material() == True):
#     print("yo too small")
# elif(board.can_claim_fifty_moves() == True):
#     print("50")
# elif(board.can_claim_draw() == True):
#     print("draw dumbass")
# print("\nDONE")

def generate_list(q = 0, r = 0, b = 0, n = 0):
    rows, cols = (8, 8)
    board_list = [['e' for i in range(cols)] for j in range(rows)]

    def place_piece(current_list, piece):
        col = random.randint(0,7)
        row = random.randint(0,7)
        while(current_list[col][row] != 'e'):
            col = random.randint(0,7)
            row = random.randint(0,7)
        current_list[col][row] = piece

    while(q > 0):
        place_piece(board_list, 'Q')
        q = q - 1
    while(r > 0):
        place_piece(board_list, 'R')
        r = r - 1
    while(b > 0):
        place_piece(board_list, 'B')
        b = b - 1
    while(n > 0):
        place_piece(board_list, 'N')
        n = n - 1
    
    place_piece(board_list, "K")
    place_piece(board_list, "k")

    return board_list


def generate_fen(board_list):
    fen = ""
    for row in range(8):
        num = 0
        for col in range(8):
            if board_list[row][col] == 'e':
                num = num + 1
            else: 
                fen += str(num)
                num = 0
                fen += board_list[row][col]
        if num > 0:
            fen += str(num)
        if row < 7:
            fen += '/'

    fen += " w - - 0 1"
    return fen



# Generates random board from given number of pieces (queen, rook, bishop, knight)
def generate_random_board(q = 0, r = 0, b = 0, n = 0):
    mylist = generate_list(q,r,b,n)

    fen = generate_fen(mylist)

    try:
        board = chess.Board(fen)
    except ValueError:
        board = generate_random_board(q,r,b,n)
    
    


    if(not board.is_valid()):
        board = generate_random_board(q,r,b,n)
    return board



def eval_function(mode, move, board):
    total_ev = 0
    board.push_san(move)
    black_moves = list(board.legal_moves)
    for x in range(0, len(black_moves)-1):
            black_moves[x] = str(black_moves[x])
    def isCheckmateInOne():
        return board.is_checkmate()
    
    def isStalemate():
        return board.is_stalemate()

    def canBeTaken():
        for x in black_moves:
            if(move[2:] == x[:2]):
                return True
    
    def cuts_king_on_edge_rank():
        for x in black_moves:




    if(isCheckmateInOne() == True):
        return 1000000
    elif(isStalemate() == True):
        return -50
    elif(canBeTaken() == True):
        return -50
    

    board.pop()





def main():
    board = generate_random_board(1)
    print(board)

    mode = "q"
    move_dict = {}
    legal_moves = list(board.legal_moves)
    print(board.piece_map())

    move_counter = 1
    for x in range(1,10):
        legal_moves = list(board.legal_moves)
        for y in range(0, len(legal_moves)-1):
            legal_moves[y] = str(legal_moves[y])
        print(board)
        move_dict.clear()
        for y in legal_moves:
            highest_eval = -1000000
            highest_eval_idx = -1
            if(move_counter % 2 == 1):
                move_dict.update{y:eval_function(mode, y, board)}
                if(move_dict.get(y) == 1000000):
                    board.push_san(y)
                    break
                for z in range(0,len(legal_moves)-1):
                    if(move_dict.get(legal_moves[z]) > highest):
                        move_dict.get(legal_moves[z]) = highest
                        highest_eval_idx = z
                board.push_san(legal_moves[highest_eval_idx])
                
            else:
                rand = random.randint(0,len(legal_moves)-1)
                move = legal_moves[rand]
                board.push_san(move)
                break
        move_counter += 1
    
if __name__ == '__main__':
    main()
