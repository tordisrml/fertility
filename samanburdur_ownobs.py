#Program in development
#Finding ways to compara old and new fertility blup and
#use matplotlib

import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns

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
        'CI12_I','CI23_I','CI34_I',
        'fertility_1','fertility_2','fertility_3','frjosemi']
    )

ownobs = pd.read_csv(
    "../data/dmu_fertility.txt",
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

ownobs = pd.merge(left=ownobs[
    ['code_id']
    ], right=id_code[['id','code_id']], on='code_id', how='left')

saman = pd.merge(left=ownobs['id'], right=saman, on='id', how='left')


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

#Only plot animals born after 2000
# saman2006 = saman[saman['BY'] > 2006]

# #Correlation heat map for all traits in dataframe!
# plt.figure(figsize=(8,8))
# seaborn.heatmap(saman[['CR0_I', 'CR0_P',
#     'ICF1_I','ICF2_I','ICF3_I',
#     'ICF1_P','ICF2_P','ICF3_P',
#     'IFL1_I','IFL2_I','IFL3_I',
#     'IFL1_P','IFL2_P','IFL3_P',
#     'CI12_I','CI23_I','CI34_I',
#     'fertility_1','fertility_2','fertility_3','frjosemi']].corr(), annot=True, cmap='coolwarm')
# plt.title('Fylgni á milli kynbótaeinkunna fyrir eiginleika hjá gripum fæddum eftir 2006', fontsize = 20)
#
# # Correlation heat map for all traits in dataframe!
# plt.figure(figsize=(8,8))
# seaborn.heatmap(saman[['CR0_I','CR0_P',
#     'ICF_I','ICF_P',
#     'IFL_I','IFL_P',
#     'new_I', 'new_P',
#     'CI_I',
#     'fertility_1','fertility_2','fertility_3','frjosemi']].corr(), annot=True, cmap='coolwarm')
# plt.title('Fylgni á milli kynbótaeinkunna fyrir eiginleika hjá gripum fæddum eftir 2006', fontsize = 20)

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



#Print info and a part of the dataset
print(saman.iloc[450000:450030])
print(saman.info())




#Style of plot
#plt.style.use('Solarize_Light2')
#Print to see avalable styles
# print(plt.style.available) mediumslateblue

# plt.plot((saman2001.groupby('BY')['ICF1_I'].mean()), label='ICF1_I', color='mediumslateblue')
# plt.plot((saman2001.groupby('BY')['ICF2_I'].mean()), label='ICF2_I', color='royalblue' )
# plt.plot((saman2001.groupby('BY')['ICF3_I'].mean()), label='ICF3_I', color='navy')
# plt.plot((saman2001.groupby('BY')['ICF1_P'].mean()), label='ICF1_P', color='cornflowerblue')
# plt.plot((saman2001.groupby('BY')['ICF2_P'].mean()), label='ICF2_P', color='mediumblue')
# # plt.plot((saman2001.groupby('BY')['ICF3_P'].mean()), label='ICF3_P', color='slateblue')
# plt.plot((saman2001.groupby('BY')['ICF_I'].mean()), label='ICF_I', color='mediumslateblue', linewidth=4)
# plt.plot((saman2001.groupby('BY')['ICF_P'].mean()), label='ICF_P', color='blue', linewidth=4)
#
# # plt.plot((saman2001.groupby('BY')['IFL1_I'].mean()), label='IFL1_I', color='green')
# # plt.plot((saman2001.groupby('BY')['IFL2_I'].mean()), label='IFL2_I', color='forestgreen')
# # plt.plot((saman2001.groupby('BY')['IFL3_I'].mean()), label='IFL3_I', color='mediumseagreen')
# # plt.plot((saman2001.groupby('BY')['IFL1_P'].mean()), label='IFL1_P', color='springgreen')
# # plt.plot((saman2001.groupby('BY')['IFL2_P'].mean()), label='IFL2_P', color='aquamarine')
# # plt.plot((saman2001.groupby('BY')['IFL3_P'].mean()), label='IFL3_P', color='seagreen')
# plt.plot((saman2001.groupby('BY')['IFL_I'].mean()), label='IFL_I', color='lime', linewidth=4)
# plt.plot((saman2001.groupby('BY')['IFL_P'].mean()), label='IFL_P', color='limegreen', linewidth=4)
#
# plt.plot((saman2001.groupby('BY')['CR0_I'].mean()), label='CR0_I', color='slategrey', linewidth=4)
# plt.plot((saman2001.groupby('BY')['CR0_P'].mean()), label='CR0_P', color='black', linewidth=4)
#
# plt.plot((saman2001.groupby('BY')['new_I'].mean()), label='new_I', color='orchid', linewidth=4)
# plt.plot((saman2001.groupby('BY')['new_P'].mean()), label='new_P', color='deeppink', linewidth=4)
# plt.plot((saman2001.groupby('BY')['CI_I'].mean()), label='CI_I', color='yellow', linewidth=4)
# plt.plot((saman2001.groupby('BY')['frjosemi'].mean()), label='frjosemi', color='red')


fig, ax1 = plt.subplots()
ax1.set_xlim(2006, 2020)

# plt.set_style.use('seaborn')
# plt.sns.set_style("dark")

ax1.plot(
    (saman.groupby('BY')['CR0_I'].mean()),
    label='CR_I',
    color='slategrey',
    linestyle=':',
    linewidth=3)

ax1.plot(
    (saman.groupby('BY')['CR0_P'].mean()),
    label='CR_P',
    color='black',
    linestyle=':',
    linewidth=3)

ax1.plot(
    (saman.groupby('BY')['ICF_I'].mean()),
    label='ICF_I',
    color='mediumslateblue',
    linewidth=3)

ax1.plot(
    (saman.groupby('BY')['ICF_P'].mean()),
    label='ICF_P',
    color='blue',
    #linestyle='--',
    linewidth=3)

ax1.plot(
    (saman.groupby('BY')['IFL_I'].mean()),
    label='IFL_I',
    color='aquamarine',
    linewidth=3)

ax1.plot(
    (saman.groupby('BY')['IFL_P'].mean()),
    label='IFL_P',
    color='green',
    #linestyle='--',
    linewidth=3)

ax1.plot(
    (saman.groupby('BY')['CI_I'].mean()),
    label='CI_I',
    color='yellow',
    linestyle='--',
    linewidth=3)

ax1.plot(
    (saman.groupby('BY')['new_I'].mean()),
    label='new_I',
    color='orchid',
    linestyle='-.',
    linewidth=3)


ax1.plot(
    (saman.groupby('BY')['new_P'].mean()),
    label='new_P',
    color='deeppink',
    linestyle='-.',
    linewidth=3)



ax2 = ax1.twinx()

ax2.plot(
    (saman.groupby('BY')['frjosemi'].mean()),
    label='frjosemi',
    color='red',
    linewidth=3)

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






#Gamalt:
# #Labels for x and y
# plt.xlabel('Birth Year')
# plt.ylabel('EBV')
# #Title of plot
# plt.title('Estimated breeding values for ICF and IFL by Birth year')

#Show legends of plotted values, names are in 'label' above
# plt.legend()
#
# #Show the plot in home computer via Xming
plt.show()

#plt.savefig('plot.png')
