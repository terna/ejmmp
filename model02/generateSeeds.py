import commonVar as cmv
import random as r


# seed must be a valid int number in range -2147483648 through 2147483647; here we set a super seed
# into the model machine cell

def generateSeeds():
    cmv.seedList=[]
    # seeds for class instances and functions (estimete); entrepreneurMax 
    # is the max number of firm that will be created
    nSeeds=cmv.agentNum + cmv.entrepreneurMax + cmv.bankMax + 50
    
    for i in range(nSeeds):
        cmv.seedList.append(r.randint(-2147483648,2147483647))      