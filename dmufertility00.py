
#Thordis Thorarinsdottir 2021
#---------------------------------------------------------------------------
#Fertility datafile
#---------------------------------------------------------------------------
#This is a program that takes info about inseminations(ins) of cows and
#creates these fertility traits:
#1)days between calving and first ins (ICF)
#2)days between first and last ins (IFL)
#3) conception rate at first ins for heifers (CR)
#It also creates fixed effects for DMU runs and cleans away wrong obsv.
#Program also groups into Herd-year groups and cleanes away rows that are
# alone in herd-year groups
#Takes about 5 minutes to run
#The herd-year grouping takes up most of the time
#---------------------------------------------------------------------------

import pandas as pd
import numpy as np
import datetime
from collections import Counter
#---------------------------------------------------------------------------
#Info for program, can be replaced
#---------------------------------------------------------------------------
#Date of the data collection from Huppa!
collectiondate = '20210625'
collectiondate = pd.to_datetime(collectiondate, format='%Y%m%d')
#---------------------------------------------------------------------------
#Name of insemination file from Huppa
insfile = "../data/saedingar.csv"
#Name of cow file from Huppa
cowfile = "../data/gripalisti.csv"
#---------------------------------------------------------------------------

#---------------------------------------------------------------------------
#Datafile 1, info about inseminations. One line for every ins.
#---------------------------------------------------------------------------
ins_df = pd.read_csv(
    insfile,
    header=None,
    sep = '\t',
    names=['id','ins','tech','comment','lact']
    ) #einstaklingsnumer, insamination date, techinician, comment, lactation no.
print( f'Reading saedingar is finished' )
#---------------------------------------------------------------------------
#Datafile 2, info about cows. One line for every cow.
#---------------------------------------------------------------------------
cows_df = pd.read_csv(
    cowfile,
    header=None,
    sep = '\t',
    names=['id','herd','birth','death','calv1','calv2','calv3','calv4']
    ) #einstaklingsnumer, herd no, rest are dates
print( f'Reading gripalisti is finished' )
#---------------------------------------------------------------------------

#'ins','birth','death','calv1','calv2','calv3','calv4' formatted into dates
ins_df['ins'] = pd.to_datetime(ins_df['ins'], format='%Y%m%d')

cows_df[['birth','death','calv1','calv2','calv3','calv4']] = cows_df[
    ['birth','death','calv1','calv2','calv3','calv4']
    ].apply(
    lambda x: pd.to_datetime(x, format='%Y%m%d'))

#---------------------------------------------------------------------------
#Datafiles sorted before merge
cows_df = cows_df.sort_values(by=['id'])
ins_df = ins_df.sort_values(by=['id','ins'])

#---------------------------------------------------------------------------
#Number of calvings in data counted
#This is so wrong observations can be cleaned away
#---------------------------------------------------------------------------
cows_df.loc[
(cows_df['calv1'].notnull().astype(int) == 0) &
(cows_df['calv2'].notnull().astype(int) == 0) &
(cows_df['calv3'].notnull().astype(int) == 0) &
(cows_df['calv4'].notnull().astype(int) == 0)
,'no_calv'] = 0
cows_df.loc[
(cows_df['calv1'].notnull().astype(int) == 1) &
(cows_df['calv2'].notnull().astype(int) == 0) &
(cows_df['calv3'].notnull().astype(int) == 0) &
(cows_df['calv4'].notnull().astype(int) == 0)
,'no_calv'] = 1
cows_df.loc[
(cows_df['calv1'].notnull().astype(int) == 1) &
(cows_df['calv2'].notnull().astype(int) == 1) &
(cows_df['calv3'].notnull().astype(int) == 0) &
(cows_df['calv4'].notnull().astype(int) == 0)
,'no_calv'] = 2
cows_df.loc[
(cows_df['calv1'].notnull().astype(int) == 1) &
(cows_df['calv2'].notnull().astype(int) == 1) &
(cows_df['calv3'].notnull().astype(int) == 1) &
(cows_df['calv4'].notnull().astype(int) == 0)
,'no_calv'] = 3
cows_df.loc[
(cows_df['calv1'].notnull().astype(int) == 1) &
(cows_df['calv2'].notnull().astype(int) == 1) &
(cows_df['calv3'].notnull().astype(int) == 1) &
(cows_df['calv4'].notnull().astype(int) == 1)
,'no_calv'] = 4

#---------------------------------------------------------------------------
# Is the cow culled after any lactation?
# --------------------------------------
# Heifers
cows_df.loc[
(cows_df['no_calv'] == 0) & (cows_df['death'].notnull().astype(int) == 1), 'culled'] = 0
cows_df.loc[
(cows_df['no_calv'] == 1) & (cows_df['death'].notnull().astype(int) == 1), 'culled'] = 1
cows_df.loc[
(cows_df['no_calv'] == 2) & (cows_df['death'].notnull().astype(int) == 1), 'culled'] = 2
cows_df.loc[
(cows_df['no_calv'] == 3) & (cows_df['death'].notnull().astype(int) == 1), 'culled'] = 3

# --------------------------------------
# print(cows_df.iloc[100115:100165])
# print(cows_df.info())


#Faulty obs. collected and marked as 9
cows_df.loc[
(cows_df['no_calv'] != 0) & (cows_df['no_calv'] != 1) & (cows_df['no_calv'] != 2)
& (cows_df['no_calv'] != 3) & (cows_df['no_calv'] != 4),
'no_calv'] = 9
#wrongcalv_df.to_csv('wrongcalv.csv', index=False)
#---------------------------------------------------------------------------

#---------------------------------------------------------------------------
#Two files merged into one file where info about cows follows each ins.
df = pd.merge(left=ins_df, right=cows_df,on='id' )
print( f'Gripalisti and saedingar have been merged' )
#---------------------------------------------------------------------------

#---------------------------------------------------------------------------
# In which lactation does the ins occur?
# --------------------------------------
# Heifers who are inseminated but do not calve
df.loc[
(df['no_calv'] == 0), 'ins_lact'] = 7
#Heifers that calve inseminations
df.loc[
(df['no_calv'] > 0) & (df['ins'] < df['calv1']), 'ins_lact'] = 0
#Lactations 1
df.loc[
(df['no_calv'] >= 1) & (df['ins'] > df['calv1']) & (df['ins'] < df['calv2']),
'ins_lact'] = 1
df.loc[
(df['no_calv'] == 1) & (df['ins'] > df['calv1']), 'ins_lact'] = 1
#Lactations 2
df.loc[
(df['no_calv'] >= 2) & (df['ins'] > df['calv2']) & (df['ins'] < df['calv3']),
'ins_lact'] = 2
df.loc[
(df['no_calv'] == 2) & (df['ins'] > df['calv2']), 'ins_lact'] = 2
#Lactations 3
df.loc[
(df['no_calv'] >= 3) & (df['ins'] > df['calv3']) & (df['ins'] < df['calv4']),
'ins_lact'] = 3
df.loc[
(df['no_calv'] == 3) & (df['ins'] > df['calv3']), 'ins_lact'] = 3
# --------------------------------------



#Wrong ins located and marked as 99
df.loc[
(df['ins_lact'] != 0.0) & (df['ins_lact'] != 7.0) & (df['ins_lact'] != 1.0)
& (df['ins_lact'] != 2.0) & (df['ins_lact'] != 3.0),
'ins_lact'] = 99.0
#Ins that happen before 2008 are marked as 88
df.loc[
(df['ins'] < '2008-01-01'),
'ins_lact'] = 88.0
#Ins have comments located are marked as 77
df.loc[
(df['comment'].notnull().astype(int) == 1),
'ins_lact'] = 77.0
# --------------------------------------
print( f'Lactation for inseminations have been found' )
#---------------------------------------------------------------------------

#---------------------------------------------------------------------------
#Splitting info into lactations and counting ins per lact.
#---------------------------------------------------------------------------
heifers_df = df[(df['ins_lact'] == 0.0) | (df['ins_lact'] == 7.0)]
lact1_df = df[df['ins_lact'] == 1.0]
lact2_df = df[df['ins_lact'] == 2.0]
lact3_df = df[df['ins_lact'] == 3.0]
#---------------------------------------------------------------------------

#Wrong ins were marked and collected
wrongins = df[(df['ins_lact'] == 99.0) | (df['ins_lact'] == 88.0) |
(df['ins_lact'] == 77.0)]
wrongins.loc[:,'check'] = 1
wrongins = wrongins[['id','check']]
wrongins.columns = ['id', 'ins_lact']
wrongins = wrongins.drop_duplicates(subset=['id'])
#They are merged into the cows dataframe so cows can be cleaned away later
cows_df = pd.merge(left=cows_df[
['id','herd','birth','death','calv1','calv2','calv3','calv4','no_calv','culled']
], right=wrongins[['id','ins_lact']], on='id', how='left')
#---------------------------------------------------------------------------
# print(cows_df.iloc[100000:100015])
# print(cows_df.info())
#---------------------------------------------------------------------------
#This is a function to count ins per lactation and collect the first and last ins
def inscount (df1,firstins, lastins, T, tech):
    df1.loc[:,'T'] = df1.groupby('id')['id'].transform('count') #Total ins
    df1.loc[:,'No'] = df1.groupby('id')['id'].cumcount() + 1 #number of each ins
    #The last ins
    df1.loc[(df1['T'] == df1['No']), lastins] = df1['ins']
    #Tota number of heifer ins
    df1.loc[(df1['T'] == df1['No']), T] = df1['T']
    #First ins
    df1.loc[(df1['No'] == 1), firstins] = df1['ins']
    #First heifer tech
    df1.loc[(df1['No'] == 1), tech] = df1['tech']
    #First and last observations locaed
    first = df1[df1[firstins] == df1['ins'] ]
    last = df1[df1[lastins] == df1['ins']]
    #First and last observations put in seperate dataframes
    first = first.loc[:, ['id',firstins,tech]]
    last = last.loc[:, ['id',lastins,T]]
    #First and last heifer ins merged into one dataframe
    df1 = pd.merge(left=first, right=last)
    df1['check'] = (collectiondate - df1[firstins]).dt.days ##############################
    df1 = df1.loc[(df1['check'] > 302 )] ##############################
    return df1
#---------------------------------------------------------------------------
heifers_df = inscount(heifers_df, 'first_h', 'last_h', 'T_h', 'tech_h' )
lact1_df = inscount(lact1_df, 'first_1', 'last_1', 'T_1', 'tech_1' )
lact2_df = inscount(lact2_df, 'first_2', 'last_2', 'T_2', 'tech_2' )
lact3_df = inscount(lact3_df, 'first_3', 'last_3', 'T_3', 'tech_3' )
#---------------------------------------------------------------------------

#These results are merged into the cows data
cows_df = pd.merge(left=cows_df, right=heifers_df, on='id', how='left')
cows_df = pd.merge(left=cows_df, right=lact1_df, on='id', how='left')
cows_df = pd.merge(left=cows_df, right=lact2_df, on='id', how='left')
cows_df = pd.merge(left=cows_df, right=lact3_df, on='id', how='left')

# cows_df = cows_df.merge(heifers_df, on='id', how='outer')
# cows_df = cows_df.merge(lact1_df, on='id', how='outer')
# cows_df = cows_df.merge(lact2_df, on='id', how='outer')
# cows_df = cows_df.merge(lact3_df, on='id', how='outer')

print( f'First and last inseminations have been found' )


#---------------------------------------------------------------------------
#Feritlity traits and traits for cleaning and fixed effecsts
#---------------------------------------------------------------------------
#Age at first ins at each lact
cows_df['AGEi_h'] = (cows_df['first_h'] - cows_df['birth']).dt.days
#cows_df['AGEi_1'] = (cows_df['first_1'] - cows_df['birth']).dt.days
#cows_df['AGEi_2'] = (cows_df['first_2'] - cows_df['birth']).dt.days
#cows_df['AGEi_3'] = (cows_df['first_3'] - cows_df['birth']).dt.days
#Age at calving at each lact
cows_df['AGEc_1'] = (cows_df['calv1'] - cows_df['birth']).dt.days
cows_df['AGEc_2'] = (cows_df['calv2'] - cows_df['birth']).dt.days
cows_df['AGEc_3'] = (cows_df['calv3'] - cows_df['birth']).dt.days
#Gestation lenght
cows_df['gest1'] = (cows_df['calv1'] - cows_df['last_h']).dt.days
cows_df['gest2'] = (cows_df['calv2'] - cows_df['last_1']).dt.days
cows_df['gest3'] = (cows_df['calv3'] - cows_df['last_2']).dt.days
#Calving interval
cows_df['CI12'] = (cows_df['calv2'] - cows_df['calv1']).dt.days
cows_df['CI23'] = (cows_df['calv3'] - cows_df['calv2']).dt.days
cows_df['CI34'] = (cows_df['calv4'] - cows_df['calv3']).dt.days
#---------------------------------------------------------------------------
#Fertility trait, days between calving and first ins
cows_df['ICF1'] = (cows_df['first_1'] - cows_df['calv1']).dt.days
cows_df['ICF2'] = (cows_df['first_2'] - cows_df['calv2']).dt.days
cows_df['ICF3'] = (cows_df['first_3'] - cows_df['calv3']).dt.days
#Fertility trait, days between first and last ins
cows_df['IFLh'] = (cows_df['last_h'] - cows_df['first_h']).dt.days
cows_df['IFL1'] = (cows_df['last_1'] - cows_df['first_1']).dt.days
cows_df['IFL2'] = (cows_df['last_2'] - cows_df['first_2']).dt.days
cows_df['IFL3'] = (cows_df['last_3'] - cows_df['first_3']).dt.days
#1-4 days count as one ins period so IFL set to zero
cows_df.loc[(cows_df['IFLh'] <= 4) &(cows_df['IFLh'] >= 1),'IFLh'] = 0
cows_df.loc[(cows_df['IFL1'] <= 4) &(cows_df['IFL1'] >= 1),'IFL1'] = 0
cows_df.loc[(cows_df['IFL2'] <= 4) &(cows_df['IFL2'] >= 1),'IFL2'] = 0
cows_df.loc[(cows_df['IFL3'] <= 4) &(cows_df['IFL3'] >= 1),'IFL3'] = 0
#---------------------------------------------------------------------------
cows_df.loc[(cows_df['IFL1'] == 0) &(cows_df['calv2'].notnull().astype(int) == 0),'IFL1x'] = 21
#---------------------------------------------------------------------------
#Fertility trait, conception rate at first calving for heifers
cows_df.loc[
(cows_df['IFLh'] == 0) &
(cows_df['calv1'].notnull().astype(int) == 1), #calv1, there is an obsv.
'CRh'] = 1
cows_df.loc[
(cows_df['IFLh'] >= 5) &
(cows_df['calv1'].notnull().astype(int) == 1),
'CRh'] = 0
cows_df.loc[
(cows_df['IFLh'] >= 0) &
(cows_df['calv1'].notnull().astype(int) == 0), #calv1, there is no obsv.
'CRh'] = 0

print(cows_df.iloc[100415:100465])
print(cows_df.info())

# prev = cows_df[['id','first_h','last_h','first_1','last_1','calv1','calv2','culled','IFLh','CRh','T_h','IFL1']]
#
# # prev.loc[(prev['IFLh'] > 0) &(prev['IFLh'] < 6), 'iflx'] = 1
# # prev.loc[(prev['IFLh'] == 0) , 'iflx'] = 0
# # prev.loc[(prev['IFLh'] > 5 ) , 'iflx'] = 6
# #
# # prev.loc[:,'iflxc'] = prev.groupby('iflx')['iflx'].transform('count') #Total ins
#
# print(prev.iloc[100115:100165])
# print(prev.info())

# print(Counter(prev['iflxc']).keys()) # equals to list(set(words))
# print(Counter(prev['iflxc']).values()) # counts the elements' frequency
