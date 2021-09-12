import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import seaborn
from scipy import stats
from scipy.stats import spearmanr

df = pd.read_csv(
    "../data/heildareinkunn.txt",
    header=None,
    sep = ' ',
    names=['id','afurdamat', 'frjosemi', 'frumutala', 'jugur',
        'spenar', 'mjaltir', 'skap', 'ending','heildareinkunn']
    )

nytt = pd.read_csv(
    "../data/allblup10020210912.txt",
    header=None,
    sep = ' ',
    names=['id', 'CR0',
        'ICF1','ICF2','ICF3','ICF',
        'IFL1','IFL2','IFL3','IFL',
        'CI12','CI23','CI34', 'CI',
        'fertility_1','fertility_2','fertility_3','frjosemi','new']
    )

# code_df = pd.read_csv(
#     "../data/id_code2.txt",
#     header=None,
#     sep = ' ',
#     names=['id','code_id','sex']
#     )

df = pd.merge(left=df, right=nytt[['id', 'CR0','ICF','IFL', 'new']], on='id')


widths = [15,15,15,12,1,7,20,20]
ped = pd.read_fwf(
    "../data/Pgree_24jun2021.txt",
    widths=widths,
    header=None,
    names=['id','dam','sire','unused','sex','unused2', 'name', 'unused3']
    )
ped = ped.drop(
    ['dam','unused','unused2', 'unused3'], axis = 1)


df = pd.merge(left=df, right=ped, on='id')

df['sire_count'] = df.groupby('sire')['sire'].transform('count')

df.loc[(df['ending'] != 100), 'nyheild'] = (df['afurdamat']*0.36 +
                df['new']*0.10 +
                df['frumutala']*0.08 +
                df['jugur']*0.10 +
                df['spenar']*0.10 +
                df['mjaltir']*0.08 +
                df['skap']*0.08 +
                df['ending']*0.10)
df.loc[(df['ending'] == 100), 'nyheild'] = (df['afurdamat']*0.36 +
                df['new']*0.11 +
                df['frumutala']*0.09 +
                df['jugur']*0.11 +
                df['spenar']*0.13 +
                df['mjaltir']*0.10 +
                df['skap']*0.10 +
                df['ending']*0.0)

df['BY'] = (df.id.astype(str).str[:4]).astype(int)

df2006 = df[df['BY'] > 2006]
dfnaut = df[df['ending'] != 100]
#
# #Correlation heat map for all traits in dataframe!
# plt.figure(figsize=(8,8))
# seaborn.heatmap(dfnaut[['afurdamat', 'frjosemi', 'frumutala', 'jugur',
#     'spenar', 'mjaltir', 'skap', 'ending','heildareinkunn', 'new', 'nyheild']
#     ].corr(), annot=True, cmap='coolwarm')
# plt.title('Fylgni' , fontsize = 20)

# print(df.iloc[500000:500025])
# print(dfnaut.info())
print(df.iloc[50000:50015])
print(df.info())

#Checking spearman correlations,
# rho, p = spearmanr(dfnaut['frjosemi'], dfnaut['new'])
# #This will print out in the terminal
# print(rho)
# print(p)

# plt.show()
#
#
#
dfnaut[['new','nyheild']] = dfnaut[['new','nyheild']].astype(float).round().astype(int)
dfnaut.to_excel("../data/dfnaut20210912.xlsx", index=False, header=True)
