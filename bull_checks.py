#Program to locate bulls that have a certain number of daughters in ped files
#Thordis Thorarinsdottir 2021
import pandas as pd
import numpy as np
from collections import Counter
#-------------------------------------------------------------------
#Reading in id codes to replace in SOL files
code_df = pd.read_csv(
    "../data/id_code.txt",
    header=None,
    sep = ' ',
    names=['id','code_id']
    )
#-------------------------------------------------------------------
#Reading in DMU observation file
df = pd.read_csv(
    "../data/dmu_fertility.txt",
    header=None,
    sep = ' ',
    names=['code_id','H_BY','HC1','HC2','HC3','IYM0','IYM1','IYM2',
        'IYM3','AGEi_h','AGEc_1','AGEc_2','AGEc_3','tech_h',
        'CRh','ICF1','ICF2','ICF3','IFL1','IFL2','IFL3']
    )
#-------------------------------------------------------------------
#Reading pedigree
ped = pd.read_csv(
    "../data/dmu_ped.ped",
    header=None,
    sep = ' ',
    names=['id','dam','sire']
    )
#-------------------------------------------------------------------

#Merging code id file and dataframe
df= pd.merge(left=df[
    ['code_id','CRh','ICF1','ICF2','ICF3','IFL1','IFL2','IFL3']
    ], right=code_df[['id','code_id']], on='code_id', how='left')

#Merging pedigree with df
df= pd.merge(left=df, right=ped[['id','sire']], on='id', how='left')

#Counting the number of offpsring per sire
df['sire_count'] = df.groupby('sire')['sire'].transform('count')

#Locating sires that have more than 50 daughters
sires = df[(
    df['sire_count'] > 50) & (df['sire'] > 0)
]

sires['sire_count'] = sires.groupby('sire')['sire'].transform('count')

#Creating a file with sires that have more than 50 daughters
sires = sires[['sire', 'sire_count']]
sires = sires.sort_values(by=['sire'])
#Delete duplicates
sires = sires.drop_duplicates(subset=['sire'])
sires.to_csv("../data/sire_50.txt", index=False, header=False, sep=' ')


# print(sires.iloc[30000:30015])
print(sires.info())
#This print the values of the sire_count variable in the terminal
# print('sire')
# print(Counter(sires['sire_count']).keys()) # equals to list(set(words))
# print(Counter(sires['sire_count']).values()) # counts the elements' frequency
#
# print(sires['sire'].nunique())
