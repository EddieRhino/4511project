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
    board_cpy = board.copy()
    total_ev = 0
    move2 = str(move)
    curr_board = board_cpy.piece_map()
    our_orig_king_position = int(board_cpy.king(chess.WHITE))
    our_orig_queen_position = -1
    for x in range(0,64):
        if(str(curr_board.get(x)) == "Q"):
            our_orig_queen_position = x
            break
    board_cpy.push_san(move2)

    curr_board = board_cpy.piece_map()
    our_new_queen_position = -1
    for x in range(0,64):
        if(str(curr_board.get(x)) == "Q"):
            our_new_queen_position = x
            break

    black_moves = list(board_cpy.legal_moves)
    
    king_position = int(board_cpy.king(chess.BLACK))
    for x in range(0, len(black_moves)):
            black_moves[x] = str(black_moves[x])
    def isCheckmateInOne():
        return board_cpy.is_checkmate()
    
    def isStalemate():
        return board_cpy.is_stalemate()

    def canBeTaken():
        if(board_cpy.is_check() == False):
            return False
        else:
            for x in range(0,len(black_moves)):
                if(chess.square_name(our_new_queen_position) == str((black_moves[x]))[2:]):
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
        if(which_corner == 0):
            return 0
        our_king_pos = int(board_cpy.king(chess.WHITE))
        queenLocation = -1
        for x in range(0,64):
            if(str(curr_board.get(x)) == "Q"):
                queenLocation = x
                break
        if(((which_corner == 5) or (king_position == 8)) and (queenLocation == 25)): #king target square = 10
            if(our_king_pos == 18):
                return 10000
            elif(abs(18-our_king_pos) < abs(18-our_orig_king_position)):
                return 100
            else:
                return 0
        elif(((which_corner == 5) or (king_position == 1)) and (queenLocation == 11)): #king target square = 17
            if(our_king_pos == 18):
                return 10000
            elif(abs(18-our_king_pos) < abs(18-our_orig_king_position)):
                return 100
            else:
                return 0
            
        elif(((which_corner == 6) or (king_position == 48)) and (queenLocation == 33)): #king target square = 50
            if(our_king_pos == 42):
                return 10000
            elif(abs(42-our_king_pos) < abs(42-our_orig_king_position)):
                return 100
            else:
                return 0
        elif(((which_corner == 6) or (king_position == 57)) and (queenLocation == 51)): #king target square = 41
            if(our_king_pos == 42):
                return 10000
            elif(abs(42-our_king_pos) < abs(42-our_orig_king_position)):
                return 100
            else:
                return 0
        elif(((which_corner == 7) or (king_position == 55)) and (queenLocation == 38)): #king target square = 53
            if((our_king_pos) == 45):
                return 10000
            elif(abs(45-our_king_pos) < abs(45-our_orig_king_position)):
                return 100
            else:
                return 0
        elif(((which_corner == 7) or (king_position == 62)) and (queenLocation == 52)): #king target square = 46
            if((our_king_pos) == 45):
                return 10000
            elif(abs(46-our_king_pos) < abs(46-our_orig_king_position)):
                return 100
            else:
                return 0
        elif((((which_corner == 8) or (king_position == 15)) and (queenLocation == 30))): #king target square = 13
            if(our_king_pos == 21):
                return 10000
            elif(abs(21-our_king_pos) < abs(21-our_orig_king_position)):
                return 100
            else:
                return 0
        elif(((which_corner == 8) or (king_position == 6)) and (queenLocation == 12)): #king target square = 22
            if(our_king_pos == 21):
                return 10000
            elif(abs(21-our_king_pos) < abs(21-our_orig_king_position)):
                return 100
            else:
                return 0
        else:
            return 0

    def bring_our_king_to_middle():
        king_move_val = int(board_cpy.king(chess.WHITE)) - our_orig_king_position
        
        if(our_orig_king_position <= 15):
            if((king_move_val) >= 8):
                return 500
            else:
                return 0
        elif(our_orig_king_position >= 48):
            if((king_move_val) <= -8):
                return 500
            else:
                return 0
        elif((our_orig_king_position % 8 == 0) or (our_orig_king_position % 8 == 1)):
            if(our_orig_king_position >= 32):
                if(king_move_val == -7):
                    return 500
                elif(king_move_val == 1):
                    return 400
                else:
                    return 0
            else: #9 to 18
                if(king_move_val == 9):
                    return 500
                elif(king_move_val == 1):
                    return 400
                else:
                    return 0
        elif((our_orig_king_position % 8 == 6) or (our_orig_king_position % 8 == 7)):
            if(our_orig_king_position >= 32): #54 to 45
                if(king_move_val == -7):
                    return 500
                elif(king_move_val == -1):
                    return 400
                else:
                    return 0
            else: #14 to 21
                if(king_move_val == 7):
                    return 500
                elif(king_move_val == -1):
                    return 400
                else:
                    return 0
        return 0

    def queen_cuts_king_on_edge_rank():
        if((isKingOnBackRank() == 1) and (move2[2] == 'b')):
            return 20
        elif((isKingOnBackRank() == 2) and (move2[2] == 'g')):
            return 20
        elif((isKingOnBackRank() == 3) and (move2[3] == '7')):
            return 20
        elif((isKingOnBackRank() == 4) and (move2[3] == '2')):
            return 20
        else:
            return 0

    def queenKnightsDistance():
        queenLocation = -1
        for x in range(0,64):
            if(str(curr_board.get(x)) == "Q"):
                queenLocation = x
                break
        board_cpy.set_piece_at(queenLocation, chess.Piece(chess.KNIGHT, chess.WHITE))
        if(isKingOnBackRank() == 0):
            if(board_cpy.is_check() == True):
                board_cpy.set_piece_at(queenLocation, chess.Piece(chess.QUEEN, chess.WHITE))
                return 10
            else:
                board_cpy.set_piece_at(queenLocation, chess.Piece(chess.QUEEN, chess.WHITE))
                return 0
        else:
            if((board_cpy.is_check() == True) and (queen_cuts_king_on_edge_rank() != 0)):
                board_cpy.set_piece_at(queenLocation, chess.Piece(chess.QUEEN, chess.WHITE))
                return 50
            else:
                board_cpy.set_piece_at(queenLocation, chess.Piece(chess.QUEEN, chess.WHITE))
                return 0
        

    #def kingOpposition():


    if(isCheckmateInOne() == True):
        #print("CHECKMATE")
        return 1000000
    elif(isStalemate() == True):
        #print("STALEMATE")
        return -100000
    elif(canBeTaken() == True):
        #print("BLUNDERED A PIECE")
        return -100000000
    else:
        total_ev = queenKingInCorner() + queenKnightsDistance() + queen_cuts_king_on_edge_rank() + bring_our_king_to_middle()

        return total_ev




def main():
    board = generate_random_board(1)
    mode = "q"
    move_dict = {}
    legal_moves = list(board.legal_moves)
    curr_board = board.piece_map()
    found_move = False
    move_counter = 0
    while(board.is_checkmate() == False and board.is_stalemate() == False and board.is_insufficient_material() == False and board.can_claim_fifty_moves() == False and board.can_claim_draw() == False):
    #for x in range(0,10):
        legal_moves = list(board.legal_moves)
        found_move = False
        move_counter += 1
        for p in range(0, len(legal_moves)):
            legal_moves[p] = str(legal_moves[p])
        move_dict.clear()
        for y in range(0, len(legal_moves)):
            if(move_counter % 2 == 1):
                move_dict.update({y:eval_function(mode, str(legal_moves[y]), board)})             
            else:
                rand = random.randint(0,len(legal_moves)-1)
                move = legal_moves[rand]
                board.push_san(str(move))
                break
        if(move_counter % 2 == 1):
            highest_eval = -1000000
            highest_eval_idx = -1
            print(move_dict)
            for z in range(0,len(legal_moves)):
                if((move_dict.get(z)) > highest_eval):
                    highest_eval = int(move_dict.get(z))
                    highest_eval_idx = z
            board.push_san(str(legal_moves[highest_eval_idx]))
            print(highest_eval_idx)
            print(str(legal_moves[highest_eval_idx]))
            print(board)
        else:
            continue

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
    print("GAME OVER")
    
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
