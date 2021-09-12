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
    "//home/thordis/DMU4tests/Phantom/CR_ICF/SOL",
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
sol1 = sol1[(sol1['1_code_effect'] == 4) & (sol1['code_id'] > 0)]
print(sol1.iloc[6000:6015])
print(sol1.info())
#-------------------------------------------------------------
#Merge the SOL and the id code file
sol1= pd.merge(left=sol1[
    ['code_id','2_trait_no', '6_no_obs','8_BLUP', 'SE']
    ], right=id_code[['id','code_id']], on='code_id', how='left')

#Split the large file into smaller ones by lactations
cr1_sol = sol1[sol1['2_trait_no'] == 4 ]
icf_sol1 = sol1[sol1['2_trait_no'] == 2 ]
icf_sol2 = sol1[sol1['2_trait_no'] == 3 ]
icf_sol3 = sol1[sol1['2_trait_no'] == 1 ]

#Rename the BLUP solutions for each trait by the trait and lactation
cr1_sol[['BLUP_CR0_ICF', 'SE_CR_ICF']] = cr1_sol[['8_BLUP','SE']]
icf_sol1[['BLUP_ICF1_I', 'SE_ICF1']] = icf_sol1[['8_BLUP','SE']]
icf_sol2[['BLUP_ICF2_I', 'SE_ICF2']] = icf_sol2[['8_BLUP','SE']]
icf_sol3[['BLUP_ICF3_I', 'SE_ICF3']] = icf_sol3[['8_BLUP','SE']]

#Merge the files so there will be a file with one line per cow with all solutions
saman= pd.merge(left=cr1_sol[
    ['id', 'BLUP_CR0_ICF', 'SE_CR_ICF']
    ], right=icf_sol1[['id','BLUP_ICF1_I', 'SE_ICF1']], on='id')
saman= pd.merge(left=saman, right=icf_sol2[['id','BLUP_ICF2_I', 'SE_ICF2']
    ], on='id')
saman= pd.merge(left=saman, right=icf_sol3[['id','BLUP_ICF3_I', 'SE_ICF3']
    ], on='id')


#-------------------------------------------------------------
#CR0_IFL_inbreed4
#-------------------------------------------------------------
widths = [1,3,3,4,12,12,12,20,20]
sol2 = pd.read_fwf(
    "//home/thordis/DMU4tests/Phantom/CR_IFL/SOL",
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
sol2 =  sol2[(sol2['1_code_effect'] == 4) & (sol2['code_id'] > 0)]
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
saman= pd.merge(left=saman, right=cr2_sol[['id','BLUP_CR0_IFL','SE_CR_IFL']
    ], on='id')
saman= pd.merge(left=saman, right=ifl_sol1[['id','BLUP_IFL1_I','SE_IFL1']
    ], on='id')
saman= pd.merge(left=saman, right=ifl_sol2[['id','BLUP_IFL2_I','SE_IFL2']
    ], on='id')
saman= pd.merge(left=saman, right=ifl_sol3[['id','BLUP_IFL3_I','SE_IFL3']
    ], on='id')


#Other results to compare with!
#Phantom group results from DMU5
phantom = pd.read_csv(
    "../data/saman_phantomnew3.txt",
    header=None,
    sep=' ',
    names=['id',
        'BLUP_CR0_P','BLUP_ICF1_P','BLUP_ICF2_P','BLUP_ICF3_P',
        'BLUP_IFL1_P','BLUP_IFL2_P','BLUP_IFL3_P']
    )
#CI results
CI = pd.read_csv(
    "../data/saman_ci_P.txt",
    header=None,
    sep=' ',
    names=['id',
        'CI12','CI23','CI34']
    )

#Reading in the old fertility breeding results
gamla = pd.read_csv(
    "../data/gamla_mat.txt",
    header=None,
    sep=' ',
    names=['id','fertility_1','fertility_2','fertility_3','frjosemi']
    )


#Inbreeding results and phantom group results together in a file
saman_allt = pd.merge(left=saman, right=phantom, on='id', how='outer')
#Inbreeding results and phantom group results together in a file
saman_allt = pd.merge(left=saman_allt, right=CI, on='id',how='outer')
#Old results merged
saman_allt = pd.merge(left=saman_allt, right=gamla, on='id', how='outer')
#Written into a datafile
saman_allt.to_csv("../data/saman_G_4_5.txt", index=False, header=False, sep=' ')

#Creating a file with new results
# saman.to_csv("../data/samandmu4.txt", index=False, header=False, sep=' ')

# print(saman.iloc[6000:6015])
# print(saman.info())
