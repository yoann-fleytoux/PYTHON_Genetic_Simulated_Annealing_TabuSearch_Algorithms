from random import *
import time
import myParser
import math
from copy import deepcopy

class Node:
    def __init__(self, assignments):
        self.assignments = assignments
        self.score = None

    def generate_children(self, tasks, agents, current, resource, capacity, children):
        offspring = [Node(deepcopy(current.assignments)) for _ in range(children)]
        addOrSwap = False
        for node in offspring:
            #In this configuration, we won't use the "add" way of making kids, because we start from
            #a basic solution with all tasks assigned, so we will only make swaps
            if addOrSwap:
                nonAssigned = getAssignedTasks(agents,tasks,current.assignments, True)
                taskToAdd = randint(1,len(nonAssigned))
                taskToAdd = nonAssigned[taskToAdd]
                agentToAdd = randint(1,agents)
                while computeResourceLeft(current,resource,capacity,agentToAdd)-resource[agentToAdd][taskToAdd] < 0:
                    agentToAdd = randint(1, agents)
                for agent in node.assignments:
                    if agent == agentToAdd:
                        agent[taskToAdd] = 1
                        break
                addOrSwap = False
            else:
                taskToSwap1, taskToSwap2 = findSwapPossibility(agents, tasks, current, resource, capacity)

                if taskToSwap1 == taskToSwap2 == -1:
                    pass
                else:
                    agentToSwap1 = getAgentOfTask(node,taskToSwap1)

                    agentToSwap2 = getAgentOfTask(node,taskToSwap2)

                    for i in range(agents):
                        if i == agentToSwap1:
                            node.assignments[i][taskToSwap1] = 0
                            node.assignments[i][taskToSwap2] = 1
                        if i == agentToSwap2:
                            node.assignments[i][taskToSwap2] = 0
                            node.assignments[i][taskToSwap1] = 1
        return offspring

    def __repr__(self, ):
        return str(self.assignments)

    def __hash__(self, ):
        return str(self.assignments)

def findSwapPossibility(agents, tasks, current, resource, capacity, tries = 10):
    is1okay = False
    is2okay = False

    while not is1okay or not is2okay:
        possiblesFor1 = []
        possiblesFor2 = []
        tries-=1
        assigned = getAssignedTasks(agents, tasks, current.assignments, False)
        taskToSwap1 = randint(0, len(assigned)-1)
        taskToSwap1 = assigned[taskToSwap1]

        taskToSwap2 = randint(0, len(assigned)-1)
        taskToSwap2 = assigned[taskToSwap2]

        agentToSwap1 = getAgentOfTask(current, taskToSwap1)
        agentToSwap2 = getAgentOfTask(current, taskToSwap2)
        while agentToSwap1 == agentToSwap2:
            taskToSwap2 = randint(0, len(assigned)-1)
            taskToSwap2 = assigned[taskToSwap2]
            agentToSwap2 = getAgentOfTask(current, taskToSwap2)

        is1okay = computeResourceLeft(current.assignments, resource, capacity[agentToSwap1], agentToSwap1) - resource[agentToSwap1][taskToSwap2] + \
                resource[agentToSwap1][taskToSwap1] >= 0
        is2okay = computeResourceLeft(current.assignments, resource, capacity[agentToSwap2], agentToSwap2) - resource[agentToSwap2][taskToSwap1] + \
                resource[agentToSwap2][taskToSwap2] >= 0


        if not is1okay or not is2okay:
            for i in range(len(current.assignments[agentToSwap1])):
                if current.assignments[agentToSwap1][i]  == 1:
                    if computeResourceLeft(current.assignments, resource, capacity[agentToSwap2], agentToSwap2) - resource[agentToSwap2][i] + \
                    resource[agentToSwap2][taskToSwap2] >= 0:
                        if computeResourceLeft(current.assignments, resource, capacity[agentToSwap1], agentToSwap1) - resource[agentToSwap1][taskToSwap2] + \
                        resource[agentToSwap1][i] >= 0:
                            possiblesFor1.append(i)
            if not possiblesFor1:
                for i in range(len(current.assignments[agentToSwap2])):
                    if current.assignments[agentToSwap2][i]  == 1:
                        if computeResourceLeft(current.assignments, resource, capacity[agentToSwap1], agentToSwap1) - resource[agentToSwap1][i] + \
                        resource[agentToSwap1][taskToSwap1] >= 0:
                            if computeResourceLeft(current.assignments, resource, capacity[agentToSwap2], agentToSwap2) - resource[agentToSwap2][taskToSwap1] + \
                            resource[agentToSwap2][i] >= 0:
                                possiblesFor2.append(i)
        if possiblesFor1:
            taskToSwap1 = randint(0, len(possiblesFor1)-1)
            taskToSwap1 = possiblesFor1[taskToSwap1]
        elif possiblesFor2:
            taskToSwap2 = randint(0, len(possiblesFor2)-1)
            taskToSwap2 = possiblesFor2[taskToSwap2]
        is1okay = computeResourceLeft(current.assignments, resource, capacity[agentToSwap1], agentToSwap1) - resource[agentToSwap1][taskToSwap2] + \
                  resource[agentToSwap1][taskToSwap1] >= 0
        is2okay = computeResourceLeft(current.assignments, resource, capacity[agentToSwap2], agentToSwap2) - resource[agentToSwap2][taskToSwap1] + \
                  resource[agentToSwap2][taskToSwap2] >= 0
        if tries == 0 and not is1okay and not is2okay:
            return -1,-1

    return taskToSwap1,taskToSwap2

def getAgentOfTask(current,task):
    i = 0
    for agent in current.assignments:
        if agent[task] == 1:
            return i
        i+=1
    return -1

def evaluateFitness(solutionArray, costArray):
    score = 0
    for i in range(len(solutionArray)):
        for j in range(len(solutionArray[i])):
            score += solutionArray[i][j] * costArray[i][j]
    return score

def getAssignedTasks(agents, tasks, assignments, freeTasks):
    assigned = []
    for i in range(0, tasks):
        isAssigned = False
        for j in range(0, agents):
            if assignments[j][i] == 1:
                isAssigned = True
        if freeTasks:
            if not isAssigned:
                assigned.append(i)
        else:
            if isAssigned:
                assigned.append(i)
    return assigned

def computeResourceLeft(solutionArray, ressourceArray, agentCapacity, agentNumber):
    # calculate ressource left for the agent
    resourceLeft = agentCapacity

    for j in range(len(solutionArray[agentNumber])):  # for each task done by the current agent we remove the resource cost
        if (solutionArray[agentNumber][j]):
            resourceLeft -= ressourceArray[agentNumber][j]
    return resourceLeft

def printSolution(solutionArray):
    print ("")
    for i in range(len(solutionArray)):
        print ("Agent ",i,":", end='')
        for j in range(len(solutionArray[i])):
            if(solutionArray[i][j]):
                print(j," ", end='')
        print("")
    print ("")

def tabu(base, agents, tasks, costs, resource, capacity, tabu_length = 5, trials=10000, children=10):

    nodes = []
    nodes.append(Node(base))
    tabus = []

    bestScore = None
    while trials > 0:
        trials-=1
        current = nodes.pop()
        if current.assignments in tabus:
            current = nodes.pop()
        tabus.append(deepcopy(current.assignments))
        if len(tabus) > tabu_length:
            tabus.pop()

        for child in current.generate_children(tasks,agents,current,resource,capacity,children):
            if child.assignments not in tabus:
                scoreChild = evaluateFitness(child.assignments, costs)
                if bestScore == None:
                    bestScore = scoreChild
                    bestSolution = Node(child.assignments)
                    bestSolution.score = scoreChild
                if scoreChild < bestScore:
                    bestScore = scoreChild
                    bestSolution = Node(child.assignments)
                    bestSolution.score = scoreChild
                print(evaluateFitness(child.assignments,costs))
                nodes.append(child)
        nodes = nodes[:children]

    printSolution(bestSolution.assignments)
    print("With Score : ", bestScore)


def solveProblemFirst(agents, tasks, costs, resources, capacities, sizeOfPopulation=5):
    start_time = time.time()

    countTotalGenerationsGenerated = 0
    # we now have the data

    currentSolutionGenerated = 0

    bestSolutionYet = [[0 for x in range(tasks)] for y in range(agents)]

    # the solutions array is of size sizeOfPopulation * numberOfAgent *numberOfTask
    assignments = [[[0 for x in range(tasks)] for y in range(agents)] for z in
                                  range(sizeOfPopulation)]
    # while all the solution aren't generated
    maxIterationsPossible = 400
    '''
    if (numberOfProblem == 3):
        maxIterationPossible = 200
    '''
    maxRatioReached = 0

    while (currentSolutionGenerated != sizeOfPopulation):
        # let's generate a solution
        # each task must be assign to one agent
        # but each agent has a ressource limit
        currentTaskNumber = randint(0, tasks - 1)
        currentAgentNumber = randint(0, agents - 1)
        thresholdProbaAssignment = 50

        assignedTask = []
        # while the current solution has not all the task assigned
        countIteration = 0
        while (len(assignedTask) != tasks):
            currRatio = len(assignedTask) / tasks
            if (currRatio > maxRatioReached):
                maxRatioReached = currRatio
            # while the task have not been given
            if (currentTaskNumber == tasks):
                currentTaskNumber = 0

            while (currentTaskNumber not in assignedTask):
                # print ("current task: ", currentTaskNumber, " current agent: ", currentAgentNumber)
                # randomly check if the task is given to an agent i
                chance = randint(1, 100)  # generate a number between 1 and 100
                if (chance >= thresholdProbaAssignment):
                    # if the task is given, check if the agent has enough ressource
                    ressourceNeeded = resources[currentAgentNumber][currentTaskNumber]
                    currentAgentCapacity = capacities[currentAgentNumber]
                    # if the agent has the capicity to do the task
                    if (ressourceNeeded <= currentAgentCapacity):
                        # j=randint(0,tasks-1)
                        j = 0
                        while (computeResourceLeft(assignments[currentSolutionGenerated],
                                                   resources, currentAgentCapacity, currentAgentNumber,
                                                   ) < ressourceNeeded):
                            if (assignments[currentSolutionGenerated][currentAgentNumber][j]):
                                assignments[currentSolutionGenerated][currentAgentNumber][j] = 0
                                # print ("task ", j, " removed from agent ", currentAgentNumber)
                            j += 1
                            # if(j>tasks-1):
                            #    j=0
                        assignments[currentSolutionGenerated][currentAgentNumber][currentTaskNumber] = 1
                        assignedTask = getAssignedTasks(agents,tasks,assignments[currentSolutionGenerated], False)
                        countIteration += 1
                        # print ("task ",tasks, "assigned to agent ",currentAgentNumber )  ;
                        # else:
                        # print ("agent ",agents," has not the capacity to do ",currentTaskNumber)
                # we pass to the next agent
                currentAgentNumber += 1
                if (currentAgentNumber == agents):
                    currentAgentNumber = 0
                    # the task has been assigned
            currentTaskNumber += 1
            # printSolution(assignments[currentSolutionGenerated])
            # print (assignedTask)
            # time.sleep(1)

            if (countIteration == maxIterationsPossible):
                if (maxRatioReached < 0.90):
                    # print ("TRY AGAIN SOLUTION ",currentSolutionGenerated ," max ratio: ",maxRatioReached)
                    for i in range(agents):
                        for j in range(tasks):
                            assignments[currentSolutionGenerated][i][j] = 0
                    assignedTask = []
                    # else:
                    # print("Solution ", currentSolutionGenerated,": ",maxRatioReached )
                # time.sleep(3)
                maxRatioReached = 0
                countIteration = 0
        #print ("SOLUTION ", currentSolutionGenerated)
        # printSolution(assignments[currentSolutionGenerated])
        # time.sleep(3)
        currentSolutionGenerated += 1

    # we now have sizeOfPopulation solution
    # we sort the solutions by effectiveness
    effectivenessOfPopulation = [0 for i in range(sizeOfPopulation)]
    for i in range(sizeOfPopulation):
        effectivenessOfPopulation[i] = [evaluateFitness(assignments[i], costs), i]
        # printSolution(assignments[i])
    effectivenessOfPopulation.sort(key=lambda data: data[0])
    # print ("score: ",effectivenessOfPopulation)

    print("First generation generated in: -- %s seconds ---" % (time.time() - start_time))
    bestSolutionYet = assignments[effectivenessOfPopulation[0][1]]
    bestScoreYet = evaluateFitness(bestSolutionYet, costs)
    print("Best Score: ", bestScoreYet)
    # print(effectivenessOfPopulation[numeroPodiumSolution][1])->numero individu, numeroPodiumSolution >= 0 and numeroPodiumSolution< sizeOfPopulation
    countTotalGenerationsGenerated += currentSolutionGenerated


    return assignments,bestSolutionYet


def main():
    start_time = time.time()
    agents, tasks, costs, resources, capacities = myParser.parse("PAG2017.txt")
    nbP = 3
    children, bestSol = solveProblemFirst(agents[nbP], tasks[nbP], costs[nbP], resources[nbP], capacities[nbP],5)
    printSolution(bestSol)

    tabu(bestSol, agents[nbP], tasks[nbP], costs[nbP], resources[nbP], capacities[nbP])
    print("Total execution time:", round((time.time() - start_time)))

if __name__ == "__main__":
    main()