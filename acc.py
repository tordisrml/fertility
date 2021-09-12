import pandas as pd
import numpy as np

radnrkodi = pd.read_csv(
    "../data/radnrkodix.txt",
    header=None,
    sep = ' ',
    names=['id','code_id','stada','norec','HC1','IYM1', 'AGEc_1','sex']
    )


ped = pd.read_csv(
    "../data/dmu_ped_code.ped",
    header=None,
    sep = ' ',
    names=['code_id','sire','dam','code_id2']
    )

radnrkodi = pd.merge(left=radnrkodi, right=ped[
    ['code_id','sire','dam']], on='code_id')

#acctdm1 hleður inn radnrkodi og býr til 3 skrár úr henni
#           Input: accuraci.dat - sorted on random effect 1 (animal)
#                  accuracs.dat - sorted on sire (only sire > 0 records)
#                  accuracd.dat - sorted on dam (only dam > 0 records)

#Þær eru svona:
#13,file='accuraci.dat'-> write(20,399)irec,fix(i,1),fix(i,2),fix(i,3),ix(i),off1(i),off2(i),s(i),d(i),sex(i)
#read(13,103)ire,(ifix(j),j=1,nofix),ind,no1,no2,isire,idam,isex  !ire 0 eða 1 eftir því hvort þau eiga record

#í sire og dam skránni er þeim raðað eftir sire og dam þannig þau koma oft
#í röð eftir afkvæmum, og fá 0 og 1 fremst eftir því hvort afkvæmið á
#obs eða ekki


#Það sem acctdm1.f gerir
#Telur afkvæmi gripa, einn dálkur með afkvæmum ef hitt foreldri er þekkt,
#Annar dálkur ef hitt foreldri er óþekkt!

#Counting offpspring where both parents are known
off1 = radnrkodi[(radnrkodi['sire'] > 0) & (radnrkodi['dam'] > 0)].copy()
#counting offspring for sires
off1.loc[:,'off1_s'] = off1.groupby('sire')['sire'].transform('count')
#counting offspring for dams
off1.loc[:,'off1_d'] = off1.groupby('dam')['dam'].transform('count')

#Only sires and offspring count and dropping dublicate rows
off1s = off1[['sire','off1_s']]
off1s = off1s.drop_duplicates()
off1s.columns = ['code_id', 'off1']
off1s = off1s.sort_values(by=['code_id'])

#Only dams and offspring count and dropping dublicate rows
off1d = off1[['dam','off1_d']]
off1d = off1d.drop_duplicates()
off1d.columns = ['code_id', 'off1']
off1d = off1d.sort_values(by=['code_id'])


off1 = pd.merge(left=off1s, right=off1d, on=['code_id', 'off1'], how='outer')
radnrkodi = pd.merge(left=radnrkodi, right=off1, on=['code_id'], how='left')



off2s = radnrkodi[(radnrkodi['sire'] > 0) & (radnrkodi['dam'] == 0)].copy()
off2s.loc[:,'off2_s'] = off2s.groupby('sire')['sire'].transform('count')
off2s = off2s[['sire','off2_s']]
off2s = off2s.drop_duplicates()
off2s.columns = ['code_id', 'off2']
off2s = off2s.sort_values(by=['code_id'])

off2d = radnrkodi[(radnrkodi['sire'] == 0) & (radnrkodi['dam'] > 0)].copy()
off2d.loc[:,'off2_d'] = off2d.groupby('dam')['dam'].transform('count')
off2d = off2d[['dam','off2_d']]
off2d = off2d.drop_duplicates()
off2d.columns = ['code_id', 'off2']
off2d = off2d.sort_values(by=['code_id'])


off2 = pd.merge(left=off2s, right=off2d, on=['code_id', 'off2'], how='outer')
radnrkodi = pd.merge(left=radnrkodi, right=off2, on=['code_id'], how='left')

print(off2.iloc[500:515])
print(off2.info())

#
# print(off1s.iloc[500:515])
# print(off1s.info())
# print(off1d.iloc[500:515])
# print(off1d.info())
#
# radnrkodi = pd.merge(left=radnrkodi, right=off1s, on=['code_id', 'off1'], how='left')
# radnrkodi = pd.merge(left=radnrkodi, right=off1d, on=['code_id', 'off1'], how='left')
# radnrkodi = pd.merge(left=radnrkodi, right=off2s, on=['code_id', 'off2'], how='left')
# radnrkodi = pd.merge(left=radnrkodi, right=off2d, on=['code_id', 'off2'], how='left')
#





# radnrkodi = pd.merge(left=radnrkodi, right=off1[['code_id','sire', 'dam', 'off1_s', 'off1_d']], on=['code_id','sire', 'dam'], how='left')
# print(radnrkodi.info())
#
# off2_s = radnrkodi[(radnrkodi['sire'] > 0) & (radnrkodi['dam'] == 0)].copy()
#
# off2_s.loc[:,'off2_s'] = off2_s.groupby('sire')['sire'].transform('count')
#
# radnrkodi = pd.merge(left=radnrkodi, right=off2_s[['code_id','sire', 'dam', 'off2_s']], on=['code_id','sire', 'dam'], how='left')
#
# off2_d = radnrkodi[(radnrkodi['sire'] == 0) & (radnrkodi['dam'] > 0)].copy()
#
# off2_d.loc[:,'off2_d'] = off2_d.groupby('dam')['dam'].transform('count')
#
# radnrkodi = pd.merge(left=radnrkodi, right=off2_d[['code_id','sire', 'dam', 'off2_d']], on=['code_id','sire', 'dam'], how='left')


# radnrkodi.loc[(radnrkodi['dam'] != 0)  , 'off1'] = radnrkodi.groupby('sire')['sire'].transform('count')
# radnrkodi.loc[(radnrkodi['dam'] == 0)  , 'off2'] = radnrkodi.groupby('sire')['sire'].transform('count')



#
# data_use['IYM0_c'] = data_use.groupby('IYM0')['IYM0'].transform('count')
#
# cows_df.loc[(cows_df['T_3'] > 8) , 'wrong3'] = 'e'

print(radnrkodi.iloc[50000:50015])
print(radnrkodi.info())
