#!/usr/bin/env python3
""" logika gry kolko i krzyzyk """
import numpy as np

#gamemode
PLAYER_FIRST = True
PVP_MODE = False

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
    current = False
    
    
    def __init__(self, plansza = np.zeros(shape = (SIZE,SIZE)), side = START_SIDE):
        self.plansza = plansza
        self.side = side
        self.prev = plansza
        
        
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
        level1 = []
        level2 = []
        lastlevel = []

        level1 = expand(self.plansza,self.side,level1)
        score(level1)
        for element in level1:
            level2 = expand(element.plansza,element.side, level2)
        score(level2)

        #TBD ile tych poziomow ma byc
        #
        #

        for element in level2:
            lastlevel = expand(element.plansza,element.side, lastlevel)
        score(lastlevel)
        desiredState = highestScore(lastlevel,self.side)

        tempx, tempy = diffState(self.plansza,desiredState)
        self.makemove(tempx,tempy)
        return

    def print(self):
        for x in range(0,SIZE):
            print("\n----------------------------")
            for y in range(0, SIZE):
                print(" " + self.get(x,y) + " ", end = "|")
        print("\n----------------------------", end = "\n")


def diffState(origplansza,newplansza):
    diffx=0
    diffy=0
    for x in range(SIZE):
        for y in range(SIZE):
            if origplansza[x,y] != newplansza[x,y]:
                diffx = x
                diffy = y

    return diffx,diffy

def expand(plansza,side,lista):
    """ ekspansja """
    for x in range(SIZE):
        for y in range(SIZE):
            if canYou(plansza, x, y):
                newplansza = gamestate(plansza,side)
                newplansza.makemove(x,y)
                newplansza.prev = plansza
                lista.append(newplansza)
    return lista

def canYou(plansza, x,y):
    if plansza[x,y] == CROSS or plansza[x,y] == CIRCLE:
        return False
    return True

def score(lista):
    """ nadawanie wartosci, argumenty zawsze kolko,krzyzyk = funkcja()"""
    for element in lista:
        scoreSingle(element)
 
def scoreSingle(element):
    #TODO jakas logika nadawania wartosci
    scoreCross = 0
    scoreCircle = 0
    tempCircle = 0
    tempCross = 0

    tempCircle, tempCross = longestWinStreak(element.plansza)
    scoreCross += tempCross
    scoreCircle += tempCircle

    element.scoreCircle = scoreCircle
    element.scoreCross = scoreCross
    return

def highestScore(lista,side):
    #BFS
    scoreList = []
    for element in lista:
        temp = 0
        temp = element.scoreCross-element.scoreCircle
        while element.current == False:
            element = element.prev
            temp +=element.scoreCross-element.scoreCircle
        scoreList.append(temp)

    bestState =0
    bestScore =0
    for tempscore in scoreList:
        if side == CROSS: #jezeli krzyzyk to im wiekszy (na plusie) tym lepiej
            if tempscore > bestScore:
                bestScore = score
                temp = scoreList.index(score)
                bestState = lista[temp]
        else:
            if tempscore < bestScore:
                bestScore = score
                temp = scoreList.index(score)
                bestState = lista[temp]

    #chemy dostac nastepny ruch
    while bestState.current == False:
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
        if longestcount >=4:
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
        if longestcount >=4:
            return True
        if temp > scoreCIRCLE:
            scoreCIRCLE = temp
        if longestcount > scoreCROSS:
            scoreCROSS = longestcount
    print(str(scoreCIRCLE) + " " + str(scoreCROSS) + " " + str(x))
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
        if longestcount >=4:
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
        if longestcount >=4:
            return True
        if temp > scoreCIRCLE:
            scoreCIRCLE = temp
        if longestcount > scoreCROSS:
            scoreCROSS = longestcount
    print(str(scoreCIRCLE) + " " + str(scoreCROSS) + " " + str(x))
        #default
    return False

def scoreCols(curplansza):
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
    print(str(scoreCIRCLE) + " " + str(scoreCROSS) + " " + str(x))
        #default
    return scoreCIRCLE,scoreCROSS

def winDiag(curplansza):
    """wygrywanie przez skos"""
    #FIXME: zrobic
    return False

def checkwin(curplansza):
    """logika sprawdzania win condition"""
    #LATER: teoretycznie nie musimy sprawdzac ale wtedy nasze AI bedzie dzialac zawsze (nawet jak wygrywamy)
    #print("nie sprawdzam")
    

    if winRows(curplansza):
        print("win")
        return True
    
    if winCols(curplansza):
        print("win")
        return True
   
    if winDiag(curplansza):
        print("win")
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
    if PVP_MODE:
        state.manualmove()
    else:
        state.automatedmove()
    if PLAYER_FIRST:
        state.manualmove()
