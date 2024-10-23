# q-table based learning
# or NN based approach

import random

# BLIND:
# Q[pos: 100][reward: 2]

ACTIONS = ["left", "right", "up", "down"]
CORNERS = [(0,0), (0,9), (9,0), (9,9)]
EPSILON = 0.1
ALPHA = 0.2
GAMMA = 0.95

class RLPolicy():

    def init(self):
        self.QTable = [[[[random.random() for _ in range(4)] for _ in range(2)] for _ in range(30)] for _ in range(10*10)]

    def reset(self, agentName, friendName):
        self.name = agentName
        self.observations = []
        self.friendName = friendName

    def observe(self, obs):
        self.observations.append(obs)
        return
    
    def act(self):
        # get our last observation
        myX = self.observations[-1][0][self.name][0]
        myY = self.observations[-1][0][self.name][1]
        index = myY * 10 + myX
        steps = self.observations[-1][0]["STEPS_ELAPSED"]
        lastReward = 0 if steps == 0 else self.observations[-1][1]

        # compute our Q-learning update from the last step
        if steps > 0:
            mx = max(self.QTable[index][steps][lastReward][i] for i in range(4)) # current policy max

            increment = ALPHA * (lastReward + (GAMMA * mx - self.QTable[self.prevState[0]][self.prevState[1]][self.prevState[2]][self.prevState[3]]))
            self.QTable[self.prevState[0]][self.prevState[1]][self.prevState[2]][self.prevState[3]] += increment

        # Take a move
        choice = None
        # choose an action in an epsilon greedy manner:
        if random.random() < EPSILON:
            i = random.randint(0, 3)
            choice = ACTIONS[i]
            self.prevState = (index, steps, lastReward, i)
        else:
            best = -100000
            # take the argmax
            for i in range(4):
                val = self.QTable[index][steps][lastReward][i]
                if val > best:
                    best = val
                    choice = ACTIONS[i]
                    self.prevState = (index, steps, lastReward, i)
        
        return (self.name, choice)

import env as game

def runSingle(agent1, agent2, verbose = False):
    env = game.CooperativeReaching()
    package = env.reset(agentNames={agent1.name, agent2.name})
    terminated = False
    score = 0

    while not terminated:
        if verbose:
            print(package)

        agent1.observe(package)
        agent2.observe(package)

        a1 = agent1.act()
        a2 = agent2.act()

        package = env.step({a1[0]:a1[1], a2[0]:a2[1]})
        observation, reward, terminated, _, _, _ = package 
        score += reward

    return score

agent1, agent2 = RLPolicy(), RLPolicy()
agent1.init()
agent2.init()

f = open("logs.txt", "w")

for st in range(200):
    cumulativeScore = 0
    for it in range(1000):
        agent1.reset("1", "2")
        agent2.reset("2", "1")

        score = runSingle(agent1, agent2)
        cumulativeScore += score

    f.write(f"{st * it}, {cumulativeScore / 1000}\n")
    print("*", end="", flush=True)

agent1.reset("1", "2")
agent2.reset("2", "1")
print()
runSingle(agent1, agent2, verbose=True)

