# https://stackoverflow.com/questions/46820900/display-output-from-another-python-script-in-jupyter-notebookimport tabulate as tb

# The -i tells Python to run the file in IPython's name space, thus the script knows about all your variables

# use with
# %run -i test


import tabulate as tb

print("\nLast cycle test\n")
##########################################################################
print("\n\nAGENTS\n\n")


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
        ["(3)","firms' Loans Previous Cycle",totAgentLoansPreviousCycle,       "bank stock (+)"],\
        ["(4)","firms' Loans Current Cycle (with current interests)",cmv.totalCreditsVsAgentsSeries[-1],    "bank stock (-)"],\
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
print("\n- (1) + (2) + (3) - (4)       => ",\
                                      -totAgentDepositsPreviousCycle\
                                      +cmv.totalCheckingAccountSeries[-1]\
                                      +cmv.totalCreditsVsAgentsSeries[-1]\
                                      -cmv.totalCreditsVsAgentsSeries[-1])

print("\n+ (5) - (6) + (7) + (8) - (9) => ",
                                       +cmv.wage*totWorkers\
                                       -cmv.totalConsumptionSeries[-1]\
                                       +totFirmBankDividend\
                                       +cmv.privateClientsTotalInterestOnDepositsSeries[-1]\
                                       -cmv.privateClientsTotalInterestOnLoansSeries[-1])




print("___________________________________________________________________________________\n")
##########################################################################

print("\n\nFIRMS\n\n")

data = [["# in\nfirm\nList","num","firm\nInitEn","firm\nWorkers","firm\nDividend","firm\nProfit",\
        "firmBank\nAccount\nDeposits","firmBank\nAccount\nLoans","firm\nInt\nOn\nDeposits","firm\nInt\nOn\nLoans"]]
totInitialEndowments=0
totFirmWorkers=0
totFirmDividend=0
totFirmProfit=0
totFirmBankAccountDeposits=0
totFirmBankAccountLoans=0
totFirmInterestOnDeposits=0
totFirmInterestOnLoans=0

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
    if aFirm.bankAccount<0: totFirmBankAccountLoana+=aFirm.bankAccount
    firmBankAccountDeposits=0
    if aFirm.bankAccount>0: firmBankAccountDeposits=aFirm.bankAccount
    firmBankAccountLoans=0
    if aFirm.bankAccount<0: firmBankAccountLoans=aFirm.bankAccount
    totFirmInterestOnDeposits+=aFirm.interestOnDeposits
    totFirmInterestOnLoans+=aFirm.interestOnLoans

    
    row=[i,aFirm.num,aFirm.initEn,firmWorkers,firmDividend,aFirm.profit,firmBankAccountDeposits,firmBankAccountLoans,\
        aFirm.interestOnDeposits,aFirm.interestOnLoans]
    data.append(row)
    i+=1
    

row  =   ["tot"," ",totInitialEndowments,totFirmWorkers,totFirmDividend,totFirmProfit,\
          totFirmBankAccountDeposits,totFirmBankAccountLoans,totFirmInterestOnDeposits,totFirmInterestOnLoans]

data.append(row)
table = tb.tabulate(data, tablefmt='grid',headers="firstrow")
print(table)


print("\n\nReconciliation of firm financial accounts\n\n")

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
        ["(7)","firms' Paid Dividends Current Cycle",totFirmDividend,"bank flow (-)"]]

table = tb.tabulate(data, tablefmt='grid',headers="firstrow")
print(table)

print("\nReconciliation\n")
print("\n- (1) + (2) + (3) - (4) => ",-totFirmDepositsPreviousCycle\
                                      +totFirmBankAccountDeposits\
                                      +totFirmLoansPreviousCycle\
                                      -totFirmBankAccountLoans)

print("\n+ (5) - (6) - (7)       => ",+totalFirmRevenues\
                                      -cmv.wage*totFirmWorkers\
                                      -totFirmDividend,"\n")

print("___________________________________________________________________________________\n")
##########################################################################

print("\n\nBANKS\n\n")

data = [["# in\nbank\nList","num","bank\nInitEn","bank\nWorkers","bank\nDividend","bank\nProfit",\
        "myFirm\nBank\nAccount\nDeposits\n(t-1)",\
         "myFirm\nBank\nAccount\nLoans\n(t-1)","int\nOn\nFirm\nDeposits","int\nOn\nLoans\nto\nFirms"]]

totInitialEndowments=0
totBankWorkers=0
totBankDividend=0
totBankProfit=0
totBankAccountDepositsTminus1=0
totBankAccountDeposits=0
totBankAccountLoansTminus1=0
totBankAccountLoans=0
"""
totInterestOnDeposits=0
totInterestOnLoans=0
"""

i=0
for aBank in cmv.bankList:
    totInitialEndowments+=aBank.initEn
    totBankWorkers+=len(aBank.myWorkers)
    if aBank.profit > 0: dividend=aBank.profit/2
    else: dividend=0
    totBankDividend+=dividend
    totBankProfit+=aBank.profit
    totMyFirmBankAccountDeposits=0
    totMyFirmBankAccountDepositsTminus1=0
    totMyFirmBankAccountLoans=0
    totMyFirmBankAccountLoansTminus1=0

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
    
    row=[i,aBank.num,aBank.initEn,len(aBank.myWorkers),dividend,aBank.profit,\
         str(round(totMyFirmBankAccountDeposits,3))+"\n"+"("+str(round(totMyFirmBankAccountDepositsTminus1,3))+")",\
         str(round(totMyFirmBankAccountLoans,3))+"\n"+"("+str(round(totMyFirmBankAccountLoansTminus1,3))+")",\
         "-","-"]
    data.append(row)
    i+=1
    
row=["tot"," ",totInitialEndowments,totBankWorkers,totBankDividend,totBankProfit,\
     str(round(totBankAccountDeposits,3))+"\n"+"("+str(round(totBankAccountDepositsTminus1,3))+")",\
     str(round(totBankAccountLoans,3))+"\n"+"("+str(round(totBankAccountLoansTminus1,3))+")",\
     "-","-"]
data.append(row)

table = tb.tabulate(data, tablefmt='grid',headers="firstrow")
print(table)
