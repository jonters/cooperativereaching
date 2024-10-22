# [Milestone 3]
# Evaluation pipeline

import env as game
import policies1 as p

numPolicies = 4
policiesA = [p.RandomPolicy(), p.GoTo00(), p.ClosestCornerNotBlind(), p.Blind()]
policiesB = [p.RandomPolicy(), p.GoTo00(), p.ClosestCornerNotBlind(), p.Blind()]

def runSingle(agent1, agent2):
    env = game.CooperativeReaching()
    package = env.reset(agentNames={agent1.name, agent2.name})
    observation, _ = package
    terminated = False
    score = 0

    while not terminated:
        agent1.observe(package)
        agent2.observe(package)

        a1 = agent1.act()
        a2 = agent2.act()

        package = env.step({a1[0]:a1[1], a2[0]:a2[1]})
        observation, reward, terminated, _, _, _ = package 
        score += reward

    return score

def runPairTest():
    matrix = [[0 for _ in range(numPolicies)] for _ in range(numPolicies)]

    for i in range(numPolicies):
        for j in range(numPolicies):
            policiesA[i].reset(str(i) + "A", str(j) + "B")
            policiesB[j].reset(str(j) + "B", str(i) + "A")

            TRIALS = 30
            cumulativeScore = 0
            for _ in range(TRIALS):
                cumulativeScore += runSingle(policiesA[i], policiesB[j])
            matrix[i][j] = cumulativeScore / TRIALS
    
    for row in matrix:
        print("  ".join("{:.{}f}".format(i, 4) for i in row))
            
runPairTest()