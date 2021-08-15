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
# #herd - calving year 1
# cows_df.loc[
# (cows_df['herd'].notnull().astype(int) == 1) &
# (cows_df['calv1'].notnull().astype(int) == 1),
# 'HC1'] = (s + cows_df['calv1'].dt.strftime('%y').replace('NaT', '0').astype(int))
# #herd - calving year 2
# cows_df.loc[
# (cows_df['herd'].notnull().astype(int) == 1) &
# (cows_df['calv2'].notnull().astype(int) == 1),
# 'HC2'] = (s + cows_df['calv2'].dt.strftime('%y').replace('NaT', '0').astype(int))
# #herd - calving year 3
# cows_df.loc[
# (cows_df['herd'].notnull().astype(int) == 1) &
# (cows_df['calv3'].notnull().astype(int) == 1),
# 'HC3'] = (s + cows_df['calv3'].dt.strftime('%y').replace('NaT', '0').astype(int))
# #Filling emty cells with 0 and setting as integers
# cows_df[['H_BY','HC1','HC2','HC3']] = cows_df[
#     ['H_BY','HC1','HC2','HC3']].fillna(0, downcast='infer')
cows_df['H_BY'] = cows_df[
    'H_BY'].fillna(0, downcast='infer')
# ,'HC1','HC2','HC3'
# ,'HC1','HC2','HC3'

herd_by = cows_df[['id','herd','birth','H_BY',]].copy()

herd_by = herd_by.loc[(herd_by['herd'].notnull().astype(int) == 1) &
    (herd_by['birth'].notnull().astype(int) == 1)]

herd_by['BY'] = (herd_by.id.astype(str).str[:4]).astype(int)

herd_by = herd_by.sort_values(by=['herd','birth'])

herd_by['H_BY_c'] = herd_by.groupby('H_BY')['H_BY'].transform('count')

#---------------------------------------------------------------------------
tdf = []
for herd, data in herd_by.groupby( 'herd' ):
    # get counts and assign initial groups
    counts = data[ 'BY' ].value_counts().sort_index().to_frame()
    counts[ 'group' ] = range( counts.shape[ 0 ] )

    while True:
        gcounts = counts.groupby( 'group' ).sum()[ 'BY' ]  # group counts
        change = gcounts[ gcounts.values < 3 ]  # groups with too few

        if change.shape[ 0 ] == 0:
            # no changes, exit
            break

        # check how to merge groups
        cgroup = change.index.min()
        groups = gcounts.index.values
        g_ind = list( groups ).index( cgroup )
        if ( g_ind + 1 ) < groups.shape[ 0 ]:
            # merge forward
            ngroup = groups[ g_ind + 1 ]

        elif g_ind > 0:
            # merge backward
            ngroup = groups[ g_ind - 1 ]

        else:
            # no groups to merge
            print( f'Can not merge herd {herd}' )
            break

        counts.loc[ counts[ 'group' ] == cgroup, 'group' ] = ngroup

    # assign groups
    for ind, gdata in counts.iterrows():
        data.loc[ data[ 'BY' ] == ind, 'group' ] = gdata[ 'group' ]

    tdf.append( data )

tdf = pd.concat( tdf )
#---------------------------------------------------------------------------

# print(herd_by.iloc[175000:175020])
print(herd_by.iloc[175:195])
print(herd_by.info())
print(tdf.iloc[175:195])
print(tdf.info())

tdf.to_excel("../data/tdf.xlsx", index=False, header=True)
