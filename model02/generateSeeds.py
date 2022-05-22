import commonVar as cmv
import random as r


# seed must be a valid int number in range -2147483648 through 2147483647; here we set a super seed
# into the model machine cell

def generateSeeds():
    cmv.seedList=[]
    # seeds for class instances and functions (estimete); entrepreneurMax 
    # represents the max number of firm that will be created
    nSeeds=cmv.agentNum + cmv.entrepreneurMax + cmv.bankMax + 101
    
    for i in range(nSeeds):
        cmv.seedList.append(r.randint(-2147483648,2147483647)) 

    # if seed assignment already done in a previuous run, we erase it    

    # function # 0 - setup
    if 'setup' in cmv.functionDict: del cmv.functionDict['setup'].r
        
    # function # 1 -  buyConsumptionGoodsAll
    if 'buyConsumptionGoodsAll' in cmv.functionDict: del cmv.functionDict['buyConsumptionGoodsAll'].r
        
    # function # 2 -  buyInvestmentGoodsAll
    if 'buyInvestmentGoodsAll' in cmv.functionDict: del cmv.functionDict['buyInvestmentGoodsAll'].r
        
    # function # 3 -  buyConsumptionOrInvestmentGoodsAll
    if 'buyConsumptionOrInvestmentGoodsAll' in cmv.functionDict: 
        del cmv.functionDict['buyConsumptionOrInvestmentGoodsAll'].r
        
    # agents from position 101