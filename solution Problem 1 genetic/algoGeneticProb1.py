from random import *
import time
import myParser
import generateSolutionProb1
import math

def chooseMatingCandidates(populationOfSolution,effectivenessOfPopulation,sizeOfPopulation,numberProblem):
    firstMatingCandidateNumber=0
    secondMatingCandidateNumber=0
    thresholdProbaMatingCandidate1=80-numberProblem*10
    thresholdProbaMatingCandidate2=80-numberProblem*10
    for i in range(len(populationOfSolution)):
        chance1=randint(1, 100)
        chance2=randint(1, 100)
        if(chance1 > thresholdProbaMatingCandidate1 and firstMatingCandidateNumber != sizeOfPopulation-1):
            firstMatingCandidateNumber+=1
        if(chance2 > thresholdProbaMatingCandidate2 and secondMatingCandidateNumber != sizeOfPopulation-1):
            secondMatingCandidateNumber+=1
    return firstMatingCandidateNumber, secondMatingCandidateNumber    

# evaluate the fitness of a solution
def evaluateFitness(solutionArray, costArray):
    score = 0
    for i in range(len(solutionArray)):
        for j in range(len(solutionArray[i])):
            score += solutionArray[i][j] * costArray[i][j]
    return score

def setParam1(problemSolvedNumber):
    return{
        0: 30,
        1: 20,
        2: 10,
    }.get(problemSolvedNumber, 10) 

def setSizeOffspringPopulation(problemSolvedNumber):
    return{
        0: 80,
        1: 50,
        2: 30,
    }.get(problemSolvedNumber, 20) 

def setThresholdProbaAssignment(problemSolvedNumber):
    return{
        0: 80,
        1: 80,
        2: 90,
    }.get(problemSolvedNumber, 98) 

def setTimeLimit(problemSolvedNumber):
    return{
        0: 30,
        1: 40,
        2: 60,
    }.get(problemSolvedNumber, 120) 


#The data is contained in m,n,costs,resources,capacities
def main():

    problemSolvedNumber = int(input("Choose the set of Data used to solve the problem: 0/1/2/3: "))# 0 - 3
    start_time_total = time.time()
    agents, tasks, costs, resources, capacities = myParser.parse("PAG2017.txt")
    
    sizeOfPopulation=setParam1(problemSolvedNumber)
    #parents = generateSolutionProb1.solveProblem(agents[problemSolvedNumber], tasks[problemSolvedNumber], resources[problemSolvedNumber], capacities[problemSolvedNumber],25)
    parents = generateSolutionProb1.solveProblem(agents[problemSolvedNumber], tasks[problemSolvedNumber], resources[problemSolvedNumber], capacities[problemSolvedNumber],sizeOfPopulation)
    print("First generation generated in: -- %s seconds ---" % round((time.time() - start_time_total),2)) 

    # we sort the solutions by effectiveness
    effectivenessOfPopulation = [0 for i in range(sizeOfPopulation)]
    for i in range(sizeOfPopulation):
        effectivenessOfPopulation[i] = [evaluateFitness(parents[i], costs[problemSolvedNumber]), i]
        # generateSolutionProb1.printSolution(parents[i])
    effectivenessOfPopulation.sort(key=lambda data: data[0])
    # print ("score: ",effectivenessOfPopulation)

    
    bestSolutionYet = parents[effectivenessOfPopulation[0][1]]
    bestScoreYet = evaluateFitness(bestSolutionYet, costs[problemSolvedNumber])
    print("Best Score: ", bestScoreYet)
    # print(effectivenessOfPopulation[numeroPodiumSolution][1])->numero individu, numeroPodiumSolution >= 0 and numeroPodiumSolution< sizeOfPopulation
    countTotalGenerationGenerated = sizeOfPopulation

    #**************************************************************************************************************************

    BestIndividuals=[]
    BestIndividuals.append(bestSolutionYet)

    sizeOfFirstGeneration=setParam1(problemSolvedNumber)
    sizeOfPopulation=setSizeOffspringPopulation(problemSolvedNumber)
    first=1
    doIt=1
    numberOfIterationBeforeAskingToStop=-1
    countIteration=0
    numberOfGenerationWithoutAmeliorationBeforeStoping=5000
    countIterationGenerationWithoutAmelioration=0
    thresholdProbaAssignment=setThresholdProbaAssignment(problemSolvedNumber)
    
    thresholdProbaAssignmentInitial=thresholdProbaAssignment
    timeLimitInSeconds=setTimeLimit(problemSolvedNumber)
    swapForBest=0
    start_time = time.time()
    #**************************************************************************************************************************



    while(doIt>0 and (time.time() - start_time) < timeLimitInSeconds):
        countGeneFrom1=0
        countGeneFrom2=0
        countGeneFromBoth=0
        countGeneFromMutation=0
        children=[[[0 for x in range(tasks[problemSolvedNumber])] for y in range(agents[problemSolvedNumber])] for z in range(sizeOfPopulation) ] 
        currentSolutionGenerated=0
        couplesWhoHaveMated=[]
        startTimeGene = time.time()
        while(currentSolutionGenerated!=sizeOfPopulation):
            #select 2 solutions (better solutions have better chance to be chosen)
            isThisANewCouple=0
            while(isThisANewCouple!=1):
                if(first):
                    numeroSolution1, numeroSolution2 = chooseMatingCandidates(parents,effectivenessOfPopulation,sizeOfFirstGeneration,problemSolvedNumber)
                else:
                    numeroSolution1, numeroSolution2 = chooseMatingCandidates(parents,effectivenessOfPopulation,sizeOfPopulation,problemSolvedNumber)
                if(numeroSolution1 == numeroSolution2):
                    if(numeroSolution2 !=0):
                        numeroSolution2-=1
                    else:
                        numeroSolution2+=1
                if([numeroSolution1,numeroSolution2] not in couplesWhoHaveMated and [numeroSolution2,numeroSolution1] not in couplesWhoHaveMated):
                    couplesWhoHaveMated.append([numeroSolution1,numeroSolution2])
                    isThisANewCouple=1
                #else:
                    #print("THEY ALREADY MATED")

            #print (numeroSolution1, " reproduce with", numeroSolution2)

            numeroSolution1=effectivenessOfPopulation[numeroSolution1][1]
            numeroSolution2=effectivenessOfPopulation[numeroSolution2][1]
            #print (numeroSolution1, " reproduce with", numeroSolution2)
    
            assignedTask=[]                
            currentTaskNumber=randint(0,tasks[problemSolvedNumber]-1)
            currentAgentNumber=randint(0,agents[problemSolvedNumber]-1)

            #while the current solution has not all the task assigned
            while(len(assignedTask) != tasks[problemSolvedNumber]):       
                while (currentTaskNumber not in assignedTask):
                    #print ("current task: ", currentTaskNumber, " current agent: ", currentAgentNumber)
                    #randomly check if the task is given to an agent i
                    chance=randint(1, 100)#generate a number between 1 and 100
                    #print (numeroSolution1, numeroSolution2, len(parents), currentAgentNumber, currentTaskNumber)
                    if(chance >= thresholdProbaAssignment or parents[numeroSolution1][currentAgentNumber][currentTaskNumber] or parents[numeroSolution2][currentAgentNumber][currentTaskNumber] ):
                        #if the task is given, check if the agent has enough ressource
                        ressourceNeeded=resources[problemSolvedNumber][currentAgentNumber][currentTaskNumber]
                        currentAgentCapacity=capacities[problemSolvedNumber][currentAgentNumber]
                        #if the agent has the capicity to do the task
                        if(ressourceNeeded <= currentAgentCapacity):
                            #j=randint(0,tasks[problemSolvedNumber]-1)
                            j=0
                            while(generateSolutionProb1.computeResourceLeft(children[currentSolutionGenerated],resources[problemSolvedNumber],currentAgentCapacity,currentAgentNumber) < ressourceNeeded):
                                if(children[currentSolutionGenerated][currentAgentNumber][j]):
                                    children[currentSolutionGenerated][currentAgentNumber][j]=0
                                    #print ("task ", j, " removed from agent ", currentAgentNumber)
                                j+=1
                                #if(j>tasks[problemSolvedNumber]-1):
                                #    j=0
                            children[currentSolutionGenerated][currentAgentNumber][currentTaskNumber]=1
                            assignedTask=generateSolutionProb1.checkAssignedTask(children[currentSolutionGenerated])          
                            #print ("task ",currentTaskNumber, "assigned to agent ",currentAgentNumber )  ;
                        #else:
                            #print ("agent ",currentAgentNumber," has not the capacity to do ",currentTaskNumber)                         
                    #we pass to the next agent
                    currentAgentNumber+=1
                    if(currentAgentNumber == agents[problemSolvedNumber]):
                        currentAgentNumber=0   
                #the task has been assigned
                currentTaskNumber+=1 
                if(currentTaskNumber == tasks[problemSolvedNumber]):
                    currentTaskNumber=0
            #count similiarities
            numberOfGeneFromFirst=0
            numberOfGeneFromSecond=0
            numberOfGeneInBoth=0
            numberFromMutation=0
            #print("[",end='')
            for i in range(agents[problemSolvedNumber]):
                for j in range(tasks[problemSolvedNumber]):
                    if(children[currentSolutionGenerated][i][j]):
                        score=parents[numeroSolution1][i][j]*10+parents[numeroSolution2][i][j]
                        if(score==10):
                            numberOfGeneFromFirst+=1
            #                print(" 1 ",end='')
                        if(score==1):
                            numberOfGeneFromSecond+=1
            #                print(" 2 ",end='')
                        if(score==11):
                            numberOfGeneInBoth+=1
            #                print(" B ",end='')
                        if(score==0):
                            numberFromMutation+=1 
            #                print(" M ",end='')
            #print("]", end='  -----------------  ')
            #if(numberOfGeneFromFirst==0 and numberOfGeneFromSecond==0 and thresholdProbaAssignment > 70):
            #    thresholdProbaAssignment-=1
            #    #print("-")
            #if(numberOfGeneFromFirst > 0 and numberOfGeneFromSecond > 0 and thresholdProbaAssignment < thresholdProbaAssignmentInitial):
            #    thresholdProbaAssignment+=1
                #print("+")
            #print(numeroSolution1," GIVES ",numberOfGeneFromFirst,"|",numeroSolution2," GIVES ",numberOfGeneFromSecond," |  BOTH GIVE ",numberOfGeneInBoth," |  MUTATION: ",numberFromMutation,)
            countGeneFrom1+=numberOfGeneFromFirst
            countGeneFrom2+=numberOfGeneFromSecond
            countGeneFromBoth+=numberOfGeneInBoth
            countGeneFromMutation+=numberFromMutation
            currentSolutionGenerated+=1

        countTotalGenerationGenerated+=currentSolutionGenerated

        effectivenessOfPopulation=[0 for i in range(sizeOfPopulation)]
        for i in range(sizeOfPopulation):
            effectivenessOfPopulation[i]=[evaluateFitness(children[i],costs[problemSolvedNumber]),i]
            #generateSolutionProb1.printSolution(parents[i])
        effectivenessOfPopulation.sort( key=lambda data: data[0])
        #print ("score: ",effectivenessOfPopulation)
        bestScoreOfThisGeneration=evaluateFitness(children[effectivenessOfPopulation[0][1]],costs[problemSolvedNumber])
        if(bestScoreYet > bestScoreOfThisGeneration):
            bestScoreYet=bestScoreOfThisGeneration
        print("Best: ",bestScoreOfThisGeneration,"Best Total:",bestScoreYet,"1: ",round(100*countGeneFrom1/(sizeOfPopulation*tasks[problemSolvedNumber]),2),"% 2: ",round(100*countGeneFrom2/(sizeOfPopulation*tasks[problemSolvedNumber]),2),"% B: ",round(100*countGeneFromBoth/(sizeOfPopulation*tasks[problemSolvedNumber]),2),"% M: ",round(100*countGeneFromMutation/(sizeOfPopulation*tasks[problemSolvedNumber]),2),"% total generated: ",countTotalGenerationGenerated, " in:",round((time.time() - startTimeGene),2),"seconds")#" threshold: ", thresholdProbaAssignment, "nb pop: ", sizeOfPopulation, " nb pop origin: ",sizeOfFirstGeneration)

        if(evaluateFitness(bestSolutionYet,costs[problemSolvedNumber]) > bestScoreOfThisGeneration):
            bestSolutionYet=children[effectivenessOfPopulation[0][1]]
            BestIndividuals.append(bestSolutionYet)
            countIterationGenerationWithoutAmelioration=0
        else:
            countIterationGenerationWithoutAmelioration+=1

        if(len(BestIndividuals)==sizeOfPopulation and swapForBest):
            print("Generation of Best")
            children=BestIndividuals
            BestIndividuals=[]
            effectivenessOfPopulation=[0 for i in range(sizeOfPopulation)]
            for i in range(sizeOfPopulation):
                effectivenessOfPopulation[i]=[evaluateFitness(children[i],costs[problemSolvedNumber]),i]
                #generateSolutionProb1.printSolution(parents[i])
            effectivenessOfPopulation.sort( key=lambda data: data[0])

        countIteration+=1
        first=0

        if(countIterationGenerationWithoutAmelioration == numberOfGenerationWithoutAmeliorationBeforeStoping):
            break
        if(countIteration==numberOfIterationBeforeAskingToStop):
            countIteration=0
            doIt = int(input("New Generation: 1 , print best solution 0: "))
            #print("You have chosen: ",doIt)
        if(doIt):
            parents=children
            
    if(len(BestIndividuals)>0):
        for i in range(len(BestIndividuals)):
            generateSolutionProb1.printSolution(BestIndividuals[i])
            print("Score: ", evaluateFitness(BestIndividuals[i],costs[problemSolvedNumber]))
    else:
        print("Best Score: ",evaluateFitness(bestSolutionYet,costs[problemSolvedNumber]))
        generateSolutionProb1.printSolution(bestSolutionYet)
    print("Number total of solution tested: ", countTotalGenerationGenerated)
    print("Total execution time --- %s seconds ---" % round((time.time() - start_time_total),2))



    

if __name__ == "__main__":
    main()