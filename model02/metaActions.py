import commonVar as cmv
#import random as r
from tools import *

def produceAll():
    # no seedManager()
    cmv.totalProductionSeries.append(0)
    cmv.totalProductionInfraVarSeries.append(0)
    cmv.totalInitialInventoriesSeries.append(0)
    cmv.totalInitialInventoriesInfraVarSeries.append(0)

    for aFirm in cmv.firmList:
        aFirm.produce()
        cmv.totalProductionSeries[-1]+=aFirm.production
        cmv.totalProductionInfraVarSeries[-1]+=aFirm.production**2
        cmv.totalInitialInventoriesSeries[-1]+=aFirm.initialInventories
        cmv.totalInitialInventoriesInfraVarSeries[-1]+=aFirm.initialInventories**2

    cmv.totalProductionInfraVarSeries[-1]=\
                            (cmv.totalProductionInfraVarSeries[-1]/cmv.firmNum - \
                            (cmv.totalProductionSeries[-1]/cmv.firmNum)**2)
    cmv.totalInitialInventoriesInfraVarSeries[-1]=\
                            (cmv.totalInitialInventoriesInfraVarSeries[-1]/cmv.firmNum - \
                            (cmv.totalInitialInventoriesSeries[-1]/cmv.firmNum)**2)
                                          

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
    
    for aBank in cmv.bankList:
        aBank.computeAndApplyInterests()


def makeBankFinancialAccountsAll():
    # no seedManager()
    
    for aBank in cmv.bankList:
        aBank.makeFinancialAccounts()
        

def makeBalanceSheetAll():
    # no seedManager()
    cmv.totalProfitSeries.append(0)
    cmv.totalProfitInfraVarSeries.append(0)
    cmv.totalFinalInventoriesSeries.append(0)
    cmv.totalFinalInventoriesInfraVarSeries.append(0)
    cmv.totalLostProductionSeries.append(0)
    
    for aFirm in cmv.firmList:
        aFirm.makeBalanceSheet()
        cmv.totalProfitSeries[-1]+=aFirm.profit
        cmv.totalProfitInfraVarSeries[-1]+=aFirm.profit**2
        cmv.totalFinalInventoriesSeries[-1]+=aFirm.finalInventories
        cmv.totalFinalInventoriesInfraVarSeries[-1]+=aFirm.finalInventories**2
        cmv.totalLostProductionSeries[-1]+=aFirm.lostProduction

    cmv.totalProfitInfraVarSeries[-1]=(cmv.totalProfitInfraVarSeries[-1]/cmv.firmNum - \
                                          (cmv.totalProfitSeries[-1]/cmv.firmNum)**2)
    cmv.totalFinalInventoriesInfraVarSeries[-1]=\
                            (cmv.totalFinalInventoriesInfraVarSeries[-1]/cmv.firmNum - \
                            (cmv.totalFinalInventoriesSeries[-1]/cmv.firmNum)**2)
                                            

def distributeDividendAll():
    # no seedManager()
    for aFirm in cmv.firmList:
        aFirm.distributeDividend()