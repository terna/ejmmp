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


def plot1():
    # https://matplotlib.org/3.5.1/gallery/subplots_axes_and_figures/two_scales.html
    # https://matplotlib.org/3.5.1/tutorials/colors/colors.html
    myColor1 = 'tab:orange'
    myColor2 = 'tab:blue'
    fig1, ax1a = plt.subplots()
    ax1a.set_ylim([0, max(cmv.totalProductionSeries)])
    t=range(1,cmv.ncycles+1)
    ax1a.plot(t, cmv.totalProductionSeries, label="production", color=myColor1)
    ax1a.tick_params(axis='y', labelcolor=myColor1)
    
    ax2a = ax1a.twinx()  # instantiate a second axes that shares the same x-axis
    ax2a.set_ylim([0, max(cmv.totalProductionInfraVarSeries)])
    ax2a.plot(t, cmv.totalProductionInfraVarSeries, label="prodInVar", color=myColor2)
    ax2a.tick_params(axis='y', labelcolor=myColor2)
    fig1.legend()

def plot2():
    # https://matplotlib.org/3.5.1/gallery/subplots_axes_and_figures/two_scales.html
    # https://matplotlib.org/3.5.1/tutorials/colors/colors.html
    myColor1 = 'tab:orange'
    myColor2 = 'tab:blue'
    fig2, ax1b = plt.subplots()
    ax1b.set_ylim([min(cmv.totalProfitSeries), max(0,max(cmv.totalProfitSeries))])
    t=range(1,cmv.ncycles+1)
    ax1b.plot(t, cmv.totalProfitSeries, label="profit", color=myColor1)
    ax1b.tick_params(axis='y', labelcolor=myColor1)
    ax1b.plot([1,cmv.ncycles],[0,0], label="zero line", color=myColor1, linestyle='dashed')

    ax2b = ax1b.twinx()  # instantiate a second axes that shares the same x-axis
    ax2b.set_ylim([0, max(cmv.totalProfitInfraVarSeries)])
    ax2b.plot(t, cmv.totalProfitInfraVarSeries, label="profInVar", color=myColor2)
    ax2b.tick_params(axis='y', labelcolor=myColor2)
    fig2.legend()

def plot3():
    # https://matplotlib.org/3.5.1/gallery/subplots_axes_and_figures/two_scales.html
    # https://matplotlib.org/3.5.1/tutorials/colors/colors.html
    myColor1 = 'tab:orange'
    myColor2 = 'tab:blue'
    fig3, ax1c = plt.subplots()
    ax1c.set_ylim([min(cmv.totalInitialInventoriesSeries), \
                   max(0,max(cmv.totalInitialInventoriesSeries))])
    t=range(1,cmv.ncycles+1)
    ax1c.plot(t, cmv.totalInitialInventoriesSeries, label="initialInventories", \
              color=myColor1)
    ax1c.tick_params(axis='y', labelcolor=myColor1)
    ax1c.plot([1,cmv.ncycles],[0,0], label="zero line", color=myColor1, linestyle='dashed')

    ax2c = ax1c.twinx()  # instantiate a second axes that shares the same x-axis
    ax2c.set_ylim([0, max(cmv.totalInitialInventoriesInfraVarSeries)])
    ax2c.plot(t, cmv.totalInitialInventoriesInfraVarSeries, label="initialInventoriesInVar",\
              color=myColor2)
    ax2c.tick_params(axis='y', labelcolor=myColor2)
    fig3.legend()

def plot4():
    # https://matplotlib.org/3.5.1/gallery/subplots_axes_and_figures/two_scales.html
    # https://matplotlib.org/3.5.1/tutorials/colors/colors.html
    myColor1 = 'tab:orange'
    myColor2 = 'tab:blue'
    fig4, ax1d = plt.subplots()
    ax1d.set_ylim([min(cmv.totalFinalInventoriesSeries), \
                   max(0,max(cmv.totalFinalInventoriesSeries))])
    t=range(1,cmv.ncycles+1)
    ax1d.plot(t, cmv.totalFinalInventoriesSeries, label="finalInventories", \
              color=myColor1)
    ax1d.tick_params(axis='y', labelcolor=myColor1)
    ax1d.plot([1,cmv.ncycles],[0,0], label="zero line", color=myColor1, linestyle='dashed')

    ax2d = ax1d.twinx()  # instantiate a second axes that shares the same x-axis
    ax2d.set_ylim([0, max(cmv.totalFinalInventoriesInfraVarSeries)])
    ax2d.plot(t, cmv.totalFinalInventoriesInfraVarSeries, label="finalInventoriesInVar",\
              color=myColor2)
    ax2d.tick_params(axis='y', labelcolor=myColor2)
    fig4.legend()

def plot5():
    # https://matplotlib.org/3.5.1/gallery/subplots_axes_and_figures/two_scales.html
    # https://matplotlib.org/3.5.1/tutorials/colors/colors.html
    myColor1 = 'tab:orange'
    myColor2 = 'tab:blue'
    fig5, ax1e = plt.subplots()
    ax1e.set_ylim([0, max(cmv.totalConsumptionSeries)])
    t=range(1,cmv.ncycles+1)
    ax1e.plot(t, cmv.totalConsumptionSeries, label="consumption", color=myColor1)
    ax1e.tick_params(axis='y', labelcolor=myColor1)
    
    ax2e = ax1e.twinx()  # instantiate a second axes that shares the same x-axis
    ax2e.set_ylim([0, max(cmv.totalConsumptionInfraVarSeries)])
    ax2e.plot(t, cmv.totalConsumptionInfraVarSeries, label="consInVar", color=myColor2)
    ax2e.tick_params(axis='y', labelcolor=myColor2)
    fig5.legend()

def plot6():
    # https://matplotlib.org/3.5.1/gallery/subplots_axes_and_figures/two_scales.html
    # https://matplotlib.org/3.5.1/tutorials/colors/colors.html
    myColor1 = 'tab:orange'
    myColor2 = 'tab:blue'
    fig6, ax1f = plt.subplots()
    ax1f.set_ylim([0, max(cmv.totalInvestmentSeries)])
    t=range(1,cmv.ncycles+1)
    ax1f.plot(t, cmv.totalInvestmentSeries, label="investment", color=myColor1)
    ax1f.tick_params(axis='y', labelcolor=myColor1)
    
    ax2f = ax1f.twinx()  # instantiate a second axes that shares the same x-axis
    ax2f.set_ylim([0, max(cmv.totalInvestmentInfraVarSeries)])
    ax2f.plot(t, cmv.totalInvestmentInfraVarSeries, label="investInVar", color=myColor2)
    ax2f.tick_params(axis='y', labelcolor=myColor2)
    fig6.legend()
    
def plot7():
    # https://matplotlib.org/3.5.1/gallery/subplots_axes_and_figures/two_scales.html
    # https://matplotlib.org/3.5.1/tutorials/colors/colors.html
    myColor1 = 'tab:orange'
    myColor2 = 'tab:blue'
    fig7, ax1g = plt.subplots()
    ax1g.set_ylim([min(-0.01, min(cmv.totalCashMoneySeries)), max(0.01,max(cmv.totalCashMoneySeries))])
    t=range(1,cmv.ncycles+1)
    ax1g.plot(t, cmv.totalCashMoneySeries, label="cash-money", color=myColor1)
    ax1g.tick_params(axis='y', labelcolor=myColor1)
    
    ax2g = ax1g.twinx()  # instantiate a second axes that shares the same x-axis
    ax2g.set_ylim([0, max(0.01,max(cmv.totalCashMoneyInfraVarSeries))])
    ax2g.plot(t, cmv.totalCashMoneyInfraVarSeries, label="cash-moneyInVar", color=myColor2)
    ax2g.tick_params(axis='y', labelcolor=myColor2)
    fig7.legend()
    
def plot8():
    # https://matplotlib.org/3.5.1/gallery/subplots_axes_and_figures/two_scales.html
    # https://matplotlib.org/3.5.1/tutorials/colors/colors.html
    myColor1 = 'tab:orange'
    myColor2 = 'tab:blue'
    fig8, ax1h = plt.subplots()
    ax1h.set_ylim([min(-0.01, min(cmv.totalCheckingAccountSeries)), \
                   max(0.01,max(cmv.totalCheckingAccountSeries))])
    t=range(1,cmv.ncycles+1)
    ax1h.plot(t, cmv.totalCheckingAccountSeries, label="checking-account", color=myColor1)
    ax1h.tick_params(axis='y', labelcolor=myColor1)
    
    ax2h = ax1h.twinx()  # instantiate a second axes that shares the same x-axis
    ax2h.set_ylim([0, max(0.01,max(cmv.totalCheckingAccountInfraVarSeries))])
    ax2h.plot(t, cmv.totalCheckingAccountInfraVarSeries, label="checking-accountInVar", color=myColor2)
    ax2h.tick_params(axis='y', labelcolor=myColor2)
    fig8.legend()
    
def plot9():
    # https://matplotlib.org/3.5.1/gallery/subplots_axes_and_figures/two_scales.html
    # https://matplotlib.org/3.5.1/tutorials/colors/colors.html
    myColor1 = 'tab:orange'
    myColor2 = 'tab:blue'
    fig9, ax1i = plt.subplots()
    ax1i.set_ylim([min(-0.01, min(cmv.totalBankAccountSeries)), \
                   max(0.01,max(cmv.totalBankAccountSeries))])
    t=range(1,cmv.ncycles+1)
    ax1i.plot(t, cmv.totalBankAccountSeries, label="checking-account", color=myColor1)
    ax1i.tick_params(axis='y', labelcolor=myColor1)
    
    ax2i = ax1i.twinx()  # instantiate a second axes that shares the same x-axis
    ax2i.set_ylim([0, max(0.01,max(cmv.totalBankAccountInfraVarSeries))])
    ax2i.plot(t, cmv.totalBankAccountInfraVarSeries, label="checking-accountInVar", color=myColor2)
    ax2i.tick_params(axis='y', labelcolor=myColor2)
    fig9.legend()
    
def nationalAccounts():
    print("-------------------------------------------\n"+\
          '"national" accounts'+\
          "\n-------------------------------------------\n")
    print("%s\t%s\t%s\t%s\t\t%s\t%s\t%s" % \
          ("t","total","lost","initial","consum.","invest.","final"))
    print("\t%s\t%s\t%s\t\t\t\t%s" % ("produc.","produc.","invent.","invent."))
    for i in range(cmv.ncycles):
        print("%3d\t%.1f\t%.1f\t%.1f\t    |\t%.1f\t%.1f\t%.1f" % \
                                   (i+1,cmv.totalProductionSeries[i],
                                   -cmv.totalLostProductionSeries[i],\
                                   cmv.totalInitialInventoriesSeries[i],\
                                   cmv.totalConsumptionSeries[i],\
                                   cmv.totalInvestmentSeries[i],\
                                   cmv.totalFinalInventoriesSeries[i]))
        
    print("\n\n\n")