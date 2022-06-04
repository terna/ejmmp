import commonVar as cmv
#import random as r
from tools import *

def produceAll():
    # no seedManager()
    cmv.totalProductionSeries.append(0)
    cmv.totalProductionInfraVarSeries.append(0)
    cmv.totalInitialInventoriesSeries.append(0)
    cmv.totalInitialInventoriesInfraVarSeries.append(0)

    for anItem in cmv.firmList+cmv.bankList:
        anItem.produce()
        cmv.totalProductionSeries[-1]+=anItem.production
        cmv.totalProductionInfraVarSeries[-1]+=anItem.production**2
        cmv.totalInitialInventoriesSeries[-1]+=anItem.initialInventories
        cmv.totalInitialInventoriesInfraVarSeries[-1]+=anItem.initialInventories**2

    cmv.totalProductionInfraVarSeries[-1]=\
                            (cmv.totalProductionInfraVarSeries[-1]/(cmv.firmNum+cmv.bankNum) - \
                            (cmv.totalProductionSeries[-1]/(cmv.firmNum+cmv.bankNum))**2)
    cmv.totalInitialInventoriesInfraVarSeries[-1]=\
                            (cmv.totalInitialInventoriesInfraVarSeries[-1]/(cmv.firmNum+cmv.bankNum) - \
                            (cmv.totalInitialInventoriesSeries[-1]/(cmv.firmNum+cmv.bankNum))**2)
                                          

def payWagesAll():
    # no seedManager
    for anItem in cmv.firmList+cmv.bankList:
        anItem.payWages()


def buyConsumptionGoodsAll(r,seed):
    seedManager(r,seed,"buyConsumptionGoodsAll",buyConsumptionGoodsAll)
    cmv.totalEntrepreneurConsumptionSeries.append(0) 
    cmv.totalNonEntrepreneurConsumptionSeries.append(0)
    cmv.totalConsumptionSeries.append(0)
    cmv.totalConsumptionInfraVarSeries.append(0)
    for k in range(cmv.nOfConsumptionActions):
        buyConsumptionGoodsAll.r.shuffle(cmv.agentList)
        for anAgent in cmv.agentList:
            anAgent.buyConsumptionGoods(k)
            if k==cmv.nOfConsumptionActions-1:
                if anAgent.entrepreneur:
                    cmv.totalEntrepreneurConsumptionSeries[-1]+=anAgent.madeConsumption
                if not anAgent.entrepreneur:
                    cmv.totalNonEntrepreneurConsumptionSeries[-1]+=anAgent.madeConsumption
                cmv.totalConsumptionSeries[-1]+=anAgent.madeConsumption
                cmv.totalConsumptionInfraVarSeries[-1]+=anAgent.madeConsumption**2

    cmv.totalConsumptionInfraVarSeries[-1]=\
                              (cmv.totalConsumptionInfraVarSeries[-1]/cmv.agentNum - \
                              (cmv.totalConsumptionSeries[-1]/cmv.agentNum)**2)
                

def buyInvestmentGoodsAll(r,seed):
    seedManager(r,seed,"buyInvestmentGoodsAll",buyInvestmentGoodsAll)
    cmv.totalInvestmentSeries.append(0)
    cmv.totalInvestmentInfraVarSeries.append(0)
    for k in range(cmv.nOfInvestmentActions):
        firm_bankSafeList=cmv.firmList+cmv.bankList # safe copy without the shuffles in 
                                                    # buyInvestmentGoods
        buyInvestmentGoodsAll.r.shuffle(firm_bankSafeList)
        for anItem in firm_bankSafeList:
            anItem.buyInvestmentGoods(k)
            if k==cmv.nOfInvestmentActions-1:
                cmv.totalInvestmentSeries[-1]+=anItem.madeInvestment
                cmv.totalInvestmentInfraVarSeries[-1]+=anItem.madeInvestment**2

    cmv.totalInvestmentInfraVarSeries[-1]=\
                              (cmv.totalInvestmentInfraVarSeries[-1]/(cmv.firmNum+cmv.bankNum) - \
                              (cmv.totalInvestmentSeries[-1]/(cmv.firmNum+cmv.bankNum))**2)
                

def buyConsumptionOrInvestmentGoodsAll(r,seed):
    seedManager(r,seed,"buyConsumptionOrInvestmentGoodsAll",buyConsumptionOrInvestmentGoodsAll)

    agent_Firm_BankList=cmv.agentList+cmv.firmList+cmv.bankList

    cmv.totalEntrepreneurConsumptionSeries.append(0) 
    cmv.totalNonEntrepreneurConsumptionSeries.append(0)
    cmv.totalConsumptionSeries.append(0)
    cmv.totalConsumptionInfraVarSeries.append(0)
    cmv.totalInvestmentSeries.append(0)
    cmv.totalInvestmentInfraVarSeries.append(0)

    repetitions=max(cmv.nOfConsumptionActions,cmv.nOfInvestmentActions)

    for k in range(repetitions):
        buyConsumptionOrInvestmentGoodsAll.r.shuffle(agent_Firm_BankList)
        for anItem in agent_Firm_BankList:
            if anItem.__class__.__name__=="Agent" and\
            k < cmv.nOfConsumptionActions - 1: anItem.buyConsumptionGoods(k)
            if anItem.__class__.__name__ in ["Firm","Bank"] and\
            k < cmv.nOfInvestmentActions - 1:  anItem.buyInvestmentGoods(k)

            if k==cmv.nOfConsumptionActions-1 and anItem.__class__.__name__=="Agent":
                if anItem.entrepreneur:
                    cmv.totalEntrepreneurConsumptionSeries[-1]+=anItem.madeConsumption
                if not anItem.entrepreneur:
                    cmv.totalNonEntrepreneurConsumptionSeries[-1]+=anItem.madeConsumption
                cmv.totalConsumptionSeries[-1]+=anItem.madeConsumption
                cmv.totalConsumptionInfraVarSeries[-1]+=anItem.madeConsumption**2

            if k==cmv.nOfInvestmentActions-1 and anItem.__class__.__name__ in ["Firm","Bank"]:
                cmv.totalInvestmentSeries[-1]+=anItem.madeInvestment
                cmv.totalInvestmentInfraVarSeries[-1]+=anItem.madeInvestment**2

    cmv.totalConsumptionInfraVarSeries[-1]=\
                              (cmv.totalConsumptionInfraVarSeries[-1]/cmv.agentNum - \
                              (cmv.totalConsumptionSeries[-1]/cmv.agentNum)**2)
 
    cmv.totalInvestmentInfraVarSeries[-1]=\
                              (cmv.totalInvestmentInfraVarSeries[-1]/(cmv.firmNum+cmv.bankNum) - \
                              (cmv.totalInvestmentSeries[-1]/(cmv.firmNum+cmv.bankNum))**2)


def accountCashMoneyAll():
    # no seedManager()
    cmv.totalCashMoneySeries.append(0)
    cmv.totalCashMoneyInfraVarSeries.append(0)
    for anAgent in cmv.agentList:
        cmv.totalCashMoneySeries[-1]+=anAgent.cashMoney
        cmv.totalCashMoneyInfraVarSeries[-1]+=anAgent.cashMoney**2

    cmv.totalCashMoneyInfraVarSeries[-1]=\
                              (cmv.totalCashMoneyInfraVarSeries[-1]/cmv.agentNum - \
                              (cmv.totalCashMoneySeries[-1]/cmv.agentNum)**2)
    if abs(cmv.totalCashMoneySeries[-1])<0.00001: \
        cmv.totalCashMoneySeries[-1]=0


def accountCheckingAccountAll():
    # no seedManager()
    cmv.totalCheckingAccountSeries.append(0)
    cmv.totalCheckingAccountInfraVarSeries.append(0)
    for anAgent in cmv.agentList:
        cmv.totalCheckingAccountSeries[-1]+=anAgent.checkingAccount
        cmv.totalCheckingAccountInfraVarSeries[-1]+=anAgent.checkingAccount**2

    cmv.totalCheckingAccountInfraVarSeries[-1]=\
                              (cmv.totalCheckingAccountInfraVarSeries[-1]/cmv.agentNum - \
                              (cmv.totalCheckingAccountSeries[-1]/cmv.agentNum)**2)
    if abs(cmv.totalCheckingAccountSeries[-1])<0.00001: \
        cmv.totalCheckingAccountSeries[-1]=0


def accountBankAccountAll(): #temporary - this is an attribute of firms
    # no seedManager()
    cmv.totalBankAccountSeries.append(0)
    cmv.totalBankAccountInfraVarSeries.append(0)
    for aFirm in cmv.firmList:
        cmv.totalBankAccountSeries[-1]+=aFirm.bankAccount
        cmv.totalBankAccountInfraVarSeries[-1]+=aFirm.bankAccount**2

    cmv.totalBankAccountInfraVarSeries[-1]=\
                              (cmv.totalBankAccountInfraVarSeries[-1]/cmv.firmNum - \
                              (cmv.totalBankAccountSeries[-1]/cmv.firmNum)**2)
    if abs(cmv.totalBankAccountSeries[-1])<0.00001: \
        cmv.totalBankAccountSeries[-1]=0


def computeAndApplyInterestsAll():
    # no seedManager()
    cmv.privateClientsTotalInterestOnDepositsSeries.append(0)
    cmv.privateClientsTotalInterestOnLoansSeries.append(0)
    cmv.commercialClientsTotalInterestOnDepositsSeries.append(0)
    cmv.commercialClientsTotalInterestOnLoansSeries.append(0)
    cmv.privateClientsTotalInterestOnDepositsInfraVarSeries.append(0)
    cmv.privateClientsTotalInterestOnLoansInfraVarSeries.append(0)
    cmv.commercialClientsTotalInterestOnDepositsInfraVarSeries.append(0)
    cmv.commercialClientsTotalInterestOnLoansInfraVarSeries.append(0)
    
    for aBank in cmv.bankList:
        aBank.computeAndApplyInterests()
        cmv.privateClientsTotalInterestOnDepositsSeries[-1]+=\
                          aBank.myPrivateClientsTotalInterestOnDeposits
        cmv.privateClientsTotalInterestOnDepositsInfraVarSeries[-1]+=\
                          aBank.myPrivateClientsTotalInterestOnDeposits**2
        cmv.privateClientsTotalInterestOnLoansSeries[-1]+=\
                          aBank.myPrivateClientsTotalInterestOnLoans
        cmv.privateClientsTotalInterestOnLoansInfraVarSeries[-1]+=\
                          aBank.myPrivateClientsTotalInterestOnLoans**2
        cmv.commercialClientsTotalInterestOnDepositsSeries[-1]+=\
                          aBank.myCommercialClientsTotalInterestOnDeposits
        cmv.commercialClientsTotalInterestOnDepositsInfraVarSeries[-1]+=\
                          aBank.myCommercialClientsTotalInterestOnDeposits**2
        cmv.commercialClientsTotalInterestOnLoansSeries[-1]+=\
                          aBank.myCommercialClientsTotalInterestOnLoans
        cmv.commercialClientsTotalInterestOnLoansInfraVarSeries[-1]+=\
                          aBank.myCommercialClientsTotalInterestOnLoans**2

    cmv.privateClientsTotalInterestOnDepositsInfraVarSeries[-1]=\
               (cmv.privateClientsTotalInterestOnDepositsInfraVarSeries[-1]/cmv.bankNum - \
               (cmv.privateClientsTotalInterestOnDepositsSeries[-1]/cmv.bankNum)**2)
    cmv.privateClientsTotalInterestOnLoansInfraVarSeries[-1]=\
               (cmv.privateClientsTotalInterestOnLoansInfraVarSeries[-1]/cmv.bankNum - \
               (cmv.privateClientsTotalInterestOnLoansSeries[-1]/cmv.bankNum)**2)
    cmv.commercialClientsTotalInterestOnDepositsInfraVarSeries[-1]=\
               (cmv.commercialClientsTotalInterestOnDepositsInfraVarSeries[-1]/cmv.bankNum - \
               (cmv.commercialClientsTotalInterestOnDepositsSeries[-1]/cmv.bankNum)**2)
    cmv.commercialClientsTotalInterestOnLoansInfraVarSeries[-1]=\
               (cmv.commercialClientsTotalInterestOnLoansInfraVarSeries[-1]/cmv.bankNum - \
               (cmv.commercialClientsTotalInterestOnLoansSeries[-1]/cmv.bankNum)**2)


def makeBankFinancialAccountsAll():
    # no seedManager()
    cmv.totalDebtsVsAgentsSeries.append(0)
    cmv.totalCreditsVsAgentsSeries.append(0)
    cmv.totalDebtsVsFirmsSeries.append(0)
    cmv.totalCreditsVsFirmsSeries.append(0)
    cmv.totalDebtsVsAgentsInfraVarSeries.append(0)
    cmv.totalCreditsVsAgentsInfraVarSeries.append(0)
    cmv.totalDebtsVsFirmsInfraVarSeries.append(0)
    cmv.totalCreditsVsFirmsInfraVarSeries.append(0)
    
    for aBank in cmv.bankList:
        aBank.makeFinancialAccounts()
        cmv.totalDebtsVsAgentsSeries[-1]+=aBank.myDebtsVsAgents
        cmv.totalDebtsVsAgentsInfraVarSeries[-1]+=aBank.myDebtsVsAgents**2
        cmv.totalCreditsVsAgentsSeries[-1]+=aBank.myCreditsVsAgents
        cmv.totalCreditsVsAgentsInfraVarSeries[-1]+=aBank.myCreditsVsAgents**2
        cmv.totalDebtsVsFirmsSeries[-1]+=aBank.myDebtsVsFirms
        cmv.totalDebtsVsFirmsInfraVarSeries[-1]+=aBank.myDebtsVsFirms**2
        cmv.totalCreditsVsFirmsSeries[-1]+=aBank.myCreditsVsFirms
        cmv.totalCreditsVsFirmsInfraVarSeries[-1]+=aBank.myCreditsVsFirms**2

def makeBalanceSheetAll():
    # no seedManager()
    cmv.totalProfitSeries.append(0)
    cmv.totalProfitInfraVarSeries.append(0)
    cmv.totalFinalInventoriesSeries.append(0)
    cmv.totalFinalInventoriesInfraVarSeries.append(0)
    cmv.totalLostProductionSeries.append(0)
    cmv.totalAddedValueSeries.append(0)
    cmv.totalAddedValueInfraVarSeries.append(0)
    
    for anItem in cmv.firmList+cmv.bankList:
        anItem.makeBalanceSheet()
        cmv.totalProfitSeries[-1]+=anItem.profit
        cmv.totalProfitInfraVarSeries[-1]+=anItem.profit**2
        cmv.totalFinalInventoriesSeries[-1]+=anItem.finalInventories
        cmv.totalFinalInventoriesInfraVarSeries[-1]+=anItem.finalInventories**2
        cmv.totalLostProductionSeries[-1]+=anItem.lostProduction
        cmv.totalAddedValueSeries[-1]+=anItem.addedValue
        cmv.totalAddedValueInfraVarSeries[-1]+=anItem.addedValue**2
        
    cmv.totalProfitInfraVarSeries[-1]=(cmv.totalProfitInfraVarSeries[-1]/(cmv.firmNum+cmv.bankNum) - \
                                          (cmv.totalProfitSeries[-1]/(cmv.firmNum+cmv.bankNum))**2)
    cmv.totalFinalInventoriesInfraVarSeries[-1]=\
                            (cmv.totalFinalInventoriesInfraVarSeries[-1]/(cmv.firmNum+cmv.bankNum) - \
                            (cmv.totalFinalInventoriesSeries[-1]/(cmv.firmNum+cmv.bankNum))**2)
    cmv.totalAddedValueInfraVarSeries[-1]=(cmv.totalAddedValueInfraVarSeries[-1]/\
                                          (cmv.firmNum+cmv.bankNum) - \
                                          (cmv.totalAddedValueSeries[-1]/(cmv.firmNum+cmv.bankNum))**2)
                                            

def distributeDividendAll():
    # no seedManager()
    for anItem in cmv.firmList+cmv.bankList:
        anItem.distributeDividend()