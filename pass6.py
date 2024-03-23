import random
import numpy
import math

name = "hybrid sample"

#phase 1 : aggressive
#phase 2 : defensive

#TEAM SIGNAL: (0)phase;frame;sig;(3)island_1_state;state;state;(6)(str)island_1_loc;loc;loc;(9)island1_center;center;center

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

#script.py functions
def moveAway(x, y, Pirate):
    position = Pirate.getPosition()
    if position[0] == x and position[1] == y:
        return random.randint(1, 4)
    if random.randint(1, 2) == 1:
        return (position[0] < x) * 2 + 2
    else:
        return (position[1] > y) * 2 + 1

def circleAround(x, y, radius, Pirate, initial="abc", clockwise=True):
    position = Pirate.getPosition()
    rx = position[0]
    ry = position[1]
    pos = [[x + i, y + radius] for i in range(-1 * radius, radius + 1)]
    pos.extend([[x + radius, y + i] for i in range(radius - 1, -1 * radius - 1, -1)])
    pos.extend([[x + i, y - radius] for i in range(radius - 1, -1 * radius - 1, -1)])
    pos.extend([[x - radius, y + i] for i in range(-1 * radius + 1, radius)])
    if [rx, ry] not in pos:
        if initial != "abc":
            return moveTo(initial[0], initial[1], Pirate)
        if rx in [x + i for i in range(-1 * radius, radius + 1)] and ry in [
            y + i for i in range(-1 * radius, radius + 1)
        ]:
            return moveAway(x, y, Pirate)
        else:
            return moveTo(x, y, Pirate)
    else:
        index = pos.index([rx, ry])
        return moveTo(
            pos[(index + (clockwise * 2) - 1) % len(pos)][0],
            pos[(index + (clockwise * 2) - 1) % len(pos)][1],
            Pirate,
        )

#my functions
def move_diagonally(pirate):
    dp = pirate.getDeployPoint()
    X = pirate.getDimensionX()
    X = int(X)
    hp = 0.38 #high probability
    lp = 0.12 #low probability
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
def move_onboundary_up(pirate):
    dp = pirate.getDeployPoint()
    X = pirate.getDimensionX()
    X = int(X)
    if int(dp[0]) < X/2 :
        if int(dp[1]) == 0:
            return numpy.random.choice(numpy.arange(1, 5), p=[0.2,0.15,0.55,0.1])
        else:
            return numpy.random.choice(numpy.arange(1, 5), p=[0.55,0.15,0.2,0.1])
    else:
        if int(dp[1]) == 0:
            return numpy.random.choice(numpy.arange(1, 5), p=[0.2,0.1,0.55,0.15])
        else:
            return numpy.random.choice(numpy.arange(1, 5), p=[0.55,0.1,0.2,0.15])
def move_onboundary_side(pirate):
    dp = pirate.getDeployPoint()
    X = pirate.getDimensionX()
    X = int(X)
    if int(dp[0]) < X/2 :
        if int(dp[1]) == 0:
            return numpy.random.choice(numpy.arange(1, 5), p=[0.1,0.55,0.15,0.2])
        else:
            return numpy.random.choice(numpy.arange(1, 5), p=[0.15,0.55,0.1,0.2])
    else:
        if int(dp[1]) == 0:
            return numpy.random.choice(numpy.arange(1, 5), p=[0.1,0.2,0.15,0.55])
        else:
            return numpy.random.choice(numpy.arange(1, 5), p=[0.15,0.2,0.1,0.55])
def SetSig(obj, i, sig):
    #Sets Team Signal sig at ith index
    OldTS = obj.getTeamSignal().split(';')
    OldTS[i] = str(sig)
    obj.setTeamSignal(';'.join(OldTS))


#Functions from samples
def aggressive_ActPirate(pirate):
    frame = pirate.getTeamSignal().split(';')[1]
    frame = int(frame)
    pirate_id=pirate.getID()
    pirate_id=int(pirate_id)

    def distance(pos1, pos2):
        return numpy.sqrt((int(pos1[0])-pos2[0])**2+(int(pos1[1])-pos2[1])**2)

    if frame < 200 and distance(pirate.getPosition(),pirate.getDeployPoint()) < min(pirate.getDimensionX(),pirate.getDimensionY()):
       if pirate_id%10==0:
            if (pirate_id/10)%2==1:
                return move_onboundary_up(pirate)
            else:
                return move_onboundary_side(pirate)
       else:
            return move_diagonally(pirate)
    else:
        return spread(pirate)

def defensive_ActPirate(pirate):
    '''Each of the above functions returns a tuple of two strings (where, who), where representing the type of the tile, and who the presence of pirates:
    - where can take the following values:
    'wall' if the tile is out of bounds
    'island1', 'island2' or 'island3' if the tile is a part of an island
    'blank' in all other cases (i.e. the sea)
    - who can take the following values:
    'friend' if only pirates from the same team are on the tile
    'enemy' if only pirates from the other team are on the tile
    'both' if pirates from both teams are on the tile
    'blank' in all other cases (i.e. no pirates)'''

    curr = pirate.investigate_current()[0]
    up = pirate.investigate_up()[0]
    down = pirate.investigate_down()[0]
    left = pirate.investigate_left()[0]
    right = pirate.investigate_right()[0]
    ne = pirate.investigate_ne()[0]
    nw = pirate.investigate_nw()[0]
    se = pirate.investigate_se()[0]
    sw = pirate.investigate_sw()[0]
    x, y = pirate.getPosition()
    pirate.setSignal("")
    s = pirate.trackPlayers()
    TeamSig = pirate.getTeamSignal().split(';')

    for i in range(1,4):
        if (pirate.getSignal() == "center"+str(i)):
            print(TeamSig[1],"Returning Zero")
            x = int(TeamSig[i+5].split(',')[0])
            y = int(TeamSig[i+5].split(',')[1])
            return moveTo(x,y,pirate)
        
    else:
        for i in range(1,4):
            if str(str(x)+","+str(y)) == TeamSig[5+i] and TeamSig[8+i] != "1":
                print("Signal Set for "+pirate.getID())
                pirate.setSignal("center"+str(i))
                print(pirate.getSignal())
                SetSig(pirate,i+2,"1")
                return 0
        

        def check(obj):
            #checks whether in the direction obj is there any island or not
            return ((obj == "island1" and s[0] != "myCaptured")
            or (obj == "island2" and s[1] != "myCaptured")
            or (obj == "island3" and s[2] != "myCaptured"))
        
        if (curr == "blank"):
            if (check(up)):
                if (check(ne) and check(nw)):
                    s = up[-1] + str(x) + "," + str(y - 2)
                    SetSig(pirate, 2, s)
                elif (check(ne)):
                    s = up[-1] + str(x+1) + "," + str(y - 2)
                    SetSig(pirate, 2, s)
                else:
                    s = up[-1] + str(x-1) + "," + str(y - 2)
                    SetSig(pirate, 2, s)

            if (check(down)):
                if (check(sw) and check(se)):
                    s = down[-1] + str(x) + "," + str(y + 2)
                    SetSig(pirate, 2, s)
                elif (check(sw)):
                    s = down[-1] + str(x-1) + "," + str(y + 2)
                    SetSig(pirate, 2, s)
                else:
                    s = down[-1] + str(x+1) + "," + str(y + 2)
                    SetSig(pirate, 2, s)

            if (check(left)):
                if (check(ne) and check(se)):
                    s = left[-1] + str(x - 2) + "," + str(y)
                    SetSig(pirate, 2, s)
                elif (check(nw)):
                    s = left[-1] + str(x - 2) + "," + str(y-1)
                    SetSig(pirate, 2, s)
                else:
                    s = left[-1] + str(x - 2) + "," + str(y+1)
                    SetSig(pirate, 2, s)
                
            if (check(right)):
                if check(nw) and check(sw):
                    s = right[-1] + str(x + 2) + "," + str(y)
                    SetSig(pirate, 2, s)
                elif check(ne):
                    s = right[-1] + str(x + 2) + "," + str(y-1)
                    SetSig(pirate, 2, s)
                else:
                    s = right[-1] + str(x + 2) + "," + str(y+1)
                    SetSig(pirate, 2, s)

            if (check(nw) and not check(up) and not check(down) and not check(left) and not check(right)):
                s = nw[-1] + str(x - 2) + "," + str(y-2)
                SetSig(pirate, 2, s)
            if (check(ne) and not check(up) and not check(down) and not check(left) and not check(right)):
                s = ne[-1] + str(x + 2) + "," + str(y-2)
                SetSig(pirate, 2, s)
            if (check(sw) and not check(up) and not check(down) and not check(left) and not check(right)):
                s = sw[-1] + str(x - 2) + "," + str(y+2)
                SetSig(pirate, 2, s)
            if (check(se) and not check(up) and not check(down) and not check(left) and not check(right)):
                s = se[-1] + str(x + 2) + "," + str(y+2)
                SetSig(pirate, 2, s)

        s = TeamSig[2]
        if pirate.getID() == "4" : 
            print(TeamSig[1],"s:",s, "phases: ", TeamSig[3:12], "pos", x,y, pirate.getSignal())
            pass

        if s != "__empty__":
            if pirate.getID() == "4":
                print("Moving")
                pass
            SetSig(pirate,2+int(s[0]),str(0))
            l = s.split(",")
            x = int(l[0][1:])
            y = int(l[1])

            if int(pirate.getID())%5 == 1:
                return circleAround(x, y, 2, pirate)
            
            return moveTo(x, y, pirate)

        else:
            if pirate.getID() == "4":
                print("Spreading")
                pass
            return spread(pirate)

def aggressive_ActTeam(team):
    OldTS = team.getTeamSignal().split(';')
    OldTS[0] = 'phase1'
    team.setTeamSignal(';'.join(OldTS))

def defensive_ActTeam(team):

    #change phase
    SetSig(team,0,'phase2')
    TeamSig = team.getTeamSignal().split(';')
    l = team.trackPlayers()
    #s = sig
    s = TeamSig[2]

    #set boolean for center occupied or not
    for i in range(1,4):
        if "center"+str(i) in list(team.getListOfSignals()):
            SetSig(team,8+i,"1")

    for i in range(1,4):
        try:
            if TeamSig[2+i] == "1":
                team.buildwalls(i)
        except:
            pass

    #s = sig
    if s != "__empty__":
        island_no = int(s[0])
        #store location of island
        SetSig(team, 5 + island_no, s[1:])
        signal = l[island_no - 1]
        if signal == "myCaptured" or TeamSig[island_no+2] == "1":
            SetSig(team,2,"__empty__")
#

#CODE
def ActPirate(pirate):
    pirate.setSignal("1")
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
        #TEAM SIGNAL: (0)phase;frame;sig;(3)island_1_state;state;state;(6)(str)island_1_loc;loc;loc;(9)island1_center;center;center
        team.setTeamSignal("phase1;1;__empty__;__empty__;__empty__;__empty__;__empty__;__empty__;__empty__;0;0;0")
    SetSig(team,1,frame)
    phase = team.getTeamSignal().split(';')[0][-1]
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

    if frame > 500:
        flag = 1
    
    
    #phase1
    if flag == 0 :
        return aggressive_ActTeam(team)
    #phase2
    else:
        return defensive_ActTeam(team)