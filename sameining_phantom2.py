#This is a program that takes DMU5 SOL file from the 7 trait phantom group
#test run and creates a new file for BLUP results
#Thordis Thorarinsdottir 2021

import pandas as pd
import numpy as np


#-------------------------------------------------------------
#CR0_ICF_IFL_phantom
#-------------------------------------------------------------
#Reading in sol file
widths = [1,3,3,4,12,12,12,20,20]
sol = pd.read_fwf(
    "/home/thordis/DMUtests/7trait_p/SOL",
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
#AND ID OVER 0 BECAUSE OF PHANTOM GROUP PARENTS
# sol = sol[(sol['1_code_effect'] == 4) & (sol['code_id'] > 0)]
sol = sol[(sol['1_code_effect'] == 4) & (sol['code_id'] < 0)]
print(sol.iloc[6:15])
print(sol.info())
#-------------------------------------------------------------

#Split the large file into smaller ones by lactations
cr_sol = sol[sol['2_trait_no'] == 1 ]
icf_sol1 = sol[sol['2_trait_no'] == 2 ]
icf_sol2 = sol[sol['2_trait_no'] == 3 ]
icf_sol3 = sol[sol['2_trait_no'] == 4 ]
ifl_sol1 = sol[sol['2_trait_no'] == 5 ]
ifl_sol2 = sol[sol['2_trait_no'] == 6 ]
ifl_sol3 = sol[sol['2_trait_no'] == 7 ]
#Rename the BLUP solutions for each trait by the trait and lactation
cr_sol['BLUP_CR0'] = cr_sol['8_BLUP']
icf_sol1['BLUP_ICF1'] = icf_sol1['8_BLUP']
icf_sol2['BLUP_ICF2'] = icf_sol2['8_BLUP']
icf_sol3['BLUP_ICF3'] = icf_sol3['8_BLUP']
ifl_sol1['BLUP_IFL1'] = ifl_sol1['8_BLUP']
ifl_sol2['BLUP_IFL2'] = ifl_sol2['8_BLUP']
ifl_sol3['BLUP_IFL3'] = ifl_sol3['8_BLUP']
#Merge the files so there will be a file with one line per cow with all solutions
saman_phantom= pd.merge(left=cr_sol[
    ['code_id', 'BLUP_CR0']
    ], right=icf_sol1[['code_id','BLUP_ICF1']], on='code_id')
saman_phantom= pd.merge(left=saman_phantom, right=icf_sol2[['code_id','BLUP_ICF2']
    ], on='code_id')
saman_phantom= pd.merge(left=saman_phantom, right=icf_sol3[['code_id','BLUP_ICF3']
    ], on='code_id')
saman_phantom= pd.merge(left=saman_phantom, right=ifl_sol1[['code_id','BLUP_IFL1']
    ], on='code_id')
saman_phantom= pd.merge(left=saman_phantom, right=ifl_sol2[['code_id','BLUP_IFL2']
    ], on='code_id')
saman_phantom= pd.merge(left=saman_phantom, right=ifl_sol3[['code_id','BLUP_IFL3']
    ], on='code_id')

#Creating a file with new results
saman_phantom.to_excel("../data/saman_PHG.xlsx", index=False, header=True)
#
print(saman_phantom.iloc[6:15])
print(saman_phantom.info())
