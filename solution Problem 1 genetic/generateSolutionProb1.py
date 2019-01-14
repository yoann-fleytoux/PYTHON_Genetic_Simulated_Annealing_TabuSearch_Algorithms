from random import *
import time
import myParser
import math

def checkAssignedTask(solutionArray):
    assigned = []
    for i in range(len(solutionArray)):
        for j in range(len(solutionArray[i])):
            if (solutionArray[i][j]):
                assigned.append(j)
    return assigned

def computeResourceLeft(solutionArray, ressourceArray, agentCapacity, agentNumber):
    # calculate ressource left for the agent
    resourceLeft = agentCapacity
    for j in range(len(
            solutionArray[agentNumber])):  # for each task done by the current agent we remove the resource cost
        if (solutionArray[agentNumber][j]):
            resourceLeft -= ressourceArray[agentNumber][j]
    return resourceLeft

def printProgressBar(currRatio):
    numberOfCharacterProgressBar = 100
    ratioOnTen = math.ceil(currRatio * numberOfCharacterProgressBar)
    print("[", end='')
    for i in range(ratioOnTen):
        print("*", end='')
        for i in range(numberOfCharacterProgressBar - ratioOnTen):
            print(" ", end='')
            print("]", end='')
            print(" ", currRatio)


def printSolution(solutionArray):
    print ("")
    for i in range(len(solutionArray)):
        print ("Agent ",i,":", end='')
        for j in range(len(solutionArray[i])):
            if(solutionArray[i][j]):
                print(j," ", end='')
        print("")
    print ("")

def solveProblem(agents,tasks,resources,capacities,sizeOfPopulation):

    countTotalGenerationsGenerated = 0
    # we now have the data

    currentSolutionGenerated = 0

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
        start_time = time.time()
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
                        while (computeResourceLeft(assignments[currentSolutionGenerated],resources, currentAgentCapacity, currentAgentNumber) < ressourceNeeded):
                            if (assignments[currentSolutionGenerated][currentAgentNumber][j]):
                                assignments[currentSolutionGenerated][currentAgentNumber][j] = 0
                                # print ("task ", j, " removed from agent ", currentAgentNumber)
                            j += 1
                            # if(j>tasks-1):
                            #    j=0
                        assignments[currentSolutionGenerated][currentAgentNumber][currentTaskNumber] = 1
                        assignedTask = checkAssignedTask(assignments[currentSolutionGenerated])
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
        print ("SOLUTION ", currentSolutionGenerated," in: ",round((time.time() - start_time),2), "seconds")
        # printSolution(assignments[currentSolutionGenerated])
        # time.sleep(3)
        currentSolutionGenerated += 1

    
    return assignments
