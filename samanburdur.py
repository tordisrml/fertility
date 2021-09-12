#Program in development
#Thordis Thorarinsdottir
#Finding ways to compara old and new fertility blup and
#use matplotlib

import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import seaborn

#Read in file where results from inbreeding, phantom group and old breeding
#value results are located.
saman = pd.read_csv(
    "../data/saman_I_P_G_20210912.txt",
    header=None,
    sep=' ',
    names=['id',
        'CR0_I','ICF1_I','ICF2_I','ICF3_I','IFL1_I','IFL2_I','IFL3_I',
        'CR0_P','ICF1_P','ICF2_P','ICF3_P','IFL1_P','IFL2_P','IFL3_P',
        'CI12_P','CI23_P','CI34_P',
        'fertility_1','fertility_2','fertility_3','frjosemi']
    )
#Reading in the file used in DMU so animals that have their own observations
#can be located
ownobs = pd.read_csv(
    "../data/dmu_fertility20210911.txt",
    header=None,
    sep=' ',
    names=['code_id','HBY','HC1','HC2','HC3','IYM0','IYM1','IYM2',
        'IYM3','AGEi_h','AGEc_1','AGEc_2','AGEc_3','tech_h',
        'CRh','ICF1','ICF2','ICF3','IFL1','IFL2','IFL3']
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
# ave_group = saman.loc[(saman['BY'] == 2016)]

#Merging ownobs and id file to bring back einstaklingsnumer used in huppa
ave_group = pd.merge(left=ownobs['id'], right=ave_group, on='id', how='left')
print(ave_group.iloc[300:315])
print(ave_group.info())

# CR0_SD_I = ave_group['CR0_I'].std()
# ICF1_SD_I = ave_group['ICF1_I'].std()
# ICF2_SD_I = ave_group['ICF2_I'].std()
# ICF3_SD_I = ave_group['ICF3_I'].std()
# IFL1_SD_I = ave_group['IFL1_I'].std()
# IFL2_SD_I = ave_group['IFL2_I'].std()
# IFL3_SD_I = ave_group['IFL3_I'].std()
CI12_SD_P = ave_group['CI12_P'].std()
CI23_SD_P = ave_group['CI23_P'].std()
CI34_SD_P = ave_group['CI34_P'].std()
# CR0_mean_I = ave_group['CR0_P'].mean()
# ICF1_mean_I = ave_group['ICF1_I'].mean()
# ICF2_mean_I = ave_group['ICF2_I'].mean()
# ICF3_mean_I = ave_group['ICF3_I'].mean()
# IFL1_mean_I = ave_group['IFL1_I'].mean()
# IFL2_mean_I = ave_group['IFL2_I'].mean()
# IFL3_mean_I = ave_group['IFL3_I'].mean()
CI12_mean_P = ave_group['CI12_P'].mean()
CI23_mean_P = ave_group['CI23_P'].mean()
CI34_mean_P = ave_group['CI34_P'].mean()

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

print(CR0_SD_P)
print(ICF1_SD_P)
print(ICF2_SD_P)
print(ICF3_SD_P)
print(IFL1_SD_P)
print(IFL2_SD_P)
print(IFL3_SD_P)
print(CR0_mean_P)
print(ICF1_mean_P)
print(ICF2_mean_P)
print(ICF3_mean_P)
print(IFL1_mean_P)
print(IFL2_mean_P)
print(IFL3_mean_P)
saman = saman.drop(
    ['CR0_I','ICF1_I','ICF2_I','ICF3_I','IFL1_I','IFL2_I','IFL3_I'], axis = 1)
#
# saman['ICF_Px'] = (
#     ((saman['ICF1_P']- IFL1_mean_P)*(-1)  / IFL1_SD_P)* 0.5 +
#     ((saman['ICF2_P']- IFL2_mean_P)*(-1)  / IFL2_SD_P) * 0.3 +
#     ((saman['ICF3_P']- IFL3_mean_P)*(-1)  / IFL3_SD_P)* 0.2
#     )

                                    #((mjalt1 - ave1)/ stdv1 * 10 )+ 100
# saman['CR0_I'] = 100+(((saman['CR0_I']- CR0_mean_I ) / CR0_SD_I) * 10 )
# saman['ICF1_I'] = 100+(((saman['ICF1_I']- ICF1_mean_I )*(-1) / ICF1_SD_I) * 10 )
# saman['ICF2_I'] = 100+(((saman['ICF2_I']- ICF2_mean_I )*(-1) / ICF2_SD_I) * 10 )
# saman['ICF3_I'] = 100+(((saman['ICF3_I']- ICF3_mean_I )*(-1) / ICF3_SD_I) * 10 )
# saman['IFL1_I'] = 100+(((saman['IFL1_I']- IFL1_mean_I )*(-1) / IFL1_SD_I) * 10 )
# saman['IFL2_I'] = 100+(((saman['IFL2_I']- IFL2_mean_I )*(-1) / IFL2_SD_I) * 10 )
# saman['IFL3_I'] = 100+(((saman['IFL3_I']- IFL3_mean_I )*(-1) / IFL3_SD_I) * 10 )
saman['CI12_P'] = 100+(((saman['CI12_P']- CI12_mean_P )*(-1) / CI12_SD_P) * 10 )
saman['CI23_P'] = 100+(((saman['CI23_P']- CI23_mean_P )*(-1) / CI23_SD_P) * 10 )
saman['CI34_P'] = 100+(((saman['CI34_P']- CI34_mean_P )*(-1) / CI34_SD_P) * 10 )

saman['CR0_P'] = 100+(((saman['CR0_P']- CR0_mean_P ) / CR0_SD_P) * 10 )
saman['ICF1_P'] = 100+(((saman['ICF1_P']- ICF1_mean_P )*(-1) / ICF1_SD_P) * 10 )
saman['ICF2_P'] = 100+(((saman['ICF2_P']- ICF2_mean_P )*(-1) / ICF2_SD_P) * 10 )
saman['ICF3_P'] = 100+(((saman['ICF3_P']- ICF3_mean_P )*(-1) / ICF3_SD_P) * 10 )
saman['IFL1_P'] = 100+(((saman['IFL1_P']- IFL1_mean_P )*(-1) / IFL1_SD_P) * 10 )
saman['IFL2_P'] = 100+(((saman['IFL2_P']- IFL2_mean_P )*(-1) / IFL2_SD_P) * 10 )
saman['IFL3_P'] = 100+(((saman['IFL3_P']- IFL3_mean_P )*(-1) / IFL3_SD_P) * 10 )
# saman['ICF_Px'] = 100+(((saman['ICF_Px']- IFL3_mean_P )*(-1) / IFL3_SD_P) * 10 )
# saman['ICF_Px'] = 100+(saman['ICF_Px'] * 10)



#------------------------------------------------------------------------------

#Creating a single ICF and IFL value
# saman['ICF_I'] = (saman['ICF1_I'] * 0.5 +
#     saman['ICF2_I'] * 0.3 +
#     saman['ICF3_I'] * 0.2 )
saman['ICF_P'] = (saman['ICF1_P'] * 0.5 +
    saman['ICF2_P'] * 0.3 +
    saman['ICF3_P'] * 0.2 )
# saman['IFL_I'] = (saman['IFL1_I'] * 0.5 +
#     saman['IFL1_I'] * 0.3 +
#     saman['IFL2_I'] * 0.2 )
saman['IFL_P'] = (saman['IFL1_P'] * 0.5 +
    saman['IFL1_P'] * 0.3 +
    saman['IFL2_P'] * 0.2 )
saman['CI_P'] = (saman['CI12_P'] * 0.5 +
    saman['CI23_P'] * 0.3 +
    saman['CI34_P'] * 0.2 )
#------------------------------------------------------------------------------
#New breeding value inbreeding
# saman['new_I'] = (saman['CR0_I'] * 0.2 +
#     saman['ICF_I'] * 0.3 +
#     saman['IFL_I'] * 0.5 )
#New breeding value phantom
saman['new_P'] = (saman['CR0_P'] * 0.2 +
    saman['ICF_P'] * 0.3 +
    saman['IFL_P'] * 0.5 )

print(saman.iloc[300000:300015])
print(saman.info())
#------------------------------------------------------------------------------
#
# #Saves the dataframe to excel file
saman = saman.sort_values(by=['id'])
samanprint = saman[['id', 'CR0_P',
    'ICF1_P','ICF2_P','ICF3_P','ICF_P',
    'IFL1_P','IFL2_P','IFL3_P','IFL_P',
    'CI12_P','CI23_P','CI34_P', 'CI_P',
    'fertility_1','fertility_2','fertility_3','frjosemi','new_P']]
# samanprint.to_excel("../data/allblup10020210909.xlsx", index=False, header=True)
# samanprint.to_csv("../data/allblup10020210912x.txt", index=False, header=False, sep=' ')
# print(samanprint.info())
#
#
# #Only plot animals born after a certain year
# #Create new dataframe
# saman2006 = saman[saman['BY'] > 2006]
# # #------------------------------------------------------------------------------
# # #Correlation heat map for all traits in dataframe!
# # plt.figure(figsize=(8,8))
# # seaborn.heatmap(saman2006[['CR0_I', 'CR0_P',
# #     'ICF1_I','ICF2_I','ICF3_I',
# #     'ICF1_P','ICF2_P','ICF3_P',
# #     'IFL1_I','IFL2_I','IFL3_I',
# #     'IFL1_P','IFL2_P','IFL3_P',
# #     'CI12_P','CI23_P','CI34_P',
# #     'fertility_1','fertility_2','fertility_3','frjosemi']
# #     ].corr(), annot=True, cmap='coolwarm')
# # plt.title('Fylgni á milli kynbótaeinkunna fyrir eiginleika hjá gripum\
# #  fæddum eftir 2006', fontsize = 20)
# #
# # # Correlation heat map for all traits in dataframe!
# # plt.figure(figsize=(8,8))
# # seaborn.heatmap(saman2006[['CR0_I','CR0_P',
# #     'ICF_I','ICF_P',
# #     'IFL_I','IFL_P',
# #     'new_I', 'new_P',
# #     'CI_P',
# #     'fertility_1','fertility_2','fertility_3','frjosemi']
# #     ].corr(), annot=True, cmap='coolwarm')
# # plt.title('Fylgni á milli kynbótaeinkunna fyrir eiginleika hjá gripum\
# #  fæddum eftir 2006', fontsize = 20)
# # #------------------------------------------------------------------------------
#
# #Print info and a part of the dataset
# print(saman2006.iloc[50000:50030])
# print(saman2006.info())
# #------------------------------------------------------------------------------
# #------------------------------------------------------------------------------
# #Creation of a plot that shows the avarege breeding value for the traits for
# #each birth year
# #This creates the figure and below it is possible to add another y-axis
# fig, ax1 = plt.subplots()
# ax1.set_xlim(2008, 2020)
#
# #EBVs from DMU5
# ax1.plot(
#     (saman2006.groupby('BY')['CR0_I'].mean()),
#     label='CR_I',
#     color='slategrey',
#     linestyle=':',
#     linewidth=3)
# ax1.plot(
#     (saman2006.groupby('BY')['CR0_P'].mean()),
#     label='CR_P',
#     color='black',
#     linestyle=':',
#     linewidth=3)
# ax1.plot(
#     (saman2006.groupby('BY')['ICF_I'].mean()),
#     label='ICF_I',
#     color='mediumslateblue',
#     linewidth=3)
# ax1.plot(
#     (saman2006.groupby('BY')['ICF_P'].mean()),
#     label='ICF_P',
#     color='blue',
#     #linestyle='--',
#     linewidth=3)
# ax1.plot(
#     (saman2006.groupby('BY')['IFL_I'].mean()),
#     label='IFL_I',
#     color='aquamarine',
#     linewidth=3)
# ax1.plot(
#     (saman2006.groupby('BY')['IFL_P'].mean()),
#     label='IFL_P',
#     color='green',
#     #linestyle='--',
#     linewidth=3)
# ax1.plot(
#     (saman2006.groupby('BY')['CI_P'].mean()),
#     label='CI_P',
#     color='yellow',
#     linestyle='--',
#     linewidth=3)
# ax1.plot(
#     (saman2006.groupby('BY')['new_I'].mean()),
#     label='new_I',
#     color='orchid',
#     linestyle='-.',
#     linewidth=3)
# ax1.plot(
#     (saman2006.groupby('BY')['new_P'].mean()),
#     label='new_P',
#     color='deeppink',
#     linestyle='-.',
#     linewidth=3)
# #Creation of another y-axis in the same figure
# # ax2 = ax1.twinx()
#
# ax1.plot(
#     (saman2006.groupby('BY')['frjosemi'].mean()),
#     label='frjosemi',
#     color='red',
#     linewidth=3)
#
# #Show legends of plotted values, names are in 'label' above
# ax1.legend()
# # ax2.legend()
#
# #Labels for x and y
# ax1.set_xlabel('Birth Year' , fontsize = 15)
# ax1.set_ylabel('EBV from DMU5, standardized to 100', fontsize = 15)
# # ax2.set_ylabel('EBV from old kynbótamat', fontsize = 15)
# #Title of plot
# ax1.set_title('Average estimated breeding values by birth year for animals  \
# born after 2006', fontsize = 20)
#
#
# #Show the plot in home computer via Xming
# plt.show()
# #
# # #plt.savefig('plot.png')
