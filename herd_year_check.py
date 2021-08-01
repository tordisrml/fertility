import pandas as pd
import numpy as np
import datetime

#This is a program to check the number of cows per herd-year group

data_use2 = pd.read_csv(
    '../data/dmu_fertilityHYtest.txt',
    header=None,
    sep = ' ',
    names=['code_id','H_BY','HC1','HC2','HC3','IYM0','IYM1','IYM2',
        'IYM3','AGEi_h','AGEc_1','AGEc_2','AGEc_3','tech_h',
        'CRh','ICF1','ICF2','ICF3','IFL1','IFL2','IFL3']
    )

dmu_fertility = data_use2[['code_id','H_BY','HC1','HC2','HC3']].copy()


dmu_fertility['H_BY_c'] = dmu_fertility.groupby('H_BY')['H_BY'].transform('count')
dmu_fertility['HC1_c'] = dmu_fertility.groupby('HC1')['HC1'].transform('count')
dmu_fertility['HC2_c'] = dmu_fertility.groupby('HC2')['HC2'].transform('count')
dmu_fertility['HC3_c'] = dmu_fertility.groupby('HC3')['HC3'].transform('count')



# dmu_fertility.loc[
# (dmu_fertility['H_BY_c'] < 3) |
# (dmu_fertility['HC1_c'] < 3) |
# (dmu_fertility['HC2_c'] < 3) |
# (dmu_fertility['HC3_c'] < 3)
# ,'check'] = 1


dmu_fertility = dmu_fertility.sort_values(by=['HC1'])


dmu_fertility.loc[
    (dmu_fertility['HC1_c'] < 3),
    'HC1'] = dmu_fertility['HC1'].shift(-1)

dmu_fertility['HC1_c'] = dmu_fertility.groupby('HC1')['HC1'].transform('count')

dmu_fertility.loc[
    (dmu_fertility['HC1_c'] < 3),
    'HC1'] = dmu_fertility['HC1'].shift(-1)
dmu_fertility['HC1_c'] = dmu_fertility.groupby('HC1')['HC1'].transform('count')


dmu_fertility.loc[
    (dmu_fertility['HC1_c'] < 3),
    'HC1'] = dmu_fertility['HC1'].shift(-1)
dmu_fertility['HC1_c'] = dmu_fertility.groupby('HC1')['HC1'].transform('count')

dmu_fertility.loc[
    (dmu_fertility['HC1_c'] < 3),
    'HC1'] = dmu_fertility['HC1'].shift(-1)
dmu_fertility['HC1_c'] = dmu_fertility.groupby('HC1')['HC1'].transform('count')

dmu_fertility.loc[
    (dmu_fertility['HC1_c'] < 3),
    'HC1'] = dmu_fertility['HC1'].shift(-1)
dmu_fertility['HC1_c'] = dmu_fertility.groupby('HC1')['HC1'].transform('count')

dmu_fertility.loc[
    (dmu_fertility['HC1_c'] < 3),
    'HC1'] = dmu_fertility['HC1'].shift(-1)
dmu_fertility['HC1_c'] = dmu_fertility.groupby('HC1')['HC1'].transform('count')

dmu_fertility.loc[
    (dmu_fertility['HC1_c'] < 3),
    'HC1'] = dmu_fertility['HC1'].shift(-1)
dmu_fertility['HC1_c'] = dmu_fertility.groupby('HC1')['HC1'].transform('count')

dmu_fertility.loc[
    (dmu_fertility['HC1_c'] < 3),
    'HC1'] = dmu_fertility['HC1'].shift(-1)
dmu_fertility['HC1_c'] = dmu_fertility.groupby('HC1')['HC1'].transform('count')

dmu_fertility.loc[
    (dmu_fertility['HC1_c'] < 3),
    'HC1'] = dmu_fertility['HC1'].shift(-1)
dmu_fertility['HC1_c'] = dmu_fertility.groupby('HC1')['HC1'].transform('count')

dmu_fertility.loc[
    (dmu_fertility['HC1_c'] < 3),
    'HC1'] = dmu_fertility['HC1'].shift(-1)
dmu_fertility['HC1_c'] = dmu_fertility.groupby('HC1')['HC1'].transform('count')


dmu_fertility.loc[
    (dmu_fertility['HC1_c'] < 3),
    'HC1'] = dmu_fertility['HC1'].shift(-1)
dmu_fertility['HC1_c'] = dmu_fertility.groupby('HC1')['HC1'].transform('count')

#     'H_BYx'].fillna(0, downcast='infer')



# dmu_fertility.loc['H_Bx', 0] = dmu_fertility.loc['H_BY', 0]
#
# for i in range(1, len(dmu_fertility)):
#     dmu_fertility.loc[
#     (dmu_fertility['H_BY_c'] < 3)
#     ,dmu_fertility['H_Bx', i]] = dmu_fertility['H_BY', i-1]


# for i in range(1, len(dmu_fertility)):
#     dmu_fertility.loc[
#     (dmu_fertility['H_BY_c'] < 3)
#     ,dmu_fertility['H_BY']] = dmu_fertility['H_BY', i-1]





print(dmu_fertility.iloc[20000:20015])
print(dmu_fertility.info())
#print(dmu_fertility.H_BY_c.unique())
#
from collections import Counter
# print('H_BY_c')
# print(Counter(dmu_fertility['H_BY_c']).keys()) # equals to list(set(words))
# print(Counter(dmu_fertility['H_BY_c']).values()) # counts the elements' frequency
# print('H_BYx_c')
# print(Counter(dmu_fertility['H_BYx_c']).keys()) # equals to list(set(words))
# print(Counter(dmu_fertility['H_BYx_c']).values()) # counts the elements' frequency

print('HC1_c')
print(Counter(dmu_fertility['HC1_c']).keys()) # equals to list(set(words))
print(Counter(dmu_fertility['HC1_c']).values()) # counts the elements' frequency
# print('HC2_c')
# print(Counter(dmu_fertility['HC2_c']).keys()) # equals to list(set(words))
# print(Counter(dmu_fertility['HC2_c']).values()) # counts the elements' frequency
# print('HC3_c')
# print(Counter(dmu_fertility['HC3_c']).keys()) # equals to list(set(words))
# print(Counter(dmu_fertility['HC3_c']).values()) # counts the elements' frequency


# df = dmu_fertility[['code_id','H_BY','HC1','HC2','HC3','IYM0','IYM1','IYM2',
#     'IYM3','H_BY_c','HC1_c','HC2_c','HC3_c']].copy()
#
# df.to_csv("../data/dmu_herdyearcheck.txt", index=False, header=False, sep=' ')
