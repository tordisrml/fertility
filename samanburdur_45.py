#This is a program to comapre results from dmu5 runs and dmu4 runs

import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import seaborn

saman = pd.read_csv(
    "../data/saman_G_4_5.txt",
    header=None,
    sep=' ',
    names=['id',
        'CR0_ICF','SE_CR_ICF','ICF1','SE_ICF1','ICF2','SE_ICF2',
        'ICF3','SE_ICF3', 'CR0_IFL', 'SE_CR_IFL', 'IFL1', 'SE_IFL1',
        'IFL2', 'SE_IFL2', 'IFL3', 'SE_IFL3',

        'CR0_P','ICF1_P','ICF2_P','ICF3_P','IFL1_P','IFL2_P','IFL3_P',
        'CI12_P','CI23_P','CI34_P',
        'fertility_1','fertility_2','fertility_3','frjosemi']
    )

#Reading in the file used in DMU so animals that have their own observations
#can be located
ownobs = pd.read_csv(
    "../data/dmu_fertilitynew2.txt",
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
#Merging ownobs and id file to bring back einstaklingsnumer used in huppa
ave_group = pd.merge(left=ownobs['id'], right=ave_group, on='id', how='left')

CR0_ICF_SD = ave_group['CR0_ICF'].std()
CR0_IFL_SD = ave_group['CR0_IFL'].std()
ICF1_SD = ave_group['ICF1'].std()
ICF2_SD = ave_group['ICF2'].std()
ICF3_SD = ave_group['ICF3'].std()
IFL1_SD = ave_group['IFL1'].std()
IFL2_SD = ave_group['IFL2'].std()
IFL3_SD = ave_group['IFL3'].std()
CR0_ICF_mean = ave_group['CR0_ICF'].mean()
CR0_IFL_mean = ave_group['CR0_IFL'].mean()
ICF1_mean = ave_group['ICF1'].mean()
ICF2_mean = ave_group['ICF2'].mean()
ICF3_mean = ave_group['ICF3'].mean()
IFL1_mean = ave_group['IFL1'].mean()
IFL2_mean = ave_group['IFL2'].mean()
IFL3_mean = ave_group['IFL3'].mean()


CI12_SD_P = ave_group['CI12_P'].std()
CI23_SD_P = ave_group['CI23_P'].std()
CI34_SD_P = ave_group['CI34_P'].std()
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

saman['CR0_ICF'] = 100+(((saman['CR0_ICF']- CR0_ICF_mean ) / CR0_ICF_SD) * 10 )
saman['CR0_IFL'] = 100+(((saman['CR0_IFL']- CR0_IFL_mean ) / CR0_IFL_SD) * 10 )
saman['ICF1'] = 100+(((saman['ICF1']- ICF1_mean )*(-1) / ICF1_SD) * 10 )
saman['ICF2'] = 100+(((saman['ICF2']- ICF2_mean )*(-1) / ICF2_SD) * 10 )
saman['ICF3'] = 100+(((saman['ICF3']- ICF3_mean )*(-1) / ICF3_SD) * 10 )
saman['IFL1'] = 100+(((saman['IFL1']- IFL1_mean )*(-1) / IFL1_SD) * 10 )
saman['IFL2'] = 100+(((saman['IFL2']- IFL2_mean )*(-1) / IFL2_SD) * 10 )
saman['IFL3'] = 100+(((saman['IFL3']- IFL3_mean )*(-1) / IFL3_SD) * 10 )
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
#------------------------------------------------------------------------------

#Creating a single ICF and IFL value
saman['CR0'] = ((saman['CR0_ICF'] + saman['CR0_IFL'])/2 )

saman['ICF'] = (saman['ICF1'] * 0.5 +
    saman['ICF2'] * 0.3 +
    saman['ICF3'] * 0.2 )
saman['IFL'] = (saman['IFL1'] * 0.5 +
    saman['IFL1'] * 0.3 +
    saman['IFL2'] * 0.2 )

saman['ICF_P'] = (saman['ICF1_P'] * 0.5 +
    saman['ICF2_P'] * 0.3 +
    saman['ICF3_P'] * 0.2 )
saman['IFL_P'] = (saman['IFL1_P'] * 0.5 +
    saman['IFL1_P'] * 0.3 +
    saman['IFL2_P'] * 0.2 )
saman['CI_P'] = (saman['CI12_P'] * 0.5 +
    saman['CI23_P'] * 0.3 +
    saman['CI34_P'] * 0.2 )

#------------------------------------------------------------------------------
#New breeding value inbreeding
saman['new_4'] = (saman['CR0'] * 0.2 +
    saman['ICF'] * 0.3 +
    saman['IFL'] * 0.5 )
#New breeding value phantom
saman['new_P'] = (saman['CR0_P'] * 0.2 +
    saman['ICF_P'] * 0.3 +
    saman['IFL_P'] * 0.5 )
#------------------------------------------------------------------------------

#Dataframe with animals born after 2006
saman2006 = saman[saman['BY'] > 2004]
#Reading in a file with sires that have more than 50 daughters
sires50 = pd.read_csv(
    "../data/sire_50.txt",
    header=None,
    sep = ' ',
    names=['id', 'sire_count']
    )
#Merging code sire file and and file with EBVs
sires50 = pd.merge(left=sires50, right=saman, on='id', how='left')

saman_own = pd.merge(left=ownobs['id'], right=saman, on='id', how='left')

#  #------------------------------------------------------------------------------
#  #------------------------------------------------------------------------------
# #Correlation heat map for traits in dataframe!
# plt.figure(figsize=(8,8))
# seaborn.heatmap(sires50[['CR0_ICF','ICF1','ICF2',
#         'ICF3','CR0_IFL','IFL1','IFL2','IFL3', 'CR0',
#         'CR0_P','ICF1_P','ICF2_P','ICF3_P','IFL1_P','IFL2_P','IFL3_P',
#         'CI12_P','CI23_P','CI34_P',
#         'fertility_1','fertility_2','fertility_3','frjosemi']
#     ].corr(), annot=True, cmap='coolwarm')
# plt.title('Fylgni á milli kynbótaeinkunna fyrir eiginleika hjá nautum sem\
#  eiga +50 dætur', fontsize = 20)
#  # Correlation heat map for traits in dataframe!
# plt.figure(figsize=(8,8))
# seaborn.heatmap(sires50[['CR0','CR0_P',
#      'ICF','ICF_P',
#      'IFL','IFL_P',
#      'new_4', 'new_P',
#      'CI_P','fertility_1','fertility_2','fertility_3','frjosemi']
#      ].corr(), annot=True, cmap='coolwarm')
# plt.title('Fylgni á milli kynbótaeinkunna fyrir eiginleika hjá nautum sem\
#   eiga +50 dætur', fontsize = 20)
#  #------------------------------------------------------------------------------
#  #------------------------------------------------------------------------------
#
# plt.figure(figsize=(8,8))
# seaborn.heatmap(saman2006[['CR0_ICF','ICF1','ICF2',
#          'ICF3','CR0_IFL','IFL1','IFL2','IFL3', 'CR0',
#          'CR0_P','ICF1_P','ICF2_P','ICF3_P','IFL1_P','IFL2_P','IFL3_P',
#          'CI12_P','CI23_P','CI34_P',
#          'fertility_1','fertility_2','fertility_3','frjosemi']
#      ].corr(), annot=True, cmap='coolwarm')
# plt.title('Fylgni á milli kynbótaeinkunna fyrir eiginleika hjá gripum\
#   fæddum eftir 2006', fontsize = 20)
# plt.figure(figsize=(8,8))
# seaborn.heatmap(saman2006[['CR0','CR0_P',
#     'ICF','ICF_P',
#     'IFL','IFL_P',
#     'new_4', 'new_P',
#     'CI_P','fertility_1','fertility_2','fertility_3','frjosemi']
#     ].corr(), annot=True, cmap='coolwarm')
# plt.title('Fylgni á milli kynbótaeinkunna fyrir eiginleika hjá gripum\
#  fæddum eftir 2006', fontsize = 20)
#
# #------------------------------------------------------------------------------
# #------------------------------------------------------------------------------
# plt.figure(figsize=(8,8))
# seaborn.heatmap(saman_own[
#     ['CR0_ICF','ICF1','ICF2',
#             'ICF3','CR0_IFL','IFL1','IFL2','IFL3', 'CR0',
#             'CR0_P','ICF1_P','ICF2_P','ICF3_P','IFL1_P','IFL2_P','IFL3_P',
#             'CI12_P','CI23_P','CI34_P',
#             'fertility_1','fertility_2','fertility_3','frjosemi']
#     ].corr(), annot=True, cmap='coolwarm')
# plt.title('Correlation between EBVs for animals that have their own observations\
#  for new fertility evaluation', fontsize = 20)
# # Correlation heat map for all traits in dataframe!
# plt.figure(figsize=(8,8))
# seaborn.heatmap(saman_own[['CR0','CR0_P',
#     'ICF','ICF_P',
#     'IFL','IFL_P',
#     'new_4', 'new_P',
#     'CI_P','fertility_1','fertility_2','fertility_3','frjosemi']
#     ].corr(), annot=True, cmap='coolwarm')
# plt.title('Correlation between EBVs for animals that have their own observations\
#  for new fertility evaluation', fontsize = 20)
# #------------------------------------------------------------------------------
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
#Creation of a plot that shows the avarege breeding value for the traits for
#each birth year
# #This creates the figure and below it is possible to add another y-axis
# fig, ax1 = plt.subplots()
# ax1.set_xlim(2006, 2018)
# ax1.set_ylim(80, 120)
#
# #Does not work, no style is used
# # plt.set_style.use('seaborn')
# # plt.sns.set_style("dark")
#
# #EBVs from DMU5
# ax1.plot(
#     (saman2006.groupby('BY')['CR0'].mean()),
#     label='CR0',
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
#     (saman2006.groupby('BY')['ICF'].mean()),
#     label='ICF',
#     color='mediumslateblue',
#     linewidth=3)
# ax1.plot(
#     (saman2006.groupby('BY')['ICF_P'].mean()),
#     label='ICF_P',
#     color='blue',
#     #linestyle='--',
#     linewidth=3)
# ax1.plot(
#     (saman2006.groupby('BY')['IFL'].mean()),
#     label='IFL',
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
#     (saman2006.groupby('BY')['new_4'].mean()),
#     label='new_4',
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
# ax1.set_ylabel('EBV from DMU5, standardized to 100 ', fontsize = 15)
# # ax2.set_ylabel('EBV from old kynbótamat', fontsize = 15)
# #Title of plot
# ax1.set_title('Average estimated breeding values by birth year for cows with \
# their observation for new fertility traits', fontsize = 20)

# sires50 = sires50.astype(float).round().astype(int)

genvar_CR0 = 0.0034468
genvar_ICF1 = 37.6831415
genvar_ICF2 = 57.5724257
genvar_ICF3 = 32.2040674
genvar_IFL1 = 43.5298544
genvar_IFL2 = 28.1500849
genvar_IFL3 = 43.2162786

#Accuraccy caluculations
sires50['CR_ICF_r'] = (np.sqrt(1-((sires50['SE_CR_ICF']**2)/genvar_CR0)))
sires50['CR_IFL_r'] = (np.sqrt(1-((sires50['SE_CR_IFL']**2)/genvar_CR0)))
sires50['ICF1_r'] = (np.sqrt(1-((sires50['SE_ICF1']**2)/genvar_ICF1)))
sires50['ICF2_r'] = (np.sqrt(1-((sires50['SE_ICF2']**2)/genvar_ICF2)))
sires50['ICF3_r'] = (np.sqrt(1-((sires50['SE_ICF3']**2)/genvar_ICF3)))
sires50['IFL1_r'] = (np.sqrt(1-((sires50['SE_IFL1']**2)/genvar_IFL1)))
sires50['IFL2_r'] = (np.sqrt(1-((sires50['SE_IFL2']**2)/genvar_IFL2)))
sires50['IFL3_r'] = (np.sqrt(1-((sires50['SE_IFL3']**2)/genvar_IFL3)))

siresprint = sires50[['id', 'sire_count',
        'CR0_ICF','CR_ICF_r', 'CR0_IFL', 'CR_IFL_r', 'CR0','CR0_P',
        'ICF1','ICF1_r','ICF2','ICF2_r',
        'ICF3','ICF3_r', 'ICF',  'ICF1_P','ICF2_P','ICF3_P',
        'IFL1', 'IFL1_r',
        'IFL2', 'IFL2_r', 'IFL3', 'IFL3_r','IFL', 'IFL1_P','IFL2_P','IFL3_P',

        'CI12_P','CI23_P','CI34_P', 'CI_P',
        'fertility_1','fertility_2','fertility_3','frjosemi','new_4', 'new_P']]



siresprint.to_excel("../data/sires50_100scale20211005.xlsx", index=False, header=True)


plt.show()
print(sires50.iloc[150:160])
print(sires50.info())
