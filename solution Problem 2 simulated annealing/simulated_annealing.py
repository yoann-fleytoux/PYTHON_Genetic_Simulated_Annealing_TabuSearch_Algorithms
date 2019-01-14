from random import randint
import time
import math

def constraint1(solution):
	return 85.334407 + 0.0056858*solution[1]*solution[4]+0.0006262*solution[0]*solution[3] - 0.0022053*solution[2]*solution[4] - 92

def constraint2(solution):
	return -85.334407 - 0.0056858*solution[1]*solution[4] - 0.0006262*solution[0]* solution[3] + 0.0022053*solution[2]* solution[4]

def constraint3(solution):
	return 80.51249 + 0.0071317*solution[1]* solution[4] + 0.0029955*solution[0]* solution[1]+ 0.0021813*solution[2]*solution[2] - 110

def constraint4(solution):
	return -80.51249 - 0.0071317*solution[1]* solution[4] - 0.0029955*solution[0]* solution[1]- 0.0021813*solution[2]*solution[2]  + 90

def constraint5(solution):
	return 9.300961+ 0.0047026*solution[2]* solution[4] + 0.0012547*solution[0]* solution[2] + 0.0019085*solution[2]* solution[3] - 25

def constraint6(solution):
	return -9.300961 - 0.0047026*solution[2]* solution[4] - 0.0012547*solution[0]* solution[2] - 0.0019085*solution[2]* solution[3] + 20 

def testC1(solution):
	return (constraint1(solution) <= 0)

def testC2(solution):
	return (constraint2(solution) <= 0)

def testC3(solution):
	return (constraint3(solution) <= 0)

def testC4(solution):
	return (constraint4(solution) <= 0)

def testC5(solution):
	return (constraint5(solution) <= 0)

def testC6(solution):
	return (constraint6(solution) <= 0)

def testAllConstraints(solution):
	return (testC1(solution) and testC2(solution) and testC3(solution) and testC4(solution) and testC5(solution) and testC6(solution))

def testBoundary(solution,numberVariable):
	lowerBounds=[78,33,27,27,27]
	upperBounds=[102,45,45,45,45]
	correct=1
	if(solution[numberVariable] < lowerBounds[numberVariable]):
		correct=0
	if(solution[numberVariable] > upperBounds[numberVariable]):
		correct=0
	return correct

def testBoundaries(solution):
	correct=1
	for i in range(5):
		if(testBoundary(solution,i)==0):
			correct=0
			break;
	
	return correct

def fitness(solution):
	score= 5.3578547*solution[2]*solution[2] + 0.8356891*solution[0]* solution[4] + 37.293239*solution[0] - 40792.141
	score=round(score,10)
	return score

def generateRandomValueforVariableI(numberVariable):
	lowerBounds=[78,33,27,27,27]
	upperBounds=[102,45,45,45,45]
	result=lowerBounds[numberVariable]+randint(0,(upperBounds[numberVariable]-lowerBounds[numberVariable])*100)/100
	result=round(result,3)
	#print("result var",numberVariable,"is",result)
	return result
def generateRandomSolution():
	solutionGenerated=[generateRandomValueforVariableI(0),generateRandomValueforVariableI(1),generateRandomValueforVariableI(2),generateRandomValueforVariableI(3),generateRandomValueforVariableI(4)]
	return solutionGenerated

def generateCorrectRandomSolution():
	solutionCorrect=[]
	correct=0
	while(not correct):
		solutionCorrect=generateRandomSolution()
		correct=testAllConstraints(solutionCorrect)
		#if(not correct):
		#	print("fail constraints")
		if(correct):
			correct=testBoundaries(solutionCorrect)
			#if(not correct):
			#	print("fail boundaries")

	return solutionCorrect

def getProba(oldSolution,newSolution,temperature):
	#print(oldSolution)
	#print(newSolution)
	scoreOld=fitness(oldSolution)
	scoreNew=fitness(newSolution)
	if(scoreNew<=scoreOld):
		return 1
	else:
		score=math.exp((scoreOld-scoreNew)/temperature)
		#print(scoreOld)
		#print(scoreNew)
		#print("delta:",scoreOld-scoreNew,"temp:",temperature)
		#print(score)
		return score

def printbestSolutions(solution):
	for i in range(len(solution)):
		print(solution[i])
		print("Score:",fitness(solution[i]))

#def computeProba():

#def generateFirstSolution():

#def generateNewSolutionInNeighboorhood():

#solution is a list of 5 float

#this is a min problem

solution=generateCorrectRandomSolution()
bestSolutions=[]
bestSolutions.append(solution)
BestScoreYet=fitness(solution)
print("Starting Score:",BestScoreYet)
#print(solution)
#print("Best:",fitness(solution))
iterationMax=1000
temperature=2000#t near 0-> like hill climbing, t high-> random walk
temperatureAtStart=temperature
sizeNeighboorhood=10
maxTime=60
nbRandomRestart=0
#for the number of iteration
countIterration=0

nbIterationFailedBeforeRandomRestart=10000
nbIterationFail=0
start_time = time.time()
while(countIterration <= iterationMax or (time.time()-start_time) < maxTime):
	#we try to move one of the variables randomly
	numberVariableMoved=randint(0,len(solution)-1)
	moveLenght=0.1*randint(1,sizeNeighboorhood)
	direction=randint(0,1)
	if(direction==0):
		direction=-1
	newSolution=solution[:]
	#newSolution.pop(numberVariableMoved)
	#newSolution.insert(numberVariableMoved,solution[numberVariableMoved]+round(moveLenght*direction,3))
	newSolution[numberVariableMoved]=round(newSolution[numberVariableMoved]+direction*moveLenght,3)
	if(testBoundaries(newSolution) and testAllConstraints(newSolution)):
		#print("avant:",solution,direction,"*",moveLenght,"v",numberVariableMoved)
		#print("après:",newSolution)
		probaGate=getProba(solution,newSolution,temperature)
		proba=randint(0,100)/100
		if(proba >= (1-probaGate)):
			solution=newSolution
			nbIterationFail=0
			#print(solution)
			#print("Fitness:",fitness(solution),"iteration:",countIterration,"curr temp:",temperature,"time:",round((time.time() - start_time),2), "seconds")
			if(fitness(solution) < BestScoreYet):
				bestSolutions.append(solution)
				BestScoreYet=fitness(solution)
				print("New best score:",BestScoreYet)
		else:
			#print("fail temp")
			nbIterationFail+=1
			if(temperature>1):
				temperature=round(temperature-0.5,2)
			else:
				print("Restart")
				nbIterationFail=0
				nbRandomRestart+=1
				solution=generateCorrectRandomSolution()
				temperature=temperatureAtStart
				if(fitness(solution) < BestScoreYet and solution not in bestSolutions):
					bestSolutions.append(solution)
					BestScoreYet=fitness(solution)
	else:
		nbIterationFail+=1

	#else:
		#print("fail condition")
	countIterration+=1
	#else:
	#	print("fail move")
print("nb Random Restart:",nbRandomRestart)
print("nb Iteration:",countIterration)
#print("Best score:",BestScoreYet)
printbestSolutions(bestSolutions)
print("Total execution time:",round((time.time() - start_time)))