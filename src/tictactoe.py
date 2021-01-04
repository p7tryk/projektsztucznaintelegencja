""" logika gry kolko i krzyzyk """
import numpy as np

#constants
CIRCLE = 1
CROSS  = 2
SIZE   = 7
WIN    = 5
SIDE   = CIRCLE
#

class gamestate:
    """plansza + wartosc stanu gry"""
    plansza = 0
    rank = 0
    side = CROSS
    prev = 0
    def getstate(self):
        return self.plansza

    def getrank(self):
        return self.rank

    def setState(self, inplansza):
        self.plansza = inplansza

    def setrank(self,value):
        self.rank = value

    def genState(self):
        self.plansza = np.zeros(shape = (SIZE,SIZE))

    def checkwin(self):
        """logika sprawdzania win condition"""
        print("nie sprawdzam")
        self.print()
        return False
    def makemove(self,x,y):
        #TODO sprawdzic czy legalny
        self.plansza[x,y] = self.side
        self.checkwin()

        if self.side == CIRCLE:
            self.side = CROSS
        else:
            self.side = CIRCLE

    def manualmove(self):
        x = input("wpisz x dla " + str(self.side) + "\n")
        y = input("wpisz y dla " + str(self.side) + "\n")
        self.makemove(x,y)
        self.checkwin()

    def automatedmove(self):
        g = 0
    def print(self):
        print(self.plansza)






def expand(plansza,side):
    """ ekspansja """
    lista = []
    for x in range(SIZE):
        for y in range(SIZE):
            if plansza[x][y] != 0:
                newplansza = plansza
                newplansza[x][y] = side
                lista.append(newplansza)

    return lista

def rank(lista):
    for element in lista:
        #TODO jakas logika nadawania wartosci
        element = 0
def choosePath(lista):
    #TODO BFS? DFS?
    lista = 0



#gameloop
state = gamestate()
state.genState()

while(1):
    state.print()
    state.manualmove()
    state.manualmove()
