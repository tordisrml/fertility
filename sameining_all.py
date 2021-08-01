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
#Reading in the old fertility breeding results
gamla = pd.read_csv(
    "../data/gamla_mat.txt",
    header=None,
    sep=' ',
    names=['id','fertility_1','fertility_2','fertility_3','frjosemi']
    )

widths = [1,3,3,4,12,12,12,20,20]

#-------------------------------------------------------------
#CR0_ICF_IFL_inbreed
#-------------------------------------------------------------
#Reading in sol file
sol = pd.read_fwf(
    "/home/thordis/DMUtests/CR0_ICF_IFL_inbreed/SOL",
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
sol = sol[sol['1_code_effect'] == 4 ]
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
cr_sol['BLUP_CR0_I'] = cr_sol['8_BLUP']
icf_sol1['BLUP_ICF1_I'] = icf_sol1['8_BLUP']
icf_sol2['BLUP_ICF2_I'] = icf_sol2['8_BLUP']
icf_sol3['BLUP_ICF3_I'] = icf_sol3['8_BLUP']
ifl_sol1['BLUP_IFL1_I'] = ifl_sol1['8_BLUP']
ifl_sol2['BLUP_IFL2_I'] = ifl_sol2['8_BLUP']
ifl_sol3['BLUP_IFL3_I'] = ifl_sol3['8_BLUP']
#Merge the files so there will be a file with one line per cow with all solutions
saman_inbreed= pd.merge(left=cr_sol[
    ['id', 'BLUP_CR0_I']
    ], right=icf_sol1[['id','BLUP_ICF1_I']], on='id')
saman_inbreed= pd.merge(left=saman_inbreed, right=icf_sol2[['id','BLUP_ICF2_I']], on='id')
saman_inbreed= pd.merge(left=saman_inbreed, right=icf_sol3[['id','BLUP_ICF3_I']], on='id')
saman_inbreed= pd.merge(left=saman_inbreed, right=ifl_sol1[['id','BLUP_IFL1_I']], on='id')
saman_inbreed= pd.merge(left=saman_inbreed, right=ifl_sol2[['id','BLUP_IFL2_I']], on='id')
saman_inbreed= pd.merge(left=saman_inbreed, right=ifl_sol3[['id','BLUP_IFL3_I']], on='id')

#Creating a file with new and old results.
#saman_inbreed = pd.merge(left=saman, right=gamla, on='id')
#saman_inbreed.to_csv("../data/saman_inbreed.txt", index=False, header=False, sep=' ')

#-------------------------------------------------------------
#CR0_ICF_IFL_phantom
#-------------------------------------------------------------
#Reading in sol file
sol2 = pd.read_fwf(
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
sol2 = sol2[sol2['1_code_effect'] == 4 ]
#-------------------------------------------------------------
#Merge the SOL and the id code file
sol2= pd.merge(left=sol2[
    ['code_id','2_trait_no', '6_no_obs','8_BLUP']
    ], right=id_code[['id','code_id']], on='code_id', how='left')
#Split the large file into smaller ones by lactations
cr_sol = sol2[sol2['2_trait_no'] == 1 ]
icf_sol1 = sol2[sol2['2_trait_no'] == 2 ]
icf_sol2 = sol2[sol2['2_trait_no'] == 3 ]
icf_sol3 = sol2[sol2['2_trait_no'] == 4 ]
ifl_sol1 = sol2[sol2['2_trait_no'] == 5 ]
ifl_sol2 = sol2[sol2['2_trait_no'] == 6 ]
ifl_sol3 = sol2[sol2['2_trait_no'] == 7 ]
#Rename the BLUP solutions for each trait by the trait and lactation
cr_sol['BLUP_CR0_P'] = cr_sol['8_BLUP']
icf_sol1['BLUP_ICF1_P'] = icf_sol1['8_BLUP']
icf_sol2['BLUP_ICF2_P'] = icf_sol2['8_BLUP']
icf_sol3['BLUP_ICF3_P'] = icf_sol3['8_BLUP']
ifl_sol1['BLUP_IFL1_P'] = ifl_sol1['8_BLUP']
ifl_sol2['BLUP_IFL2_P'] = ifl_sol2['8_BLUP']
ifl_sol3['BLUP_IFL3_P'] = ifl_sol3['8_BLUP']
#Merge the files so there will be a file with one line per cow with all solutions
saman_phantom= pd.merge(left=cr_sol[
    ['id', 'BLUP_CR0_P']
    ], right=icf_sol1[['id','BLUP_ICF1_P']], on='id')
saman_phantom= pd.merge(left=saman_phantom, right=icf_sol2[['id','BLUP_ICF2_P']], on='id')
saman_phantom= pd.merge(left=saman_phantom, right=icf_sol3[['id','BLUP_ICF3_P']], on='id')
saman_phantom= pd.merge(left=saman_phantom, right=ifl_sol1[['id','BLUP_IFL1_P']], on='id')
saman_phantom= pd.merge(left=saman_phantom, right=ifl_sol2[['id','BLUP_IFL2_P']], on='id')
saman_phantom= pd.merge(left=saman_phantom, right=ifl_sol3[['id','BLUP_IFL3_P']], on='id')
#Creating a file with new and old results.
# saman_phantom = pd.merge(left=saman, right=gamla, on='id')
# saman_phantom.to_csv("../data/saman_phantom.txt", index=False, header=False, sep=' ')


#Inbreeding results and phantom group results together in a file
saman_allt = pd.merge(left=saman_inbreed, right=saman_phantom, on='id')
saman_allt = pd.merge(left=saman_allt, right=gamla, on='id')
saman_allt.to_csv("../data/saman_allt.txt", index=False, header=False, sep=' ')


print(saman_allt.iloc[600000:600015])
print(saman_allt.info())
