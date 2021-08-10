import pandas as pd
import numpy as np
from collections import Counter

ped = pd.read_csv(
    "../data/dmu_ped.ped",
    header=None,
    sep=' ',
    names=['id','dam','sire']
    )

#Make birth year from id number an integer
ped['BY'] = (ped.id.astype(str).str[:4]).astype(int)

ped.loc[
(ped['dam'] == 0),
'nodam'] = ped['BY']

ped.loc[
(ped['sire'] == 0),
'nosire'] = ped['BY']


nodam = ped[ (ped['nodam'].notnull().astype(int) == 1)]
nodam = nodam.drop(['id', 'dam', 'sire', 'BY', 'nosire'], axis = 1)
nodam.columns = ['BY']
nodam['nodam_c'] = nodam.groupby('BY')['BY'].transform('count')
nodam = nodam.drop_duplicates()

# nodam.to_csv("../data/nodam.csv", index=False, header=False, sep=' ')

nosire = ped[(ped['nosire'].notnull().astype(int) == 1) ]
nosire = nosire.drop(['id', 'dam', 'sire', 'BY', 'nodam'], axis = 1)
nosire.columns = ['BY']
nosire['nosire_c'] = nosire.groupby('BY')['BY'].transform('count')
nosire = nosire.drop_duplicates()


noparents = pd.merge(left=nosire, right=nodam, on='BY', how='outer').fillna(0, downcast='infer')


ped = ped.drop(['id', 'dam', 'sire', 'nosire', 'nodam'], axis = 1)
ped['BY_c'] = ped.groupby('BY')['BY'].transform('count')
ped = ped.drop_duplicates()

noparents = pd.merge(left=noparents, right=ped, on='BY', how='outer').fillna(0, downcast='infer')

# nosire.to_csv("../data/nosire.csv", index=False, header=False, sep=' ')

noparents.to_excel("../data/noparents.xlsx", index=False, header=False)

# print(pednoparents.iloc[100:115])
# print(pednoparents.info())

print(noparents)
