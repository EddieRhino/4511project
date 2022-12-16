from EndgameCode import *



class DictionaryMaker():
    dictionary = {}
    black_dictionary = {}

    def __init__(self, table):
        for item in table:
            self.dictionary[item] = None

    def fill_dictionary(self):
        for depth in range(20):
            self.black_dictionary = {}
            print("Starting phase", depth)
            self.fill_with_depth(depth)

    def maximum_depth_from_black(self,board):
        for move in board.legal_moves:
            board.push(move)
            if(self.dictionary.get(GetCompFromFen(board.fen())) == None):
                board.pop()
                self.black_dictionary[GetCompFromFen(board.fen())] = False
                return False
            board.pop()
        if(board.is_stalemate() or board.is_insufficient_material()):
            self.black_dictionary[GetCompFromFen(board.fen())] = False
            return False
        self.black_dictionary[GetCompFromFen(board.fen())] = True
        return True


    def fill_with_depth(self, depth):
        temp_dictionary = {}

        for item in self.dictionary:
            board = chess.Board(item)
            if(depth == 0):
                for move in board.legal_moves:
                    board.push(move)
                    if board.is_checkmate():
                        temp_dictionary[item] = (depth, move)
                        break
                    board.pop()
            elif self.dictionary[item] != None:
                continue
            else:
                for move in board.legal_moves:
                    board.push(move)
                    min_depth = self.black_dictionary.get(GetCompFromFen(board.fen()))
                    if min_depth:
                        temp_dictionary[item] = (depth,move)
                        break
                    elif min_depth != None:
                        board.pop()
                        continue
                    
                    is_win = self.maximum_depth_from_black(board)
                    if is_win:
                        temp_dictionary[item] = (depth,move)
                        break
                    board.pop()
        
        def transfer_dictionary(temp_dict):
            for item in temp_dict:
                self.dictionary[item] = temp_dict[item]
        
        transfer_dictionary(temp_dictionary)


    def WriteDictToFile(self, filename):
        try:
            f = open(filename, 'w')
            for item in self.dictionary:
                f.write(f"{item}\t")
                f.write(f"{self.dictionary.get(item)}\n")
            print("Writing to file successful")
        except:
            print("Error writing to file", filename)

    

                

