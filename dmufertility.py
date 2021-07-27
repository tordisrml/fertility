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
    )
#---------------------------------------------------------------------------
#Datafile 2, info about cows. One line for every cow.
#---------------------------------------------------------------------------
cows_df = pd.read_csv(
    "../data/gripalisti.csv",
    header=None,
    sep = '\t',
    names=['id','herd','birth','death','calv1','calv2','calv3','calv4']
    )
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
#---------------------------------------------------------------------------

#---------------------------------------------------------------------------
# In which lactation does the ins occur?
# --------------------------------------
# Heifers who are inseminated but do not calve
df.loc[
(df['no_calv'] == 0),
'ins_lact'] = 7
#Heifers that calve inseminations
df.loc[
(df['no_calv'] > 0) & (df['ins'] < df['calv1']),
'ins_lact'] = 0
#Lactations 1
df.loc[
(df['no_calv'] >= 1) & (df['ins'] > df['calv1']) & (df['ins'] < df['calv2']),
'ins_lact'] = 1
df.loc[
(df['no_calv'] == 1) & (df['ins'] > df['calv1']),
'ins_lact'] = 1
#Lactations 2
df.loc[
(df['no_calv'] >= 2) & (df['ins'] > df['calv2']) & (df['ins'] < df['calv3']),
'ins_lact'] = 2
df.loc[
(df['no_calv'] == 2) & (df['ins'] > df['calv2']),
'ins_lact'] = 2
#Lactations 3
df.loc[
(df['no_calv'] >= 3) & (df['ins'] > df['calv3']) & (df['ins'] < df['calv4']),
'ins_lact'] = 3
df.loc[
(df['no_calv'] == 3) & (df['ins'] > df['calv3']),
'ins_lact'] = 3

#Wrong ins located and marked as 99
df.loc[
(df['ins_lact'] != 0.0) & (df['ins_lact'] != 7.0) & (df['ins_lact'] != 1.0)
& (df['ins_lact'] != 2.0) & (df['ins_lact'] != 3.0),
'ins_lact'] = 99.0
#Ins that happen before 2008 are marked as 88
df.loc[
(df['ins'] < '2001-01-01'),
'ins_lact'] = 88.0
#Ins have comments located are marked as 77
df.loc[
(df['comment'].notnull().astype(int) == 1),
'ins_lact'] = 77.0
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


#When the following code runs this error messege apprears, the code still works!

# See the caveats in the documentation: http://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html#returning-a-view-versus-a-copy
#   lact2_df['T'] = lact2_df.groupby('id')['id'].transform('count')
# frjosemi.py:187: SettingWithCopyWarning:
# A value is trying to be set on a copy of a slice from a DataFrame.
# Try using .loc[row_indexer,col_indexer] = value instead

#---------------------------------------------------------------------------
#Heifers
#The number of each ins is counted and the total number of ins
heifers_df['T'] = heifers_df.groupby('id')['id'].transform('count')
heifers_df['No'] = heifers_df.groupby('id')['id'].cumcount() + 1
#The last ins
heifers_df.loc[
(heifers_df['T'] == heifers_df['No']),
'last_h'] = heifers_df['ins']
#Tota number of heifer ins
heifers_df.loc[
(heifers_df['T'] == heifers_df['No']),
'T_h'] = heifers_df['T']
#First ins
heifers_df.loc[
(heifers_df['No'] == 1),
'first_h'] = heifers_df['ins']
#First heifer tech
heifers_df.loc[
(heifers_df['No'] == 1),
'tech_h'] = heifers_df['tech']
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
lact1_df['T'] = lact1_df.groupby('id')['id'].transform('count')
lact1_df['No'] = lact1_df.groupby('id')['id'].cumcount() + 1
#The last ins
lact1_df.loc[
(lact1_df['T'] == lact1_df['No']),
'last_1'] = lact1_df['ins']
#Tota number of lact1 ins
lact1_df.loc[
(lact1_df['T'] == lact1_df['No']),
'T_1'] = lact1_df['T']
#First ins
lact1_df.loc[
(lact1_df['No'] == 1),
'first_1'] = lact1_df['ins']
#First lact1 tech
lact1_df.loc[
(lact1_df['No'] == 1),
'tech_1'] = lact1_df['tech']
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
lact2_df['T'] = lact2_df.groupby('id')['id'].transform('count')
lact2_df['No'] = lact2_df.groupby('id')['id'].cumcount() + 1
#The last ins
lact2_df.loc[
(lact2_df['T'] == lact2_df['No']),
'last_2'] = lact2_df['ins']
#Tota number of lact2 ins
lact2_df.loc[
(lact2_df['T'] == lact2_df['No']),
'T_2'] = lact2_df['T']
#First ins
lact2_df.loc[
(lact2_df['No'] == 1),
'first_2'] = lact2_df['ins']
#First lact2 tech
lact2_df.loc[
(lact2_df['No'] == 1),
'tech_2'] = lact2_df['tech']
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
lact3_df['T'] = lact3_df.groupby('id')['id'].transform('count')
lact3_df['No'] = lact3_df.groupby('id')['id'].cumcount() + 1
#The last ins
lact3_df.loc[
(lact3_df['T'] == lact3_df['No']),
'last_3'] = lact3_df['ins']
#Tota number of lact3 ins
lact3_df.loc[
(lact3_df['T'] == lact3_df['No']),
'T_3'] = lact3_df['T']
#First ins
lact3_df.loc[
(lact3_df['No'] == 1),
'first_3'] = lact3_df['ins']
#First lact3 tech
lact3_df.loc[
(lact3_df['No'] == 1),
'tech_3'] = lact3_df['tech']
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

#HY groups????
#Double ins?????

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
cows_df.loc[
(cows_df['T_h'] > 8) ,
'wrong'] = 'e'
cows_df.loc[
(cows_df['T_1'] > 8) ,
'wrong1'] = 'e'
cows_df.loc[
(cows_df['T_2'] > 8) ,
'wrong2'] = 'e'
cows_df.loc[
(cows_df['T_3'] > 8) ,
'wrong3'] = 'e'
# f) ICF 20-230 days
cows_df.loc[
(cows_df['ICF1'] < 20) | (cows_df['ICF1'] > 230),
'wrong1'] = 'f'
cows_df.loc[
(cows_df['ICF2'] < 20) | (cows_df['ICF2'] > 230),
'wrong2'] = 'f'
cows_df.loc[
(cows_df['ICF3'] < 20) | (cows_df['ICF3'] > 230),
'wrong3'] = 'f'
# g) IFL 0-365 days
cows_df.loc[
(cows_df['IFL1'] > 365),
'wrong1'] = 'g'
cows_df.loc[
(cows_df['IFL2'] > 365),
'wrong2'] = 'g'
cows_df.loc[
(cows_df['IFL3'] > 365),
'wrong3'] = 'g'

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
# #Creating fixed effect Herd - Birth year / Calving years
# s = cows_df['herd'] * 100
# cows_df['H_BY'] = s + cows_df['birth'].dt.year
# cows_df['HC1'] = s + cows_df['calv1'].dt.year
# cows_df['HC2'] = s + cows_df['calv2'].dt.year
# cows_df['HC3'] = s + cows_df['calv3'].dt.year
# cows_df[['H_BY','HC1','HC2','HC3']] = cows_df[
#     ['H_BY','HC1','HC2','HC3']].fillna(0, downcast='infer')


#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!11
#ATH AÐ BREYTA KANNSKI Í LOCATE ÞAR SEM CALV ER EKKI 0 EÐA NaT
#ANNARS VEÐRUR 00 ÞAÐ SAMA OG ÞEGAR GRIPIR ERU
# EÐA NEI, ÞAÐ EIGA ENGIR GRIPIR EKKI AÐ VERA MEÐ HERD OG BIRTH YEAR
#OG ALLAR SÆÐINGAR EIGA AÐ VERA EFTIR 2001
#Creating fixed effect Herd - Birth year / Calving years
s = cows_df['herd'] * 100
cows_df['H_BY'] = s + cows_df['birth'].dt.strftime('%y').replace('NaT', '0').astype(int)
cows_df['HC1'] = s + cows_df['calv1'].dt.strftime('%y').replace('NaT', '0').astype(int)
cows_df['HC2'] = s + cows_df['calv2'].dt.strftime('%y').replace('NaT', '0').astype(int)
cows_df['HC3'] = s + cows_df['calv3'].dt.strftime('%y').replace('NaT', '0').astype(int)
cows_df[['H_BY','HC1','HC2','HC3']] = cows_df[
    ['H_BY','HC1','HC2','HC3']].fillna(0, downcast='infer')

#Creating first Insemanation year - month fixed effect
cows_df[['IYM0','IYM1','IYM2','IYM3']] = cows_df[
    ['first_h','first_1','first_2','first_3']
    ].apply(
    lambda s: s.dt.strftime('%Y%m').replace('NaT', '0').astype(int))

#Filling in for missing values for technician in heifer ins
cows_df['tech_h'] = cows_df['tech_h'].fillna(0, downcast='infer')

#Fixed effects - Age at first ins in MONTHS - Age at calving in MONTHS
cows_df[['AGEi_h','AGEc_1','AGEc_2','AGEc_3']] = cows_df[
    ['AGEi_h','AGEc_1','AGEc_2','AGEc_3']
    ].apply(
    lambda s: (s / 30.5).apply(np.ceil).fillna(0).astype(int))
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


#Counting number of cows per Herd-year class
data_use['H_BY_c'] = data_use.groupby('H_BY')['H_BY'].transform('count')
data_use['HC1_c'] = data_use.groupby('HC1')['HC1'].transform('count')
data_use['HC2_c'] = data_use.groupby('HC2')['HC2'].transform('count')
data_use['HC3_c'] = data_use.groupby('HC3')['HC3'].transform('count')
#Locate and mark cows that are alone in herd year class
data_use.loc[
(data_use['H_BY_c'] == 1) |
(data_use['HC1_c'] == 1) |
(data_use['HC2_c'] == 1) |
(data_use['HC3_c'] == 1)
,'check2'] = 1
#Only use cows that are not alone in herd-year class
data_use2 = data_use[(
    data_use['check2'].notnull().astype(int) == 0)
]

# #Checks again on herd-year classes
# data_use2['H_BY_c'] = data_use2.groupby('H_BY')['H_BY'].transform('count')
# data_use2['HC1_c'] = data_use2.groupby('HC1')['HC1'].transform('count')
# data_use2['HC2_c'] = data_use2.groupby('HC2')['HC2'].transform('count')
# data_use2['HC3_c'] = data_use2.groupby('HC3')['HC3'].transform('count')
# data_use2.loc[
# (data_use2['H_BY_c'] == 1) |
# (data_use2['HC1_c'] == 1) |
# (data_use2['HC2_c'] == 1) |
# (data_use2['HC3_c'] == 1)
# ,'check3'] = 1
# #Observations that DON'T fulfill every condition are collected
# data_use3 = data_use2[(
#     data_use2['check3'].notnull().astype(int) == 0)
# ]

#Filling in missin values for DMU, -999.0 for reals
#Real columns
realc = ['CRh','ICF1','ICF2','ICF3','IFL1','IFL2','IFL3']
data_use2[realc] = data_use2[realc].fillna(-999.0)

#---------------------------------------------------------------------------
#File with code numbers for DMU runs
#---------------------------------------------------------------------------
code_df = pd.read_csv(
    "../data/id_code.txt",
    header=None,
    sep = ' ',
    names=['id','code_id']
    )

data_use2 = pd.merge(left=data_use2, right=code_df, on='id', how='left')

# ---- AIS AS A FIXED EFFECT FOR IFL??????
# ----- ATHUGA HERD SIZE

#---------------------------------------------------------------------------
#Creating the DMU datafile
dmu_fertility = data_use2[['code_id','H_BY','HC1','HC2','HC3','IYM0','IYM1','IYM2',
    'IYM3','AGEi_h','AGEc_1','AGEc_2','AGEc_3','tech_h',
    'CRh','ICF1','ICF2','ICF3','IFL1','IFL2','IFL3']].copy()
#,'H_BY_c','HC1_c','HC2_c','HC3_c'
#DMU datafile
dmu_fertility.to_csv("../data/dmu_fertility2001.txt", index=False, header=False, sep=' ')



#This is code to create a datafile to be used in some statistical analyses.
#-----------------------------------------------------------------------
# #Basic statistics
# data_use['birthy'] = data_use[
#     ['birth']
#     ].apply(
#     lambda s: s.dt.strftime('%Y').replace('NaT', '0').astype(int))
#
# fertility_stat = data_use[['id','birthy','no_calv',
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
print(dmu_fertility.iloc[50000:50015])
print(cows_df.info())
print(data_use2.info())
print(data_not_used.info())
#print(cows_df.columns.tolist())
#print(data_use['id'].nunique())
#print(data_not_used['id'].nunique())
#print(data_use.AGEc_3.unique())
