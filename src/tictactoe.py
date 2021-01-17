""" logika gry kolko i krzyzyk """
import numpy as np

#gamemode
PLAYER_FIRST = True
PVP_MODE = True

#constants
CIRCLE = 1
CROSS  = 2
SIZE   = 7
WIN    = 5
START_SIDE  = CROSS
#

class gamestate:
    """plansza + wartosc stanu gry"""
    plansza = 0
    score = 0
    side = START_SIDE
    prev = 0
    def getstate(self):
        return self.plansza

    def getscore(self):
        return self.score

    def setState(self, inplansza):
        self.plansza = inplansza

    def setscore(self,value):
        self.score = value

    def genState(self):
        self.plansza = np.zeros(shape = (SIZE,SIZE))

    def checkwin(self):
        """logika sprawdzania win condition"""
        #LATER: teoretycznie nie musimy sprawdzac ale wtedy nasze AI bedzie dzialac zawsze (nawet jak wygrywamy)
        print("nie sprawdzam")
        self.print()
        return False
    def makemove(self,x,y):
        #nie sprawdzamy czy jest legalny ale chuj
        self.plansza[x,y] = self.side
        self.checkwin()

        if self.side == CIRCLE:
            self.side = CROSS
        else:
            self.side = CIRCLE

    def manualmove(self):
        x = input("wpisz x dla " + ("kółko" if self.side == CIRCLE else "krzyżyk") + "\n")
        y = input("wpisz y dla " + ("kółko" if self.side == CIRCLE else "krzyżyk") + "\n")
        self.makemove(int(x)-1,int(y)-1)
        self.checkwin()
    def get(self, x, y):
        temp = self.plansza[x,y]
        if temp == CROSS:
            return "X"
        if temp == CIRCLE:
            return "O"
        else:
            return " "
        

    def automatedmove(self):
        """ tutaj wszystko zwiazane z sztuczna intelgencja"""
        g = 0
    def print(self):
        for x in range(0,SIZE):
            print("\n----------------------------")
            for y in range(0, SIZE):
                print(" " + self.get(x,y) + " ", end = "|")
        print("\n----------------------------", end = "\n")





def expand(plansza,side):
    """ ekspansja """
    lista = []
    for x in range(SIZE):
        for y in range(SIZE):
            if plansza[x,y] != 0:
                #TODO jak kopiowac te numpy array
                newplansza = plansza
                newplansza[x,y] = side
                lista.append(newplansza)

    return lista

def score(lista):
    for element in lista:
        #TODO jakas logika nadawania wartosci
        element = 0
def choosePath(lista):
    #TODO BFS? DFS?
    lista = 0



#gameloop
state = gamestate()
state.genState()
state.print()
while(1):
    #game loop tu sumie nic nie zmieniac juz nigdy
    if PLAYER_FIRST:
        state.manualmove()
    if PVP_MODE:
        state.manualmove()
    else:
        state.automatedmove()
    if PLAYER_FIRST:
        state.manualmove()
        
