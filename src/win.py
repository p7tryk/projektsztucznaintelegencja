EMPTY  = 0
CIRCLE = 1
CROSS  = 2
SIZE   = 7
WIN    = 5
START_SIDE  = CROSS
DEPTH = 2

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
    return False
