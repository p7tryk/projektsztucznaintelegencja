#!/usr/bin/env python3
""" logika gry kolko i krzyzyk """
import numpy as np
import score as sc
import win as wn


#gamemode
PLAYER_FIRST = True
PVP_MODE = False

#constants
EMPTY  = 0
CIRCLE = 1
CROSS  = 2
SIZE   = 7
WIN    = 5
START_SIDE  = CROSS
DEPTH = 2
#ai variables
SCORE_LONGEST_MULTIPLIER = 10
SCORE_NEIGHBOUR_MULTIPLIER = 2

#
class gamestate:
    """plansza + wartosc stanu gry"""
    plansza = 0
    scoreCircle = 0
    scoreCross = 0
    side = START_SIDE
    prev = None
    current = False


    def __init__(self, plansza = np.zeros(shape = (SIZE,SIZE)), side = START_SIDE):
        self.plansza = plansza
        self.side = side


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
        #time.sleep(3) #FIXME: usunac na koniec

        level1 = []
        level2 = []
        lastlevel = []

        level1 = expand(self,self.side,level1)
        score(level1)
        # for element in level1:
        #     level2 = expand(element.plansza,element.side, level2)
        # score(level2)

        #TBD ile tych poziomow ma byc
        #
        #

        for element in level1:
            lastlevel = expand(element,element.side, lastlevel)
        score(lastlevel)
        desiredState = highestScore(lastlevel,self.side)
        tempx, tempy = sc.diffState(self.plansza,desiredState.plansza)

        # print("input do automatedmove")
        # debugPlansza(self.plansza)
        # print("endinput do automatedmove")
        print("makemove(" + str(tempx) + "," + str(tempy)+")")
        self.makemove(tempx,tempy)
        state.print()
        return

    def print(self):
        scoreSingle(self)
        for x in range(0,SIZE):
            print("\n----------------------------")
            for y in range(0, SIZE):
                print(" " + self.get(x,y) + " ", end = "|")
        print("\n----------------------------" + "krzyzyk score=" + str(self.scoreCross) , end = "\n")
        print("                            " + "kolko score=" + str(self.scoreCircle))




def expand(oldgamestate,side,lista):
    """ ekspansja """
    elements = 0
    for x in range(SIZE):
        for y in range(SIZE):
            if canYou(oldgamestate.plansza, x, y):
                newgamestate = gamestate(np.copy(oldgamestate.plansza),side)
                newgamestate.makemove(x,y)
                newgamestate.prev = oldgamestate
                lista.append(newgamestate)
                elements+=1
    #print("ekspansja zakonczona elementow=" + str(elements))
    if elements == 0:
        debugPlansza(oldgamestate.plansza)
    return lista

def canYou(plansza, x,y):
    if plansza[x,y] == CROSS or plansza[x,y] == CIRCLE:
        return False
    return True

def score(lista):
    """ nadawanie wartosci, argumenty zawsze kolko,krzyzyk = funkcja()"""
    #print("scoring len(lista)= " + str(len(lista)))
    for element in lista:
        scoreSingle(element)
 
def scoreSingle(element):
    #FIXME: lepsza logika nadawania wyniku
    scoreCross = 0
    scoreCircle = 0
    tempCircle = 0
    tempCross = 0

    #najdluzsze sciezki w rzedach
    tempCircle, tempCross = sc.longestWinStreak(element.plansza)
    tempCircle *= SCORE_LONGEST_MULTIPLIER
    tempCross *= SCORE_LONGEST_MULTIPLIER
    scoreCross += tempCross*tempCross
    scoreCircle += tempCircle*tempCircle
    #ocen najblizsze pola
    tempCircle, tempCross = sc.freeSpacesScore(element.plansza)
    tempCircle *= SCORE_NEIGHBOUR_MULTIPLIER
    tempCross *= SCORE_NEIGHBOUR_MULTIPLIER
    scoreCross += tempCross
    scoreCircle += tempCircle
    #ocen najblizsze pola
    tempCircle, tempCross = sc.longestMaybeStreak(element.plansza)
    tempCircle *= SCORE_LONGEST_MULTIPLIER
    tempCross *= SCORE_LONGEST_MULTIPLIER
    scoreCross += tempCross
    scoreCircle += tempCircle

    #na pierwszej generacji
    if element.prev!= None:
        tempCircle, tempCross = sc.scoreMiddle(element.prev.plansza,element.plansza)
        scoreCross += tempCross*tempCross
        scoreCircle += tempCircle*tempCircle
        

    win = checkwin(element.plansza)
    if element.side == CIRCLE and win:
        scoreCircle += 100000
    if element.side == CROSS and win:
        scoreCross += 100000


    element.scoreCircle = scoreCircle
    element.scoreCross = scoreCross
    return



def highestScore(lista,side):
    #BFS
    scoreList = []
    for element in lista:
        temp = 0
        temp = element.scoreCross-element.scoreCircle
        while element.prev != None:
            element = element.prev
            temp +=element.scoreCross-element.scoreCircle
        scoreList.append(temp)

    bestState = lista[0]
    bestScore = 0
    for tempscore in scoreList:
        if side == CROSS: #jezeli krzyzyk to im wiekszy (na plusie) tym lepiej
            if tempscore > bestScore:
                bestScore = tempscore
                temp = scoreList.index(tempscore)
                #print("index of scorelist ="+str(temp))
                bestState = lista[temp]
        else:
            if tempscore < bestScore:
                bestScore = tempscore
                temp = scoreList.index(tempscore)
                #print("index of scorelist ="+str(temp))
                bestState = lista[temp]

    #chemy dostac nastepny ruch
    for x in range(DEPTH-1):
        bestState = bestState.prev
    print("best state dla" + ("kółko" if bestState.side == CIRCLE else "krzyżyk")\
          + " "  + str(bestScore))
    bestState.print()
    print("endbeststate")
    return bestState



def debugPlansza(plansza):
    tempstate = gamestate(plansza)
    scoreSingle(tempstate)
    for x in range(0,SIZE):
        print("\n----------------------------")
        for y in range(0, SIZE):
            print(" " + tempstate.get(x,y) + " ", end = "|")
    print("\n----------------------------" + "krzyzyk score=" + str(tempstate.scoreCross) , end = "\n")
    print("                            " + "kolko score=" + str(tempstate.scoreCircle))

#wincheck










def checkwin(curplansza):
    """logika sprawdzania win condition"""
    #FIXME: win po skosie
    #print("nie sprawdzam")
    

    if wn.winRows(curplansza):
        print("win rzad")
        return True
    
    if wn.winCols(curplansza):
        print("win kolumna")
        return True
    if wn.winDiag(curplansza):
        print("win diag")
        return True
    return False


#gameloop
state = gamestate()
state.genState()
state.current = True
while(1):
    #game loop tu sumie nic nie zmieniac juz nigdy
    if PLAYER_FIRST:
        state.manualmove()
    if checkwin(state.plansza):
        print("game over")
        break
    if PVP_MODE:
        state.manualmove()
    else:
        state.automatedmove()
    if checkwin(state.plansza):
        print("game over")
        break
    if not PLAYER_FIRST:
        state.manualmove()
    if checkwin(state.plansza):
        print("game over")
        break
