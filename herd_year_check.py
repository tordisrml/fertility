import pandas as pd
import numpy as np

#This is a program to check the number of cows per herd-year group 

dmu_fertility = pd.read_csv(
    'dmu_fertility2001.txt',
    header=None,
    sep = ' ',
    names=['code_id','H_BY','HC1','HC2','HC3','IYM0','IYM1','IYM2',
        'IYM3','AGEi_h','AGEc_1','AGEc_2','AGEc_3','tech_h',
        'CRh','ICF1','ICF2','ICF3','IFL1','IFL2','IFL3','H_BY_c','HC1_c','HC2_c','HC3_c']
    )


dmu_fertility['H_BY_c'] = dmu_fertility.groupby('H_BY')['H_BY'].transform('count')
dmu_fertility['HC1_c'] = dmu_fertility.groupby('HC1')['HC1'].transform('count')
dmu_fertility['HC2_c'] = dmu_fertility.groupby('HC2')['HC2'].transform('count')
dmu_fertility['HC3_c'] = dmu_fertility.groupby('HC3')['HC3'].transform('count')



dmu_fertility.loc[
(dmu_fertility['H_BY_c'] == 1) |
(dmu_fertility['HC1_c'] == 1) |
(dmu_fertility['HC2_c'] == 1) |
(dmu_fertility['HC3_c'] == 1)
,'check'] = 1


print(dmu_fertility.iloc[50000:50015])
print(dmu_fertility.info())
#print(dmu_fertility.H_BY_c.unique())

from collections import Counter
print('H_BY_c')
print(Counter(dmu_fertility['H_BY_c']).keys()) # equals to list(set(words))
print(Counter(dmu_fertility['H_BY_c']).values()) # counts the elements' frequency
print('HC1_c')
print(Counter(dmu_fertility['HC1_c']).keys()) # equals to list(set(words))
print(Counter(dmu_fertility['HC1_c']).values()) # counts the elements' frequency
print('HC2_c')
print(Counter(dmu_fertility['HC2_c']).keys()) # equals to list(set(words))
print(Counter(dmu_fertility['HC2_c']).values()) # counts the elements' frequency
print('HC3_c')
print(Counter(dmu_fertility['HC3_c']).keys()) # equals to list(set(words))
print(Counter(dmu_fertility['HC3_c']).values()) # counts the elements' frequency
