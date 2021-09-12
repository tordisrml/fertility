import pandas as pd
import numpy as np

ownobs = pd.read_csv(
    "../data/dmu_fertilitynew2.txt",
    header=None,
    sep=' ',
    names=['code_id',
        'CR0_I','ICF1_I','ICF2_I','ICF3_I','IFL1_I','IFL2_I','IFL3_I',
        'CR0_P','ICF1_P','ICF2_P','ICF3_P','IFL1_P','IFL2_P','IFL3_P',
        'CI12_I','CI23_I','CI34_I',
        'fertility_1','fertility_2','fertility_3','frjosemi']
    )

code_df = pd.read_csv(
    "../data/id_code2.txt",
    header=None,
    sep = ' ',
    names=['id','code_id','sex']
    )

df = pd.merge(left=ownobs, right=code_df, on='code_id', how='left')

id = df['id']

id.to_csv("../data/PROB.ped", index=False, header=False)
