import commonVar as cmv
import random as r


# seed must be a valid int number in range -2147483648 through 2147483647; here we set a super seed
# into the model machine cell

def generateSeeds():
    cmv.functionSeedList=[]
    # seeds for functions (currently quite large as quantity)
    cmv.agentSeedList=[]
    # seeds for agent class instances; quantity = cmv.agentNum 
    cmv.firmSeedList=[]
    # seeds for firm class instances using cmv.entrepreneurMax as a tentative quantity 
    # (add positions if new firms are created while the simulation is running)
    cmv.bankSeedList=[]
    # seeds for bank class instances; quantity = cmv.bankMax
    
    for i in range(10):
        cmv.functionSeedList.append(r.randint(-2147483648,2147483647)) 

    for i in range(cmv.agentNum):
        cmv.agentSeedList.append(r.randint(-2147483648,2147483647)) 
        
    # if seed assignment are already done in a previuous run, we erase them    

    # function # 0 - setup
    if 'setup' in cmv.functionDict: del cmv.functionDict['setup'].r
        
    # function # 1 -  buyConsumptionGoodsAll
    if 'buyConsumptionGoodsAll' in cmv.functionDict: del cmv.functionDict['buyConsumptionGoodsAll'].r
        
    # function # 2 -  buyInvestmentGoodsAll
    if 'buyInvestmentGoodsAll' in cmv.functionDict: del cmv.functionDict['buyInvestmentGoodsAll'].r
        
    # function # 3 -  buyConsumptionOrInvestmentGoodsAll
    if 'buyConsumptionOrInvestmentGoodsAll' in cmv.functionDict: 
        del cmv.functionDict['buyConsumptionOrInvestmentGoodsAll'].r
        
 