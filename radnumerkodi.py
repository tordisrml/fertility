import pandas as pd
import numpy as np

#---------------------------------------------------------------------------
#Datafile 1, info about inseminations. One line for every ins.
#---------------------------------------------------------------------------
df = pd.read_csv(
    "../data/dmu_fertilitynew2.txt",
    header=None,
    sep = ' ',
    names=['code_id','HBY','HC1','HC2','HC3','IYM0','IYM1','IYM2',
        'IYM3','AGEi_h','AGEc_1','AGEc_2','AGEc_3','tech_h',
        'CRh','ICF1','ICF2','ICF3','IFL1','IFL2','IFL3']
    )


code_df = pd.read_csv(
    "../data/id_code2.txt",
    header=None,
    sep = ' ',
    names=['id','code_id','sex']
    )

# ped = pd.read_csv(
#     "../data/dmu_ped.ped",
#     header=None,
#     sep = ' ',
#     names=['id','dam','sire']
#     )


df = pd.merge(left=code_df, right=df, on='code_id', how='outer')
# df = pd.merge(left=df, right=ped, on='id', how='left')

df['BY'] = (df.id.astype(str).str[:4]).astype(int)

df.loc[(df['BY'] == 2017) & (df['IYM1'] > 0) ,'stada'] = 1
df.loc[(df['BY'] == 2016) & (df['IYM1'] > 0) ,'stada'] = 1
df.loc[(df['BY'] == 2015) & (df['IYM1'] > 0) ,'stada'] = 1
df.loc[(df['BY'] == 2014) & (df['IYM1'] > 0) ,'stada'] = 1
df.loc[(df['BY'] == 2013) & (df['IYM1'] > 0) ,'stada'] = 1
df.loc[(df['BY'] == 2012) & (df['IYM1'] > 0) ,'stada'] = 1

df.loc[(df['BY'] == 2017) & (df['IYM1'] == 0) ,'stada'] = 0
df.loc[(df['BY'] == 2016) & (df['IYM1'] == 0) ,'stada'] = 0
df.loc[(df['BY'] == 2015) & (df['IYM1'] == 0) ,'stada'] = 0
df.loc[(df['BY'] == 2014) & (df['IYM1'] == 0) ,'stada'] = 0
df.loc[(df['BY'] == 2013) & (df['IYM1'] == 0) ,'stada'] = 0
df.loc[(df['BY'] == 2012) & (df['IYM1'] == 0) ,'stada'] = 0

df.loc[(df['BY'] > 2017) | (df['BY'] < 2012) ,'stada'] = 0

df.loc[
(df['IYM1'] > 0) &
(df['IYM2'] > 0) &
(df['IYM3'] > 0)
,'norec'] = 3

df.loc[
(df['IYM1'] > 0) &
(df['IYM2'] > 0) &
(df['IYM3'] == 0)
,'norec'] = 2

df.loc[
(df['IYM1'] > 0) &
(df['IYM2'] == 0) &
(df['IYM3'] == 0)
,'norec'] = 1

df.loc[
(df['IYM1'] == 0) &
(df['IYM2'] == 0) &
(df['IYM3'] == 0)
,'norec'] = 0


radnrkodi = df[['id','code_id','stada','norec','HC1','IYM1', 'AGEc_1','sex']].fillna(0, downcast='infer')

print(radnrkodi.iloc[503000:503015])
print(df.info())
print(radnrkodi.info())

print(df['stada'].value_counts())
print(df['HC1'].value_counts())
print(df['IYM1'].value_counts())
print(df['AGEc_1'].value_counts())

radnrkodi.to_csv("../data/radnrkodix.txt", index=False, header=False, sep=' ')
np.savetxt('../data/radnrkodi.txt', radnrkodi, fmt='%+15s %+8s %+2s %+2s %+9s %+9s %+9s %+1s ')
