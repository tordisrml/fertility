import pandas as pd
import numpy as np

import math
import statistics
import scipy.stats

#This is a program to compare old and new fertility evaluation. 

saman = pd.read_csv(
    "../data/saman.txt",
    header=None,
    sep=' ',
    names=['id',
        'BLUP_ICF1','BLUP_ICF2','BLUP_ICF3',
        'BLUP_IFL1','BLUP_IFL2','BLUP_IFL3',
        'fertility_1','fertility_2','fertility_3','frjosemi']
    )
