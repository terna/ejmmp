"""
Here we import and prepare two datasets containing the relevant info about data on sector size (naio.xlsx) and about employment per sector (sbs.xlsx). Datasets are in excel format (as provided by EUROSTAT), and required some manipulation to be clean.
We had to:
- exclude some initial rows containing info not relevant for the model and negatively affecting the format of our data, 
- reset the index to have dataset with indexes starting from 0 (to be done twice because of the header)
- drop NaN and invalid characters 
- reattribute correctly column names (i.e. headers)
- exclude the inital rows with empty values and headers (once setted at their correct place)
"""


import csv
import pandas as pd
import numpy as np
#pd.set_option('future.no_silent_downcasting', True)

naio = pd.read_excel('naio.xlsx', sheet_name = 'Sheet1')
naio = naio.iloc[9:93]
naio = naio.reset_index(drop=True)
naio = naio.dropna(axis=1, how='all')
naio = naio.loc[:, (naio != ":").any()]
naio.columns=naio.iloc[0,:]
naio=naio.drop(index=[0,1]) #empty values for all the row
naio = naio.reset_index(drop=True)

sbs = pd.read_excel('sbs.xlsx', sheet_name = 'Sheet 1')
#sbs = sbs.drop(index=9) #empty values for all the row
sbs = sbs.iloc[8:26]
sbs = sbs.reset_index(drop=True)
sbs = sbs.replace(":", np.nan)
sbs = sbs.replace("e", np.nan) #e = estimated
sbs = sbs.replace("c", np.nan) #c = confidential
sbs.columns=sbs.iloc[0,:]
sbs = sbs.dropna(axis=1,how='all')
sbs = sbs.drop(index=[0,1]) #empty values for all the row
sbs = sbs.reset_index(drop=True)