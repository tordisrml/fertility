#This is a program that takes DMU5 SOL file from calving interval
#test run and creates a file for BLUP results

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
    "/home/thordis/DMUtests/CI_inbreed/SOL",
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
CIsol1 = sol[sol['2_trait_no'] == 1 ]
CIsol2 = sol[sol['2_trait_no'] == 2 ]
CIsol3 = sol[sol['2_trait_no'] == 3 ]

#Rename the BLUP solutions for each trait by the trait and lactation
CIsol1['CI12'] = CIsol1['8_BLUP']
CIsol2['CI23'] = CIsol2['8_BLUP']
CIsol3['CI34'] = CIsol3['8_BLUP']

#Merge the files so there will be a file with one line per cow with all solutions
saman_inbreed= pd.merge(left=CIsol1[
    ['id', 'CI12']
    ], right=CIsol2[['id','CI23']], on='id')
saman_inbreed= pd.merge(left=saman_inbreed, right=CIsol3[['id','CI34']], on='id')


#Creating a file with new results
saman_inbreed.to_csv("../data/saman_ci.txt", index=False, header=False, sep=' ')



print(saman_inbreed.iloc[600000:600015])
print(saman_inbreed.info())
