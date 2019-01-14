
#Parses the whole file
def parseProblem(m,n,i,lines):
    costs = [None]*m
    resources = [None]*m
    for j in range(0,m):
        wordsCosts = lines[i+j+1].split()
        cost = []
        for k in range(0,n):
            cost.append(int(wordsCosts[k]))
        costs[j] = cost
    for j in range(0,m):
        wordsResources = lines[i+j+m+1].split()
        resource = []
        for k in range(0,n):
            resource.append(int(wordsResources[k]))
        resources[j] = resource
    wordsCapacities = lines[i+m+m+1].split()
    capacities = []
    for k in range(0,m):
        capacities.append(int(wordsCapacities[k]))
    return(costs,resources,capacities)

#Detects the numbers of problems to parse
def numberOfProblems(lines):
    total = 0

    for line in lines:
        found = line.find("Problema")
        if found != -1 and found != 0:
            total+=1
    return total

#The data is contained in m,n,costsOfPb,resourcesOfPb,capacitiesOfPb
def parse(filename):
    file = open(filename, "r")
    lines = file.readlines()
    nbPb = numberOfProblems(lines)

    countLines = 0
    agents = [None]*nbPb
    tasks = [None]*nbPb
    lineWithMandN = False
    problemsPassed = 0

    costsOfPb = [None] * nbPb
    resourcesOfPb = [None] * nbPb
    capacitiesOfPb = [None] * nbPb
    for i in range(0, len(lines)):
        if problemsPassed == nbPb:
            break
        words = lines[i].split()
        if lineWithMandN:
            agents[problemsPassed] = int(words[0])
            tasks[problemsPassed] = int(words[1])
            costsOfPb[problemsPassed], resourcesOfPb[problemsPassed], capacitiesOfPb[problemsPassed] = parseProblem(agents[problemsPassed], tasks[problemsPassed], i, lines)
            problemsPassed += 1
            lineWithMandN = False

        if "Problema" in words:
            lineWithMandN = True

    file.close()
    return agents,tasks,costsOfPb,resourcesOfPb,capacitiesOfPb

#if __name__ == "__main__":
#    main()