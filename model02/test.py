# https://stackoverflow.com/questions/46820900/display-output-from-another-python-script-in-jupyter-notebookimport tabulate as tb

# The -i tells Python to run the file in IPython's name space, thus the script knows about all your variables

# use with
# %run -i test


import tabulate as tb


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


print("\n\nReconciliation of firm accounts\n\n")