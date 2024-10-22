# [Milestone 2]: implement all different agent policies I can think of
# here, I'm assuming this is just policies without RL

import random

ACTIONS = ["left", "right", "up", "down"]
CORNERS = [(0,0), (0,9), (9,0), (9,9)]

# This policy moves randomly
class RandomPolicy():
    
    def reset(self, agentName, friendName):
        self.name = agentName
        self.observations = []
        self.friendName = friendName

    def observe(self, obs):
        self.observations.append(obs)
        return
    
    def act(self):
        return (self.name, random.choice(ACTIONS))

# Both agents try to move to (0, 0)
class GoTo00():

    def reset(self, agentName, friendName):
        self.name = agentName
        self.observations = []
        self.friendName = friendName

    def observe(self, obs):
        self.observations.append(obs)
        return
    
    def act(self):
        myY = self.observations[-1][0][self.name][1]

        if myY > 0:
            return (self.name, "down")
        else:
            return (self.name, "left")
    
# Agents move to the corner which has the closest
class ClosestCornerNotBlind():

    def reset(self, agentName, friendName):
        self.name = agentName
        self.observations = []
        self.friendName = friendName

    def observe(self, obs):
        self.observations.append(obs)
        return
    
    def act(self):
        myX = self.observations[-1][0][self.name][0]
        myY = self.observations[-1][0][self.name][1]

        friendX = self.observations[-1][0][self.friendName][0]
        friendY = self.observations[-1][0][self.friendName][1]

        bestCorner = None
        bestDist = 10000
        for x, y in CORNERS:
            dist = abs(myX - x) + abs(myY - y) + abs(friendX - x) + abs(friendY - y)
            if dist < bestDist:
                bestDist = dist
                bestCorner = (x, y) 

        x, y = bestCorner
        if myY < y:
            return (self.name, "up")
        elif myY > y: 
            return (self.name, "down")
        else:
            if myX == x: # if we've already reached the corner, stay there
                if x == 0:
                    return (self.name, "left")
                else:
                    return (self.name, "right")
            elif myX < x:
                return (self.name, "right")
            else: 
                return (self.name, "left")
            
# Agents are blind of other position
# one rotates clockwise around the corners, the other rotates counterclockwise
# when they receive positive reward, they stay
# we ensure they will stay on corners when steps % 2 == 0 so we don't "pass over" each other
class Blind():

    def reset(self, agentName, friendName):
        self.name = agentName
        self.observations = []
        self.friendName = friendName

    def observe(self, obs):
        self.observations.append(obs)
        return
    
    def act(self):
        x = self.observations[-1][0][self.name][0]
        y = self.observations[-1][0][self.name][1]

        # if we are at a corner
        if x in [0, 9] and y in [0, 9]:
            # if reward is positive stay in place
            # wait for 10 turns
            steps = self.observations[-1][0]["STEPS_ELAPSED"]
            if (steps > 0 and self.observations[-1][1] > 0) or steps % 10 != 0:
                # note that we have to check steps > 0, because no reward on turn 1
                if x == 0:
                    return (self.name, "left")
                else:
                    return (self.name, "right")
        
        # if we are on the edge, then rotate in a direction [clockwise/counterclockwise]
        if x in [0, 9] or y in [0, 9]:
            if self.name < self.friendName: # clockwise
                if x == 0 and y < 9:
                    return (self.name, "up")
                elif x == 9 and y > 0:
                    return (self.name, "down")
                elif y == 0 and x > 0:
                    return (self.name, "left")
                elif y == 9 and x < 9:
                    return (self.name, "right")
            else: # counterclockwise
                if x == 0 and y > 0:
                    return (self.name, "down")
                elif x == 9 and y < 9:
                    return (self.name, "up")
                elif y == 0 and x < 9:
                    return (self.name, "right")
                elif y == 9 and x > 0:
                    return (self.name, "left")

        # otherwise, make our way to the closest edge
        up = (9-y, "up")
        down = (y, "down")
        left = (x, "left")
        right = (9-x, "right")
        return (self.name, min(up, down, left, right)[1])