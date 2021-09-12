#This program takes result files from DMU5 test runs and
#combines results together in a big file along with old BLUP results

import pandas as pd
import numpy as np


#Reading in the old fertility breeding results
gamla = pd.read_csv(
    "../data/gamla_mat.txt",
    header=None,
    sep=' ',
    names=['id','fertility_1','fertility_2','fertility_3','frjosemi']
    )

#Inbreeding results
inbreed = pd.read_csv(
    "../data/saman_inbreednew2.txt",
    header=None,
    sep=' ',
    names=['id',
        'BLUP_CR0_I','BLUP_ICF1_I','BLUP_ICF2_I','BLUP_ICF3_I',
        'BLUP_IFL1_I','BLUP_IFL2_I','BLUP_IFL3_I']
    )
#Phantom group results
phantom = pd.read_csv(
    "../data/saman_phantom20210912.txt",
    header=None,
    sep=' ',
    names=['id',
        'BLUP_CR0_P','BLUP_ICF1_P','BLUP_ICF2_P','BLUP_ICF3_P',
        'BLUP_IFL1_P','BLUP_IFL2_P','BLUP_IFL3_P']
    )

#CI results
CI = pd.read_csv(
    "../data/saman_ci.txt",
    header=None,
    sep=' ',
    names=['id',
        'CI12','CI23','CI34']
    )

#Inbreeding results and phantom group results together in a file
saman_allt = pd.merge(left=inbreed, right=phantom, on='id')
#Inbreeding results and phantom group results together in a file
saman_allt = pd.merge(left=saman_allt, right=CI, on='id')
#Old results merged
saman_allt = pd.merge(left=saman_allt, right=gamla, on='id')
#Written into a datafile
saman_allt.to_csv("../data/saman_I_P_G_20210912.txt", index=False, header=False, sep=' ')

print(saman_allt.iloc[600000:600015])
print(saman_allt.info())
