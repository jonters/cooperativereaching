import gymnasium as gym
import random
import numpy as np

class CooperativeReaching(gym.Env):

    MIN_X, MIN_Y = 0, 0
    MAX_X, MAX_Y = 9, 9
    playerCoords = [[-1, -1], [-1, -1]]
    steps = 0
    agentToPlayer, playerToAgent = {}, {}

    MOVESET = {
        'up': (0, 1),
        'down': (0, -1),
        'left': (-1, 0),
        'right': (1, 0)
    }
    
    CORNERS = [(0,0), (0,9), (9,0), (9,9)]

    def __init__(self, render_mode = None):
        if render_mode:
            print("Rendering is not supported for this environment")
            exit()
        
        # self.observation_space = gym.spaces.Box(low=-3.4028235e+8, high=3.4028235e+8, shape=(5,), dtype=np.float32)
        # self.action_space = gym.spaces.Dict("")

        self.action_space = None
        self.observation_space = None

        self.reset()
    
    # since the observation format was not specified, I just defined one here
    # observation: dictionary with key as agent_name, value as position of agent, steps elapsed
    def getObservation(self):
        return {
            self.playerToAgent[0]: tuple(self.playerCoords[0]),
            self.playerToAgent[1]: tuple(self.playerCoords[1]),
            "STEPS_ELAPSED": self.steps
        }
    
    def reward(self):
        p1Tpl = tuple(self.playerCoords[0])
        p2Tpl = tuple(self.playerCoords[1])
        
        if p1Tpl == p2Tpl:
            return 1 if p1Tpl in self.CORNERS else 0
        return 0
    
    def getTerminated(self):
        if self.steps >= 30:
            return True
        return False
    
    def outOfBounds(self):
        if min(self.playerCoords[0][0], self.playerCoords[1][0]) < self.MIN_X:
            return True
        elif max(self.playerCoords[0][0], self.playerCoords[1][0]) > self.MAX_X:
            return True
        elif min(self.playerCoords[0][1], self.playerCoords[1][1]) < self.MIN_Y:
            return True
        elif max(self.playerCoords[0][1], self.playerCoords[1][1]) > self.MAX_Y:
            return True
        return False

    # build our dictionary corresponding given agent name to player number
    def initializeAgentNames(self, action):
        for i, agentName in enumerate(action):
            if agentName == "STEPS_ELAPSED":
                print("Invalid agent name \"STEPS_ELAPSED\"")
                exit()
            self.agentToPlayer[agentName] = i
            self.playerToAgent[i] = agentName

    # returns according to the format of gymnasium
    # specifically: 
    def step(self, action):
        self.steps += 1

        # action is a dict with the format {<agent_name>: <action>}
        for agentName in action:
            # if agentName is not recognized, we put it in
            if agentName not in self.agentToPlayer:
                self.initializeAgentNames(action)
            agentID = self.agentToPlayer[agentName]
            
            # update position
            move = action[agentName]
            if move in self.MOVESET:
                self.playerCoords[agentID][0] += self.MOVESET[move][0]
                self.playerCoords[agentID][1] += self.MOVESET[move][1]

                if self.outOfBounds(): # undo the move if we are out of bounds
                    self.playerCoords[agentID][0] -= self.MOVESET[move][0]
                    self.playerCoords[agentID][1] -= self.MOVESET[move][1]
            
            else:
                print(f"Move \"{move}\" is not valid, skipping action")

        # I've used "done" previously but apparently now it is deprecated?
        # I'm assuming that's in lieu of terminated and truncated
        # done is still attached at the end because that seems like how the docs format it

        terminated = self.getTerminated()
        truncated = False
        done = terminated or truncated

        return (self.getObservation(), self.reward(), terminated, truncated, {}, done)
    
    # I define an optional argument for agentNames if we want to specify them earlier
    def reset(self, seed = 0, agentNames = set()):
        # randomly place two agents
        self.playerCoords[0] = [random.randint(self.MIN_X, self.MAX_X), random.randint(self.MIN_Y, self.MAX_Y)]
        self.playerCoords[1] = [random.randint(self.MIN_X, self.MAX_X), random.randint(self.MIN_Y, self.MAX_Y)]

        self.steps = 0
        self.agentToPlayer = {}
        self.playerToAgent = {0: "agent1", 1: "agent2"} # default 
        
        if "STEPS_ELAPSED" in agentNames:
            print("Invalid agent name \" STEPS_ELAPSED \"")
            exit()

        for i, name in enumerate(agentNames):
            self.playerToAgent[i] = name
            self.agentToPlayer[name] = i

        return (self.getObservation(), {})
    
    def close(self):
        return


env = CooperativeReaching()
