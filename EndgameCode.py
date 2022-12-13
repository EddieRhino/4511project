import random
import chess

dictionary = {}
black_dictionary = {}

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

def generate_black_fen(board_list):
    fen = ""
    for row in range(8):
        num = 0
        for col in range(8):
            if board_list[row][col] == 'e':
                num = num + 1
            else: 
                if num != 0:
                    fen += str(num)
                num = 0
                fen += board_list[row][col]
        if num > 0:
            fen += str(num)
        if row < 7:
            fen += '/'

    fen += " b - - 0 1"
    return fen

def generate_fen(board_list):
    fen = ""
    for row in range(8):
        num = 0
        for col in range(8):
            if board_list[row][col] == 'e':
                num = num + 1
            else: 
                if num != 0:
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


class ChessAgent:
    def move(self, board):
        pass

class RandomAgent(ChessAgent):
    def __init__(self):
        pass
    def move(self, board):
        legal_moves = list(board.legal_moves)
        rand = random.randint(0,len(legal_moves)-1)
        move = str(legal_moves[rand])
        board.push_san(move)
        return board

class UserAgent(ChessAgent):
    def __init__(self):
        pass
    def move(self, board):
        legal_moves = list(board.legal_moves)
        print("Please enter your move:")
        san = input()
        move = chess.Move.from_uci(str(san))
        while(not move in legal_moves):
            print(san)
            print("Illegal move, please enter a legal move ")
            print("Legal moves: ", legal_moves)
            san = input()
            
        board.push_san(str(san))
        return board


class DictionaryAgent(ChessAgent):
    def __init__(self, dictionary):
        self.dictionary = dictionary
    
    def move(self, board):
        fen = board.fen()
        space = fen.find(" ")
        comp_fen = fen[:space + 2:]

        (move,num) = self.dictionary.get(comp_fen)
        if move != None:
            board.push_san(move)
            return board

        # If (For some reason) move isn't in the dictionary, do a random move
        print("Move not in Dictionary: executing random move")
        legal_moves = list(board.legal_moves)
        rand = random.randint(0,len(legal_moves)-1)
        move = str(legal_moves[rand])
        board.push_san(move)
        return board


class Game:
    white_agent = None
    black_agent = None

    def __init__(self, white = RandomAgent(), black = RandomAgent()):
        self.black_agent = black
        self.white_agent = white
    
    def get_board(self):
        return board

    def play_random_game(self, q,r,b,n):
        board = generate_random_board(q,r,b,n)
        print(board)
        print("\n")
        while(not board.is_checkmate() and not board.is_stalemate() and not board.is_insufficient_material() and\
        not board.is_fivefold_repetition() and not board.is_seventyfive_moves()):
            if(board.turn):
                board = self.white_agent.move(board)
            else:
                board = self.black_agent.move(board)
            print(board)
            print("\n")
        print(board.outcome())
    



def GetCompFromFen(fen):
    space = fen.find(" ")
    return fen[:space + 2:]

def CreateWhitePossiblePositionsTable():
    #set to all empty
    rows, cols = (8, 8)
    board_list = [['e' for i in range(cols)] for j in range(rows)]

    possiblepos = []

    #iterate through every pos, add it to possiblepos
    for queenpos in range(64):
        
        row = int(queenpos/8)
        col = queenpos % 8
        board_list[row][col] = 'Q'


        for wkingpos in range(64):
            if(wkingpos == queenpos):
                continue


            wkrow = int(wkingpos/8)
            wkcol = wkingpos % 8
            board_list[wkrow][wkcol] = 'K'
           

            
            for bkingpos in range(64):
                if queenpos == bkingpos or wkingpos == bkingpos:
                    continue


                bkrow = int(bkingpos/8)
                bkcol = bkingpos % 8
                board_list[bkrow][bkcol] = 'k'
                
                fen = generate_fen(board_list)
                try:
                    board = chess.Board(fen)
                    if(board.is_valid()):
                        possiblepos.append(fen)
                except ValueError:
                    print("Invalid position: ",queenpos, wkingpos, bkingpos)

                
                board_list[bkrow][bkcol] = 'e'

            board_list[wkrow][wkcol] = 'e'

        board_list[row][col] = 'e'

    for i in range(len(possiblepos)):
        possiblepos[i] = GetCompFromFen(possiblepos[i])
    return possiblepos


def CreateBlackPossiblePositionsTable():
    #set to all empty
    rows, cols = (8, 8)
    board_list = [['e' for i in range(cols)] for j in range(rows)]

    possiblepos = []
    counter = 0

    #iterate through every pos, add it to possiblepos
    for queenpos in range(64):
        
        row = int(queenpos/8)
        col = queenpos % 8
        board_list[row][col] = 'Q'


        for wkingpos in range(64):
            if(wkingpos == queenpos):
                continue


            wkrow = int(wkingpos/8)
            wkcol = wkingpos % 8
            board_list[wkrow][wkcol] = 'K'
           

            
            for bkingpos in range(64):
                if queenpos == bkingpos or wkingpos == bkingpos:
                    continue


                bkrow = int(bkingpos/8)
                bkcol = bkingpos % 8
                board_list[bkrow][bkcol] = 'k'
                
                fen = generate_black_fen(board_list)
                try:
                    board = chess.Board(fen)
                    if(board.is_valid()):
                        possiblepos.append(fen)
                except ValueError:
                    print("Invalid position: ",queenpos, wkingpos, bkingpos)

                
                board_list[bkrow][bkcol] = 'e'

            board_list[wkrow][wkcol] = 'e'

        board_list[row][col] = 'e'

    for i in range(len(possiblepos)):
        possiblepos[i] = GetCompFromFen(possiblepos[i])
    print(counter)
    return possiblepos



def FindAllCheckmates(table):
    all_checkmates = []
    for fen in table:
        fen += " - - 0 1"
        board = chess.Board(fen)
        if(board.is_checkmate()):
            all_checkmates.append(fen)
    print(all_checkmates)
    print(len(all_checkmates))


class Node():
    depth_win = -1
    children = []

    def __init__(self, is_white, board):
        self.board = chess.Board(board.fen())
        self.fen = board.fen()
        space = self.fen.find(" ")
        self.comp_fen = self.fen[:space + 2:]
        self.is_white = is_white

    def __str__(self, depth=1):
        return str(len(children))



# returns a node
def CreateMinimaxTree(found_positions, board, white_turn, num_moves):
    pass

def CreateTree(my_list, board, depth, is_white):
    #Error Checking
    if(depth > 19):
        return (None,[])
    root = Node(is_white, board)
    if(root.comp_fen in my_list):
        return (None,[])
    if(is_white and root.comp_fen in dictionary):
        return (None,[])
    
    return_list = []

    my_list.append(root.comp_fen)
    return_list.append(root.comp_fen)

    if(board.is_checkmate()):
        root.depth_win = 0
        return (root, my_list)
    elif board.is_stalemate() or board.is_insufficient_material():
        root.depth_win = 100
        return (root, return_list)
    



    # Iterate through all moves. Check if in list already or in 
    # Dictionary, if so pass, else do the same for children
    legal_moves = list(board.legal_moves)
    counter = 0
    fen = board.fen()
    
    for move in legal_moves:
        counter += 1
        board = chess.Board(fen)

        

        
        
              
        board.push_san(str(move))
        
        (child,new_list) = CreateTree(my_list, board, depth+1, not is_white)

        if child == None:
            continue

        my_list.append(new_list)
        return_list.append(new_list)

        
        root.children.append(child)

        

    
    return (root,return_list)


# Return the depth of win, -1 on error
def AddToDictionary_WithMaxDepth(root, max_depth):
    # For all white moves, add current fen + minimum depth win move
    if root.is_white:
        if max_depth < 1:
            return 200
        if root.comp_fen in dictionary:
            (move, num) = dictionary.get(root.comp_fen)
            if(num < 200):
                return num + 1

        print("For loop started")

        return_depth = 200
        return_node = None
        for child in root.children:
            temp_depth = AddToDictionary_WithMaxDepth(child, max_depth - 1)
            if temp_depth < return_depth or temp_depth != -1:
                return_node = child
                return_depth = temp_depth

        print("For loop ended")
        
        if return_node == None:
            print("Error. Return depth:", return_depth)
            return 200

        board = chess.Board(root.fen)
        final_move = None
        for move in board.legal_moves:
            board = chess.Board(root.fen)
            board.push_san(str(move))
            fen = board.fen()
            space = fen.find(" ")
            comp_fen = fen[:space + 2:]
            if comp_fen == return_node.comp_fen:
                final_move = move
                break

        if final_move != None:
            dictionary[root.comp_fen] = (final_move, return_depth)
        return return_depth + 1

    
    # For all black moves, add nothing to the dictionary, simply call the function again
    # Set black_dictionary to the max depth of all children
    else:
        if max_depth < 1:
            return 200
        if root.comp_fen in black_dictionary:
            return black_dictionary[root.comp_fen] + 1
        #Checkmate - return depth of 1 for win
        if root.depth_win == 0:
            return 1
        #Stalemate - return high depth for stalemate
        if root.depth_win == 100:
            return 101
        return_depth = -1
        for child in root.children:
            temp_depth = AddToDictionary_WithMaxDepth(child, max_depth)
            if temp_depth > return_depth:
                return_depth = temp_depth

        if return_depth != -1:
            black_dictionary[root.comp_fen] = return_depth
            return return_depth + 1




def CreateDictionary(q=0,r=0,b=0,n=0,table = None):

    counter = 1
    tree = None

    print("Phase 1 done")

    for position in table:
        print("Next phase: phase", counter)
        if(len(dictionary) >= len(table)):
            break
        
        board = chess.Board(position)

        fen = board.fen()
        space = fen.find(" ")
        comp_fen = fen[:space + 2:]


        if (comp_fen in dictionary and dictionary[comp_fen] < 200):
            (move, num) = dictionary[comp_fen]
            if num < 200:
                counter += 1
                continue

        (tree,mylist) = CreateTree([], board, 0, True)

        print("Phase 1.1 done, starting phase 1.2")

        for i in range(1,10):
            AddToDictionary_WithMaxDepth(tree, i)

        counter += 1
        print(board)
        print(dictionary.get(comp_fen))
    return dictionary

        
        
        

        





    
    
