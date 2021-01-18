import constants as const

def winRows(curplansza):
    """wygrywajace kolumny"""

    scoreCROSS = 0
    scoreCIRCLE = 0
    for x in range(const.SIZE):
        temp = 0
        count = 0
        longestcount = 0

        for y in range(const.SIZE):
            if curplansza[x,y] == const.CIRCLE:
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
        for y in range(const.SIZE):
            if curplansza[x,y] == const.CROSS:
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
    for x in range(const.SIZE):
        temp = 0
        count = 0
        longestcount = 0
       
        for y in range(const.SIZE):
            if curplansza[y,x] == const.CIRCLE:
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
        for y in range(const.SIZE):
            if curplansza[y,x] == const.CROSS:
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
