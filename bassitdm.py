#This is a program that takes the file bassitdm.????
#where BLUP results for all animals is stored and collects the fertility blup
#to be compared in another file

import pandas as pd
import numpy as np

widths = [
    15,4,4,4,
    4,4,4,
    4,4,4,
    4,4,4,
    4,4,4,
    4,4,4,
    4,4,4,  #22

    4,4,4,4,
    4,4,4,4,  #8

    4,4,4,4,4,4,
    4,4,4,4,
    4,4,4,4,4,
    4,4,4,4,4,4,
    4,4,4,4,
    4,4,4,4,4,4,
    4,4,4,4,      #35

    4,4,4,4,4,4,4,4,4,4,4,4,4,4 #14
    ]

df = pd.read_fwf(
    "../data/bassitdm.mai21a",
    header=None,
    widths=widths,
    names=['id','milk_kg_1','milk_kg_2','milk_kg_3',
    'fat_kg_1','fat_kg_2','fat_kg_3',
    'protein_kg_1','protein_kg_2','protein_kg_3',
    'fat_%_1','fat_%_2','fat_%_3',
    'protein_%_1','protein_%_2','protein_%_3',
    'fertility_1','fertility_2','fertility_3',
    'SCS_1','SCS_2','SCS_3',                            #22

    'bandmal_eldra', 'bolur_eldra', 'malir_eldra','fotstada_eldra',
    'jugurlag_festa_eldra', 'spenalengd_lag_eldra', 'mjaltir_eldra', 'skap_eldra',  #8

    'boldypt', 'utlogur', 'yfirlina', 'malabreidd', 'malahalli', 'malabratti',
    'stada_haekla_hlid', 'stada_haekla_aftan', 'klaufhalli', 'jugurfesta',
    'jugurband', 'jugurdypt', 'spenalengd', 'spenaþykkt', 'spenastada',
    'mjaltir1', 'skap1', 'mjaltarod', 'gaedarod', 'ending', 'mjolkurmagn',
    'fitumagn', 'proteinmagn', 'fituhlutfall', 'proteinhlutfall',
    'eigin_afurdir', 'afurdamat', 'frjosemi', 'frumutala', 'skrokkur', 'jugur',
    'spenar', 'mjaltir2', 'skap2', 'heildareinkunn',                  #35

    'no_daughters_yield', 'yield_acc',
    'no_daughters_SCS', 'SCS_acc',
    'no_daughters_utlit_gamla', 'utlit_gamla_acc',
    'no_daughters_utlit_nyja', 'utlit_nyja_acc',
    'no_daughters_mjaltir', 'mjaltir_acc',
    'no_daughters_ending',
    'mjolkuruthald', 'fituuthald', 'proteinuthald'   #14  --> 79
    ]
    )

#Locate fertilty breeding results and put in a seperate file
fertilty = df.loc[:, ['id','fertility_1','fertility_2','fertility_3','frjosemi']]
fertilty.to_csv("../data/gamla_mat.txt", index=False, header=False, sep=' ')

print(df.iloc[50000:50015])
print(df.info())
