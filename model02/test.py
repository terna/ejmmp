# https://stackoverflow.com/questions/46820900/display-output-from-another-python-script-in-jupyter-notebookimport tabulate as tb

# The -i tells Python to run the file in IPython's name space, thus the script knows about all your variables

# use with
# %run -i test


import tabulate as tb

print("\nLast cycle test\n")
##########################################################################
print("\n\nAGENTS\n\n")


print("\nReconciliation of agents' financial accounts\n")

if cmv.cycle==0: totAgentDepositsPreviousCycle=0
else: totAgentDepositsPreviousCycle=cmv.totalDebtsVsAgentsSeries[-2]

if cmv.cycle==0: totAgentLoansPreviousCycle=0
else: totAgentLoansPreviousCycle=cmv.totalCreditsVsAgentsSeries[-2]
    
totWorkers=0
totFirmBankDividend=0
for anItem in (cmv.firmList+cmv.bankList):
    totWorkers+=len(anItem.myWorkers)
    if anItem.profit>0: totFirmBankDividend+=anItem.profit/2


data = [[" "," ","cycle "+str(cmv.cycle+1), " "],\
        ["(1)","agents' Deposits Previous Cycle",totAgentDepositsPreviousCycle,"bank stock (-)"],
        ["(2)","agents' Deposits Current Cycle (with current interests)",cmv.totalCheckingAccountSeries[-1],"bank stock (+)"],\
        ["(3)","agents' Loans Previous Cycle",totAgentLoansPreviousCycle,       "bank stock (+)"],\
        ["(4)","agents' Loans Current Cycle (with current interests)",cmv.totalCreditsVsAgentsSeries[-1],    "bank stock (-)"],\
        ["(5)","agents' Wages Current Cycle",cmv.wage*totWorkers,                 "bank flow (+)"],\
        ["(6)","agents' Consumption Current Cycle",cmv.totalConsumptionSeries[-1],"bank flow (-)"],\
        ["(7)","agents' Perceived Dividends Current Cycle",totFirmBankDividend,   "bank flow (+)"],\
        ["(8)","agents' Interests On Deposits Current Cycle",cmv.privateClientsTotalInterestOnDepositsSeries[-1],\
                                                                                 "bank flow (+)"],\
        ["(9)","agents' Interests On Loans Current Cycle",cmv.privateClientsTotalInterestOnLoansSeries[-1],\
                                                                                  "bank flow (-)"]]

table = tb.tabulate(data, tablefmt='grid',headers="firstrow")
print(table)

print("\nReconciliation\n")
print("\n- (1) + (2) + (3) - (4)       => ",round(\
                                      -totAgentDepositsPreviousCycle\
                                      +cmv.totalCheckingAccountSeries[-1]\
                                      +cmv.totalCreditsVsAgentsSeries[-1]\
                                      -cmv.totalCreditsVsAgentsSeries[-1],4))

print("\n+ (5) - (6) + (7) + (8) - (9) => ",round(\
                                       +cmv.wage*totWorkers\
                                       -cmv.totalConsumptionSeries[-1]\
                                       +totFirmBankDividend\
                                       +cmv.privateClientsTotalInterestOnDepositsSeries[-1]\
                                       -cmv.privateClientsTotalInterestOnLoansSeries[-1],4))




print("___________________________________________________________________________________\n")
##########################################################################

print("\n\nFIRMS\n\n")

data = [["# in\nfirm\nList","num","firm\nInitEn","firm\nWorkers","firm\nProfit\n(firm\nDivid)","firm\nInvest\nment",\
        "firmBank\nAccount\nDeposits","firmBank\nAccount\nLoans","firm\nInt\nOn\nDeposits","firm\nInt\nOn\nLoans"]]
totInitialEndowments=0
totFirmWorkers=0
totFirmDividend=0
totFirmProfit=0
totFirmBankAccountDeposits=0
totFirmBankAccountLoans=0
totFirmInterestOnDeposits=0
totFirmInterestOnLoans=0
totFirmInvestments=0

i=0
for aFirm in cmv.firmList:
    if aFirm.profit>0: firmDividend=aFirm.profit/2
    else: firmDividend=0
    totInitialEndowments+=aFirm.initEn
    firmWorkers=len(aFirm.myWorkers)
    totFirmWorkers+=firmWorkers
    totFirmDividend+=firmDividend
    totFirmProfit+=aFirm.profit
    if aFirm.bankAccount>0: totFirmBankAccountDeposits+=aFirm.bankAccount
    if aFirm.bankAccount<0: totFirmBankAccountLoans+=abs(aFirm.bankAccount)
    firmBankAccountDeposits=0
    if aFirm.bankAccount>0: firmBankAccountDeposits=aFirm.bankAccount
    firmBankAccountLoans=0
    if aFirm.bankAccount<0: firmBankAccountLoans=abs(aFirm.bankAccount)
    totFirmInterestOnDeposits+=aFirm.interestOnDeposits
    totFirmInterestOnLoans+=aFirm.interestOnLoans
    totFirmInvestments+=aFirm.madeInvestment

    
    row=[i,aFirm.num,aFirm.initEn,firmWorkers,str(round(aFirm.profit,3))+"\n("+str(round(firmDividend,3))+")",\
         aFirm.madeInvestment,firmBankAccountDeposits,firmBankAccountLoans,\
         aFirm.interestOnDeposits,aFirm.interestOnLoans]
    data.append(row)
    i+=1
    

row  =   ["tot"," ",totInitialEndowments,totFirmWorkers,\
          str(round(totFirmProfit,3))+"\n("+str(round(totFirmDividend,3))+")",totFirmInvestments,\
          totFirmBankAccountDeposits,totFirmBankAccountLoans,totFirmInterestOnDeposits,totFirmInterestOnLoans]

data.append(row)
table = tb.tabulate(data, tablefmt='grid',headers="firstrow",floatfmt=".3f")
print(table)


print("\n\nReconciliation of firms' financial accounts\n\n")

if cmv.cycle==0: totFirmDepositsPreviousCycle=totInitialEndowments
else: totFirmDepositsPreviousCycle=cmv.totalDebtsVsFirmsSeries[-2]

if cmv.cycle==0: totFirmLoansPreviousCycle=0
else: totFirmLoansPreviousCycle=cmv.totalCreditsVsFirmsSeries[-2]
    
totalFirmRevenues=0
for aFirm in cmv.firmList:
    totalFirmRevenues+=aFirm.revenues
    
data = [[" "," ","cycle "+str(cmv.cycle+1), " "],\
        ["(1)","firms' Deposits Previous Cycle",totFirmDepositsPreviousCycle,"bank stock (-)"],
        ["(2)","firms' Deposits Current Cycle (with current interests)",totFirmBankAccountDeposits,\
                                                                       "bank stock (+)"],\
        ["(3)","firms' Loans Previous Cycle",totFirmLoansPreviousCycle,"bank stock (+)"],\
        ["(4)","firms' Loans Current Cycle (with current interests)",totFirmBankAccountLoans,\
                                                                       "bank stock (-)"],\
        ["(5)","firms' Revenues Current Cycle (with interests on deposits)",totalFirmRevenues,"bank flow (+)"],\
        ["(6)","firms' Paid Wages Current Cycle",cmv.wage*totFirmWorkers,"bank flow (-)"],\
        ["(7)","firms' Paid Dividends Current Cycle",totFirmDividend,"bank flow (-)"],\
        ["(8)","firms' Interests On Loans Current Cycle",cmv.commercialClientsTotalInterestOnLoansSeries[-1],\
                                                                                              "bank flow (-)"],\
        ["(9)","firms' Investments",totFirmInvestments,"bank flow (-)"]]


table = tb.tabulate(data, tablefmt='grid',headers="firstrow")
print(table)

print("\nReconciliation\n")
print("\n- (1) + (2) + (3) - (4)       => ",round(-totFirmDepositsPreviousCycle\
                                            +totFirmBankAccountDeposits\
                                            +totFirmLoansPreviousCycle\
                                            -totFirmBankAccountLoans,4))

print("\n+ (5) - (6) - (7) - (8) - (9) => ",round(+totalFirmRevenues\
                                            -cmv.wage*totFirmWorkers\
                                            -totFirmDividend\
                                            -cmv.commercialClientsTotalInterestOnLoansSeries[-1]\
                                            -totFirmInvestments,4),"\n")

print("___________________________________________________________________________________\n")
##########################################################################

print("\n\nBANKS\n\n")

data = [["# in\nbank\nList\n(num)","bank\nInitEn\n(bank\nWorkers)","bank\nProfit\n(bank\nDivid)",\
        "bank\nInvest\nment","myFirm\nBank\nAccount\nDeposits\n(t-1)","myFirm\nBank\nAccount\nLoans\n(t-1)",\
         "myAgent\nChecking\nAccount\nDeposits\n(t-1)","myAgent\nChecking\nAccount\nLoans\n(t-1)",\
         "central\nBank\nBalance"]]

totInitialEndowments=0
totBankWorkers=0
totBankDividend=0
totBankProfit=0
totBankAccountDepositsTminus1=0
totBankAccountDeposits=0
totBankAccountLoansTminus1=0
totBankAccountLoans=0
totCheckingAccountDepositsTminus1=0
totCheckingAccountDeposits=0
totCheckingAccountLoansTminus1=0
totCheckingAccountLoans=0
totBankInvestments=0

i=0
for aBank in cmv.bankList:
    totInitialEndowments+=aBank.initEn
    totBankWorkers+=len(aBank.myWorkers)
    totBankInvestments+=aBank.madeInvestment
    if aBank.profit > 0: dividend=aBank.profit/2
    else: dividend=0
    totBankDividend+=dividend
    totBankProfit+=aBank.profit
    totMyFirmBankAccountDeposits=0
    totMyFirmBankAccountDepositsTminus1=0
    totMyFirmBankAccountLoans=0
    totMyFirmBankAccountLoansTminus1=0
    totMyAgentCheckingAccountDepositsTminus1=0
    totMyAgentCheckingAccountDeposits=0
    totMyAgentCheckingAccountLoansTminus1=0
    totMyAgentCheckingAccountLoans=0
    
    

    for aFirm in aBank.myCommercialClients:
        if aFirm.bankAccountTminus1 > 0: totMyFirmBankAccountDepositsTminus1+=aFirm.bankAccountTminus1
        if aFirm.bankAccount > 0:        totMyFirmBankAccountDeposits       +=aFirm.bankAccount
    totBankAccountDepositsTminus1+=totMyFirmBankAccountDepositsTminus1
    totBankAccountDeposits+=totMyFirmBankAccountDeposits

    for aFirm in aBank.myCommercialClients:
        if aFirm.bankAccountTminus1 < 0: totMyFirmBankAccountLoansTminus1+=abs(aFirm.bankAccountTminus1)
        if aFirm.bankAccount < 0:        totMyFirmBankAccountLoans       +=abs(aFirm.bankAccount)
    totBankAccountLoansTminus1+=totMyFirmBankAccountLoansTminus1
    totBankAccountLoans+=totMyFirmBankAccountLoans
    
    for anAgent in aBank.myPrivateClients:
        if anAgent.checkingAccountTminus1 > 0: totMyAgentCheckingAccountDepositsTminus1+=anAgent.checkingAccountTminus1
        if anAgent.checkingAccount > 0:        totMyAgentCheckingAccountDeposits       +=anAgent.checkingAccount
    totCheckingAccountDepositsTminus1+=totMyAgentCheckingAccountDepositsTminus1
    totCheckingAccountDeposits+=totMyAgentCheckingAccountDeposits
    
    for anAgent in aBank.myPrivateClients:
        if anAgent.checkingAccountTminus1 < 0: totMyAgentCheckingAccountLoansTminus1+=abs(anAgent.checkingAccountTminus1)
        if anAgent.checkingAccount < 0:        totMyAgentCheckingAccountLoans       +=abs(anAgent.checkingAccount)
    totCheckingAccountLoansTminus1+=totMyAgentCheckingAccountLoansTminus1
    totCheckingAccountLoans+=totMyAgentCheckingAccountLoans

    row=[str(i)+"\n("+str(aBank.num)+")",str(round(aBank.initEn,3))+"\n("+str(len(aBank.myWorkers))+")",\
         str(round(aBank.profit,3))+"\n("+str(round(dividend,3))+")",round(aBank.madeInvestment,3),\
         str(round(totMyFirmBankAccountDeposits,3))+"\n"+"("+str(round(totMyFirmBankAccountDepositsTminus1,3))+")",\
         str(round(totMyFirmBankAccountLoans,3))+"\n"+"("+str(round(totMyFirmBankAccountLoansTminus1,3))+")",\
         str(round(totMyAgentCheckingAccountDeposits,3))+"\n"+"("+str(round(totMyAgentCheckingAccountDepositsTminus1,3))+")",\
         str(round(totMyAgentCheckingAccountLoans,3))+"\n"+"("+str(round(totMyAgentCheckingAccountLoansTminus1,3))+")",\
         aBank.centralBankAccount]
    data.append(row)
    i+=1


totCentralBankDepositsPreviousCycle=0
totCentralBankLoansPreviousCycle=0
totCentralBankDeposits=0
totCentralBankLoans=0
totCentralBankBalance=0

for aBank in cmv.bankList:    
    if cmv.cycle==0: 
        totCentralBankDepositsPreviousCycle+=aBank.initEn
        totCentralBankLoansPreviousCycle=+0
    else: 
        if aBank.centralBankAccountTminus1 > 0 :
            totCentralBankDepositsPreviousCycle+=aBank.centralBankAccountTminus1
        if aBank.centralBankAccountTminus1 < 0 :
            totCentralBankLoansPreviousCycle+=abs(aBank.centralBankAccountTminus1)

    if aBank.centralBankAccount > 0 :
        totCentralBankDeposits+=aBank.centralBankAccount
    if aBank.centralBankAccount < 0 :
        totCentralBankLoans+=abs(aBank.centralBankAccount)

    totCentralBankBalance+=aBank.centralBankAccount

    
row=["tot",str(round(totInitialEndowments,3))+"\n("+str(totBankWorkers)+")",\
     str(round(totBankProfit,3))+"\n("+str(round(totBankDividend,3))+")",totBankInvestments,\
     str(round(totBankAccountDeposits,3))+"\n"+"("+str(round(totBankAccountDepositsTminus1,3))+")",\
     str(round(totBankAccountLoans,3))+"\n"+"("+str(round(totBankAccountLoansTminus1,3))+")",\
     str(round(totCheckingAccountDeposits,3))+"\n"+"("+str(round(totCheckingAccountDepositsTminus1,3))+")",\
     str(round(totCheckingAccountLoans,3))+"\n"+"("+str(round(totCheckingAccountLoansTminus1,3))+")",\
     round(totCentralBankBalance,3)]
data.append(row)

table = tb.tabulate(data, tablefmt='grid',headers="firstrow",floatfmt=".3f")
print(table)

print("\n\nReconciliation of banks' financial accounts with the central bank\n\n")

    
totalBankRevenues=0
totBankWorkers=0
totBankDividend=0
for aBank in cmv.bankList:
    totalBankRevenues+=aBank.revenues
    totBankWorkers+=len(aBank.myWorkers)
    if aBank.profit > 0: totBankDividend+=aBank.profit/2
    
data = [[" "," ","cycle "+str(cmv.cycle+1), " "],\
        ["(1)","banks' Deposits at CB Previous Cycle",totCentralBankDepositsPreviousCycle,"central bank stock (+)"],
        ["(2)","banks' Deposits at CB Current Cycle (with current interests)",totCentralBankDeposits,\
                                                                       "central bank stock (-)"],\
        ["(3)","banks' Loans by CB Previous Cycle",totCentralBankLoansPreviousCycle,"central bank stock (-)"],\
        ["(4)","banks' Loans by CB Current Cycle (with current interests)",totCentralBankLoans,\
                                                                       "central bank stock (+)"],\
        ["(5)","firms' Deposits Previous Cycle",totBankAccountDepositsTminus1,"firm deposit stock (+)"],\
        ["(6)","firms' Deposits Current Cycle (with current interests)",totBankAccountDeposits,"firm deposit stock (-)"],\
        ["(7)","agents' Deposits Previous Cycle",totCheckingAccountDepositsTminus1,"agent deposit stock (+)"],\
        ["(8)","agents' Deposits Current Cycle (with current interests)",totCheckingAccountDeposits,"agent deposit stock (-)"],\

        ["(9)", "firms' Loans Previous Cycle",totBankAccountLoansTminus1,"firm loan stock (-)"],\
        ["(10)","firms' Loans Current Cycle (with current interests)",totBankAccountLoans,"firm loan stock (+)"],\
        ["(11)","agents' Loans Previous Cycle",totCheckingAccountLoansTminus1,"agent loan stock (-)"],\
        ["(12)","agents' Loans Current Cycle (with current interests)",totCheckingAccountLoans,"agent loan stock (+)"],\


        ["(13)","banks' Revenues Current Cycle (with interests on deposits at CB)",totalBankRevenues,"central bank flow (+)"],\
        ["(14)","banks' Paid Wages Current Cycle",cmv.wage*totBankWorkers,"central bank flow (-)"],\
        ["(15)","banks' Paid Dividends Current Cycle",totBankDividend,"central bank flow (-)"],\
        ["(16)","agents' Interests On Deposits Current Cycle",cmv.privateClientsTotalInterestOnDepositsSeries[-1],\
                                                                                                  "bank flow (-)"],\
        ["(17)","firms' Interests On Deposits Current Cycle",cmv.commercialClientsTotalInterestOnDepositsSeries[-1],\
                                                                                                  "bank flow (-)"],\
        ["(18)","banks' Investments",totBankInvestments,"bank flow (-)"]]


table = tb.tabulate(data, tablefmt='grid',headers="firstrow")
print(table)

print("\nReconciliation\n")
print("\n+ (1) - (2) - (3) + (4) + (5) - (6) + (7) - (8) - (9) + (10) - (11) + (12) => ",\
                                                              round(+totCentralBankDepositsPreviousCycle\
                                                                    -totCentralBankDeposits\
                                                                    -totCentralBankLoansPreviousCycle\
                                                                    +totCentralBankLoans\
                                                                    +totBankAccountDepositsTminus1\
                                                                    -totBankAccountDeposits\
                                                                    +totCheckingAccountDepositsTminus1\
                                                                    -totCheckingAccountDeposits\
                                                                    -totBankAccountLoansTminus1\
                                                                    +totBankAccountLoans\
                                                                    -totCheckingAccountLoansTminus1\
                                                                    +totCheckingAccountLoans,4))

print("\n+ (13) - (14) - (15) - (16) - (17) - (18)                                  => ",\
                                                              round(+totalBankRevenues\
                                                                    -cmv.wage*totBankWorkers\
                                                                    -totBankDividend\
                                                                    -cmv.privateClientsTotalInterestOnDepositsSeries[-1]\
                                                                    -cmv.commercialClientsTotalInterestOnDepositsSeries[-1]\
                                                                    -totBankInvestments\
                                                                    ,4),"\n")

