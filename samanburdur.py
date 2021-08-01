#Program in development
#Finding ways to compara old and new fertility blup and
#use matplotlib

import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

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

#Make birth year from id number an integer
saman['BY'] = (saman.id.astype(str).str[:4]).astype(int)

#Genetic SD from DMUAI runs (from MCs project)
ICF1_SD = 6.13866
ICF2_SD = 7.58765
ICF3_SD = 5.67486
IFL1_SD = 6.59772
IFL2_SD = 5.30567
IFL3_SD = 6.57391

#Standardize the results with genetic SD
#Multiplied by -1 to so improvements are posative
saman['BLUP_ICF1'] = (saman['BLUP_ICF1'] / ICF1_SD)*(-1)
saman['BLUP_ICF2'] = (saman['BLUP_ICF2'] / ICF2_SD)*(-1)
saman['BLUP_ICF3'] = (saman['BLUP_ICF3'] / ICF3_SD)*(-1)
saman['BLUP_IFL1'] = (saman['BLUP_IFL1'] / IFL1_SD)*(-1)
saman['BLUP_IFL2'] = (saman['BLUP_IFL2'] / IFL2_SD)*(-1)
saman['BLUP_IFL3'] = (saman['BLUP_IFL3'] / IFL3_SD)*(-1)


# saman['BLUP_ICF1'] = (saman['BLUP_ICF1'] / ICF1_SD) + 100
# saman['BLUP_ICF2'] = (saman['BLUP_ICF2'] / ICF1_SD) + 100
# saman['BLUP_ICF3'] = (saman['BLUP_ICF3'] / ICF1_SD) + 100
# saman['BLUP_IFL1'] = (saman['BLUP_IFL1'] / ICF1_SD) + 100
# saman['BLUP_IFL2'] = (saman['BLUP_IFL2'] / ICF1_SD) + 100
# saman['BLUP_IFL3'] = (saman['BLUP_IFL3'] / ICF1_SD) + 100

#Creating a single ICF and IFL value
saman['BLUP_ICF'] = (saman['BLUP_ICF1'] * 0.5 +
    saman['BLUP_ICF2'] * 0.3 +
    saman['BLUP_ICF3'] * 0.2 )
saman['BLUP_IFL'] = (saman['BLUP_IFL1'] * 0.5 +
    saman['BLUP_IFL2'] * 0.3 +
    saman['BLUP_IFL3'] * 0.2 )




# saman[[
#     'BLUP_ICF1','BLUP_ICF2','BLUP_ICF3', 'BLUP_ICF',
#     'BLUP_IFL1','BLUP_IFL2','BLUP_IFL3', 'BLUP_IFL',
#     'fertility_1','fertility_2','fertility_3','frjosemi']] = saman[[
#     'BLUP_ICF1','BLUP_ICF2','BLUP_ICF3', 'BLUP_ICF',
#     'BLUP_IFL1','BLUP_IFL2','BLUP_IFL3', 'BLUP_IFL',
#     'fertility_1','fertility_2','fertility_3','frjosemi']].astype(float).round().astype(int)

#Print Summary statistics
# print(saman[[
#     'BLUP_ICF1','BLUP_ICF2','BLUP_ICF3',
#     'BLUP_IFL1','BLUP_IFL2','BLUP_IFL3',
#     'fertility_1','fertility_2','fertility_3','frjosemi']].describe())

#Print correlations between variables
# print(saman[[
#     'BLUP_ICF1','BLUP_ICF2','BLUP_ICF3', 'BLUP_ICF',
#     'BLUP_IFL1','BLUP_IFL2','BLUP_IFL3', 'BLUP_IFL',
#     'fertility_1','fertility_2','fertility_3','frjosemi']].corr())


#Print info and a part of the dataset
print(saman.iloc[450000:450030])
print(saman.info())

#Only plot animals born after 2000
saman2001 = saman[saman['BY'] > 2001]


#Style of plot
#plt.style.use('Solarize_Light2')
#Print to see avalable styles
# print(plt.style.available)

plt.plot((saman2001.groupby('BY')['BLUP_ICF'].mean()), label='ICF')
# plt.plot((saman2001.groupby('BY')['BLUP_ICF1'].mean()), label='ICF1')
# plt.plot((saman2001.groupby('BY')['BLUP_ICF2'].mean()), label='ICF2')
# plt.plot((saman2001.groupby('BY')['BLUP_ICF3'].mean()), label='ICF3')
plt.plot((saman2001.groupby('BY')['BLUP_IFL'].mean()), label='IFL')
# plt.plot((saman2001.groupby('BY')['BLUP_IFL1'].mean()), label='IFL1')
# plt.plot((saman2001.groupby('BY')['BLUP_IFL2'].mean()), label='IFL2')
# plt.plot((saman2001.groupby('BY')['BLUP_IFL3'].mean()), label='IFL3')

#Labels for x and y
plt.xlabel('Birth Year')
plt.ylabel('EBV')
#Title of plot
plt.title('Estimated breeding values for ICF and IFL by Birth year')

#Show legends of plotted values, names are in 'label' above
plt.legend()

#Show the plot in home computer via Xming
plt.show()

#plt.savefig('plot.png')
