#!/usr/bin/env python
# coding: utf-8

# ## test ff multi
# Powered by [Eleonora Priori](https://www.ecoaz.unito.it/do/docenti.pl/Alias?eleonora.priori#tab-profilo) and [Pietro Terna](https://terna.to.it/) 
# 

# In[1]:


from mpi4py import MPI
from repast4py import context as ctx
import repast4py 
from repast4py import parameters
from repast4py import schedule
from repast4py import core
from typing import Tuple, List, Dict
import numpy as np
import pandas as pd
import pickle
import csv
import os
import sys
import time
import sectors

comm = MPI.COMM_WORLD
rank    = comm.Get_rank()
rankNum = comm.Get_size() 

if rankNum > 0: print('rank', rank, 'starting',flush=True)

# create the context to hold the agents and manage cross process
# synchronization
context = ctx.SharedContext(comm)

# Initialize the default schedule runner, HERE to create the t() function,
# returning the tick value
runner = schedule.init_schedule_runner(comm)

#Initializes the repast4py.parameters.params dictionary with the model input parameters.
params = parameters.init_params("test_ff_multi.yaml", "")

#generate random seed
repast4py.random.init(rng_seed=params['myRandom.seed'][rank]) #each rank has a seed
rng = repast4py.random.default_rng 

#timer T()
startTime=-1
def T():
    global startTime
    if startTime < 0:
        startTime=time.time()
    return time.time() - startTime
T() #launches the timer

#cpuTimer Tc()
startCpuTime=-1
def Tc():
    global startCpuTime
    if startCpuTime < 0:
        startCpuTime=time.process_time()
    return time.process_time() - startCpuTime
Tc() #launches the cpu timer

#read control key from firm-features-generation
with open("control4text_ff.txt", "r") as f:
    control = int(f.read())


# In[2]:


class Firm(core.Agent):

    TYPE = 0

    def __init__(self, local_id: int, rank: int, sector: int, labor: int, capital: float, capitalR: float, wage: float,\
                 intermediate: list, country: int): 
                 #, minOrderDuration:int,\
                 #maxOrderDuration:int, recipe: float, laborProductivity: float, maxOrderProduction: float,\
                 #assetsUsefulLife: float, plannedMarkup: float, orderObservationFrequency: int, productionType: int,\
                 #sectorialClass: int):
        super().__init__(id=local_id, type=Firm.TYPE, rank=rank) #uid

        self.sector=sector
        self.labor=labor
        self.capital=capital
        self.capitalR=capitalR
        self.wage=wage
        self.intermediate = intermediate
        self.country = country
        #self.investment = investment

        """
        self.unavailableLabor=0
        self.unavailableCapital=0
        self.minOrderDuration=minOrderDuration
        self.maxOrderDuration=maxOrderDuration
        self.recipe = recipe
        self.laborProductivity=laborProductivity
        self.maxOrderProduction=maxOrderProduction
        self.assetsUsefulLife=assetsUsefulLife
        self.plannedMarkup=plannedMarkup
        self.orderObservationFrequency=orderObservationFrequency
        self.productionType=productionType
        self.sectorialClass=sectorialClass 
        """


# In[3]:


class EUstat(core.Agent):

    TYPE = 1

    def __init__(self, local_id: int, rank: int): 
        super().__init__(id=local_id, type=EUstat.TYPE, rank=rank) #uid

        self.rankResults = [] # it will be filled in fillingRankResults

    def save(self) -> Tuple:
        """
        Saves the state of the EUstat as a Tuple.
        """
        return (self.uid, 
                (self.rankResults)
               )

    def update(self, dynState: Tuple):
        #for i in range(len(self.rankResults)): # self.rankResults is a list to be filled on the way by appending the required items
           self.rankResults = dynState


# In[4]:


# Local cache: avoids recreating agents already present on this rank
agent_cache = {}  # Dict[uid, Agent]

def restore_agent(agent_data: tuple): 
    """
    Reconstructs or updates an agent from serialized data.
    It is the complement of `save()` and is passed to context.synchronize(...).

    agent_data: a tuple in the form (uid, state_tuple)
    where uid is typically (owner_rank, TYPE, local_id)
    and state_tuple is the tuple returned by save().    
    """
    uid, state = agent_data
    agent_type = uid[1]  # conventionally: uid = (rank, TYPE, local_id)

    # EUstat
    if agent_type == EUstat.TYPE:
        if uid in agent_cache:
            ag = agent_cache[uid]
            # Consistency with the template: we ALWAYS use update(dynState)
            ag.update(state)
        else:
            # Ricreazione da zero rispettando l'ordine della tupla di save()
            # a = state 
            ag = EUstat(uid[0],uid[2]) #, a)
            agent_cache[uid] = ag
        return ag

    # If unknown individuals arrive, explicitly fail
    raise ValueError(f"restore_agent: unknown type in uid {uid}")


# In[5]:


def statistics(y_true, y_est):

    y_true = np.array(y_true)
    y_est  = np.array(y_est)

    n = y_true.shape[0]

    #MAE, Mean Absolute Error
    # $ MAE = \frac{1}{n}\sum_{i=1}^n | yi - \hat{y}_i | $
    mae = abs(y_true - y_est).mean()

    # RMSE, Root Mean Squared Error
    # $ RMSE = \sqrt{\frac{1}{n}\sum_{i=1}^n ( y_i - \hat{y}_i )^2} $
    rmse = (((y_true - y_est)**2).sum()/n)**0.5

    # MAPE, Mean Absolute Percentage Error
    # $ MAPE = \frac{100}{n}\sum_{i=1}^n \left| \frac{y_i - \hat{y}_i}{y_i} \right| $
    safeDiv = np.where(y_true == 0, 0.000001, 0)
    mape = (abs((y_true - y_est) / (y_true+safeDiv)).sum()) * 100 / n

    # R², coefficient of determination
    # $ R^2 = 1 - \frac{\sum (y_i - \hat{y}_i)^2}{\sum (y_i - \bar{y})^2} $
    if ((y_true - y_true.mean())**2).sum() == 0: r2 = 0
    else: r2 = 1 - (((y_true - y_est)**2).sum()/((y_true - y_true.mean())**2).sum())**0.5

    return (mae,rmse,mape,r2,n)  #,rmse, mape,r2,count)


#   
#   
# $ MAE = \frac{1}{n}\sum_{i=1}^n | yi - \hat{y}_i | $
# 
# $ RMSE = \sqrt{\frac{1}{n}\sum_{i=1}^n ( y_i - \hat{y}_i )^2} $
# 
# $ MAPE = \frac{100}{n}\sum_{i=1}^n \left| \frac{y_i - \hat{y}_i}{y_i} \right| $
# 
# $ R^2 = 1 - \frac{\sum (y_i - \hat{y}_i)^2}{\sum (y_i - \bar{y})^2} $
# 

# In[6]:


from IPython.display import display, HTML
def stop_execution(message):
    display(HTML(f"<pre>{message}</pre>"))
    raise SystemExit(0)


# 
# 
# $ MAE = \frac{1}{n}\sum_{i=1}^n | yi - \hat{y}_i | $
# 
# $ RMSE = \sqrt{\frac{1}{n}\sum_{i=1}^n ( y_i - \hat{y}_i )^2} $
# 
# $ MAPE = \frac{100}{n}\sum_{i=1}^n \left| \frac{y_i - \hat{y}_i}{y_i} \right| $
# 
# $ R^2 = 1 - \frac{\sum (y_i - \hat{y}_i)^2}{\sum (y_i - \bar{y})^2} $
# 

# In[7]:


def generateOutput(countryLabel, modelOutput, AFF_FirmNumber, countAFF_Firms, propFactor, AFF_WorkerNumber, countAFF_WorkerNumber,
                   Eu_FirmNumber, countActualExPostFirmNumber, Eu_WorkerNumber, countWorkers, Eu_EmployeeCompensations,
                   countEmployeeCompensations, Eu_GDP_withVAT2022, Eu_AddedValue2022, countCapitalR, markupTentative,
                   Eu_Intermediate2022, intermediateTotal, substitutionRate, substitutionRateL, firmSubstitutions,
                   allfirmSubstitutionsByBuyerSector, simulationFirmsExAnteNumber, allfirmSubstitutionsByVendorSector):

    if rank != 0: return

    employeeCompensations_CapitalR_markupAugmented = \
       int(markupTentative*(countEmployeeCompensations/1000000 + countCapitalR/1000))
    capitalR_fullMarkupAugmented = \
       int(countCapitalR/1000 + (markupTentative-1)*(countEmployeeCompensations/1000000 + countCapitalR/1000))
    table_data = [
        [' ',          'EU 27', 'simulation', 'simulation to'],
        [' ',          ' ',     ' ',          'EU scale'],
        ['AFF Firm Number', AFF_FirmNumber, countAFF_Firms, int(countAFF_Firms * propFactor)], 
        ['AFF Worker Number', AFF_WorkerNumber, countAFF_WorkerNumber, int(countAFF_WorkerNumber * propFactor)], 
        ['Firm Number', Eu_FirmNumber, countActualExPostFirmNumber, int(countActualExPostFirmNumber * propFactor)],
        ['Worker Number', Eu_WorkerNumber, countWorkers, int(countWorkers * propFactor)],
        ['Empl. Compens.', int(Eu_EmployeeCompensations), int(countEmployeeCompensations/1000000), 
                           int(countEmployeeCompensations * propFactor / 1000000)],                                                                                                                              
        ['Cap. R & Op. Surplus', int(Eu_AddedValue2022 - Eu_EmployeeCompensations), capitalR_fullMarkupAugmented, 
                                 int(capitalR_fullMarkupAugmented*propFactor)],
        ['GDP curr. p. (VAT)', Eu_GDP_withVAT2022, 'N.B. contains VAT',' '],
        ['Add. Val. basic p.', Eu_AddedValue2022,
                               employeeCompensations_CapitalR_markupAugmented,
                               int(employeeCompensations_CapitalR_markupAugmented*propFactor)],
        ['Int. goods basic p.', int(Eu_Intermediate2022), int(intermediateTotal/1000000),
         int(intermediateTotal * propFactor / 1000000)]
    ]

    print("\n", countryLabel, "\n", file=modelOutput)

    print(f"Markup tentative {100*(markupTentative-1)}%", file=modelOutput)
    for row in table_data:
        print("{: >20} {: >20} {: >20} {: >20}".format(*row), file=modelOutput)

    print("\n AFF => Agriculture, Forestry and Fishing\n\n", file=modelOutput)

    # investments
    print("\nINVESTMENT TABLES\n", file=modelOutput)
    print(f"Investment regular substitution rate {substitutionRate}", file=modelOutput) 
    print(f"Investment long term substitution rate {substitutionRateL} for sectors 44 and 45", file=modelOutput)
    print()

    table2_data = [
        [' ', 'EU 27 (*)', 'simulation', 'simulation to'],
        [' ', ' ', ' ', 'EU scale'],
        ['Gross fixed c. formation', '3320258.70',
         int(100*firmSubstitutions/1000)/100.0,
         int(100*(firmSubstitutions/1000)*(Eu_FirmNumber/countActualExPostFirmNumber))/100.0]
    ]

    for row in table2_data:
        print("{: >20} {: >20} {: >20} {: >20}".format(*row), file=modelOutput)

    # by buying sectors
    print("\n", file=modelOutput)
    tot1 = 0
    buyingSectorsPurchases = []
    print(f"{'BUYING SECTORS':<35}{'Simulated investment purchases':<35}{'SIM. EU SCALE'}", file=modelOutput)

    for i in range(len(sectors.sectorNames)):
        print(f"{sectors.sectorNames[i][0:30]:<35}{allfirmSubstitutionsByBuyerSector[i]/1000:<16.2f}\
                {(allfirmSubstitutionsByBuyerSector[i]/1000)*(Eu_FirmNumber/countActualExPostFirmNumber):.2f}", file=modelOutput)

        buyingSectorsPurchases.append((allfirmSubstitutionsByBuyerSector[i]/1000) *
                                      (Eu_FirmNumber/countActualExPostFirmNumber))
        tot1 += allfirmSubstitutionsByBuyerSector[i] / 1000

    print(f"{'totals'[0:30]:<35}{tot1:<35.2f}{tot1*(Eu_FirmNumber/countActualExPostFirmNumber):.2f}", file=modelOutput)

    print("(*) EU 27 Gross Fixed Capital Formation is 3320258.70, but here we consider only substitutions."
          "With ", simulationFirmsExAnteNumber, "ex-ante firms and smart capital option, substitutions are ",
          tot1*(Eu_FirmNumber/countActualExPostFirmNumber), file=modelOutput)

    if countryLabel == 'totEU27':
        with open('buyingSectorsPurchases.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            for value in buyingSectorsPurchases:
                writer.writerow([value])

    if countryLabel == 'totEU27' and rankNum == 1 and \
        not (int(tot1*(Eu_FirmNumber/countActualExPostFirmNumber)) >= control/1.01 and
            int(tot1*(Eu_FirmNumber/countActualExPostFirmNumber)) <= control*1.01):

        stop_execution(
            "\n! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! \n"
            "Wrong control test, run again firm-features-generation to align investment table to new test_ff_multi choices"
            "\n! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! \n"
                      )

    print("\nINVESTMENT TABLES (continue)\n", file=modelOutput)           

    # by vending sectors
    print("\n\n\n", file=modelOutput)
    corrCoeff = tot1*(Eu_FirmNumber/countActualExPostFirmNumber)/3320258.70
    tot1 = tot2 = tot3 = tot4 = 0
    y_true = []
    y_est = []

    print(f"{'VENDING SECTORS':<35}{'EU GrossCapitalFormation':<28}{'SIM. EU SCALE':<20}{'diff (sim - actual)'}", file=modelOutput)
    print(f"{'':<35}{'scaled to substitutions':28}", file=modelOutput)

    for i in range(len(sectors.sectorNames)):
        inv = (allfirmSubstitutionsByVendorSector[i]/1000) * (Eu_FirmNumber/countActualExPostFirmNumber)
        y_est.append(inv)
        y_true.append(sectors.GrossCapitalFormation[i] * corrCoeff)
        diff = inv - sectors.GrossCapitalFormation[i] * corrCoeff

        if sectors.GrossCapitalFormation[i] == 0:
            rel100 = 0
        else:
            rel100 = 100 * diff / (sectors.GrossCapitalFormation[i] * corrCoeff)

        print(f"{sectors.sectorNames[i][0:30]:<35}"
              f"{sectors.GrossCapitalFormation[i]*corrCoeff:<33.2f}"
              f"{inv:<20.2f}{diff:<20.3f}{rel100:.2f}%", file=modelOutput)

        tot1 += sectors.GrossCapitalFormation[i] * corrCoeff
        tot2 += inv
        tot3 += diff
        tot4 += diff**2

    print(f"{'totals'[0:30]:<35}{tot1:<33.2f}{tot2:<20.2f}{tot3:,.2f}", file=modelOutput)
    print(" ",file=modelOutput)
    print(f"Sum of the squares of the diffs {tot4:,.2f}", file=modelOutput)

    (mae, rmse, mape, r2, ncases) = statistics(y_true, y_est)
    print(f"MAE  = {mae:.3f}", file=modelOutput)
    print(f"RMSE = {rmse:.3f}", file=modelOutput)
    print(f"MAPE = {mape:.2f}%", file=modelOutput)
    print(f"R²   = {r2:.3f}", file=modelOutput)
    print(f"n    = {ncases:.0f}", file=modelOutput)


# In[8]:


def generateGDPOutput(countryLabel, modelOutput, propFactor, countEmployeeCompensations, countCapitalR, markupTentative):

    print(countryLabel, \
          int(markupTentative*(countEmployeeCompensations * propFactor/1000000 + countCapitalR * propFactor/1000)), \
          file=modelOutput)


# In[9]:


def scalarSummingResultsOverRanks(n):
    tot = 0
    for i in range(1, rankNum):
        rankEUstat_ghost = context.ghost_agent((0,1,i))
        tot += rankEUstat_ghost.rankResults[n]
    return tot

def summingResultsOverRanks(n):
    tot = [0] * 28
    for i in range(1, rankNum):
        rankEUstat_ghost = context.ghost_agent((0,1,i))
        for j in range(28):
            tot[j] += rankEUstat_ghost.rankResults[n][j]
    return tot

def summingMatrixResultsOverRanks(n):
    tot = np.zeros([65,28])
    for i in range(1,rankNum):
        rankEUstat_ghost = context.ghost_agent((0,1,i))
        for j in range(28):
            for k in range(65):
                tot[k,j] += rankEUstat_ghost.rankResults[n][k,j] 
    return tot


def scalingWorkerDistribution(worker_distribution):
    values = [0] * 1849
    # class 1-9
    tot = 0
    for i in range(9): 
        tot += worker_distribution[i]
    for i in range(9):
        values[i] = worker_distribution[i] / tot
    # class 10-19
    tot = 0 
    for i in range(9, 19):
        tot += worker_distribution[i]
    for i in range(9, 19):
        values[i] = worker_distribution[i] / tot
    # class 20-49
    tot = 0 
    for i in range(19, 49):
        tot += worker_distribution[i]
    for i in range(19, 49):
        values[i] = worker_distribution[i] / tot
    # class 50-249
    tot = 0 
    for i in range(49, 249):
        tot += worker_distribution[i]
    for i in range(49, 249):
        values[i] = worker_distribution[i] / tot
    # class 250 or more (1849)
    tot = 0 
    for i in range(249, 1849):
        tot += worker_distribution[i]
    for i in range(249, 1849):
        values[i] = worker_distribution[i] / tot     
    return values

def cumulateWorkerSubdistributions(scaled_worker_distribution):

    # we exlcude the first position of each class because it keeps constant while we need to cumulate values from the second of the series
    for i in range(1,9):
        scaled_worker_distribution[i] = scaled_worker_distribution[i - 1] + scaled_worker_distribution[i] 
    for i in range(10,19):
        scaled_worker_distribution[i] = scaled_worker_distribution[i - 1] + scaled_worker_distribution[i]
    for i in range(20,49):
        scaled_worker_distribution[i] = scaled_worker_distribution[i - 1] + scaled_worker_distribution[i]  
    for i in range(50,249):
        scaled_worker_distribution[i] = scaled_worker_distribution[i - 1] + scaled_worker_distribution[i] 
    for i in range(250,1849):
        scaled_worker_distribution[i] = scaled_worker_distribution[i - 1] + scaled_worker_distribution[i]  
    return(scaled_worker_distribution)


class Model:

    def __init__(self):


        #ghosts' list or lists
        self.EUstatGhostList=[] #used only if rank == 0 but cannot be in an if to be seen below for sure

        # SCHEDULE
        runner.schedule_event(          0.0,     self.initGhosts) 
        runner.schedule_repeating_event(0.0,  1, self.interactingWithFirms)
        runner.schedule_repeating_event(0.1,  1, self.aggregatingResultsByCountry)

        runner.schedule_repeating_event(0.2,  1, self.fillingRankResults)
        runner.schedule_repeating_event(0.3,  1, self.synchronizeRanks)
        runner.schedule_repeating_event(0.4,  1, self.aggregatingRanks)
        runner.schedule_repeating_event(0.5,  1, self.showResults)

        runner.schedule_stop(0.6)
        runner.schedule_end_event(self.finish)

        self.eu_countries = ['Austria', 'Belgium', 'Bulgaria', 'Croatia', 'Cyprus', 'Czechia', 
                             'Denmark', 'Estonia', 'Finland', 'France', 'Germany', 'Greece', 
                             'Hungary', 'Ireland', 'Italy', 'Latvia', 'Lithuania', 'Luxembourg', 
                             'Malta', 'Netherlands', 'Poland', 'Portugal', 'Romania', 'Slovakia', 
                             'Slovenia', 'Spain', 'Sweden', 'totEU27']

        self.selected_countries = params['selected_countries']

        self.adjustingCoefficient = [0.93511967, 1.34627374, 0.38795621, 0.52569532, 0.60651504,
                                     0.51024537, 1.26077407, 0.47361468, 1.1191402 , 1.42657781,
                                     1.21729098, 0.61532255, 0.45692187, 1.88032905, 1.20364701,
                                     0.36661676, 0.44535584, 1.42412552, 0.46966663, 1.14829832,
                                     0.5623732 , 0.47692036, 0.51976848, 0.58076294, 0.6340686 ,
                                     0.83739389, 1.13975439, 1.00478666]

        # computed in GNP27basicPrices file (it provides adjustment by measuring the error)

        ####################################################################################################
        ###################################### CREATE EUstat AGENT ##########################################
        ####################################################################################################

        if rank != 0:
            rankEUstat = EUstat (0, rank)

            context.add(rankEUstat)


        ####################################################################################################
        ###################################### CREATE FIRM AGENTS ##########################################
        ####################################################################################################

        with open('naio_io_N.xp', 'rb') as f:
            intermediateInputs = pickle.load(f) #numpy array, only numeric, see last row of firm-features-generation.ipynb
                                                #eliminating nan in col 43 (used), not in 64 (never used)

        #firm investment shares
        """
        nama = 3
        while nama != 0 and nama != 1 and nama != 2:
            nama = int(input("What table of investment shares? "+\
                   "Please, use only 0/1/2 to chose invTableNoNama (0) or invTableNama (1) or invTableNamaIPF (2) "))
            if nama != 0 and nama != 1 and nama != 2: 
                print("Please, use only 1/0 to express yes/no values")
        """
        nama = params['tableOfInvestmentShares']
        print('rank', rank, 'tableOfInvestmentShare', nama)

        if nama==0: self.invShares = pd.read_pickle("./invTableNoNama.xp") #ignoring nama infos
        if nama==1: self.invShares = pd.read_pickle("./invTableNama.xp")   #using nama infos
        if nama==2: self.invShares = pd.read_pickle("./invTableNamaIPF.xp")   #using nama infos

        self.invSharesNp = self.invShares.to_numpy()
        #print(self.invSharesNp)

        #65 rows x 66 columns
        #print (self.invShares)
        #print (self.invShares.iloc[0,0]) #Crop
        #print (self.invShares.iloc[1,0]) #Forest
        #print (self.invShares.iloc[0,1]) #0.002242 values for invTableNoNama (here and following)
        #print (self.invShares.iloc[1,1]) #0.002242
        #print (self.invShares.iloc[0,2]) #0.000131
        #print (self.invShares.iloc[1,2]) #0.000131
        #print (self.invShares.iloc[43,0]) #Imputed 
        #print (self.invShares.iloc[44,0]) #Real

        for i in range(64): #64, as rows 0:63
            intermediateInputs[i,43]=0
            #intermediateInputs[i,64]=0 #col 64 never user, as sector 65 was dropped

        fileName = "ff_with_class_limits.csv" #input("file name? ")

        # how many firms
        #self.simulationFirmsExAnteNumber = int(input("how many firms? "))
        self.simulationFirmsExAnteNumber = params['howManyFirms']
        print('rank', rank, 'how many firms', self.simulationFirmsExAnteNumber)

        with open("workers_distribution.xp", "rb") as f:
            worker_distribution = pickle.load(f)

        scaled_worker_distribution = scalingWorkerDistribution(worker_distribution) 
        cumulated_worker_distribution = cumulateWorkerSubdistributions(scaled_worker_distribution)

        # smart capital
        """
        self.smart_capital = 2
        while self.smart_capital != 0 and self.smart_capital != 1:
            self.smart_capital = int(input("use smart capital? (Please, use only 1/0 to express True/False values) "))
            if self.smart_capital != 0 and self.smart_capital != 1: print("Please, use only 1/0 to express True/False values")
        """
        self.smart_capital = params['useSmartCapital']
        print('rank', rank, 'use smart capital', self.smart_capital)


        with open('addedvalue_countryshares.xp', 'rb') as f:
            addedvalue_countryshares = pickle.load(f)
            # addedvalue_countryshares['Country', 'Share in 2020'] where 'Country' is an index, not a column
            # to call the share use addedvalue_countryshares.iloc[0,x]
            # can also call by country doing addedvalue_countryshares.at['Austria', 'Share in 2020']


        eu_firms_by_employed_number = pd.read_pickle("./eu_firms_by_employed_number.xp") # this is a list of dfs (0-9, 10-19,20-49,50-249,>250)
        sector_special_cases = ['1', '2', '3', '44'] # agri-silvi-fish and imputed rents
        agri_eu27 = pd.read_pickle("./agri_eu27.xp") # agri-silvi-fish shares (countries are cols to keep \\consistency with eu_firms_by_employed_number)
        self.eu27_owners = pd.read_pickle("./eu27_ownership.xp") # 44 sector, imputed rents from houses ownership by EU country

        #importing csv file containing info about firms 
        with open(fileName, newline='') as csvfile:
            firmReader= csv.reader(csvfile, delimiter=',')#, quoting=csv.QUOTE_NONNUMERIC)

            self.rowNumber=-1 #to skip the row of the headers
            k=0 
            createImputedRentsFirms = True
            if rank != 0: createImputedRentsFirms = False # to avoid firms creation from sect44 in ranks != 0

            for row in firmReader: #for each record in .csv
                #print(row)
                labor = 0 
                if self.rowNumber>=0: # skip if -1
                    if row[4]=='': row[4]=0 # it pertains with last rows (naio sector 65)                       
                    sector = row[0]

                    #*****************************************************************************************
                    initialFirmCreationNumber= round(float(row[4]) * self.simulationFirmsExAnteNumber)
                    firmCreationNumber = initialFirmCreationNumber // rankNum # integer division between integers returns integer

                    if rank == 0:
                        remainderFirmCreationNumber = initialFirmCreationNumber % rankNum

                        if remainderFirmCreationNumber > 0:
                            firmCreationNumber += remainderFirmCreationNumber


                    if sector =='44' and createImputedRentsFirms:
                        firmCreationNumber= 27 # number of EU countries
                        createImputedRentsFirms = False

                    countImputedRentsFirms = 0

                    #*****************************************************************************************
                    # class attribution
                    if row[3] == "From 0 to 9 persons employed": 
                        cl = 0
                        r_min = 0
                        r_max = 8
                    if row[3] == "From 10 to 19 persons employed": 
                        cl = 1
                        r_min = 9 
                        r_max = 18
                    if row[3] == "From 20 to 49 persons employed": 
                        cl = 2
                        r_min = 19
                        r_max = 48
                    if row[3] == "From 50 to 249 persons employed": 
                        cl = 3
                        r_min = 49
                        r_max = 248
                    if row[3] == "250 persons employed or more": 
                        cl = 4
                        r_min = 249
                        r_max = 1848


                    for i in range(firmCreationNumber):
                        if row[0] == '1' or row[0] == '2' or row[0] == '3': #agri, silvi and fishing
                            randomizer = rng.uniform()
                            if randomizer <= 0.2: labor = 0
                            elif randomizer <= 0.9 : labor = 1
                            else: labor = 2
                        else:
                            randomizer = rng.uniform()
                            j = r_min
                            while randomizer > cumulated_worker_distribution[j]: 
                                j += 1 
                            labor = j + 1
                            if labor - 1 > r_max: stop_execution("Selection exceeded in assigning firm labor")       

                            if sector =='44': labor = 0 # no employees in a virtual sector


                        # assignation of EU country label/number 
                        country_randomizer = rng.uniform()
                        # assigning rule: we attribute the first country with a cumulative share higher than the random number we draw
                        # non-special cases sectors come from the sbs_countries file, while agriculture sector is treaten in the agri_eu27 file
                        country_counter = 0
                        if not row[0] in sector_special_cases:
                            if eu_firms_by_employed_number[cl].iloc[int(row[0]), -1] != 0: # to avoid sectors with all zeros 
                                while eu_firms_by_employed_number[cl].iloc[int(row[0]), country_counter] <= country_randomizer: country_counter += 1

                        elif row[0] == '44' and rank == 0: # imputed rents
                            country_counter = countImputedRentsFirms
                            countImputedRentsFirms += 1

                        else: # agri forestry and fishing
                            if agri_eu27.iloc[int(row[0])-1, -1] != 0:
                                while agri_eu27.iloc[int(row[0])-1, country_counter] <= country_randomizer: country_counter += 1


                        capital= float(row[11]) + rng.random()*(float(row[12]) - float(row[11]))
                        if self.smart_capital:
                            capital = labor * float(row[10]) # row[10] = recipe 

                        capitalR = float(row[13])
                        wage = float(row[14])

                        # labor and capital adjustments follow according to the self.adjustingCoefficient list (being ordered by country)
                        #if sector not in sector_special_cases[0:3]: # exclude agri silvi fish adjustingCoefficient should not apply there            
                            #labor *= self.adjustingCoefficient[country_counter]
                            #labor = int(labor)
                            #capital *= self.adjustingCoefficient[country_counter]

                        wage *= self.adjustingCoefficient[country_counter]
                        capital *= self.adjustingCoefficient[country_counter]

                        # intermediate do not need adjustments as k and l being yet correct
                        intermediate=[]

                        for s in range(65):
                            intermediate.append(intermediateInputs[s,int(row[0])-1]*(0.95+0.10*rng.random()))

                        """
                        minOrderDuration= row[5]
                        maxOrderDuration= row[6]
                        recipe= row[7] #K/L 
                        laborProductivity= row[8]
                        maxOrderProduction= row[9]
                        avgAssetsUsefulLife=row[10]  #https://www.oecd.org/sdd/productivity-stats/43734711.pdf
                        plannedMarkup=row[11]
                        orderObservationFrequency=rng.integers(row[12], row[13]+1)
                        productionType=int(row[14]) #productionType in firm-features.csv indicates the production of
                                                #investment goods if it is into the investmentGoods list in yaml
                        sectorialClass=int(self.rowNumber)
                        """
                        aFirm =Firm(k, rank, int(sector), labor, capital, capitalR, wage, intermediate, country_counter) #, minOrderDuration,\
                                #maxOrderDuration, recipe, laborProductivity,\
                                #maxOrderProduction, avgAssetsUsefulLife, plannedMarkup, orderObservationFrequency, productionType,\
                                #sectorialClass)



                        context.add(aFirm)
                        k += 1 # first element of the UID of the agents

                        #print(aFirm.uid, aFirm.sector, aFirm.country)

                self.rowNumber += 1
                self.simulationFirmsExPostNumber=k #one more, here is a count, not an id


    #create ghosts
    def initGhosts(self):

        #EUstat ghost, to be pulled from non 0 ranks and to be sent to the 0 rank
        # print("rank",rank,"initGhosts1",flush=True)

        ghostsToRequest = [] # list of tuples containing for each ghost the uid and its rank;

        if rank == 0:
            for rankId in range(1,rankNum):
                ghostsToRequest.append( ((0,EUstat.TYPE,rankId),rankId) )

        # print("rank",rank,"initGhosts2",flush=True)

        #create ghosts and pull them
        context.request_agents(ghostsToRequest,restore_agent)

        # print("rank",rank,"initGhosts3",flush=True)

        #the list of central planner ghosts in rank 0 (the for cycle does not work if rankNum==1)
        if rank == 0:
            for i in range(1,rankNum):
                self.EUstatGhostList.append(agent_cache[(0,EUstat.TYPE,i)])

        print("rank",rank,"self.EUstatGhostList",self.EUstatGhostList,flush=True)



    #interactingWithFirms
    def interactingWithFirms(self):

        #print(self.firmCount)

        if self.simulationFirmsExPostNumber==0:
            print("No firms created.")
        else:
            # a check
            self.countActualExPostFirmNumber = len(list(context.agents(agent_type=0)))
            if self.countActualExPostFirmNumber != self.simulationFirmsExPostNumber:
                print("DISASTER")
                quit()

            self.AFF_FirmNumber = 10000000
            self.Eu_FirmNumber = 32251874 + self.AFF_FirmNumber
            self.AFF_WorkerNumber = 9000000
            self.Eu_WorkerNumber = 162467679 + 9000000
            self.Eu_EmployeeCompensations = 7447036.79
            self.Eu_GDP_withVAT2022 = 16144780 #https://ec.europa.eu/eurostat/databrowser/view/tec00001/default/table?lang=en
            self.Eu_AddedValue2022 = 14303899 #naio table 2022 (milions) total Added value, gross
            self.Eu_Intermediate2022 = 16939701.18 	 
            self.propFactor = self.Eu_FirmNumber / self.countActualExPostFirmNumber


            self.countWorkers = [0] * 28
            self.countEmployeeCompensations = [0] * 28
            self.countCapitalR = [0] * 28
            self.countAFF_Firms = [0] * 28
            self.countAFF_WorkerNumber = [0] * 28
            self.intermediateTotal = [0] * 28
            self.firmSubstitutions= [0] * 28

            self.intBySectors=[0]*64
            self.addValBySectors=[0]*64
            self.substitutionRate =0.1
            self.substitutionRateL=0.01667 #for sectors 44 and 45, 60 years of duration
            #self.allfirmSubstitutionsByVendorSector=[0]*65
            self.allfirmSubstitutionsByVendorSector=np.zeros([65,28])
            self.allfirmSubstitutionsByBuyerSector=np.zeros([65,28])


            for aFirm in context.agents(agent_type=0):

                self.countWorkers[aFirm.country] += aFirm.labor
                self.countEmployeeCompensations[aFirm.country] += aFirm.labor*aFirm.wage
                self.countCapitalR[aFirm.country] += aFirm.capital*aFirm.capitalR
                if int(aFirm.sector) <= 3: 
                    self.countAFF_Firms[aFirm.country] += 1
                    self.countAFF_WorkerNumber[aFirm.country] +=aFirm.labor

                #added value
                addedValue=aFirm.labor*aFirm.wage + aFirm.capital*1000*aFirm.capitalR

                self.markupTentative=1.25
                addedValue *= self.markupTentative 
                #self.addValBySectors[aFirm.sector-1]+=addedValue1

                #intermediate goods acquisition (must consider markup)
                for s in range(64):
                    self.intermediateTotal[aFirm.country] += addedValue*aFirm.intermediate[s]
                    #self.intBySectors[aFirm.sector-1]+= addedValue*aFirm.intermediate[s]

                # capital substitutions (firm capital is in thousands of euros)
                # imputed rents
                if aFirm.sector == 44: 
                    # from ff_with_class_limits, we use the number of the sector not the position!
                    aFirm.capital=30000000*1000*self.eu27_owners.iloc[-1,aFirm.country]

                    # the whole EU capital of the sector, to be subdived by countries
                    # see firm-features-generation for explanation, cell "Imputed rents special case"
                    self.firmSubstitutions[aFirm.country] +=((aFirm.capital*self.substitutionRateL)/self.Eu_FirmNumber)*self.simulationFirmsExAnteNumber
                                         # it will be reported to the EU scale

                    self.allfirmSubstitutionsByBuyerSector[aFirm.sector-1, aFirm.country] += ((aFirm.capital*self.substitutionRateL)\
                                                                                /self.Eu_FirmNumber)*self.simulationFirmsExAnteNumber

                    # buying uniquely from constructions (ie sector 27!)
                    self.allfirmSubstitutionsByVendorSector[27-1, aFirm.country]+=(aFirm.capital*self.substitutionRateL/self.Eu_FirmNumber)*\
                                                                                                               self.simulationFirmsExAnteNumber
                    # for s in range(1,66):
                    #    self.allfirmSubstitutionsByVendorSector[s-1]+=aFirm.capital*self.substitutionRateL*self.invSharesNp[aFirm.sector-1,s]

                #real estate
                elif aFirm.sector == 45: # from ff_with_class_limits, we use the number of sector not the position!
                    self.firmSubstitutions[aFirm.country] += aFirm.capital*self.substitutionRateL
                    self.allfirmSubstitutionsByBuyerSector[aFirm.sector-1, aFirm.country] += aFirm.capital*self.substitutionRateL

                    for s in range(1,66):
                        self.allfirmSubstitutionsByVendorSector[s-1, aFirm.country]+=aFirm.capital*self.substitutionRateL*\
                                                                                            self.invSharesNp[aFirm.sector-1,s]
                else:                                        
                    self.firmSubstitutions[aFirm.country] +=aFirm.capital*self.substitutionRate
                    self.allfirmSubstitutionsByBuyerSector[aFirm.sector-1, aFirm.country] += aFirm.capital*self.substitutionRate

                    for s in range(1,66):
                        #self.allfirmSubstitutionsByVendorSector[s-1]+=aFirm.capital*self.substitutionRate*self.invShares.iloc[aFirm.sector-1,s]
                        self.allfirmSubstitutionsByVendorSector[s-1, aFirm.country]+=aFirm.capital*self.substitutionRate*\
                                                                                        self.invSharesNp[aFirm.sector-1,s]


    def aggregatingResultsByCountry(self):
        for j in range(27):
            self.countWorkers[27] += self.countWorkers[j]
            self.countEmployeeCompensations[27] += self.countEmployeeCompensations[j] 
            self.countCapitalR[27] += self.countCapitalR[j] 
            self.countAFF_Firms[27] += self.countAFF_Firms[j]
            self.countAFF_WorkerNumber[27] += self.countAFF_WorkerNumber[j] 
            self.intermediateTotal[27] += self.intermediateTotal[j]
            self.firmSubstitutions[27] += self.firmSubstitutions[j] 

            self.allfirmSubstitutionsByVendorSector[:, 27] += self.allfirmSubstitutionsByVendorSector[:,j]
            self.allfirmSubstitutionsByBuyerSector[:, 27] += self.allfirmSubstitutionsByBuyerSector[:,j]


    # fill the list self.rankResults
    def fillingRankResults(self):
        if rank == 0:
            return

        rankEUstat_uid = (0,1,rank)
        rankEUstat = context.agent(rankEUstat_uid)  
        rankEUstat.rankResults.append(self.countActualExPostFirmNumber) # rankEUstat.rankResults[0]
        rankEUstat.rankResults.append(self.countWorkers) # rankEUstat.rankResults[1]
        rankEUstat.rankResults.append(self.countEmployeeCompensations) # rankEUstat.rankResults[2]
        rankEUstat.rankResults.append(self.countCapitalR) # rankEUstat.rankResults[3]
        rankEUstat.rankResults.append(self.countAFF_Firms) # rankEUstat.rankResults[4]
        rankEUstat.rankResults.append(self.countAFF_WorkerNumber) # rankEUstat.rankResults[5]
        rankEUstat.rankResults.append(self.intermediateTotal) # rankEUstat.rankResults[6]
        #rankEUstat.rankResults.append(self.intBySectors) # rankEUstat.rankResults[] - temporary unused
        #rankEUstat.rankResults.append(self.addValBySectors) # rankEUstat.rankResults[] - temporary unused 
        rankEUstat.rankResults.append(self.firmSubstitutions) # rankEUstat.rankResults[7]
        rankEUstat.rankResults.append(self.allfirmSubstitutionsByVendorSector) # rankEUstat.rankResults[8] - matrix
        rankEUstat.rankResults.append(self.allfirmSubstitutionsByBuyerSector) # rankEUstat.rankResults[9] - matrix
        #rankEUstat.rankResults.append(self.) # rankEUstat.rankResults[]

        #print(rank, rankEUstat.rankResults)

    def synchronizeRanks(self):
        if rankNum > 1: context.synchronize(restore_agent)


    def aggregatingRanks(self):
        if rankNum == 1: return
        if rank != 0: return         

        self.countActualExPostFirmNumber += scalarSummingResultsOverRanks(0)
        for j in range(28):
            self.countWorkers[j] += summingResultsOverRanks(1)[j]   
            self.countEmployeeCompensations[j] += summingResultsOverRanks(2)[j]
            self.countCapitalR[j] += summingResultsOverRanks(3)[j]
            self.countAFF_Firms[j] += summingResultsOverRanks(4)[j]
            self.countAFF_WorkerNumber[j] += summingResultsOverRanks(5)[j]
            self.intermediateTotal[j] += summingResultsOverRanks(6)[j]
            self.firmSubstitutions[j] += summingResultsOverRanks(7)[j]

        #allFirmSubstitutionsByVendorSectorList = summingListResultsOverRanks(8)
            for k in range(len(self.allfirmSubstitutionsByVendorSector)):
            #self.allfirmSubstitutionsByVendorSector[j] += allFirmSubstitutionsByVendorSectorList[j]
                self.allfirmSubstitutionsByVendorSector[k,j] += summingMatrixResultsOverRanks(8)[k,j]
                self.allfirmSubstitutionsByBuyerSector[k,j] += summingMatrixResultsOverRanks(9)[k,j]


       # allFirmSubstitutionsByBuyerSectorList = summingListResultsOverRanks(9)
       # for j in range(len(self.allfirmSubstitutionsByBuyerSector)):    
            #self.allfirmSubstitutionsByBuyerSector[j] += allFirmSubstitutionsByBuyerSectorList[j]

        self.propFactor = self.Eu_FirmNumber / self.countActualExPostFirmNumber # redefined here to be updated with rankNum > 1


    # show results
    def showResults(self):
        generateOutput("totEU27", sys.stdout, self.AFF_FirmNumber, self.countAFF_Firms[27], self.propFactor, self.AFF_WorkerNumber,\
                    self.countAFF_WorkerNumber[27], self.Eu_FirmNumber, self.countActualExPostFirmNumber, self.Eu_WorkerNumber,\
                    self.countWorkers[27], self.Eu_EmployeeCompensations, self.countEmployeeCompensations[27], self.Eu_GDP_withVAT2022,\
                    self.Eu_AddedValue2022, self.countCapitalR[27], self.markupTentative, self.Eu_Intermediate2022, self.intermediateTotal[27],\
                    self.substitutionRate, self.substitutionRateL, self.firmSubstitutions[27], self.allfirmSubstitutionsByBuyerSector[:,27],\
                    self.simulationFirmsExAnteNumber, self.allfirmSubstitutionsByVendorSector[:,27])

        if self.selected_countries == []: return

        for aCountry in self.selected_countries:
            with open(self.eu_countries[aCountry]+'.txt', 'w', newline='') as txtfile:
                #print(txtfile)
                generateOutput(self.eu_countries[aCountry], txtfile, self.AFF_FirmNumber,
                                self.countAFF_Firms[aCountry], self.propFactor,
                                self.AFF_WorkerNumber, self.countAFF_WorkerNumber[aCountry],
                                self.Eu_FirmNumber, self.countActualExPostFirmNumber,
                                self.Eu_WorkerNumber, self.countWorkers[aCountry],
                                self.Eu_EmployeeCompensations, self.countEmployeeCompensations[aCountry],
                                self.Eu_GDP_withVAT2022, self.Eu_AddedValue2022,
                                self.countCapitalR[aCountry], self.markupTentative,
                                self.Eu_Intermediate2022, self.intermediateTotal[aCountry],
                                self.substitutionRate, self.substitutionRateL,
                                self.firmSubstitutions[aCountry],
                                self.allfirmSubstitutionsByBuyerSector[:, aCountry],
                                self.simulationFirmsExAnteNumber,
                                self.allfirmSubstitutionsByVendorSector[:, aCountry]
                              )

        if rank == 0: 
            print("\n", 'Add. Val. basic p. by country', "\n")
            for aCountry in range(len(self.eu_countries)):
                generateGDPOutput(self.eu_countries[aCountry], sys.stdout, self.propFactor, 
                                  self.countEmployeeCompensations[aCountry], self.countCapitalR[aCountry],
                                  self.markupTentative)


    #finish
    def finish(self):
        print("\n\n")
        print(f"Rank {rank}, gloabal time {T()}, cpu time {Tc()}")
        print("\nRank ", rank, "concluded")

    def start(self):
        runner.execute()

def run():

    model = Model() 
    model.start()

run()

#file name: ff_with_class_limits.csv


# **to run the code in a multi-rank way, from the terminal launch:**  
# 
# mpirun -n x ipython test_ff_multi.ipynb
