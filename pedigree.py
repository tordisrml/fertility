#Thordis Thorarinsdottir 2021!
#This is a program that takes the pedigree file from Huppa, switches out
#the Huppa ID numbers and creates a code number to be used in DMU runs

#Input file "Pgree_?????????.txt" from Huppa
#Output files: "id_code.txt" and "dmu_ped_code.ped"

import pandas as pd
import numpy as np

#Read the pedigree file that coms from huppa
widths = [15,15,15,61]
ped = pd.read_fwf(
    "../data/Pgree_24jun2021.txt",
    widths=widths,
    header=None,
    names=['id','dam','sire','unused']
    )

#Only 3 columns are needed
del ped['unused']

ped = ped.sort_values(by=['id'])

#For some reason there are some duplecate records, they need to be deleted
ped = ped.drop_duplicates(subset=['id'])

#The creation of code id's to be used in DMU
ped['code_id'] = ped.index
ped['code_id'] = ped['code_id'] + 1

#Creation of a file with animal numbers and matching code numbers
code = ped[['id','code_id']].copy() #dataset with codenumbers for everyone
code.to_csv('id_code.txt', index=False, header=False, sep=' ')

#renaming the columns for a pedigree file with code id's
code.columns = ['sire', 'code_sire']
#sire code id's merged with a pedigree file
ped = pd.merge(left=ped, right=code, on='sire', how='left').fillna(0, downcast='infer')

#renaming the columns for a pedigree file with code id's
code.columns = ['dam', 'code_dam']
#dam code id's merged with a pedigree file
ped = pd.merge(left=ped, right=code, on='dam', how='left').fillna(0, downcast='infer')

#The pedigree file for DMU needs 4 columns, column 4 will be the code id's again
ped['code_id2'] = ped['code_id']

#Creation of a pedigree file with code id's to be used in DMU
dmu_ped_code = ped[['code_id','code_sire','code_dam','code_id2']]
dmu_ped_code.to_csv("../data/dmu_ped_code.ped", index=False, header=False, sep=' ')

# #Creation of a pedigree file with with normal id's
# dmu_ped = ped[['id','dam','sire']]
# dmu_ped.to_csv("../data/dmu_ped.ped", index=False, header=False, sep=' ')


print(ped.iloc[50000:50015])
print(ped.info())
