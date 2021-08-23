
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

#---------------------------------------------------------------------------
#Datafile 1, info about inseminations. One line for every ins.
#---------------------------------------------------------------------------
ins_df = pd.read_csv(
    "../data/saedingar.csv",
    header=None,
    sep = '\t',
    names=['id','ins','tech','comment','lact']
    ) #einstaklingsnumer, insamination date, techinician, comment, lactation no.
print( f'Reading saedingar is finished' )
#---------------------------------------------------------------------------
#Datafile 2, info about cows. One line for every cow.
#---------------------------------------------------------------------------
cows_df = pd.read_csv(
    "../data/gripalisti.csv",
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
#calvings extracted from cows dataframe
df_temp = cows_df.loc[:, ['calv1','calv2','calv3','calv4']]

#calvings counted, will return NaN if calvings in wrong order
df2  = df_temp.copy()
df2.columns = np.arange(df2.shape[1]) + 1
mask = (df2.apply(pd.Series.last_valid_index, axis=1).fillna(0) == df2.count(axis=1))
df_temp.loc[mask, 'no_calv'] = df_temp.notna().sum(1)

#Adds the calving count to the cows data
cows_df['no_calv'] = df_temp['no_calv']

#Faulty obs. collected and marked as 9
cows_df.loc[
(cows_df['no_calv'] != 0) & (cows_df['no_calv'] != 1) & (cows_df['no_calv'] != 2)
& (cows_df['no_calv'] != 3) & (cows_df['no_calv'] != 4),
'no_calv'] = 9
#wrongcalv_df.to_csv('wrongcalv.csv', index=False)
#---------------------------------------------------------------------------

#---------------------------------------------------------------------------
#Two files merged into one file where info about cows follows each ins.
df = pd.merge(left=ins_df, right=cows_df)
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
#They are merged into the cows dataframe so cows can be cleaned away later
cows_df = pd.merge(left=cows_df[
['id','herd','birth','death','calv1','calv2','calv3','calv4','no_calv']
], right=wrongins[['id','ins_lact']], on='id', how='left')
#---------------------------------------------------------------------------

#---------------------------------------------------------------------------
#Heifers
#The number of each ins is counted and the total number of ins
heifers_df.loc[:,'T'] = heifers_df.groupby('id')['id'].transform('count')
heifers_df.loc[:,'No'] = heifers_df.groupby('id')['id'].cumcount() + 1
#The last ins
heifers_df.loc[
(heifers_df['T'] == heifers_df['No']), 'last_h'] = heifers_df['ins']
#Tota number of heifer ins
heifers_df.loc[
(heifers_df['T'] == heifers_df['No']), 'T_h'] = heifers_df['T']
#First ins
heifers_df.loc[
(heifers_df['No'] == 1), 'first_h'] = heifers_df['ins']
#First heifer tech
heifers_df.loc[(heifers_df['No'] == 1), 'tech_h'] = heifers_df['tech']
#First and last observations locaed
firstheifers_df = heifers_df[heifers_df['first_h'] == heifers_df['ins'] ]
lastheifers_df = heifers_df[heifers_df['last_h'] == heifers_df['ins']]
#First and last observations put in seperate dataframes
firstheifers_df = firstheifers_df.loc[:, ['id','first_h','tech_h']]
lastheifers_df = lastheifers_df.loc[:, ['id','last_h','T_h']]
#First and last heifer ins merged into one dataframe
heifers_df = pd.merge(left=firstheifers_df, right=lastheifers_df)
#---------------------------------------------------------------------------
#Lactation1
#The number of each ins is counted and the total number of ins
lact1_df.loc[:,'T'] = lact1_df.groupby('id')['id'].transform('count')
lact1_df.loc[:,'No'] = lact1_df.groupby('id')['id'].cumcount() + 1
#The last ins
lact1_df.loc[(lact1_df['T'] == lact1_df['No']), 'last_1'] = lact1_df['ins']
#Tota number of lact1 ins
lact1_df.loc[(lact1_df['T'] == lact1_df['No']), 'T_1'] = lact1_df['T']
#First ins
lact1_df.loc[(lact1_df['No'] == 1), 'first_1'] = lact1_df['ins']
#First lact1 tech
lact1_df.loc[(lact1_df['No'] == 1), 'tech_1'] = lact1_df['tech']
#First and last observations locaed
firstlact1_df = lact1_df[lact1_df['first_1'] == lact1_df['ins'] ]
lastlact1_df = lact1_df[lact1_df['last_1'] == lact1_df['ins']]
#First and last observations put in seperate dataframes
firstlact1_df = firstlact1_df.loc[:, ['id','first_1','tech_1']]
lastlact1_df = lastlact1_df.loc[:, ['id','last_1','T_1']]
#First and last lact1 ins merged into one dataframe
lact1_df = pd.merge(left=firstlact1_df, right=lastlact1_df)
#---------------------------------------------------------------------------
#Lactation2
#The number of each ins is counted and the total number of ins
lact2_df.loc[:,'T'] = lact2_df.groupby('id')['id'].transform('count')
lact2_df.loc[:,'No'] = lact2_df.groupby('id')['id'].cumcount() + 1
#The last ins
lact2_df.loc[(lact2_df['T'] == lact2_df['No']), 'last_2'] = lact2_df['ins']
#Tota number of lact2 ins
lact2_df.loc[(lact2_df['T'] == lact2_df['No']), 'T_2'] = lact2_df['T']
#First ins
lact2_df.loc[(lact2_df['No'] == 1), 'first_2'] = lact2_df['ins']
#First lact2 tech
lact2_df.loc[(lact2_df['No'] == 1), 'tech_2'] = lact2_df['tech']
#First and last observations locaed
firstlact2_df = lact2_df[lact2_df['first_2'] == lact2_df['ins'] ]
lastlact2_df = lact2_df[lact2_df['last_2'] == lact2_df['ins']]
#First and last observations put in seperate dataframes
firstlact2_df = firstlact2_df.loc[:, ['id','first_2','tech_2']]
lastlact2_df = lastlact2_df.loc[:, ['id','last_2','T_2']]
#First and last lact2 ins merged into one dataframe
lact2_df = pd.merge(left=firstlact2_df, right=lastlact2_df)
#---------------------------------------------------------------------------
#Lactation3
#The number of each ins is counted and the total number of ins
lact3_df.loc[:,'T'] = lact3_df.groupby('id')['id'].transform('count')
lact3_df.loc[:,'No'] = lact3_df.groupby('id')['id'].cumcount() + 1
#The last ins
lact3_df.loc[(lact3_df['T'] == lact3_df['No']), 'last_3'] = lact3_df['ins']
#Tota number of lact3 ins
lact3_df.loc[(lact3_df['T'] == lact3_df['No']), 'T_3'] = lact3_df['T']
#First ins
lact3_df.loc[(lact3_df['No'] == 1), 'first_3'] = lact3_df['ins']
#First lact3 tech
lact3_df.loc[(lact3_df['No'] == 1), 'tech_3'] = lact3_df['tech']
#First and last observations locaed
firstlact3_df = lact3_df[lact3_df['first_3'] == lact3_df['ins'] ]
lastlact3_df = lact3_df[lact3_df['last_3'] == lact3_df['ins']]
#First and last observations put in seperate dataframes
firstlact3_df = firstlact3_df.loc[:, ['id','first_3','tech_3']]
lastlact3_df = lastlact3_df.loc[:, ['id','last_3','T_3']]
#First and last lact3 ins merged into one dataframe
lact3_df = pd.merge(left=firstlact3_df, right=lastlact3_df)

#These results are merged into the cows data
cows_df = cows_df.merge(heifers_df, on='id', how='outer')
cows_df = cows_df.merge(lact1_df, on='id', how='outer')
cows_df = cows_df.merge(lact2_df, on='id', how='outer')
cows_df = cows_df.merge(lact3_df, on='id', how='outer')

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
#Fertility trait, conception rate at first calving for heifers
cows_df.loc[
(cows_df['IFLh'] == 0) |
(cows_df['IFLh'] == 1) |
(cows_df['IFLh'] == 2) |
(cows_df['IFLh'] == 3) |
(cows_df['IFLh'] == 4) &
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

print( f'Fertility traits have been created' )
#---------------------------------------------------------------------------
#---------------------------------------------------------------------------
#Cleaning starts, animals who are sorted out are collected into a seperate file
# a) Age at first calving 550-1100 days
# b) Age at first ins 270-900 days
# c) Calving interval 208-600 days
# d) Gestastion lenght 260-302 days
# e) Number of ins 1-8 per lact
# f) ICF 20-230 days
# g) IFL 0-365 days

#---------------------------------------------------------------------------
#Other cleaning:
#Herd missing
#Insemanation years only after 2008-01-01
#Records for later lactations were excluded if information about previous lactations
    #were not available.
#Ins with comments cleaned away
#Records for later lactations were excluded if information about previous lactations
    #were not available.

#---------------------------------------------------------------------------

# a) Age at first calving 550-1100 days
cows_df.loc[
(cows_df['AGEc_1'] < 550) | (cows_df['AGEc_1'] > 1100),
'wrong'] = 'a'
# b) Age at first ins 270-900 days
cows_df.loc[
(cows_df['AGEi_h'] < 270) | (cows_df['AGEi_h'] > 900),
'wrong'] = 'b'
# c) Calving interval 208-600 days
cows_df.loc[
(cows_df['CI12'] < 208) | (cows_df['CI12'] > 600),#lact1
'wrong1'] = 'c'
cows_df.loc[
(cows_df['CI23'] < 208) | (cows_df['CI23'] > 600), #lact2
'wrong2'] = 'c'
cows_df.loc[
(cows_df['CI34'] < 208) | (cows_df['CI34'] > 600), #lact3
'wrong3'] = 'c'
# d) Gestastion lenght 260-302 days
cows_df.loc[
(cows_df['gest1'] < 260) | (cows_df['gest1'] > 302),
'wrong1'] = 'd'
cows_df.loc[
(cows_df['gest2'] < 260) | (cows_df['gest2'] > 302),
'wrong2'] = 'd'
cows_df.loc[
(cows_df['gest3'] < 260) | (cows_df['gest3'] > 302),
'wrong3'] = 'd'
# e) Number of ins 1-8 per lact
cows_df.loc[(cows_df['T_h'] > 8) , 'wrong'] = 'e'
cows_df.loc[(cows_df['T_1'] > 8) , 'wrong1'] = 'e'
cows_df.loc[(cows_df['T_2'] > 8) , 'wrong2'] = 'e'
cows_df.loc[(cows_df['T_3'] > 8) , 'wrong3'] = 'e'
# f) ICF 20-230 days
cows_df.loc[(cows_df['ICF1'] < 20) | (cows_df['ICF1'] > 230), 'wrong1'] = 'f'
cows_df.loc[(cows_df['ICF2'] < 20) | (cows_df['ICF2'] > 230), 'wrong2'] = 'f'
cows_df.loc[(cows_df['ICF3'] < 20) | (cows_df['ICF3'] > 230), 'wrong3'] = 'f'
# g) IFL 0-365 days
cows_df.loc[(cows_df['IFL1'] > 365), 'wrong1'] = 'g'
cows_df.loc[(cows_df['IFL2'] > 365), 'wrong2'] = 'g'
cows_df.loc[(cows_df['IFL3'] > 365), 'wrong3'] = 'g'

#---------------------------------------------------------------------------
#Checking if cows have the correct order of ins registered
cows_df.loc[
(cows_df['first_h'].notnull().astype(int) == 1) &
(cows_df['first_1'].notnull().astype(int) == 0) &
(cows_df['first_2'].notnull().astype(int) == 0) &
(cows_df['first_3'].notnull().astype(int) == 0)
,'check'] = 1000
cows_df.loc[
(cows_df['first_h'].notnull().astype(int) == 1) &
(cows_df['first_1'].notnull().astype(int) == 1) &
(cows_df['first_2'].notnull().astype(int) == 0) &
(cows_df['first_3'].notnull().astype(int) == 0)
,'check'] = 1100
cows_df.loc[
(cows_df['first_h'].notnull().astype(int) == 1) &
(cows_df['first_1'].notnull().astype(int) == 1) &
(cows_df['first_2'].notnull().astype(int) == 1) &
(cows_df['first_3'].notnull().astype(int) == 0)
,'check'] = 1110
cows_df.loc[
(cows_df['first_h'].notnull().astype(int) == 1) &
(cows_df['first_1'].notnull().astype(int) == 1) &
(cows_df['first_2'].notnull().astype(int) == 1) &
(cows_df['first_3'].notnull().astype(int) == 1)
,'check'] = 1111
cows_df.loc[
(cows_df['first_h'].notnull().astype(int) == 0) &
(cows_df['first_1'].notnull().astype(int) == 1) &
(cows_df['first_2'].notnull().astype(int) == 0) &
(cows_df['first_3'].notnull().astype(int) == 0)
,'check'] = 100
cows_df.loc[
(cows_df['first_h'].notnull().astype(int) == 0) &
(cows_df['first_1'].notnull().astype(int) == 1) &
(cows_df['first_2'].notnull().astype(int) == 1) &
(cows_df['first_3'].notnull().astype(int) == 0)
,'check'] = 110
cows_df.loc[
(cows_df['first_h'].notnull().astype(int) == 0) &
(cows_df['first_1'].notnull().astype(int) == 1) &
(cows_df['first_2'].notnull().astype(int) == 1) &
(cows_df['first_3'].notnull().astype(int) == 1)
,'check'] = 111
#---------------------------------------------------------------------------

#---------------------------------------------------------------------------
#Above all wrong obsv. were marked, now observ. are sorted into a correct
#datafile and a wrong datafile

#Observations that fulfill every condition are collected
data_use = cows_df[(
    cows_df['herd'].notnull().astype(int) == 1) & (  #herd missing
    cows_df['birth'].notnull().astype(int) == 1) & (  #no birth year
    cows_df['wrong'].notnull().astype(int) == 0) & ( #AFC or AFI wrong
    cows_df['wrong1'].notnull().astype(int) == 0) & (
    cows_df['wrong2'].notnull().astype(int) == 0) & (
    cows_df['wrong3'].notnull().astype(int) == 0) & (
    cows_df['ins_lact'] != 99.0) & ( #ins did not register on a lactation
    cows_df['ins_lact'] != 88.0) & ( #ins happens before 2008
    cows_df['ins_lact'] != 77.0) & ( #ins has a comment
    cows_df['no_calv'] != 9.0) & ( #Order of calving not correct
    cows_df['check'].notnull().astype(int) == 1) #correct orders of ins.
]
print( f'First cleaning is finished' )
#Observations that DON'T fulfill every condition are collected
data_not_used = cows_df[(
    cows_df['herd'].notnull().astype(int) == 0) | (  #herd missing
    cows_df['birth'].notnull().astype(int) == 0) | ( #no birth year
    cows_df['wrong'].notnull().astype(int) == 1) | ( #AFC or AFI wrong
    cows_df['wrong1'].notnull().astype(int) == 1) | ( #first lact wrong
    cows_df['wrong2'].notnull().astype(int) == 1) | ( #second lact wrong
    cows_df['wrong3'].notnull().astype(int) == 1) | ( #third lact wrong
    cows_df['ins_lact'] == 99.0) | (  #ins did not register on a lactation
    cows_df['ins_lact'] == 88.0) & ( #ins happens before 2008
    cows_df['ins_lact'] == 77.0) & ( #ins has a comment
    cows_df['no_calv'] == 9.0) & (  #Order of calving not correct
    cows_df['check'].notnull().astype(int) == 0)
]
#data_not_used.to_excel("../data/data_not_used.xlsx", index=False)

#Dropping unused columns
data_use = data_use.drop(
    ['wrong', 'wrong1', 'wrong2', 'wrong3', 'check', 'ins_lact', 'no_calv',
    'last_h','last_1','last_2','last_3'], axis = 1)
#---------------------------------------------------------------------------

#---------------------------------------------------------------------------
#Filling in for missing values for technician in heifer ins
data_use['tech_h'] = data_use['tech_h'].fillna(0, downcast='infer')
#Count no of obs for each tech
data_use['tech_h_c'] = data_use.groupby('tech_h')['tech_h'].transform('count')
#Delete if less than 3
data_use = data_use[(data_use['tech_h_c'] > 2) ]
#---------------------------------------------------------------------------
#Fixed effects - Age at first ins in MONTHS - Age at calving in MONTHS
data_use[['AGEi_h','AGEc_1','AGEc_2','AGEc_3']] = data_use[
    ['AGEi_h','AGEc_1','AGEc_2','AGEc_3']
    ].apply(
    lambda s: (s / 30.5).apply(np.ceil).fillna(0).astype(int))
#Counting how many cows are in each age group
data_use['age0'] = data_use.groupby('AGEi_h')['AGEi_h'].transform('count')
data_use['age1'] = data_use.groupby('AGEc_1')['AGEc_1'].transform('count')
data_use['age2'] = data_use.groupby('AGEc_2')['AGEc_2'].transform('count')
data_use['age3'] = data_use.groupby('AGEc_3')['AGEc_3'].transform('count')
#Delete rows that are less then 3 in a group
data_use = data_use[
    (data_use['age0'] > 2) &
    (data_use['age1'] > 2) &
    (data_use['age2'] > 2) &
    (data_use['age3'] > 2)
]
#---------------------------------------------------------------------------

#---------------------------------------------------------------------------
#This is a function to create herd x year group fixed effect
#If cows are fewer than 3 in a group the function tries to combine with group
#above or below WITHIN SAME HERD
#---------------------------------------------------------------------------
def hy_grouping(element, df, col, group, df1):
    tdf = []
    for herd, data in df.groupby( element ):
        # get counts and assign initial groups
        counts = data[ col ].value_counts().sort_index().to_frame()
        counts[ 'group' ] = range( counts.shape[ 0 ] )

        while True:
            gcounts = counts.groupby( 'group' ).sum()[ col ]  # group counts
            change = gcounts[ gcounts.values < 4 ]  # groups with too few

            if change.shape[ 0 ] == 0:
                # no changes, exit
                break

            # check how to merge groups
            cgroup = change.index.min()
            groups = gcounts.index.values
            g_ind = list( groups ).index( cgroup )
            if ( g_ind + 1 ) < groups.shape[ 0 ]:
                # merge forward
                ngroup = groups[ g_ind + 1 ]

            elif g_ind > 0:
                # merge backward
                ngroup = groups[ g_ind - 1 ]

            else:
                # no groups to merge
                print( f'Can not merge element {element}' )
                break

            counts.loc[ counts[ 'group' ] == cgroup, 'group' ] = ngroup

        # assign groups
        for ind, gdata in counts.iterrows():
            data.loc[ data[ col ] == ind, 'group' ] = gdata[ 'group' ]

        tdf.append( data )

    tdf = pd.concat( tdf )

    tdf[ group ] = tdf[ element ].astype( 'str' ) + tdf[ 'group' ].astype( int ).astype( str )

    df1 = pd.merge(left=df1, right=tdf[['id', group]], on='id',
        how='outer').fillna(0, downcast='infer')

    return df1
#---------------------------------------------------------------------------
#---------------------------------------------------------------------------

#Creating year columns for herd-year fixed effect
data_use[['BY','C1','C2','C3']] = data_use[
    ['birth','calv1','calv2','calv3']
    ].apply(
    lambda s: s.dt.strftime('%Y'))

#Create a dataframe to group herd-year groups
ids = data_use['id'].copy()
herd_by = data_use[['id','herd','birth','BY','first_h']].copy()
herd_c1 = data_use[['id','herd','calv1','C1','first_1']].copy()
herd_c2 = data_use[['id','herd','calv2','C2','first_2']].copy()
herd_c3 = data_use[['id','herd','calv3','C3','first_3']].copy()

#Only include relevant rows
herd_by = herd_by.loc[(herd_by['herd'].notnull().astype(int) == 1) &
    (herd_by['birth'].notnull().astype(int) == 1) &
    (herd_by['first_h'].notnull().astype(int) == 1)]

herd_c1 = herd_c1.loc[(herd_c1['herd'].notnull().astype(int) == 1) &
    (herd_c1['calv1'].notnull().astype(int) == 1) &
    (herd_c1['first_1'].notnull().astype(int) == 1)]

herd_c2 = herd_c2.loc[(herd_c2['herd'].notnull().astype(int) == 1) &
    (herd_c2['calv2'].notnull().astype(int) == 1) &
    (herd_c2['first_2'].notnull().astype(int) == 1)]

herd_c3 = herd_c3.loc[(herd_c3['herd'].notnull().astype(int) == 1) &
    (herd_c3['calv3'].notnull().astype(int) == 1) &
    (herd_c3['first_3'].notnull().astype(int) == 1)]

#Sort the dataframes by relevant date
herd_by = herd_by.sort_values(by=['herd','birth'])
herd_c1 = herd_c1.sort_values(by=['herd','calv1'])
herd_c2 = herd_c2.sort_values(by=['herd','calv2'])
herd_c3 = herd_c3.sort_values(by=['herd','calv3'])

#---------------------------------------------------------------------------
#Calling function above to create herd-year groups in all lactations
#---------------------------------------------------------------------------
print( f'Starting with herd x birth year' )
ids = hy_grouping('herd', herd_by, 'BY', 'HBY', ids)

print( f'Starting with herd x calving year 1' )
ids = hy_grouping('herd', herd_c1, 'C1', 'HC1', ids)

print( f'Starting with herd x calving year 2' )
ids = hy_grouping('herd', herd_c2, 'C2', 'HC2', ids)

print( f'Starting with herd x calving year 3' )
ids = hy_grouping('herd', herd_c3, 'C3', 'HC3', ids)

#---------------------------------------------------------------------------
#Merging herd-year groups with main dataframe
data_use = pd.merge(left=data_use, right=ids, on='id', how='left')
#---------------------------------------------------------------------------

#Counting how many cows are in each herd-year group
data_use['HBY_c'] = data_use.groupby('HBY')['HBY'].transform('count')
data_use['HC1_c'] = data_use.groupby('HC1')['HC1'].transform('count')
data_use['HC2_c'] = data_use.groupby('HC2')['HC2'].transform('count')
data_use['HC3_c'] = data_use.groupby('HC3')['HC3'].transform('count')
#Delete rows that are alone in a group
data_use = data_use[
    (data_use['HBY_c'] > 2) &
    (data_use['HC1_c'] > 2) &
    (data_use['HC2_c'] > 2) &
    (data_use['HC3_c'] > 2)
]

#---------------------------------------------------------------------------
#Creating year columns for ins-year-month fixed effect
data_use[['IY0','IY1','IY2','IY3']] = data_use[
    ['first_h','first_1','first_2','first_3']
    ].apply(
    lambda s: s.dt.strftime('%Y').replace('NaT', '0').astype(int))
data_use[['IM0','IM1','IM2','IM3']] = data_use[
    ['first_h','first_1','first_2','first_3']
    ].apply(
    lambda s: s.dt.strftime('%m').replace('NaT', '0').astype(int))
#---------------------------------------------------------------------------
#Create a dataframe for ins-year-month fixed effect
ids = data_use['id'].copy()
ym0 = data_use[['id','IY0','IM0']].copy()
ym1 = data_use[['id','IY1','IM1']].copy()
ym2 = data_use[['id','IY2','IM2']].copy()
ym3 = data_use[['id','IY3','IM3']].copy()

#Only include relevant rows
ym0 = ym0.loc[(ym0['IY0'] > 0)]
ym1 = ym1.loc[(ym1['IY1'] > 0)]
ym2 = ym2.loc[(ym2['IY2'] > 0)]
ym3 = ym3.loc[(ym3['IY3'] > 0)]
print(ym0.iloc[10000:10015])
print(ym0.info())

#Sort the dataframes by relevant date
ym0 = ym0.sort_values(by=['IY0','IM0'])
ym1 = ym1.sort_values(by=['IY1','IM1'])
ym2 = ym2.sort_values(by=['IY2','IM2'])
ym3 = ym3.sort_values(by=['IY3','IM3'])

#---------------------------------------------------------------------------
#Calling function above to create ins-year-month fixed effect
#---------------------------------------------------------------------------
print( f'Starting with ins year x month 0' )
ids = hy_grouping('IY0', ym0, 'IM0', 'IYM0', ids)
print( f'Starting with ins year x month 1' )
ids = hy_grouping('IY1', ym1, 'IM1', 'IYM1', ids)
print( f'Starting with ins year x month 2' )
ids = hy_grouping('IY2', ym2, 'IM2', 'IYM2', ids)
print( f'Starting with ins year x month 3' )
ids = hy_grouping('IY3', ym3, 'IM3', 'IYM3', ids)

#---------------------------------------------------------------------------
#Merging herd-year groups with main dataframe
data_use = pd.merge(left=data_use, right=ids, on='id', how='left')
#---------------------------------------------------------------------------

#Counting how many cows are in each  ins-year-month group
data_use['IYM0_c'] = data_use.groupby('IYM0')['IYM0'].transform('count')
data_use['IYM1_c'] = data_use.groupby('IYM1')['IYM1'].transform('count')
data_use['IYM2_c'] = data_use.groupby('IYM2')['IYM2'].transform('count')
data_use['IYM3_c'] = data_use.groupby('IYM3')['IYM3'].transform('count')
#Delete rows that are less then 3
data_use = data_use[
    (data_use['IYM0_c'] > 2) &
    (data_use['IYM1_c'] > 2) &
    (data_use['IYM2_c'] > 2) &
    (data_use['IYM3_c'] > 2)
]
#---------------------------------------------------------------------------

#Filling in missin values for DMU, -999.0 for reals
#Real columns
realc = ['CRh','ICF1','ICF2','ICF3','IFL1','IFL2','IFL3']
data_use[realc] = data_use[realc].fillna(-999.0)

#---------------------------------------------------------------------------
#File with code numbers for DMU runs
#---------------------------------------------------------------------------
code_df = pd.read_csv(
    "../data/id_code.txt",
    header=None,
    sep = ' ',
    names=['id','code_id']
    )

data_use = pd.merge(left=data_use, right=code_df, on='id', how='left')

data_use = data_use.sort_values(by=['code_id'])
#---------------------------------------------------------------------------

#Creating the DMU datafile
dmu_fertility = data_use[['code_id','HBY','HC1','HC2','HC3','IYM0','IYM1','IYM2',
    'IYM3','AGEi_h','AGEc_1','AGEc_2','AGEc_3','tech_h',
    'CRh','ICF1','ICF2','ICF3','IFL1','IFL2','IFL3']].copy()

# DMU datafile
dmu_fertility.to_csv("../data/dmu_fertilitynew2.txt", index=False, header=False, sep=' ')

# # This is code to create a datafile to be used in some statistical analyses.
# # -----------------------------------------------------------------------
# #Basic statistics
# fertility_stat = data_use[['id','BY','no_calv',
#     'AGEi_h','AGEc_1','AGEc_2','AGEc_3','tech_h',
#     'T_h','T_1','T_2','T_3',
#     'gest1','gest2','gest3','CI12','CI23','CI34',
#     'CRh','ICF1','ICF2','ICF3','IFL1','IFL2','IFL3']].copy()
#
# fertility_stat[
#     ['T_h','T_1','T_2','T_3','gest1','gest2','gest3','CI12','CI23','CI34',]
#     ] = fertility_stat[
#     ['T_h','T_1','T_2','T_3','gest1','gest2','gest3','CI12','CI23','CI34',]
#     ].fillna(-999.0)
# #Basic statistics datafile
# fertility_stat.to_csv("../data/fertility_stat.txt", index=False, header=False, sep=' ')


#print(cows_df.iloc[50000:50015])
print(data_use.iloc[50000:50015])
print(cows_df.info())
print(data_use.info())
# print(data_not_used.info())
#print(cows_df.columns.tolist())
#print(data_use['id'].nunique())
#print(data_not_used['id'].nunique())
#print(data_use.AGEc_3.unique())
