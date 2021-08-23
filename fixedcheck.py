import pandas as pd
import numpy as np
import datetime

data_use = pd.read_csv(
    "../data/dmu_fertilitynew.txt",
    header=None,
    sep = ' ',
    names=['id','HBY','HC1','HC2','HC3','IYM0','IYM1','IYM2',
        'IYM3','AGEi_h','AGEc_1','AGEc_2','AGEc_3','tech_h',
        'CRh','ICF1','ICF2','ICF3','IFL1','IFL2','IFL3']
    )


def hy_grouping(df, col, group, df1):
    tdf = []
    for herd, data in df:
        # get counts and assign initial groups
        counts = data[ col ].value_counts().sort_index().to_frame()
        counts[ 'group' ] = range( counts.shape[ 0 ] )

        while True:
            gcounts = counts.groupby( 'group' ).sum()[ col ]  # group counts
            change = gcounts[ gcounts.values < 5 ]  # groups with too few

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

    df1 = pd.merge(left=df1, right=tdf[['id', group]], on='id',
        how='outer').fillna(0, downcast='infer')

    return df1
#---------------------------------------------------------------------------
#---------------------------------------------------------------------------



#Create a dataframe to group herd-year groups
ids = data_use['id'].copy()
heif = data_use[['id','IYM0']].copy()
# lact1 = data_use[['id','IYM1']].copy()
# lact2 = data_use[['id','IYM2']].copy()
# lact3 = data_use[['id','IYM3']].copy()

#Only include relevant rows
heif = heif.loc[(heif['IYM0'] != 0) ]
print(heif.info())
# lact1 = lact1.loc[(lact1['IYM1'].notnull().astype(int) == 1) ]
# lact2 = lact2.loc[(lact2['IYM2'].notnull().astype(int) == 1) ]
# lact2 = lact3.loc[(lact3['IYM3'].notnull().astype(int) == 1) ]


#Sort the dataframes by relevant date
heif = heif.sort_values(by=['IYM0'])
# lact1 = lact1.sort_values(by=['IYM1'])
# lact2 = lact2.sort_values(by=['IYM2'])
# lact2 = lact2.sort_values(by=['IYM3'])

#---------------------------------------------------------------------------
#Calling function above to create herd-year groups in all lactations
#---------------------------------------------------------------------------
print( f'Starting with herd x birth year' )
ids = hy_grouping(heif, 'IYM0', 'IYM0', ids)

# print( f'Starting with herd x calving year 1' )
# ids = hy_grouping(lact1, 'IYM1', 'IYM1', ids)
#
# print( f'Starting with herd x calving year 2' )
# ids = hy_grouping(lact2, 'IYM2', 'IYM2', ids)
#
# print( f'Starting with herd x calving year 3' )
# ids = hy_grouping(lact2, 'IYM3', 'IYM3', ids)



data_use = data_use.sort_values(by=['id'])
#---------------------------------------------------------------------------
#Merging herd-year groups with main dataframe
data_use = pd.merge(left=data_use, right=ids, on='id', how='left')
#---------------------------------------------------------------------------

# #Counting how many cows are in each herd-year group
# data_use['HBY_c'] = data_use.groupby('HBY')['HBY'].transform('count')
# data_use['HC1_c'] = data_use.groupby('HC1')['HC1'].transform('count')
# data_use['HC2_c'] = data_use.groupby('HC2')['HC2'].transform('count')
# data_use['HC3_c'] = data_use.groupby('HC3')['HC3'].transform('count')
# #Delete rows that are alone in a group
# data_use = data_use[
#     (data_use['HBY_c'] != 1) &
#     (data_use['HC1_c'] != 1) &
#     (data_use['HC2_c'] != 1) &
#     (data_use['HC3_c'] != 1)
# ]


print(data_use.iloc[50000:50015])
print(data_use.info())
