import constants as const

def diffState(origplansza,newplansza):
    diffx=6
    diffy=6
    #print("diffstate1")
    #debugPlansza(origplansza)
    #print("diffstate2")
    #debugPlansza(newplansza)
    #print("enddiffstate")
    for x in range(const.SIZE):
        for y in range(const.SIZE):
            if origplansza[x,y] != newplansza[x,y]:
                diffx = x
                diffy = y

    return diffx,diffy

def scoreMiddle(oldplansza, newplansza):

    scoreCircle = 0
    scoreCross = 0
    
    tempx,tempy = diffState(oldplansza, newplansza)
    if newplansza[tempx,tempy] == const.CIRCLE:
        scoreCircle=(tempx%(const.SIZE/2+1))+(tempy%(const.SIZE/2+1))
    return scoreCircle, scoreCross

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
def longestMaybeStreak(plansza):
    """ returns scoreCircle,scoreCross"""
    scoreCross = 0
    scoreCircle = 0
    tempCross = 0
    tempCircle = 0

    tempCircle, tempCross = scoreMaybeRows(plansza)
    scoreCross += tempCross
    scoreCircle += tempCircle

    tempCircle, tempCross = scoreMaybeCols(plansza)
    scoreCross += tempCross
    scoreCircle += tempCircle

    return scoreCircle, scoreCross

def scoreMaybeCols(curplansza):
    """mozliwe cols"""
    
    scoreCROSS = 0
    scoreCIRCLE = 0
    for x in range(const.SIZE):
        temp = 0
        count = 0
        longestcount = 0
       
        for y in range(const.SIZE):
            if curplansza[y,x] != const.CROSS:
                count+=1
                if count > longestcount:
                    longestcount = count
            else:
                count=0
        
        
        temp = longestcount

            #cross
        count = 0
        longestcount = 0
        for y in range(const.SIZE):
            if curplansza[y,x] != const.CIRCLE:
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

def scoreMaybeRows(curplansza):
    """mozliwe rzedy"""
    
    scoreCROSS = 0
    scoreCIRCLE = 0
    for x in range(const.SIZE):
        temp = 0
        count = 0
        longestcount = 0
       
        for y in range(const.SIZE):
            if curplansza[x,y] != const.CROSS:
                count+=1
                if count > longestcount:
                    longestcount = count
            else:
                count=0
        
        
        temp = longestcount

            #cross
        count = 0
        longestcount = 0
        for y in range(const.SIZE):
            if curplansza[x,y] != const.CIRCLE:
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
        
        if temp > scoreCIRCLE:
            scoreCIRCLE = temp
        if longestcount > scoreCROSS:
            scoreCROSS = longestcount
    #print(str(scoreCIRCLE) + " " + str(scoreCROSS) + " " + str(x))
        #default
    return scoreCIRCLE,scoreCROSS
def scoreRows(curplansza):
    """wygrywajace rzedy"""
    
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
        
        if temp > scoreCIRCLE:
            scoreCIRCLE = temp
        if longestcount > scoreCROSS:
            scoreCROSS = longestcount
    #print(str(scoreCIRCLE) + " " + str(scoreCROSS) + " " + str(x))
        #default
    return scoreCIRCLE,scoreCROSS

def freeSpacesScore(curplansza):
    scoreCROSS = 0
    scoreCIRCLE = 0
    for x in range(const.SIZE):
        for y in range(const.SIZE):
            if curplansza[y,x] == const.CIRCLE:
                for helpX in range(-1,2,1):
                    for helpY in range(-1,2,1):            
                        if checkCenter(helpX,helpY):
                            if checkOutOfRange(x,helpX,y,helpY):
                                if curplansza[y+helpY,x+helpX] == const.CIRCLE:
                                    scoreCIRCLE+=const.SCORE_NEIGHBOUR_FRIENDLY
                                if curplansza[y+helpY,x+helpX] == 0:
                                    scoreCIRCLE+=const.SCORE_NEIGHBOUR_EMPTY
                                if curplansza[y+helpY,x+helpX] == const.CROSS:
                                    scoreCIRCLE+=const.SCORE_NEIGHBOUR_ENEMY
                                    #print(str(helpY) + " " + str(helpX))
                                
                                    
                        
        for y in range(const.SIZE):
            if curplansza[y,x] == const.CROSS:
                for helpX in range(-1,2,1):
                    for helpY in range(-1,2,1):
                         if checkCenter(helpX,helpY):
                            if checkOutOfRange(x,helpX,y,helpY):
                                if curplansza[y+helpY,x+helpX] == const.CROSS:
                                    scoreCROSS+=const.SCORE_NEIGHBOUR_FRIENDLY
                                if curplansza[y+helpY,x+helpX] == 0:
                                    scoreCROSS+=const.SCORE_NEIGHBOUR_EMPTY
                                if curplansza[y+helpY,x+helpX] == const.CIRCLE:
                                    scoreCROSS+=const.SCORE_NEIGHBOUR_ENEMY
    #print(str(scoreCIRCLE) + " " + str(scoreCROSS))
    return scoreCIRCLE,scoreCROSS
def checkCenter(x,y):
    if x == 0:
        if y == 0:
            return False
    return True

def checkOutOfRange(x, helpX , y , helpY):
    if x+helpX >= const.SIZE:
        return False
    if x+helpX < 0:
        return False
    if y+helpY >= const.SIZE:
        return False
    if y+helpY < 0:
        return False
    return True
