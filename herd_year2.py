import pandas as pd
import numpy as np
import datetime


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

cows_df[['birth','death','calv1','calv2','calv3','calv4']] = cows_df[
    ['birth','death','calv1','calv2','calv3','calv4']
    ].apply(
    lambda x: pd.to_datetime(x, format='%Y%m%d'))


#Creating fixed effect Herd - Birth year / Calving years
s = cows_df['herd'] * 100
#herd - birth year
cows_df.loc[
(cows_df['herd'].notnull().astype(int) == 1) &
(cows_df['birth'].notnull().astype(int) == 1),
'H_BY'] = (s + cows_df['birth'].dt.strftime('%y').replace('NaT', '0').astype(int))
#herd - calving year 1
cows_df.loc[
(cows_df['herd'].notnull().astype(int) == 1) &
(cows_df['calv1'].notnull().astype(int) == 1),
'HC1'] = (s + cows_df['calv1'].dt.strftime('%y').replace('NaT', '0').astype(int))
#herd - calving year 2
cows_df.loc[
(cows_df['herd'].notnull().astype(int) == 1) &
(cows_df['calv2'].notnull().astype(int) == 1),
'HC2'] = (s + cows_df['calv2'].dt.strftime('%y').replace('NaT', '0').astype(int))
#herd - calving year 3
cows_df.loc[
(cows_df['herd'].notnull().astype(int) == 1) &
(cows_df['calv3'].notnull().astype(int) == 1),
'HC3'] = (s + cows_df['calv3'].dt.strftime('%y').replace('NaT', '0').astype(int))
#Filling emty cells with 0 and setting as integers
cows_df[['H_BY','HC1','HC2','HC3']] = cows_df[
    ['H_BY','HC1','HC2','HC3']].fillna(0, downcast='infer')

herd_by = cows_df[['id','herd','birth','H_BY',]].copy()


#Creating first Insemanation year - month fixed effect
herd_by[['IYM0']] = herd_by[
    ['first_h','first_1','first_2','first_3']
    ].apply(
    lambda s: s.dt.strftime('%Y%m').replace('NaT', '0').astype(int))

print(herd_by.iloc[20000:20015])
print(herd_by.info())
