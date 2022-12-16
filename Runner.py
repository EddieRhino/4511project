from EndgameCode import *
import time
from EndgameCode2 import *
import json

table = None
try:
    f = open('table_file.txt', 'r')
    data = f.read()
    table = data.split("\n")
except:
    table = CreateWhitePossiblePositionsTable()
    with open('table_file.txt', 'w') as f:
        for line in table:
            f.write("%s\n" % line)



dictionary = WriteFileToDict("dictionary.txt")

# dictionary = DictionaryMaker(table)
# dictionary.fill_dictionary()
# dictionary.WriteDictToFile("dictionary.txt")


# with open('dictionary.txt','w') as dictionary_file:
#     dictionary_file.write(json.dumps(dictionary.dictionary))

for i in range(20):
    game = Game(DictionaryAgent(dictionary), UserAgent())
    game.play_random_game(1,0,0,0)
