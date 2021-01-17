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

    
    
    def makemove(self,x,y):
        #nie sprawdzamy czy jest legalny ale chuj
        self.plansza[x,y] = self.side
        checkwin(self.plansza)

        if self.side == CIRCLE:
            self.side = CROSS
        else:
            self.side = CIRCLE

    def manualmove(self):
        state.print()
        x = input("wpisz x dla " + ("kółko" if self.side == CIRCLE else "krzyżyk") + "\n")
        y = input("wpisz y dla " + ("kółko" if self.side == CIRCLE else "krzyżyk") + "\n")
        self.makemove(int(y)-1,int(x)-1)
        checkwin(self.plansza)
    def get(self, x, y):
        temp = self.plansza[x,y]
        if temp == CROSS:
            return "X"
        if temp == CIRCLE:
            return "O"
        else:
            return " "
        

    def automatedmove(self):
        state.print()
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

#wincheck
def winCols(curplansza):
    """wygrywajace kolumny"""
    for x in range(SIZE):
        #circle
        count = 0
        longestcount = 0
        for y in range(SIZE):
            if curplansza[x,y] == CIRCLE:
                count+=1
                if count > longestcount:
                    longestcount = count
                else:
                    count=0
            if longestcount >=4:
                return True
   
            #cross
        count = 0
        longestcount = 0
        for y in range(SIZE):
            if curplansza[x,y] == CROSS:
                count+=1
                if count > longestcount:
                    longestcount = count
                else:
                    count=0
            if longestcount >=4:
                return True
        #default
        return False

def winRows(curplansza):
    """wygrywajace kolumny"""
    for x in range(SIZE):
        #circle
        count = 0
        longestcount = 0
        for y in range(SIZE):
            if curplansza[x,y] == CIRCLE:
                count+=1
                if count > longestcount:
                    longestcount = count
            else:
                count=0
            if longestcount >=4:
                return True
            
            #cross
            count = 0
            longestcount = 0
        for y in range(SIZE):
            if curplansza[x,y] == CROSS:
                count+=1
                if count > longestcount:
                    longestcount = count
                else:
                    count=0
            if longestcount >=4:
                return True
        #default
        return False

def winDiag(curplansza):
    """wygrywanie przez skos"""
    #FIXME: zrobic
    return False

def checkwin(curplansza):
    """logika sprawdzania win condition"""
    #LATER: teoretycznie nie musimy sprawdzac ale wtedy nasze AI bedzie dzialac zawsze (nawet jak wygrywamy)
    #print("nie sprawdzam")
    win = False
    
    win = winRows(curplansza)
    if win:
        print("win")
        return True
    win = winCols(curplansza)
    if win:
        print("win")
        return True
    win = winDiag(curplansza)
    if win:
        print("win")
        return True
    return win


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

