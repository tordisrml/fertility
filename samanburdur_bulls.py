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
from scipy import stats
from scipy.stats import spearmanr

#This is a program to compare old and new fertility evaluation.

saman = pd.read_csv(
    "../data/saman_I_P_G.txt",
    header=None,
    sep=' ',
    names=['id',
        'CR0_I','ICF1_I','ICF2_I','ICF3_I','IFL1_I','IFL2_I','IFL3_I',
        'CR0_P','ICF1_P','ICF2_P','ICF3_P','IFL1_P','IFL2_P','IFL3_P',
        'CI12_I','CI23_I','CI34_I',
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
CI12_SD = 8.79335
CI23_SD = 8.95628
CI34_SD = 6.11366

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
saman['CI12_I'] = (saman['CI12_I'] / CI12_SD)*(-1)
saman['CI23_I'] = (saman['CI23_I'] / CI23_SD)*(-1)
saman['CI34_I'] = (saman['CI34_I'] / CI34_SD)*(-1)


#Creating a single ICF and IFL value
saman['ICF_I'] = (saman['ICF1_I']*0.5 + saman['ICF2_I']*0.3+ saman['ICF3_I'] * 0.2)
saman['ICF_P'] = (saman['ICF1_P']*0.5 + saman['ICF2_P']*0.3 + saman['ICF3_P']*0.2 )
saman['IFL_I'] = (saman['IFL1_I'] * 0.5 +
    saman['IFL1_I'] * 0.3 +
    saman['IFL2_I'] * 0.2 )
saman['IFL_P'] = (saman['IFL1_P'] * 0.5 +
    saman['IFL1_P'] * 0.3 +
    saman['IFL2_P'] * 0.2 )

saman['CI_I'] = (saman['CI12_I'] * 0.5 +
    saman['CI23_I'] * 0.3 +
    saman['CI34_I'] * 0.2 )

#New breeding value inbreeding
saman['new_I'] = (saman['CR0_I'] * 0.2 +
    saman['ICF_I'] * 0.3 +
    saman['IFL_I'] * 0.5 )
#New breeding value phantom
saman['new_P'] = (saman['CR0_P'] * 0.2 +
    saman['ICF_P'] * 0.3 +
    saman['IFL_P'] * 0.5 )


#Reading in id codes to replace in SOL files
sires50 = pd.read_csv(
    "../data/sire_50.txt",
    header=None,
    sep = ' ',
    names=['id', 'sire_count']
    )

#Merging code id file and dataframe
sires50= pd.merge(left=sires50, right=saman, on='id', how='left')

# print(sires50.groupby("BY").describe())

describe = sires50.groupby("BY").describe().to_csv("my_description.csv")


#Correlation heat map for all traits in dataframe!
plt.figure(figsize=(8,8))
seaborn.heatmap(sires50[['CR0_I', 'CR0_P',
    'ICF1_I','ICF2_I','ICF3_I',
    'ICF1_P','ICF2_P','ICF3_P',
    'IFL1_I','IFL2_I','IFL3_I',
    'IFL1_P','IFL2_P','IFL3_P',
    'CI12_I','CI23_I','CI34_I',
    'fertility_1','fertility_2','fertility_3','frjosemi']].corr(), annot=True, cmap='coolwarm')
plt.title('Fylgni á milli kynbótaeinkunna fyrir eiginleika hjá nautum sem eiga +50 dætur', fontsize = 20)

# Correlation heat map for all traits in dataframe!
plt.figure(figsize=(8,8))
seaborn.heatmap(sires50[['CR0_I','CR0_P',
    'ICF_I','ICF_P',
    'IFL_I','IFL_P',
    'new_I', 'new_P',
    'CI_I',
    'fertility_1','fertility_2','fertility_3','frjosemi']].corr(), annot=True, cmap='coolwarm')
plt.title('Fylgni á milli kynbótaeinkunna fyrir eiginleika hjá nautum sem eiga +50 dætur', fontsize = 20)

rho, p = spearmanr(sires50['frjosemi'], sires50['CI_I'])

print(rho)
print(p)

# plt.plot((sires50.groupby('BY')['ICF1_I'].mean()), label='ICF1_I', color='mediumslateblue', linewidth=4)
# plt.plot((sires50.groupby('BY')['ICF2_I'].mean()), label='ICF2_I', color='royalblue', linewidth=4)
# plt.plot((sires50.groupby('BY')['ICF3_I'].mean()), label='ICF3_I', color='navy', linewidth=4)
# plt.plot((sires50.groupby('BY')['ICF1_P'].mean()), label='ICF1_P', color='cornflowerblue', linewidth=4)
# plt.plot((sires50.groupby('BY')['ICF2_P'].mean()), label='ICF2_P', color='mediumblue', linewidth=4)
# plt.plot((sires50.groupby('BY')['ICF3_P'].mean()), label='ICF3_P', color='slateblue', linewidth=4)
# plt.plot((sires50.groupby('BY')['ICF_I'].mean()), label='ICF_I', color='mediumslateblue', linewidth=4)
# plt.plot((sires50.groupby('BY')['ICF_P'].mean()), label='ICF_P', color='blue', linewidth=4)

# plt.plot((sires50.groupby('BY')['IFL1_I'].mean()), label='IFL1_I', color='green')
# plt.plot((sires50.groupby('BY')['IFL2_I'].mean()), label='IFL2_I', color='forestgreen')
# plt.plot((sires50.groupby('BY')['IFL3_I'].mean()), label='IFL3_I', color='mediumseagreen')
# plt.plot((sires50.groupby('BY')['IFL1_P'].mean()), label='IFL1_P', color='springgreen')
# plt.plot((sires50.groupby('BY')['IFL2_P'].mean()), label='IFL2_P', color='aquamarine')
# plt.plot((sires50.groupby('BY')['IFL3_P'].mean()), label='IFL3_P', color='seagreen')
# plt.plot((sires50.groupby('BY')['IFL_I'].mean()), label='IFL_I', color='lime', linewidth=4)
# plt.plot((sires50.groupby('BY')['IFL_P'].mean()), label='IFL_P', color='limegreen', linewidth=4)
#
# plt.plot((sires50.groupby('BY')['CR0_I'].mean()), label='CR0_I', color='slategrey', linewidth=4)
# plt.plot((sires50.groupby('BY')['CR0_P'].mean()), label='CR0_P', color='black', linewidth=4)

# plt.plot((sires50.groupby('BY')['new_I'].mean()), label='new_I', color='orchid', linewidth=4)
# plt.plot((sires50.groupby('BY')['new_P'].mean()), label='new_P', color='deeppink', linewidth=4)
# plt.plot((sires50.groupby('BY')['CI_I'].mean()), label='CI_I', color='yellow', linewidth=4)
# plt.plot((sires50.groupby('BY')['frjosemi'].mean()), label='frjosemi', color='red')




# #Labels for x and y
# plt.xlabel('Birth Year')
# plt.ylabel('EBV')
# #Title of plot
# plt.title('Estimated breeding values for ICF and IFL by Birth year')
#
# #Show legends of plotted values, names are in 'label' above
# plt.legend()

print(sires50.iloc[300:315])
print(sires50.info())

# #Show the plot in home computer via Xming
plt.show()

#plt.savefig('plot.png')
