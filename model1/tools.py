import matplotlib.pyplot as plt
import commonVar as cmv

def makeHist():
    print("-------------------------------------------\n"+\
          "employer number "+ str(len(cmv.employerList))+\
          "\n-------------------------------------------\n")
    cmv.employerSizeList=[]
    list(cmv.employerSizeList.append(cmv.employerList[i].num) \
                                for i in range(len(cmv.employerList)))
    #print(cmv.employerSizeList)

    plt.hist(cmv.employerSizeList,20,facecolor='orange')
    plt.xlabel("# of employees")
    plt.ylabel("# of employeers")
    plt.title("Distribution of the employers by number of employees")      


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
    ax1g.set_ylim([min(0, min(cmv.totalCashMoneySeries)), max(cmv.totalCashMoneySeries)])
    t=range(1,cmv.ncycles+1)
    ax1g.plot(t, cmv.totalCashMoneySeries, label="cash-money", color=myColor1)
    ax1g.tick_params(axis='y', labelcolor=myColor1)
    
    ax2g = ax1g.twinx()  # instantiate a second axes that shares the same x-axis
    ax2g.set_ylim([0, max(cmv.totalCashMoneyInfraVarSeries)])
    ax2g.plot(t, cmv.totalCashMoneyInfraVarSeries, label="cash-moneyInVar", color=myColor2)
    ax2g.tick_params(axis='y', labelcolor=myColor2)
    fig7.legend()
    

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