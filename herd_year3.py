import pandas as pd
import numpy as np
import datetime

#---------------------------------------------------------------------------
def hy_grouping(df, col, group, df1):
    tdf = []

    for herd, data in df.groupby( 'herd' ):
        # get counts and assign initial groups
        counts = data[ col ].value_counts().sort_index().to_frame()
        counts[ 'group' ] = range( counts.shape[ 0 ] )

        while True:
            gcounts = counts.groupby( 'group' ).sum()[ col ]  # group counts
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
            data.loc[ data[ col ] == ind, 'group' ] = gdata[ 'group' ]

        tdf.append( data )

    tdf = pd.concat( tdf )

    tdf[ group ] = tdf[ 'herd' ].astype( 'str' ) + tdf[ 'group' ].astype( int ).astype( str )

    df1 = pd.merge(left=df1, right=tdf[['id', group]], on='id', how='outer').fillna(0, downcast='infer')

    return df1

#---------------------------------------------------------------------------

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
cows_df = cows_df.drop(['death', 'calv4'], axis = 1)
#'ins','birth','death','calv1','calv2','calv3','calv4' formatted into dates
cows_df[['birth','calv1','calv2','calv3']] = cows_df[
    ['birth','calv1','calv2','calv3']
    ].apply(
    lambda x: pd.to_datetime(x, format='%Y%m%d'))

#Creating year columns
cows_df[['BY','C1','C2','C3']] = cows_df[
    ['birth','calv1','calv2','calv3']
    ].apply(
    lambda s: s.dt.strftime('%Y'))


#Create a dataframe to group
herd_by = cows_df[['id','herd','birth','BY']].copy()
herd_c1 = cows_df[['id','herd','calv1','C1']].copy()
herd_c2 = cows_df[['id','herd','calv2','C2']].copy()
herd_c3 = cows_df[['id','herd','calv3','C3']].copy()
ids = cows_df['id'].copy()

herd_by = herd_by.loc[(herd_by['herd'].notnull().astype(int) == 1) &
    (herd_by['birth'].notnull().astype(int) == 1)]
herd_c1 = herd_c1.loc[(herd_c1['herd'].notnull().astype(int) == 1) &
    (herd_c1['calv1'].notnull().astype(int) == 1)]
herd_c2 = herd_c2.loc[(herd_c2['herd'].notnull().astype(int) == 1) &
    (herd_c2['calv2'].notnull().astype(int) == 1)]
herd_c3 = herd_c3.loc[(herd_c3['herd'].notnull().astype(int) == 1) &
    (herd_c3['calv3'].notnull().astype(int) == 1)]

herd_by = herd_by.sort_values(by=['herd','birth'])
herd_c1 = herd_c1.sort_values(by=['herd','calv1'])
herd_c2 = herd_c2.sort_values(by=['herd','calv2'])
herd_c3 = herd_c3.sort_values(by=['herd','calv3'])


print( f'Starting with herd x birth year' )
ids = hy_grouping(herd_by, 'BY', 'H_BY', ids)

print( f'Starting with herd x calving year 1' )
ids = hy_grouping(herd_c1, 'C1', 'H_C1', ids)

print( f'Starting with herd x calving year 2' )
ids = hy_grouping(herd_c2, 'C2', 'H_C2', ids)

print( f'Starting with herd x calving year 3' )
ids = hy_grouping(herd_c3, 'C3', 'H_C3', ids)

cows_df = pd.merge(left=cows_df, right=ids, on='id', how='outer')

# print(herd_by.iloc[175000:175020])
print(cows_df.iloc[155000:155015])
print(cows_df.info())
# print(tdf.iloc[175:195])
# print(tdf.info())

# tdf.to_excel("../data/tdf.xlsx", index=False, header=True)
