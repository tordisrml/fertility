#This is a program that takes DMU5 SOL file from the 7 trait inbreeding
#test run and creates a new file for BLUP results
#Thordis Thorarinsdottir 2021

#MUNA AÐ Í CR IFL ER CR AFTAST!!!!!!


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
#CR0_ICF_inbreed4
#-------------------------------------------------------------
#Reading in sol file
widths = [1,3,3,4,12,12,12,20,20]
sol1 = pd.read_fwf(
    "//home/thordis/DMU4tests/Inbreeding/CR_ICF/SOL",
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
        'SE'   #S
    ]
    )
#Only keep genetic effectss
sol1 = sol1[sol1['1_code_effect'] == 4 ]
#-------------------------------------------------------------
#Merge the SOL and the id code file
sol1= pd.merge(left=sol1[
    ['code_id','2_trait_no', '6_no_obs','8_BLUP', 'SE']
    ], right=id_code[['id','code_id']], on='code_id', how='left')
#Split the large file into smaller ones by lactations
cr1_sol = sol1[sol1['2_trait_no'] == 1 ]
icf_sol1 = sol1[sol1['2_trait_no'] == 2 ]
icf_sol2 = sol1[sol1['2_trait_no'] == 3 ]
icf_sol3 = sol1[sol1['2_trait_no'] == 4 ]

#Rename the BLUP solutions for each trait by the trait and lactation
cr1_sol[['BLUP_CR0_ICF', 'SE_CR_ICF']] = cr1_sol[['8_BLUP','SE']]
icf_sol1[['BLUP_ICF1_I', 'SE_ICF1']] = icf_sol1[['8_BLUP','SE']]
icf_sol2[['BLUP_ICF2_I', 'SE_ICF2']] = icf_sol2[['8_BLUP','SE']]
icf_sol3[['BLUP_ICF3_I', 'SE_ICF3']] = icf_sol3[['8_BLUP','SE']]

#Merge the files so there will be a file with one line per cow with all solutions
saman_inbreed= pd.merge(left=cr1_sol[
    ['id', 'BLUP_CR0_ICF', 'SE_CR_ICF']
    ], right=icf_sol1[['id','BLUP_ICF1_I', 'SE_ICF1']], on='id')
saman_inbreed= pd.merge(left=saman_inbreed, right=icf_sol2[['id','BLUP_ICF2_I', 'SE_ICF2']
    ], on='id')
saman_inbreed= pd.merge(left=saman_inbreed, right=icf_sol3[['id','BLUP_ICF3_I', 'SE_ICF3']
    ], on='id')


#-------------------------------------------------------------
#CR0_IFL_inbreed4
#-------------------------------------------------------------
widths = [1,3,3,4,12,12,12,20,20]
sol2 = pd.read_fwf(
    "//home/thordis/DMU4tests/Inbreeding/CR_IFL/SOL",
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
        'SE'   #S
    ]
    )
#Only keep genetic effectss
sol2 = sol2[sol2['1_code_effect'] == 4 ]
#-------------------------------------------------------------
#Merge the SOL and the id code file
sol2= pd.merge(left=sol2[
    ['code_id','2_trait_no', '6_no_obs','8_BLUP', 'SE']
    ], right=id_code[['id','code_id']], on='code_id', how='left')
#Split the large file into smaller ones by lactations
cr2_sol = sol2[sol2['2_trait_no'] == 1 ]
ifl_sol1 = sol2[sol2['2_trait_no'] == 2 ]
ifl_sol2 = sol2[sol2['2_trait_no'] == 3 ]
ifl_sol3 = sol2[sol2['2_trait_no'] == 4 ]
#Rename the BLUP solutions for each trait by the trait and lactation
cr2_sol[['BLUP_CR0_IFL', 'SE_CR_IFL']] = cr2_sol[['8_BLUP','SE']]
ifl_sol1[['BLUP_IFL1_I', 'SE_IFL1']] = ifl_sol1[['8_BLUP','SE']]
ifl_sol2[['BLUP_IFL2_I', 'SE_IFL2']] = ifl_sol2[['8_BLUP','SE']]
ifl_sol3[['BLUP_IFL3_I', 'SE_IFL3']] = ifl_sol3[['8_BLUP','SE']]
#Merge the files so there will be a file with one line per cow with all solutions
saman_inbreed= pd.merge(left=saman_inbreed, right=cr2_sol[['id','BLUP_CR0_IFL','SE_CR_IFL']
    ], on='id')
saman_inbreed= pd.merge(left=saman_inbreed, right=ifl_sol1[['id','BLUP_IFL1_I','SE_IFL1']
    ], on='id')
saman_inbreed= pd.merge(left=saman_inbreed, right=ifl_sol2[['id','BLUP_IFL2_I','SE_IFL2']
    ], on='id')
saman_inbreed= pd.merge(left=saman_inbreed, right=ifl_sol3[['id','BLUP_IFL3_I','SE_IFL3']
    ], on='id')






#Creating a file with new results
# saman_inbreed.to_csv("../data/samandmu4_inbreed.txt", index=False, header=False, sep=' ')

print(saman_inbreed.iloc[600000:600015])
print(saman_inbreed.info())
