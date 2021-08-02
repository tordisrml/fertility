#Program in development
#Finding ways to compara old and new fertility blup and
#use matplotlib

import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import seaborn

import math
import statistics
import scipy.stats



#This is a program to compare old and new fertility evaluation.

saman = pd.read_csv(
    "../data/saman_I_P_G.txt",
    header=None,
    sep=' ',
    names=['id',
        'CR0_I','ICF1_I','ICF2_I','ICF3_I','IFL1_I','IFL2_I','IFL3_I',
        'CR0_P','ICF1_P','ICF2_P','ICF3_P','IFL1_P','IFL2_P','IFL3_P',
        'fertility_1','fertility_2','fertility_3','frjosemi']
    )

#Make birth year from id number an integer
saman['BY'] = (saman.id.astype(str).str[:4]).astype(int)

#Genetic SD from DMUAI runs (from MCs project)
CR0_SD = 0.059823333
ICF1_SD = 6.13866
ICF2_SD = 7.58765
ICF3_SD = 5.67486
IFL1_SD = 6.59772
IFL2_SD = 5.30567
IFL3_SD = 6.57391

#Standardize the results with genetic SD
#Multiplied by -1 to so improvements are posative
saman['CR0_I'] = (saman['CR0_I'] / CR0_SD)
saman['ICF1_I'] = (saman['ICF1_I'] / ICF1_SD)*(-1)
saman['ICF2_I'] = (saman['ICF2_I'] / ICF2_SD)*(-1)
saman['ICF3_I'] = (saman['ICF3_I'] / ICF3_SD)*(-1)
saman['IFL1_I'] = (saman['IFL1_I'] / IFL1_SD)*(-1)
saman['IFL2_I'] = (saman['IFL2_I'] / IFL2_SD)*(-1)
saman['IFL3_I'] = (saman['IFL3_I'] / IFL3_SD)*(-1)
saman['CR0_P'] = (saman['CR0_P'] / CR0_SD)
saman['ICF1_P'] = (saman['ICF1_P'] / ICF1_SD)*(-1)
saman['ICF2_P'] = (saman['ICF2_P'] / ICF2_SD)*(-1)
saman['ICF3_P'] = (saman['ICF3_P'] / ICF3_SD)*(-1)
saman['IFL1_P'] = (saman['IFL1_P'] / IFL1_SD)*(-1)
saman['IFL2_P'] = (saman['IFL2_P'] / IFL2_SD)*(-1)
saman['IFL3_P'] = (saman['IFL3_P'] / IFL3_SD)*(-1)


# #Correlation heat map for all traits in dataframe!
# plt.figure(figsize=(8,8))
# seaborn.heatmap(saman[['CR0_I','ICF1_I','ICF2_I','ICF3_I','IFL1_I','IFL2_I','IFL3_I',
#     'CR0_P','ICF1_P','ICF2_P','ICF3_P','IFL1_P','IFL2_P','IFL3_P',
#     'fertility_1','fertility_2','fertility_3','frjosemi']].corr(), annot=True, cmap='coolwarm')


#Creating a single ICF and IFL value
saman['ICF_I'] = (saman['ICF1_I'] * 0.5 +
    saman['ICF2_I'] * 0.3 +
    saman['ICF3_I'] * 0.2 )
saman['ICF_P'] = (saman['ICF1_P'] * 0.5 +
    saman['ICF2_P'] * 0.3 +
    saman['ICF3_P'] * 0.2 )
saman['IFL_I'] = (saman['IFL1_I'] * 0.5 +
    saman['IFL1_I'] * 0.3 +
    saman['IFL2_I'] * 0.2 )
saman['IFL_P'] = (saman['IFL1_P'] * 0.5 +
    saman['IFL1_P'] * 0.3 +
    saman['IFL2_P'] * 0.2 )

#New breeding value inbreeding
saman['new_I'] = (saman['CR0_I'] * 0.2 +
    saman['ICF_I'] * 0.3 +
    saman['IFL_I'] * 0.5 )
#New breeding value phantom
saman['new_P'] = (saman['CR0_P'] * 0.2 +
    saman['ICF_P'] * 0.3 +
    saman['IFL_P'] * 0.5 )


#Correlation heat map for all traits in dataframe!
plt.figure(figsize=(8,8))
seaborn.heatmap(saman[['CR0_I','CR0_P','ICF_I','ICF_P','IFL_I','IFL_P',
    'new_I', 'new_P',
    'fertility_1','fertility_2','fertility_3','frjosemi']].corr(), annot=True, cmap='coolwarm')

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
#saman2001 = saman[saman['BY'] > 2001]


#Style of plot
#plt.style.use('Solarize_Light2')
#Print to see avalable styles
# print(plt.style.available)
#
# plt.plot((saman2001.groupby('BY')['BLUP_ICF'].mean()), label='ICF')
# # plt.plot((saman2001.groupby('BY')['BLUP_ICF1'].mean()), label='ICF1')
# # plt.plot((saman2001.groupby('BY')['BLUP_ICF2'].mean()), label='ICF2')
# # plt.plot((saman2001.groupby('BY')['BLUP_ICF3'].mean()), label='ICF3')
# plt.plot((saman2001.groupby('BY')['BLUP_IFL'].mean()), label='IFL')
# # plt.plot((saman2001.groupby('BY')['BLUP_IFL1'].mean()), label='IFL1')
# # plt.plot((saman2001.groupby('BY')['BLUP_IFL2'].mean()), label='IFL2')
# # plt.plot((saman2001.groupby('BY')['BLUP_IFL3'].mean()), label='IFL3')
#
# #Labels for x and y
# plt.xlabel('Birth Year')
# plt.ylabel('EBV')
# #Title of plot
# plt.title('Estimated breeding values for ICF and IFL by Birth year')
#
# #Show legends of plotted values, names are in 'label' above
# plt.legend()
#
# #Show the plot in home computer via Xming
plt.show()

#plt.savefig('plot.png')
