#!/usr/bin/env python3
""" logika gry kolko i krzyzyk """
import time
import numpy as np

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
SCORE_NEIGHBOUR_ENEMY = 5
SCORE_NEIGHBOUR_FRIENDLY = 3
SCORE_NEIGHBOUR_EMPTY = 1
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
        tempx, tempy = diffState(self.plansza,desiredState.plansza)

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


def diffState(origplansza,newplansza):
    diffx=6
    diffy=6
    #print("diffstate1")
    #debugPlansza(origplansza)
    #print("diffstate2")
    #debugPlansza(newplansza)
    #print("enddiffstate")
    for x in range(SIZE):
        for y in range(SIZE):
            if origplansza[x,y] != newplansza[x,y]:
                diffx = x
                diffy = y

    return diffx,diffy

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
    tempCircle, tempCross = longestWinStreak(element.plansza)
    tempCircle *= SCORE_LONGEST_MULTIPLIER
    tempCross *= SCORE_LONGEST_MULTIPLIER
    scoreCross += tempCross*tempCross
    scoreCircle += tempCircle*tempCircle
    #ocen najblizsze pola
    tempCircle, tempCross = freeSpacesScore(element.plansza)
    tempCircle *= SCORE_NEIGHBOUR_MULTIPLIER
    tempCross *= SCORE_NEIGHBOUR_MULTIPLIER
    scoreCross += tempCross
    scoreCircle += tempCircle

    #na pierwszej generacji
    if element.prev!= None:
        tempCircle, tempCross = scoreMiddle(element.prev.plansza,element.plansza)
        scoreCross += tempCross*tempCross
        scoreCircle += tempCircle*tempCircle
        

    win = checkwin(element.plansza)
    if element.side == CIRCLE and win:
        scoreCircle += 1000
    if element.side == CROSS and win:
        scoreCross += 1000


    element.scoreCircle = scoreCircle
    element.scoreCross = scoreCross
    return
def scoreMiddle(oldplansza, newplansza):

    scoreCircle = 0
    scoreCross = 0
    
    tempx,tempy = diffState(oldplansza, newplansza)
    if newplansza[tempx,tempy] == CIRCLE:
        scoreCircle=(tempx%(SIZE/2+1))+(tempy%(SIZE/2+1))
    return scoreCircle, scoreCross
def freeSpacesScore(curplansza):
    scoreCROSS = 0
    scoreCIRCLE = 0
    for x in range(SIZE):
        for y in range(SIZE):
            if curplansza[y,x] == CIRCLE:
                for helpX in range(-1,2,1):
                    for helpY in range(-1,2,1):            
                        if checkCenter(helpX,helpY):
                            if checkOutOfRange(x,helpX,y,helpY):
                                if curplansza[y+helpY,x+helpX] == CIRCLE:
                                    scoreCIRCLE+=SCORE_NEIGHBOUR_FRIENDLY
                                if curplansza[y+helpY,x+helpX] == 0:
                                    scoreCIRCLE+=SCORE_NEIGHBOUR_EMPTY
                                if curplansza[y+helpY,x+helpX] == CROSS:
                                    scoreCIRCLE+=SCORE_NEIGHBOUR_ENEMY
                                    #print(str(helpY) + " " + str(helpX))
                                
                                    
                        
        for y in range(SIZE):
            if curplansza[y,x] == CROSS:
                for helpX in range(-1,2,1):
                    for helpY in range(-1,2,1):
                         if checkCenter(helpX,helpY):
                            if checkOutOfRange(x,helpX,y,helpY):
                                if curplansza[y+helpY,x+helpX] == CROSS:
                                    scoreCROSS+=SCORE_NEIGHBOUR_FRIENDLY
                                if curplansza[y+helpY,x+helpX] == 0:
                                    scoreCROSS+=SCORE_NEIGHBOUR_EMPTY
                                if curplansza[y+helpY,x+helpX] == CIRCLE:
                                    scoreCROSS+=SCORE_NEIGHBOUR_ENEMY
    #print(str(scoreCIRCLE) + " " + str(scoreCROSS))
    return scoreCIRCLE,scoreCROSS

def checkCenter(x,y):
    if x == 0:
        if y == 0:
            return False
    return True

def checkOutOfRange(x, helpX , y , helpY):
    if x+helpX >= SIZE:
        return False
    if x+helpX < 0:
        return False
    if y+helpY >= SIZE:
        return False
    if y+helpY < 0:
        return False
    return True
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

def longestWinStreak(plansza):
    """ returns scoreCircle,scoreCross"""
    scoreCross = 0
    scoreCircle = 0
    tempCross = 0
    tempCircle = 0

    tempCircle, tempCross = scoreRows(plansza)
    scoreCross += tempCross
    scoreCircle += tempCircle

    tempCircle, tempCross = scoreCols(plansza)
    scoreCross += tempCross
    scoreCircle += tempCircle

    return scoreCircle, scoreCross

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
def winRows(curplansza):
    """wygrywajace kolumny"""

    scoreCROSS = 0
    scoreCIRCLE = 0
    for x in range(SIZE):
        temp = 0
        count = 0
        longestcount = 0

        for y in range(SIZE):
            if curplansza[x,y] == CIRCLE:
                count+=1
                if count > longestcount:
                    longestcount = count
            else:
                count=0
        if longestcount >4:
            return True

        temp = longestcount

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
        if longestcount >4:
            return True
        if temp > scoreCIRCLE:
            scoreCIRCLE = temp
        if longestcount > scoreCROSS:
            scoreCROSS = longestcount
    #print(str(scoreCIRCLE) + " " + str(scoreCROSS) + " " + str(x))
        #default
    return False

def scoreRows(curplansza):
    """wygrywajace rzedy"""
    
    scoreCROSS = 0
    scoreCIRCLE = 0
    for x in range(SIZE):
        temp = 0
        count = 0
        longestcount = 0
       
        for y in range(SIZE):
            if curplansza[x,y] == CIRCLE:
                count+=1
                if count > longestcount:
                    longestcount = count
            else:
                count=0
        
        
        temp = longestcount

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
        
        if temp > scoreCIRCLE:
            scoreCIRCLE = temp
        if longestcount > scoreCROSS:
            scoreCROSS = longestcount
    #print(str(scoreCIRCLE) + " " + str(scoreCROSS) + " " + str(x))
        #default
    return scoreCIRCLE,scoreCROSS
def scoreCols(curplansza):
    """wygrywajace kolumny"""
    
    scoreCROSS = 0
    scoreCIRCLE = 0
    for x in range(SIZE):
        temp = 0
        count = 0
        longestcount = 0
       
        for y in range(SIZE):
            if curplansza[y,x] == CIRCLE:
                count+=1
                if count > longestcount:
                    longestcount = count
            else:
                count=0
        
        
        temp = longestcount

            #cross
        count = 0
        longestcount = 0
        for y in range(SIZE):
            if curplansza[y,x] == CROSS:
                count+=1
                if count > longestcount:
                    longestcount = count
            else:
                count=0
        
        if temp > scoreCIRCLE:
            scoreCIRCLE = temp
        if longestcount > scoreCROSS:
            scoreCROSS = longestcount
    #print(str(scoreCIRCLE) + " " + str(scoreCROSS) + " " + str(x))
        #default
    return scoreCIRCLE,scoreCROSS

def winCols(curplansza):
    scoreCROSS = 0
    scoreCIRCLE = 0
    for x in range(SIZE):
        temp = 0
        count = 0
        longestcount = 0
       
        for y in range(SIZE):
            if curplansza[y,x] == CIRCLE:
                count+=1
                if count > longestcount:
                    longestcount = count
            else:
                count=0
        if longestcount >4:
            return True
        
        temp = longestcount

            #cross
        count = 0
        longestcount = 0
        for y in range(SIZE):
            if curplansza[y,x] == CROSS:
                count+=1
                if count > longestcount:
                    longestcount = count
            else:
                count=0
        if longestcount >4:
            return True
        if temp > scoreCIRCLE:
            scoreCIRCLE = temp
        if longestcount > scoreCROSS:
            scoreCROSS = longestcount
    #print(str(scoreCIRCLE) + " " + str(scoreCROSS) + " " + str(x))
        #default
    return False

def winDiag(curplansza):
    """wygrywanie przez skos"""
    #FIXME: zrobic
    return False

def checkwin(curplansza):
    """logika sprawdzania win condition"""
    #FIXME: win po skosie
    #print("nie sprawdzam")
    

    if winRows(curplansza):
        print("win rzad")
        return True
    
    if winCols(curplansza):
        print("win kolumna")
        return True
   
    if winDiag(curplansza):
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
