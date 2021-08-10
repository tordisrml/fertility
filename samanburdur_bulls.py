#Program in development
#Thordis Thorarinsdottir 2021
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

#------------------------------------------------------------------------------
#Read in file where results from inbreeding, phantom group and old breeding
#value results are located.
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

#Reading in a file with sires that have more than 50 daughters
sires50 = pd.read_csv(
    "../data/sire_50.txt",
    header=None,
    sep = ' ',
    names=['id', 'sire_count']
    )

#Merging code sire file and and file with EBVs
sires50= pd.merge(left=sires50, right=saman, on='id', how='left')
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------

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
#------------------------------------------------------------------------------
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
#------------------------------------------------------------------------------

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
#------------------------------------------------------------------------------
#New breeding value inbreeding
saman['new_I'] = (saman['CR0_I'] * 0.2 +
    saman['ICF_I'] * 0.3 +
    saman['IFL_I'] * 0.5 )
#New breeding value phantom
saman['new_P'] = (saman['CR0_P'] * 0.2 +
    saman['ICF_P'] * 0.3 +
    saman['IFL_P'] * 0.5 )
#------------------------------------------------------------------------------

#Correlation heat map for traits in dataframe!
plt.figure(figsize=(8,8))
seaborn.heatmap(sires50[['CR0_I', 'CR0_P',
    'ICF1_I','ICF2_I','ICF3_I',
    'ICF1_P','ICF2_P','ICF3_P',
    'IFL1_I','IFL2_I','IFL3_I',
    'IFL1_P','IFL2_P','IFL3_P',
    'CI12_I','CI23_I','CI34_I',
    'fertility_1','fertility_2','fertility_3','frjosemi']
    ].corr(), annot=True, cmap='coolwarm')
plt.title('Fylgni á milli kynbótaeinkunna fyrir eiginleika hjá nautum sem\
 eiga +50 dætur', fontsize = 20)

# Correlation heat map for traits in dataframe!
plt.figure(figsize=(8,8))
seaborn.heatmap(sires50[['CR0_I','CR0_P',
    'ICF_I','ICF_P',
    'IFL_I','IFL_P',
    'new_I', 'new_P',
    'CI_I',
    'fertility_1','fertility_2','fertility_3','frjosemi']
    ].corr(), annot=True, cmap='coolwarm')
plt.title('Fylgni á milli kynbótaeinkunna fyrir eiginleika hjá nautum sem\
 eiga +50 dætur', fontsize = 20)
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------

#Checking spearman correlations,
rho, p = spearmanr(sires50['frjosemi'], sires50['CI_I'])
#This will print out in the terminal
print(rho)
print(p)
#------------------------------------------------------------------------------

#Creation of a plot that shows the avarege breeding value for the traits for
#each birth year
#This creates the figure and below it is possible to add another y-axis
fig, ax1 = plt.subplots()
ax1.set_xlim(2006, 2020)

#EBVs from DMU5
ax1.plot(
    (sires50.groupby('BY')['CR0_I'].mean()),
    label='CR_I',
    color='slategrey',
    linestyle=':',
    linewidth=3)
ax1.plot(
    (sires50.groupby('BY')['CR0_P'].mean()),
    label='CR_P',
    color='black',
    linestyle=':',
    linewidth=3)
ax1.plot(
    (sires50.groupby('BY')['ICF_I'].mean()),
    label='ICF_I',
    color='mediumslateblue',
    linewidth=3)
ax1.plot(
    (sires50.groupby('BY')['ICF_P'].mean()),
    label='ICF_P',
    color='blue',
    #linestyle='--',
    linewidth=3)
ax1.plot(
    (sires50.groupby('BY')['IFL_I'].mean()),
    label='IFL_I',
    color='aquamarine',
    linewidth=3)
ax1.plot(
    (sires50.groupby('BY')['IFL_P'].mean()),
    label='IFL_P',
    color='green',
    #linestyle='--',
    linewidth=3)
ax1.plot(
    (sires50.groupby('BY')['CI_I'].mean()),
    label='CI_I',
    color='yellow',
    linestyle='--',
    linewidth=3)
ax1.plot(
    (sires50.groupby('BY')['new_I'].mean()),
    label='new_I',
    color='orchid',
    linestyle='-.',
    linewidth=3)
ax1.plot(
    (sires50.groupby('BY')['new_P'].mean()),
    label='new_P',
    color='deeppink',
    linestyle='-.',
    linewidth=3)
#Creation of another y-axis in the same figure
ax2 = ax1.twinx()
ax2.plot(
    (sires50.groupby('BY')['frjosemi'].mean()),
    label='frjosemi',
    color='red',
    linewidth=3)
#------------------------------------------------------------------------------

#Show legends of plotted values, names are in 'label' above
ax1.legend()
ax2.legend()

#Labels for x and y
ax1.set_xlabel('Birth Year' , fontsize = 15)
ax1.set_ylabel('EBV from DMU5, standardized', fontsize = 15)
ax2.set_ylabel('EBV from old kynbótamat', fontsize = 15)
#Title of plot
ax1.set_title('Average estimated breeding values by birth year for cows with \
their observation for new fertility traits', fontsize = 20)
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#Show the plot in home computer via Xming
plt.show()

print(sires50.iloc[300:315])
print(sires50.info())

#Saves the dataframe to excel file
sires50.to_excel("../data/sires50.xlsx", index=False, header=True)

#plt.savefig('plot.png')
