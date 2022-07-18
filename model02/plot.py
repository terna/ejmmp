import matplotlib.pyplot as plt
import commonVar as cmv

def plot(y1lim,y1values,y11abel,y2lim,y2values,y2label,myTitle):
    # https://matplotlib.org/3.5.1/gallery/subplots_axes_and_figures/two_scales.html
    # https://matplotlib.org/3.5.1/tutorials/colors/colors.html
    myColor0 = 'tab:green'
    myColor1 = 'tab:orange'
    myColor2 = 'tab:blue'
    fig, ax1 = plt.subplots()
    fig.suptitle(myTitle,fontsize=16)
    ax1.set_ylim(y1lim)
    t=range(1,cmv.ncycles+1)
    ax1.plot(t, y1values, label=y11abel, color=myColor1)
    ax1.tick_params(axis='y', labelcolor=myColor1)
    ax1.plot([1,cmv.ncycles],[0,0], label="zero line", color=myColor0, linestyle='dashed')

    
    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
    ax2.set_ylim(y2lim)
    ax2.plot(t, y2values, label=y2label, color=myColor2)
    ax2.tick_params(axis='y', labelcolor=myColor2)
    fig.legend()
    plt.show()

def plotOneSeries(y1lim,y1values,y11abel,myTitle):
    # https://matplotlib.org/3.5.1/gallery/subplots_axes_and_figures/two_scales.html
    # https://matplotlib.org/3.5.1/tutorials/colors/colors.html
    myColor0 = 'tab:green'
    myColor1 = 'tab:orange'
    fig, ax1 = plt.subplots()
    fig.suptitle(myTitle,fontsize=16)
    ax1.set_ylim(y1lim)
    t=range(1,cmv.ncycles+1)
    ax1.plot(t, y1values, label=y11abel, color=myColor1)
    ax1.tick_params(axis='y', labelcolor=myColor1)
    ax1.plot([1,cmv.ncycles],[0,0], label="zero line", color=myColor0, linestyle='dashed')
    fig.legend()
    plt.show()

def makePlots():
    plot([0,max(cmv.totalAddedValueSeries)],cmv.totalAddedValueSeries,"added-value",\
     [0, max(cmv.totalAddedValueInfraVarSeries)],\
     cmv.totalAddedValueInfraVarSeries,"added-valInVar"," ")

    plot([0,max(cmv.totalProductionSeries)],cmv.totalProductionSeries,"production",\
     [0, max(cmv.totalProductionInfraVarSeries)],\
     cmv.totalProductionInfraVarSeries,"prodInVar"," ")

    plot([min(cmv.totalProfitSeries), max(0,max(cmv.totalProfitSeries))],\
     cmv.totalProfitSeries,"profit",\
     [0, max(cmv.totalProfitInfraVarSeries)],\
     cmv.totalProfitInfraVarSeries,"profInVar"," ")

    plot([min(cmv.totalFirmProfitSeries), max(0,max(cmv.totalFirmProfitSeries))],\
     cmv.totalFirmProfitSeries,"firmProfit",\
     [0, max(cmv.totalFirmProfitInfraVarSeries)],\
     cmv.totalFirmProfitInfraVarSeries,"firmProfInVar"," ")

    plot([min(cmv.totalBankProfitSeries), max(0,max(cmv.totalBankProfitSeries))],\
     cmv.totalBankProfitSeries,"bankProfit",\
     [0, max(cmv.totalBankProfitInfraVarSeries)],\
     cmv.totalBankProfitInfraVarSeries,"bankProfInVar"," ")

    plot([min(cmv.totalInitialInventoriesSeries), \
      max(0.01,max(cmv.totalInitialInventoriesSeries))],\
     cmv.totalInitialInventoriesSeries,"initialInventories",\
     [0, max(0.01,max(cmv.totalInitialInventoriesInfraVarSeries))],\
     cmv.totalInitialInventoriesInfraVarSeries,"initialInventoriesInVar"," ")

    plot([min(cmv.totalFinalInventoriesSeries), \
      max(0.01,max(cmv.totalFinalInventoriesSeries))],\
     cmv.totalFinalInventoriesSeries,"finalInventories",\
     [0, max(0.01,max(cmv.totalFinalInventoriesInfraVarSeries))],\
     cmv.totalFinalInventoriesInfraVarSeries,"finalInventoriesInVar"," ")

    plot([0, max(cmv.totalConsumptionSeries)],cmv.totalConsumptionSeries,"consumption",\
     [0, max(cmv.totalConsumptionInfraVarSeries)],\
     cmv.totalConsumptionInfraVarSeries,"consInVar"," ")

    plot([0, max(cmv.totalInvestmentSeries)],cmv.totalInvestmentSeries,"investment",\
     [0, max(cmv.totalInvestmentInfraVarSeries)],\
     cmv.totalInvestmentInfraVarSeries,"investiInVar"," ")

    #plot([min(-0.01, min(cmv.totalCashMoneySeries)),max(0.01,max(cmv.totalCashMoneySeries))],\
     #cmv.totalCashMoneySeries,"cash-money",\
     #[0, max(0.01,max(cmv.totalCashMoneyInfraVarSeries))],\
     #cmv.totalCashMoneyInfraVarSeries,"cash-moneyInVar")

    plot([min(-0.01, min(cmv.totalCheckingAccountSeries)),\
      max(0.01,max(cmv.totalCheckingAccountSeries))],\
     cmv.totalCheckingAccountSeries,"checking-account",\
     [0, max(0.01,max(cmv.totalCheckingAccountInfraVarSeries))],\
     cmv.totalCheckingAccountInfraVarSeries,\
     "checking-accountInVar"," ")

    plot([min(-0.01, min(cmv.totalBankAccountSeries)),max(0.01,max(cmv.totalBankAccountSeries))],\
     cmv.totalBankAccountSeries,"bank-account",\
     [0, max(0.01,max(cmv.totalBankAccountInfraVarSeries))],\
     cmv.totalBankAccountInfraVarSeries,\
     "bank-accountInVar"," ")

    plot([min(-0.01, min(cmv.privateClientsTotalInterestOnDepositsSeries)),\
      max(0.01,max(cmv.privateClientsTotalInterestOnDepositsSeries))],\
     cmv.privateClientsTotalInterestOnDepositsSeries,"private-clients-intOnDep",\
     [0, max(0.01,max(cmv.privateClientsTotalInterestOnDepositsInfraVarSeries))],\
     cmv.privateClientsTotalInterestOnDepositsInfraVarSeries,\
     "private-clients-intOnDepInVar"," ")

    plot([min(-0.01, min(cmv.privateClientsTotalInterestOnLoansSeries)),\
      max(0.01,max(cmv.privateClientsTotalInterestOnLoansSeries))],\
     cmv.privateClientsTotalInterestOnLoansSeries,"private-clients-intOnLoans",\
     [0, max(0.01,max(cmv.privateClientsTotalInterestOnLoansInfraVarSeries))],\
     cmv.privateClientsTotalInterestOnLoansInfraVarSeries,\
     "private-clients-intOnLoansInVar"," ")

    plot([min(-0.01, min(cmv.commercialClientsTotalInterestOnDepositsSeries)),\
      max(0.01,max(cmv.commercialClientsTotalInterestOnDepositsSeries))],\
     cmv.commercialClientsTotalInterestOnDepositsSeries,"commercial-clients-intOnDep",\
     [0, max(0.01,max(cmv.commercialClientsTotalInterestOnDepositsInfraVarSeries))],\
     cmv.commercialClientsTotalInterestOnDepositsInfraVarSeries,\
     "commercial-clients-intOnDepInVar"," ")

    plot([min(-0.01, min(cmv.commercialClientsTotalInterestOnLoansSeries)),\
      max(0.01,max(cmv.commercialClientsTotalInterestOnLoansSeries))],\
     cmv.commercialClientsTotalInterestOnLoansSeries,"commercial-clients-intOnLoans",\
     [0, max(0.01,max(cmv.commercialClientsTotalInterestOnLoansInfraVarSeries))],\
     cmv.commercialClientsTotalInterestOnLoansInfraVarSeries,\
     "commercial-clients-intOnLoansInVar"," ")
    
    plot([min(-0.01, min(cmv.totalDebtsVsAgentsSeries)),\
      max(0.01,max(cmv.totalDebtsVsAgentsSeries))],\
     cmv.totalDebtsVsAgentsSeries,"debt-vs-agents",\
     [0, max(0.01,max(cmv.totalDebtsVsAgentsInfraVarSeries))],\
     cmv.totalDebtsVsAgentsInfraVarSeries,\
     "debt-vs-agentsInVar"," ")

    plot([min(-0.01, min(cmv.totalCreditsVsAgentsSeries)),\
      max(0.01,max(cmv.totalCreditsVsAgentsSeries))],\
     cmv.totalCreditsVsAgentsSeries,"credit-vs-agents",\
     [0, max(0.01,max(cmv.totalCreditsVsAgentsInfraVarSeries))],\
     cmv.totalCreditsVsAgentsInfraVarSeries,\
     "credit-vs-agentsInVar"," ")

    plot([min(-0.01, min(cmv.totalDebtsVsFirmsSeries)),\
      max(0.01,max(cmv.totalDebtsVsFirmsSeries))],\
     cmv.totalDebtsVsFirmsSeries,"debt-vs-firms",\
     [0, max(0.01,max(cmv.totalDebtsVsFirmsInfraVarSeries))],\
     cmv.totalDebtsVsFirmsInfraVarSeries,\
     "debt-vs-firmsInVar"," ")

    plot([min(-0.01, min(cmv.totalCreditsVsFirmsSeries)),\
      max(0.01,max(cmv.totalCreditsVsFirmsSeries))],\
     cmv.totalCreditsVsFirmsSeries,"credit-vs-firms",\
     [0, max(0.01,max(cmv.totalCreditsVsFirmsInfraVarSeries))],\
     cmv.totalCreditsVsFirmsInfraVarSeries,\
     "credit-vs-firmsInVar"," ")

    plot([min(-0.01, min(cmv.totalCentralBankAccountSeries)),\
      max(0.01,1.1*max(cmv.totalCentralBankAccountSeries))],\
     cmv.totalCentralBankAccountSeries,"bank-accounts-at-CB",\
     [0, max(0.01,max(cmv.totalCentralBankAccountInfraVarSeries))],\
     cmv.totalCentralBankAccountInfraVarSeries,\
     "bank-accounts-at-CB-InVar"," ")

    
    plot([min(-0.01, min(cmv.totalBankTreasuryAccountAtCentralBankSeries)),\
      max(0.01,1.1*max(cmv.totalBankTreasuryAccountAtCentralBankSeries))],\
     cmv.totalBankTreasuryAccountAtCentralBankSeries,"bank-treasury-acc-at-CB",\
     [0, max(0.01,max(cmv.totalBankTreasuryAccountAtCentralBankInfraVarSeries))],\
     cmv.totalBankTreasuryAccountAtCentralBankInfraVarSeries,\
     "bank-treasury-acc-at-CB-InVar"," ")
    
    M1=[]
    for ii in range(cmv.ncycles):
        M1.append(cmv.totalDebtsVsAgentsSeries[ii]+cmv.totalDebtsVsFirmsSeries[ii])
    
    plotOneSeries([min(-0.01, min(M1)),\
      max(0.01,max(M1))],\
     M1,"M1",\
     myTitle="M1 creation")

