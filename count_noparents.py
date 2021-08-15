#This is a program that counts how many ghost parents there are in the
#Pedigree file
#Thordis Thorarinsdottir 2021

import pandas as pd
import numpy as np
from collections import Counter

#Reading in the pedigree
ped = pd.read_csv(
    "../data/dmu_ped.ped",
    header=None,
    sep=' ',
    names=['id','dam','sire']
    )

#Make birth year from id number an integer
ped['BY'] = (ped.id.astype(str).str[:4]).astype(int)

#Locating animals that have no dam
ped.loc[
(ped['dam'] == 0),
'nodam'] = ped['BY']
#Locating animals that have no sire
ped.loc[
(ped['sire'] == 0),
'nosire'] = ped['BY']

#Creating a new dataframe for animals with no mother
nodam = ped[ (ped['nodam'].notnull().astype(int) == 1)]
#Drop all columns except for nodam
nodam = nodam.drop(['id', 'dam', 'sire', 'BY', 'nosire'], axis = 1)
#Renaming the nodam column to BY (birth year)
nodam.columns = ['BY']
#Counting the number of times each BY occurs
nodam.loc[:,'nodam_c'] = nodam.groupby('BY')['BY'].transform('count')
#Dropping the duplicates so now there is a list for each year and how many
#ghost parents there are
nodam = nodam.drop_duplicates()

# nodam.to_csv("../data/nodam.csv", index=False, header=False, sep=' ')

#Same as above!
nosire = ped[(ped['nosire'].notnull().astype(int) == 1) ]
nosire = nosire.drop(['id', 'dam', 'sire', 'BY', 'nodam'], axis = 1)
nosire.columns = ['BY']
nosire.loc[:, 'nosire_c' ] = nosire.groupby('BY')['BY'].transform('count')
nosire = nosire.drop_duplicates()

# Merging the two dataframes so each BY column is followed by the numer of
# missing sires and number of missing dams
noparents = pd.merge(left=nosire, right=nodam, on='BY', how='outer').fillna(0, downcast='infer')

#Counting the number of animals born per year
ped = ped.drop(['id', 'dam', 'sire', 'nosire', 'nodam'], axis = 1)
ped.loc[:,'BY_c'] = ped.groupby('BY')['BY'].transform('count')
ped = ped.drop_duplicates()

#Merging the number of animals born each year with the noparents dataframe
noparents = pd.merge(left=noparents, right=ped, on='BY', how='outer').fillna(0, downcast='infer')

# # nosire.to_csv("../data/nosire.csv", index=False, header=False, sep=' ')
#
noparents.to_excel("../data/noparents.xlsx", index=False, header=False)

print(noparents.iloc[100:115])
print(noparents.info())
