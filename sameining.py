#This is a program that takes DMU5 test files and collects in one file along
#with BLUP from old ferility breeding evaluation to be compared. 

import pandas as pd
import numpy as np

import math
import statistics
import scipy.stats

#Reading in id codes to replace in SOL files
id_code = pd.read_csv(
    "/home/thordis/data/id_code.txt",
    header=None,
    sep = ' ',
    names=['id','code_id']
    )
#Reading in the old fertility breeding results
gamla = pd.read_csv(
    "../data/gamla_mat.txt",
    header=None,
    sep=' ',
    names=['id','fertility_1','fertility_2','fertility_3','frjosemi']
    )

widths = [1,3,3,4,12,12,12,20,20]

#-------------------------------------------------------------
#Reading in sol file
sol = pd.read_fwf(
    "/home/thordis/DMUtests/ICF_noscale/SOL",
    header=None,
    widths=widths,
    names=['1_code_effect', #2 for fixed and 4 for genetic
        '2_trait_no',   # lact 1, 2 or 3
        '3',
        '4',
        'code_id',   #fixed effects and id's
        '6_no_obs',  #No. of observations in this class
        '7',
        '8_BLUP',  #Estimate/prediction
        '9'   #Solution from the second but last DMU5
    ]
    )
#Only keep genetic effectss
icf_sol = sol[sol['1_code_effect'] == 4 ]
#-------------------------------------------------------------
#Merge the SOL and the id code file
icf_sol= pd.merge(left=icf_sol[
    ['code_id','2_trait_no', '6_no_obs','8_BLUP']
    ], right=id_code[['id','code_id']], on='code_id', how='left')
#Split the large file into smaller ones by lactations
icf_sol1 = icf_sol[icf_sol['2_trait_no'] == 1 ]
icf_sol2 = icf_sol[icf_sol['2_trait_no'] == 2 ]
icf_sol3 = icf_sol[icf_sol['2_trait_no'] == 3 ]
#Rename the BLUP solutions for each trait by the trait and lactation
icf_sol1['BLUP_ICF1'] = icf_sol1['8_BLUP']
icf_sol2['BLUP_ICF2'] = icf_sol2['8_BLUP']
icf_sol3['BLUP_ICF3'] = icf_sol3['8_BLUP']
#Merge the files so there will be a file with one line per cow with all solutions
saman= pd.merge(left=icf_sol1[
    ['id', 'BLUP_ICF1']
    ], right=icf_sol2[['id','BLUP_ICF2']], on='id')
saman= pd.merge(left=saman, right=icf_sol3[['id','BLUP_ICF3']], on='id')

# #-------------------------------------------------------------
# #Reading in sol file
# sol = pd.read_fwf(
#     "/home/thordis/DMUtests/ICF_scale/SOL",
#     header=None,
#     widths=widths,
#     names=['1_code_effect', #2 for fixed and 4 for genetic
#         '2_trait_no',   # lact 1, 2 or 3
#         '3',
#         '4',
#         'code_id',   #fixed effects and id's
#         '6_no_obs',  #No. of observations in this class
#         '7',
#         '8_BLUP',  #Estimate/prediction
#         '9'   #Solution from the second but last DMU5
#     ]
#     )
# #Only keep genetic effectss
# icf_sol_s = sol[sol['1_code_effect'] == 4 ]
# #-------------------------------------------------------------
# #Merge the SOL and the id code file
# icf_sol_s= pd.merge(left=icf_sol_s[
#     ['code_id','2_trait_no', '6_no_obs','8_BLUP']
#     ], right=id_code[['id','code_id']], on='code_id', how='left')
# #Split the large file into smaller ones by lactations
# icf_sol1_s = icf_sol_s[icf_sol_s['2_trait_no'] == 1 ]
# icf_sol2_s = icf_sol_s[icf_sol_s['2_trait_no'] == 2 ]
# icf_sol3_s = icf_sol_s[icf_sol_s['2_trait_no'] == 3 ]
# #Rename the BLUP solutions for each trait by the trait and lactation
# icf_sol1_s['BLUP_ICF1_s'] = icf_sol1_s['8_BLUP']
# icf_sol2_s['BLUP_ICF2_s'] = icf_sol2_s['8_BLUP']
# icf_sol3_s['BLUP_ICF3_s'] = icf_sol3_s['8_BLUP']
# #Merge the files so there will be a file with one line per cow with all solutions
# saman= pd.merge(left=saman, right=icf_sol1_s[['id','BLUP_ICF1_s']], on='id')
# saman= pd.merge(left=saman, right=icf_sol2_s[['id','BLUP_ICF2_s']], on='id')
# saman= pd.merge(left=saman, right=icf_sol3_s[['id','BLUP_ICF3_s']], on='id')

#-------------------------------------------------------------
#Reading in sol file
sol = pd.read_fwf(
    "/home/thordis/DMUtests/IFL_noscale/SOL",
    header=None,
    widths=widths,
    names=['1_code_effect', #2 for fixed and 4 for genetic
        '2_trait_no',   # lact 1, 2 or 3
        '3',
        '4',
        'code_id',   #fixed effects and id's
        '6_no_obs',  #No. of observations in this class
        '7',
        '8_BLUP',  #Estimate/prediction
        '9'   #Solution from the second but last DMU5
    ]
    )
#Only keep genetic effectss
ifl_sol = sol[sol['1_code_effect'] == 4 ]
#-------------------------------------------------------------
#Merge the SOL and the id code file
ifl_sol= pd.merge(left=ifl_sol[
    ['code_id','2_trait_no', '6_no_obs','8_BLUP']
    ], right=id_code[['id','code_id']], on='code_id', how='left')
#Split the large file into smaller ones by lactations
ifl_sol1 = ifl_sol[ifl_sol['2_trait_no'] == 1 ]
ifl_sol2 = ifl_sol[ifl_sol['2_trait_no'] == 2 ]
ifl_sol3 = ifl_sol[ifl_sol['2_trait_no'] == 3 ]
#Rename the BLUP solutions for each trait by the trait and lactation
ifl_sol1['BLUP_IFL1'] = ifl_sol1['8_BLUP']
ifl_sol2['BLUP_IFL2'] = ifl_sol2['8_BLUP']
ifl_sol3['BLUP_IFL3'] = ifl_sol3['8_BLUP']
#Merge the files so there will be a file with one line per cow with all solutions
saman= pd.merge(left=saman, right=ifl_sol1[['id','BLUP_IFL1']], on='id')
saman= pd.merge(left=saman, right=ifl_sol2[['id','BLUP_IFL2']], on='id')
saman= pd.merge(left=saman, right=ifl_sol3[['id','BLUP_IFL3']], on='id')

# #-------------------------------------------------------------
# #Reading in sol file
# sol = pd.read_fwf(
#     "/home/thordis/DMUtests/IFL_scale/SOL",
#     header=None,
#     widths=widths,
#     names=['1_code_effect', #2 for fixed and 4 for genetic
#         '2_trait_no',   # lact 1, 2 or 3
#         '3',
#         '4',
#         'code_id',   #fixed effects and id's
#         '6_no_obs',  #No. of observations in this class
#         '7',
#         '8_BLUP',  #Estimate/prediction
#         '9'   #Solution from the second but last DMU5
#     ]
#     )
# #Only keep genetic effectss
# ifl_sol_s = sol[sol['1_code_effect'] == 4 ]
# #-------------------------------------------------------------
# #Merge the SOL and the id code file
# ifl_sol_s= pd.merge(left=ifl_sol_s[
#     ['code_id','2_trait_no', '6_no_obs','8_BLUP']
#     ], right=id_code[['id','code_id']], on='code_id', how='left')
# #Split the large file into smaller ones by lactations
# ifl_sol1_s = ifl_sol_s[ifl_sol_s['2_trait_no'] == 1 ]
# ifl_sol2_s = ifl_sol_s[ifl_sol_s['2_trait_no'] == 2 ]
# ifl_sol3_s = ifl_sol_s[ifl_sol_s['2_trait_no'] == 3 ]
# #Rename the BLUP solutions for each trait by the trait and lactation
# ifl_sol1_s['BLUP_IFL1_s'] = ifl_sol1_s['8_BLUP']
# ifl_sol2_s['BLUP_IFL2_s'] = ifl_sol2_s['8_BLUP']
# ifl_sol3_s['BLUP_IFL3_s'] = ifl_sol3_s['8_BLUP']
# #Merge the files so there will be a file with one line per cow with all solutions
# saman= pd.merge(left=saman, right=ifl_sol1_s[['id','BLUP_IFL1_s']], on='id')
# saman= pd.merge(left=saman, right=ifl_sol2_s[['id','BLUP_IFL2_s']], on='id')
# saman= pd.merge(left=saman, right=ifl_sol3_s[['id','BLUP_IFL3_s']], on='id')



#Creating a file with new and old results.
saman = pd.merge(left=saman, right=gamla, on='id')


saman.to_csv("../data/saman.txt", index=False, header=False, sep=' ')



# ICF_frjos1 = saman['fertility_1'].corr(saman['BLUP_ICF1'])
# ICF_frjos2 = saman['fertility_2'].corr(saman['BLUP_ICF2'])
# ICF_frjos3 = saman['fertility_3'].corr(saman['BLUP_ICF3'])
#
# print('ICF_frjos1')
# print(ICF_frjos1)
# print('ICF_frjos2')
# print(ICF_frjos2)
# print('ICF_frjos3')
# print(ICF_frjos3)

# print(df.iloc[500000:500015])
# print(df.info())
print(saman.iloc[600000:600015])
print(saman.info())
