from EndgameCode import *
import time

table = None
try:
    f = open('table_file.txt', 'r')
    data = f.read()
    table = data.split("\n")
except:
    table = CreateWhitePossiblePositionsTable()
    with open('table_file.txt', 'w') as f:
        for line in lines:
            f.write("%s\n" % line)

dictionary = {}
for pos in table:
    comp_fen = 


dictionary = CreateDictionary(0,0,0,0,table)

chess_game = Game(DictionaryAgent(dictionary), RandomAgent())
chess_game.play_random_game(1,0,0,0)