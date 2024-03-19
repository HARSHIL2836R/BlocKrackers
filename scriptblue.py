import random
import numpy
import math

name = "hybrid sample"

#phase 1 : aggressive
#phase 2 : defensive

#sample1 extra functions
def moveTo(x, y, Pirate):
    position = Pirate.getPosition()
    if position[0] == x and position[1] == y:
        return 0
    if position[0] == x:
        return (position[1] < y) * 2 + 1
    if position[1] == y:
        return (position[0] > x) * 2 + 2
    if random.randint(1, 2) == 1:
        return (position[0] > x) * 2 + 2
    else:
        return (position[1] < y) * 2 + 1
#

#sample4 extra functions
def checkfriends(pirate , quad ):
    sum = 0 
    up = pirate.investigate_up()[1]
    down = pirate.investigate_down()[1]
    left = pirate.investigate_left()[1]
    right = pirate.investigate_right()[1]
    ne = pirate.investigate_ne()[1]
    nw = pirate.investigate_nw()[1]
    se = pirate.investigate_se()[1]
    sw = pirate.investigate_sw()[1]
    
    check_tuple = ('friend', 'both')

    if(quad=='ne'):
        if(up in check_tuple):
            sum +=1 
        if(ne in check_tuple):
            sum +=1 
        if(right in check_tuple):
            sum +=1 
    if(quad=='se'):
        if(down in check_tuple):
            sum +=1 
        if(right in check_tuple):
            sum +=1 
        if(se in check_tuple):
            sum +=1 
    if(quad=='sw'):
        if(down in check_tuple):
            sum +=1 
        if(sw in check_tuple): 
            sum +=1 
        if(left in check_tuple):
            sum +=1 
    if(quad=='nw'):
        if(up in check_tuple):
            sum +=1 
        if(nw in check_tuple):
            sum +=1 
        if(left in check_tuple):
            sum +=1 

    return sum
    
def spread(pirate):
    sw = checkfriends(pirate ,'sw' )
    se = checkfriends(pirate ,'se' )
    ne = checkfriends(pirate ,'ne' )
    nw = checkfriends(pirate ,'nw' )
   
    my_dict = {'sw': sw, 'se': se, 'ne': ne, 'nw': nw}
    sorted_dict = dict(sorted(my_dict.items(), key=lambda item: item[1]))
    print("sorted_dict: ",sorted_dict)
    x, y = pirate.getPosition()
    
    if( x == 0 , y == 0):
        return random.randint(1,4)
    
    if(sorted_dict[list(sorted_dict())[3]] == 0 ):
        return random.randint(1,4)
    
    if(list(sorted_dict())[0] == 'sw'):
        return moveTo(x-1 , y+1 , pirate)
    elif(list(sorted_dict())[0] == 'se'):
        return moveTo(x+1 , y+1 , pirate)
    elif(list(sorted_dict())[0] == 'ne'):
        return moveTo(x+1 , y-1 , pirate)
    elif(list(sorted_dict())[0] == 'nw'):
        return moveTo(x-1 , y-1 , pirate)
#

#my functions
def move_diagonally(pirate):
    dp = pirate.getDeployPoint()
    X = pirate.getDimensionX()
    X = int(X)
    hp = 0.4 #high probability
    lp = 0.1 #low probability
    if int(dp[0]) < X/2 :
        if int(dp[1]) == 0:
            return numpy.random.choice(numpy.arange(1, 5), p=[lp,hp,hp,lp])
        else:
            return numpy.random.choice(numpy.arange(1, 5), p=[hp,hp,lp,lp])
    else:
        if int(dp[1]) == 0:
            return numpy.random.choice(numpy.arange(1, 5), p=[lp,lp,hp,hp])
        else:
            return numpy.random.choice(numpy.arange(1, 5), p=[hp,lp,lp,hp])

#Functions from samples
def aggressive_ActPirate(pirate):
    print(pirate.getID())
    global frame
    if frame < 200:
        return move_diagonally(pirate)
    else:
        return random.randint(1,4)

def defensive_ActPirate(pirate):
    up = pirate.investigate_up()[0]
    down = pirate.investigate_down()[0]
    left = pirate.investigate_left()[0]
    right = pirate.investigate_right()[0]
    x, y = pirate.getPosition()
    pirate.setSignal("")
    s = pirate.trackPlayers()
    
    if (
        (up == "island1" and s[0] != "myCaptured")
        or (up == "island2" and s[1] != "myCaptured")
        or (up == "island3" and s[2] != "myCaptured")
    ):
        s = up[-1] + str(x) + "," + str(y - 1)
        pirate.setTeamSignal(s)

    if (    
        (down == "island1" and s[0] != "myCaptured")
        or (down == "island2" and s[1] != "myCaptured")
        or (down == "island3" and s[2] != "myCaptured")
    ):
        s = down[-1] + str(x) + "," + str(y + 1)
        pirate.setTeamSignal(s)

    if (
        (left == "island1" and s[0] != "myCaptured")
        or (left == "island2" and s[1] != "myCaptured")
        or (left == "island3" and s[2] != "myCaptured")
    ):
        s = left[-1] + str(x - 1) + "," + str(y)
        pirate.setTeamSignal(s)

    if (
        (right == "island1" and s[0] != "myCaptured")
        or (right == "island2" and s[1] != "myCaptured")
        or (right == "island3" and s[2] != "myCaptured")
    ):
        s = right[-1] + str(x + 1) + "," + str(y)
        pirate.setTeamSignal(s)

    
    if pirate.getTeamSignal() != "":
        s = pirate.getTeamSignal()
        l = s.split(",")
        x = int(l[0][1:])
        y = int(l[1])
    
        return moveTo(x, y, pirate)

    else:
        return spread(pirate)

def aggressive_ActTeam(team):
    global phase
    phase = 1

def defensive_ActTeam(team):
    global phase
    phase =2
    l = team.trackPlayers()
    s = team.getTeamSignal()

    team.buildWalls(1)
    team.buildWalls(2)
    team.buildWalls(3)

    if s:
        island_no = int(s[0])
        signal = l[island_no - 1]
        if signal == "myCaptured":
            team.setTeamSignal("")
#

#CODE
def ActPirate(pirate):
    sig = pirate.getTeamSignal().split(';')
    if sig[0][-1] == '1':
        #phase 1
        return aggressive_ActPirate(pirate)
    else:
        #phase 2
        return defensive_ActPirate(pirate)

#CODE
def ActTeam(team):
    frame = team.getCurrentFrame()
    if frame == 1:
        team.setTeamSignal('phase1;1;')
    phase = team.getTeamSignal.split(';')[0][-1]
    phase = int(phase)
    
    #Stage 1 implimentation
    l = team.trackPlayers()[3:]
    flag = 0

    if phase == 1:
        sum = 0
        for el in l:
            if el == '':
                sum+=1
        if sum == 1:
            flag =1

    print(frame)
    print(phase)
    if frame > 1000:
        flag = 1
    
    #phase1
    if flag == 0 :
        return aggressive_ActPirate(team)
    #phase2
    else:
        return defensive_ActTeam(team)