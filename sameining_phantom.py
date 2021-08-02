#This is a program that takes DMU5 test files and collects in one file along
#with BLUP from old ferility breeding evaluation to be compared.
#Takes files from CR0_ICF_IFL_inbreed or
#From CR0_ICF_IFL_phantom

import pandas as pd
import numpy as np

#Reading in id codes to replace in SOL files
id_code = pd.read_csv(
    "/home/thordis/data/id_code.txt",
    header=None,
    sep = ' ',
    names=['id','code_id']
    )


#-------------------------------------------------------------
#CR0_ICF_IFL_inbreed
#-------------------------------------------------------------
#Reading in sol file
widths = [1,3,3,4,12,12,12,20,20]
sol = pd.read_fwf(
    "/home/thordis/DMUtests/CR0_ICF_IFL_phantom/SOL",
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
sol = sol[(sol['1_code_effect'] == 4) & (sol['code_id'] > 0)]
#-------------------------------------------------------------
#Merge the SOL and the id code file
sol= pd.merge(left=sol[
    ['code_id','2_trait_no', '6_no_obs','8_BLUP']
    ], right=id_code[['id','code_id']], on='code_id', how='left')
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
    ['id', 'BLUP_CR0']
    ], right=icf_sol1[['id','BLUP_ICF1']], on='id')
saman_phantom= pd.merge(left=saman_phantom, right=icf_sol2[['id','BLUP_ICF2']], on='id')
saman_phantom= pd.merge(left=saman_phantom, right=icf_sol3[['id','BLUP_ICF3']], on='id')
saman_phantom= pd.merge(left=saman_phantom, right=ifl_sol1[['id','BLUP_IFL1']], on='id')
saman_phantom= pd.merge(left=saman_phantom, right=ifl_sol2[['id','BLUP_IFL2']], on='id')
saman_phantom= pd.merge(left=saman_phantom, right=ifl_sol3[['id','BLUP_IFL3']], on='id')

#Creating a file with new results
saman_phantom.to_csv("../data/saman_phantom.txt", index=False, header=False, sep=' ')



print(saman_phantom.iloc[600000:600015])
print(saman_phantom.info())
