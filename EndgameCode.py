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



def eval_function(mode, move, board2):
    total_ev = 0
    move2 = str(move)
    curr_board = board2.piece_map()
    our_orig_king_position = int(board2.king(chess.WHITE))
    our_orig_queen_position = -1
    for x in range(0,64):
        if(str(curr_board.get(x)) == "Q"):
            our_queen_position = x
            break
    print(list(board2.legal_moves))
    board2.push_san(move2)
    black_moves = list(board2.legal_moves)
    curr_board = board2.piece_map()
    king_position = int(board2.king(chess.BLACK))
    for x in range(0, len(black_moves)-1):
            black_moves[x] = str(black_moves[x])
    def isCheckmateInOne():
        return board2.is_checkmate()
    
    def isStalemate():
        return board2.is_stalemate()

    def canBeTaken():
        for x in black_moves:
            if(str(move2[2:]) == str(x)[:2]):
                return True
    
    def isKingOnBackRank():
        #returns 1 if on the 'a' file, 2 if on 'h' file, 3 if on 8th rank, 4 if on 1st rank, 
        # returns 5 if in front left corner, 6 if in back left corner, 7 if in back right corner, 8 if in front right corner, 0 if not on back rank
        if(king_position == 0):
            return 5
        elif(king_position == 56):
            return 6
        elif(king_position == 63):
            return 7
        elif(king_position == 7):
            return 8
        elif((king_position % 8) == 0):
            return 1
        elif((king_position % 8) == 7):
            return 2
        elif(king_position >= 56):
            return 3
        elif(king_position <= 7):
            return 4
        return 0

    def queenKingInCorner():
        which_corner = isKingOnBackRank()
        our_king_pos = int(board2.king(chess.WHITE))
        queenLocation = -1
        for x in range(0,64):
            if(str(curr_board.get(x)) == "Q"):
                queenLocation = x
                break
        king_move_val = our_king_pos - our_orig_king_position
        if(((which_corner == 5) or (king_position == 8)) and queenLocation == 25): #king target square = 10
            if(queenLocation != our_orig_queen_position):
                return -1000
            elif(our_king_pos == 10):
                return 10000
            elif(abs(10-our_king_pos) < abs(10-our_orig_king_pos)):
                return 200
            else:
                return 0
            
        elif(((which_corner == 6) or (king_position == 48)) and queenLocation == 33): #king target square = 50
            if(queenLocation != our_orig_queen_position):
                return -1000
            elif(our_king_pos == 50):
                return 10000
            elif(abs(50-our_king_pos) < abs(50-our_orig_king_pos)):
                return 200
            else:
                return 0
        elif(((which_corner == 7) or (king_position == 55)) and queenLocation == 38): #king target square = 54
            if(queenLocation != our_orig_queen_position):
                return -1000
            elif((our_king_pos) == 54):
                return 10000
            elif(abs(54-our_king_pos) < abs(54-our_orig_king_pos)):
                return 200
            else:
                return 0
        elif(((which_corner == 8) or (king_position == 15)) and queenLocation == 13): #king target square = 14
            if(queenLocation != our_orig_queen_position):
                return -1000
            elif(our_king_pos == 14):
                return 10000
            elif(abs(14-our_king_pos) < abs(14-our_orig_king_pos)):
                return 200
            else:
                return 0
        else:
            return 0

    def bring_our_king_to_middle():
        king_move_val = int(board2.king(chess.WHITE)) - our_orig_king_position
        
        if(our_orig_king_position <= 15):
            if((king_move_val) >= 8):
                return 100
            else:
                return 0
        elif(our_orig_king_position >= 48):
            if((king_move_val) <= -8):
                return 100
            else:
                return 0
        elif((our_orig_king_position % 8 == 0) or (our_orig_king_position % 8 == 1)):
            if(our_orig_king_position >= 32):
                if(king_move_val == -7):
                    return 100
                elif(king_move_val == 1):
                    return 90
                else:
                    return 0
            else: #9 to 18
                if(king_move_val == 7):
                    return 100
                elif(king_move_val == 1):
                    return 90
                else:
                    return 0
        elif((our_orig_king_position % 8 == 6) or (our_orig_king_position % 8 == 7)):
            if(our_orig_king_position >= 32): #54 to 45
                if(king_move_val == -9):
                    return 100
                elif(king_move_val == -1):
                    return 90
                else:
                    return 0
            else: #14 to 21
                if(king_move_val == 9):
                    return 100
                elif(king_move_val == -1):
                    return 90
                else:
                    return 0
        return 0

    def queen_cuts_king_on_edge_rank():
        if((isKingOnBackRank() == 1) and (move[2] == 'b')):
            return 20
        elif((isKingOnBackRank() == 2) and (move[2] == 'g')):
            return 20
        elif((isKingOnBackRank() == 3) and (move[3] == '7')):
            return 20
        elif((isKingOnBackRank() == 4) and (move[3] == '2')):
            return 20
        return 0

    def queenKnightsDistance():
        queenLocation = -1
        for x in range(0,64):
            if(str(curr_board.get(x)) == "Q"):
                queenLocation = x
                break
        board2.set_piece_at(queenLocation, chess.Piece(chess.KNIGHT, chess.WHITE))
        if(isKingOnBackRank() == 0):
            if(board2.is_check() == True):
                board2.set_piece_at(queenLocation, chess.Piece(chess.QUEEN, chess.WHITE))
                return 10
            else:
                board2.set_piece_at(queenLocation, chess.Piece(chess.QUEEN, chess.WHITE))
                return 0
        else:
            if((board2.is_check() == True) and (queen_cuts_king_on_edge_rank() != 0)):
                return 50
            else:
                return 0
        

    #def kingOpposition():


    if(isCheckmateInOne() == True):
        return 1000000
    elif(isStalemate() == True):
        return -100000
    elif(canBeTaken() == True):
        return -100000
    total_ev = queenKingInCorner() + queenKnightsDistance() + queen_cuts_king_on_edge_rank() + bring_our_king_to_middle()
    

#    board.pop()
    return total_ev




def main():
    board = generate_random_board(1)
    mode = "q"
    move_dict = {}
    legal_moves = list(board.legal_moves)
    curr_board = board.piece_map()
    found_move = False
    move_counter = 0
    #while(board.is_checkmate() == False and board.is_stalemate() == False and board.is_insufficient_material() == False and board.can_claim_fifty_moves() == False and board.can_claim_draw() == False):
    for x in range(1,10):
        legal_moves = list(board.legal_moves)
        found_move = False
        move_counter += 1
        for y in range(0, len(legal_moves)-1):
            legal_moves[y] = str(legal_moves[y])
        print(board)
        print("\n")
        print(len(legal_moves))
        move_dict.clear()
        for y in legal_moves:
            if(move_counter % 2 == 1):
                move_dict.update({y:eval_function(mode, str(y), board)})
                if(move_dict.get(y) == 1000000):
                    board.push_san(y)
                    found_move = True
                    break
                
                
            else:
                rand = random.randint(0,len(legal_moves)-1)
                move = legal_moves[rand]
                board.push_san(move)
                break
        if((found_move == False) and (move_counter % 2 == 1)):
            highest_eval = -1000000
            highest_eval_idx = -1
            for z in range(0,len(legal_moves)-1):
                print((move_dict.get(legal_moves[z])))
                if(int(move_dict.get(legal_moves[z])) > highest_eval):
                    highest_eval = int(move_dict.get(legal_moves[z]))
                    highest_eval_idx = z
            board.push_san(legal_moves[highest_eval_idx])
    
if __name__ == '__main__':
    main()


#Board square numbers
# 56 57 58 59 60 61 62 63              
# 48 49 50 51 52 53 54 55 
# 40 41 42 43 44 45 46 47
# 32 33 34 35 36 37 38 39
# 24 25 26 27 28 29 30 31
# 16 17 18 19 20 21 22 23
# 08 09 10 11 12 13 14 15
# 00 01 02 03 04 05 06 07
