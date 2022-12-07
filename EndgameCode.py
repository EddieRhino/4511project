import random
import chess

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


board = generate_random_board(2,2)

print(board)
