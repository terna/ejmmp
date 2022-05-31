import matplotlib.pyplot as plt
import commonVar as cmv

def seedManager(r,seed,name,address):
    if not name in cmv.functionDict: cmv.functionDict[name]=address
    if not hasattr(address, "r"):
        address.r=r.Random()
        address.r.seed(seed)

    

def makeHist():
    print("-------------------------------------------\n"+\
          "enterprise number "+ str(len(cmv.entrepreneurList))+\
          "\n-------------------------------------------\n")
    cmv.enterpriseSizeList=[]
    list(cmv.enterpriseSizeList.append(len(cmv.firmList[i].myWorkers)) for i in range(cmv.firmNum))
    list(cmv.enterpriseSizeList.append(len(cmv.bankList[i].myWorkers)) for i in range(cmv.bankNum))

    plt.hist(cmv.enterpriseSizeList,20,facecolor='orange')
    plt.xlabel("# of workers")
    plt.ylabel("# of enterprises")
    plt.title("Distribution of the enterprises by number of workers")      


def nationalAccounts():
    print("-------------------------------------------\n"+\
          '"national" accounts'+\
          "\n-------------------------------------------\n")
    print("%s\t%s\t%s\t\t%s\t%s\t%s" % \
          ("  t","total","initial","consum.","invest.","final"))
    print("\t%s\t%s\t\t\t\t%s" % ("a.v.","invent.","invent."))
    for i in range(cmv.ncycles):
        print("%3d\t%.3f\t%.3f\t    |\t%.3f\t%.3f\t%.3f" % \
                                   (i+1,cmv.totalAddedValueSeries[i],
                                   cmv.totalInitialInventoriesSeries[i],\
                                   cmv.totalConsumptionSeries[i],\
                                   cmv.totalInvestmentSeries[i],\
                                   cmv.totalFinalInventoriesSeries[i]))
        
    print("\n\n\n")