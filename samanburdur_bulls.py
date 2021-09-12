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
    "../data/saman_I_P_G_new3.txt",
    header=None,
    sep=' ',
    names=['id',
        'CR0_I','ICF1_I','ICF2_I','ICF3_I','IFL1_I','IFL2_I','IFL3_I',
        'CR0_P','ICF1_P','ICF2_P','ICF3_P','IFL1_P','IFL2_P','IFL3_P',
        'CI12_I','CI23_I','CI34_I',
        'fertility_1','fertility_2','fertility_3','frjosemi']
    )

#Reading in the file used in DMU so animals that have their own observations
#can be located
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

#Reading in id codes to replace in SOL files
id_code = pd.read_csv(
    "/home/thordis/data/id_code.txt",
    header=None,
    sep = ' ',
    names=['id','code_id']
    )

#Merging ownobs and id file to bring back einstaklingsnumer used in huppa
ownobs = pd.merge(left=ownobs[
    ['code_id']
    ], right=id_code[['id','code_id']], on='code_id', how='inner')

#Make birth year from id number an integer
saman['BY'] = (saman.id.astype(str).str[:4]).astype(int)

ave_group = saman.loc[(saman['BY'] >= 2012) & (saman['BY'] <= 2017)]

#Merging ownobs and id file to bring back einstaklingsnumer used in huppa
ave_group = pd.merge(left=ownobs['id'], right=ave_group, on='id', how='left')
print(ave_group.iloc[300:315])
print(ave_group.info())

CR0_SD_I = ave_group['CR0_I'].std()
ICF1_SD_I = ave_group['ICF1_I'].std()
ICF2_SD_I = ave_group['ICF2_I'].std()
ICF3_SD_I = ave_group['ICF3_I'].std()
IFL1_SD_I = ave_group['IFL1_I'].std()
IFL2_SD_I = ave_group['IFL2_I'].std()
IFL3_SD_I = ave_group['IFL3_I'].std()
CI12_SD_I = ave_group['CI12_I'].std()
CI23_SD_I = ave_group['CI23_I'].std()
CI34_SD_I = ave_group['CI34_I'].std()
CR0_mean_I = ave_group['CR0_I'].mean()
ICF1_mean_I = ave_group['ICF1_I'].mean()
ICF2_mean_I = ave_group['ICF2_I'].mean()
ICF3_mean_I = ave_group['ICF3_I'].mean()
IFL1_mean_I = ave_group['IFL1_I'].mean()
IFL2_mean_I = ave_group['IFL2_I'].mean()
IFL3_mean_I = ave_group['IFL3_I'].mean()
CI12_mean_I = ave_group['CI12_I'].mean()
CI23_mean_I = ave_group['CI23_I'].mean()
CI34_mean_I = ave_group['CI34_I'].mean()

CR0_SD_P = ave_group['CR0_P'].std()
ICF1_SD_P = ave_group['ICF1_P'].std()
ICF2_SD_P = ave_group['ICF2_P'].std()
ICF3_SD_P = ave_group['ICF3_P'].std()
IFL1_SD_P = ave_group['IFL1_P'].std()
IFL2_SD_P = ave_group['IFL2_P'].std()
IFL3_SD_P = ave_group['IFL3_P'].std()
CR0_mean_P = ave_group['CR0_P'].mean()
ICF1_mean_P = ave_group['ICF1_P'].mean()
ICF2_mean_P = ave_group['ICF2_P'].mean()
ICF3_mean_P = ave_group['ICF3_P'].mean()
IFL1_mean_P = ave_group['IFL1_P'].mean()
IFL2_mean_P = ave_group['IFL2_P'].mean()
IFL3_mean_P = ave_group['IFL3_P'].mean()

saman['CR0_I'] = 100+(((saman['CR0_I']- CR0_mean_I ) / CR0_SD_I) * 10 )
saman['ICF1_I'] = 100+(((saman['ICF1_I']- ICF1_mean_I )*(-1) / ICF1_SD_I) * 10 )
saman['ICF2_I'] = 100+(((saman['ICF2_I']- ICF2_mean_I )*(-1) / ICF2_SD_I) * 10 )
saman['ICF3_I'] = 100+(((saman['ICF3_I']- ICF3_mean_I )*(-1) / ICF3_SD_I) * 10 )
saman['IFL1_I'] = 100+(((saman['IFL1_I']- IFL1_mean_I )*(-1) / IFL1_SD_I) * 10 )
saman['IFL2_I'] = 100+(((saman['IFL2_I']- IFL2_mean_I )*(-1) / IFL2_SD_I) * 10 )
saman['IFL3_I'] = 100+(((saman['IFL3_I']- IFL3_mean_I )*(-1) / IFL3_SD_I) * 10 )
saman['CI12_I'] = 100+(((saman['CI12_I']- CI12_mean_I )*(-1) / CI12_SD_I) * 10 )
saman['CI23_I'] = 100+(((saman['CI23_I']- CI23_mean_I )*(-1) / CI23_SD_I) * 10 )
saman['CI34_I'] = 100+(((saman['CI34_I']- CI34_mean_I )*(-1) / CI34_SD_I) * 10 )

saman['CR0_P'] = 100+(((saman['CR0_P']- CR0_mean_P ) / CR0_SD_P) * 10 )
saman['ICF1_P'] = 100+(((saman['ICF1_P']- ICF1_mean_P )*(-1) / ICF1_SD_P) * 10 )
saman['ICF2_P'] = 100+(((saman['ICF2_P']- ICF2_mean_P )*(-1) / ICF2_SD_P) * 10 )
saman['ICF3_P'] = 100+(((saman['ICF3_P']- ICF3_mean_P )*(-1) / ICF3_SD_P) * 10 )
saman['IFL1_P'] = 100+(((saman['IFL1_P']- IFL1_mean_P )*(-1) / IFL1_SD_P) * 10 )
saman['IFL2_P'] = 100+(((saman['IFL2_P']- IFL2_mean_P )*(-1) / IFL2_SD_P) * 10 )
saman['IFL3_P'] = 100+(((saman['IFL3_P']- IFL3_mean_P )*(-1) / IFL3_SD_P) * 10 )


#Creating a single ICF and IFL value
saman['ICF_I'] = (saman['ICF1_I']*0.5 + saman['ICF2_I']*0.3 + saman['ICF3_I'] * 0.2)
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

print(saman.iloc[550000:550020])
print(saman.info())

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
#Checking spearman correlations,
rho, p = spearmanr(sires50['frjosemi'], sires50['new_P'])
#This will print out in the terminal
print(rho)
print(p)
#Checking spearman correlations,
rho, p = spearmanr(sires50['frjosemi'], sires50['new_I'])
#This will print out in the terminal
print(rho)
print(p)
#------------------------------------------------------------------------------

#Creation of a plot that shows the avarege breeding value for the traits for
#each birth year
#This creates the figure and below it is possible to add another y-axis
fig, ax1 = plt.subplots()
ax1.set_xlim(2004, 2016)

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
ax1.plot(
    (sires50.groupby('BY')['frjosemi'].mean()),
    label='frjosemi',
    color='red',
    linewidth=3)

# #Creation of another y-axis in the same figure
# ax2 = ax1.twinx()
# ax2.plot(
#     (sires50.groupby('BY')['frjosemi'].mean()),
#     label='frjosemi',
#     color='red',
#     linewidth=3)
#------------------------------------------------------------------------------

#Show legends of plotted values, names are in 'label' above
ax1.legend()
# ax2.legend()

#Labels for x and y
ax1.set_xlabel('Birth Year' , fontsize = 15)
ax1.set_ylabel('EBV from DMU5, standardized to 100', fontsize = 15)
# ax2.set_ylabel('EBV from old kynbótamat', fontsize = 15)
#Title of plot
ax1.set_title('Average estimated breeding values by birth year for bulls that\
 have 50+ daughters', fontsize = 20)
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#Show the plot in home computer via Xming
plt.show()

print(sires50.iloc[300:315])
print(sires50.info())

sires50 = sires50.astype(float).round().astype(int)

# #Saves the dataframe to excel file
sires50.to_excel("../data/sires50_100scale20210824.xlsx", index=False, header=True)
#
# #plt.savefig('plot.png')
