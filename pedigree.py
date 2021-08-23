#Thordis Thorarinsdottir 2021!
#This is a program that takes the pedigree file from Huppa, switches out
#the Huppa ID numbers and creates a code number to be used in DMU runs

#Input file "Pgree_?????????.txt" from Huppa
#Output files: "id_code.txt" and "dmu_ped_code.ped"
#New output, "dmu_ped_phantom.ped" where 0 parents are grouped into phantom groups

import pandas as pd
import numpy as np

#Read the pedigree file that coms from huppa
widths = [15,15,15,12,1,46]
ped = pd.read_fwf(
    "../data/Pgree_24jun2021.txt",
    widths=widths,
    header=None,
    names=['id','dam','sire','unused','sex','unused2']
    )


#Only 3 columns are needed
# del ped[['unused','unused2']]
ped = ped.drop(
    ['unused','unused2'], axis = 1)

ped = ped.sort_values(by=['id'])

#For some reason there are some duplecate records, they need to be deleted
ped = ped.drop_duplicates(subset=['id'])

#The creation of code id's to be used in DMU
ped['code_id'] = ped.index
ped['code_id'] = ped['code_id'] + 1

ped = ped.sort_values(by=['code_id'])

#Creation of a file with animal numbers and matching code numbers
code = ped[['id','code_id']].copy() #dataset with codenumbers for everyone
code.to_csv('../data/id_code.txt', index=False, header=False, sep=' ')

#Creation of a file with animal numbers and matching code numbers
code2 = ped[['id','code_id','sex']].copy() #dataset with codenumbers for everyone
code2.to_csv('../data/id_code2.txt', index=False, header=False, sep=' ')

print(code2.info())


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

ped = ped.sort_values(by=['code_id'])
#Creation of a pedigree file with code id's to be used in DMU
dmu_ped_code = ped[['code_id','code_sire','code_dam','code_id2']]
dmu_ped_code.to_csv("../data/dmu_ped_code.ped", index=False, header=False, sep=' ')


ped = ped.sort_values(by=['id'])
#Creation of a pedigree file with with normal id's
dmu_ped = ped[['id','dam','sire']]
dmu_ped.to_csv("../data/dmu_ped.ped", index=False, header=False, sep=' ')

# #--------------------------------------------------------------------
#
# #Create a pedigree file with phantom grouping for no parents
# phantom_ped = ped[['id','code_id','code_sire','code_dam','code_id2']].copy()
#
# #Make birth year from id number an integer
# phantom_ped['BY'] = (phantom_ped.id.astype(str).str[:4]).astype(int)
#
# #All parents from animals older than 1970 go into same group
# #--------------------------------------------------------------------
# #Phantom sires
# phantom_ped.loc[
# (phantom_ped['code_sire'] == 0) & (phantom_ped['BY']  <= 1970)
# ,'code_sire'] = -1
# phantom_ped.loc[
# (phantom_ped['code_sire'] == 0) & (phantom_ped['BY']  == 1971),'code_sire'] = -2
# phantom_ped.loc[
# (phantom_ped['code_sire'] == 0) & (phantom_ped['BY']  == 1972),'code_sire'] = -2
# phantom_ped.loc[
# (phantom_ped['code_sire'] == 0) & (phantom_ped['BY']  == 1973),'code_sire'] = -3
# phantom_ped.loc[
# (phantom_ped['code_sire'] == 0) & (phantom_ped['BY']  == 1974),'code_sire'] = -3
# phantom_ped.loc[
# (phantom_ped['code_sire'] == 0) & (phantom_ped['BY']  == 1975),'code_sire'] = -4
# phantom_ped.loc[
# (phantom_ped['code_sire'] == 0) & (phantom_ped['BY']  == 1976),'code_sire'] = -4
# phantom_ped.loc[
# (phantom_ped['code_sire'] == 0) & (phantom_ped['BY']  == 1977),'code_sire'] = -5
# phantom_ped.loc[
# (phantom_ped['code_sire'] == 0) & (phantom_ped['BY']  == 1978),'code_sire'] = -5
# phantom_ped.loc[
# (phantom_ped['code_sire'] == 0) & (phantom_ped['BY']  == 1979),'code_sire'] = -6
# phantom_ped.loc[
# (phantom_ped['code_sire'] == 0) & (phantom_ped['BY']  == 1980),'code_sire'] = -6
# phantom_ped.loc[
# (phantom_ped['code_sire'] == 0) & (phantom_ped['BY']  == 1981),'code_sire'] = -7
# phantom_ped.loc[
# (phantom_ped['code_sire'] == 0) & (phantom_ped['BY']  == 1982),'code_sire'] = -7
# phantom_ped.loc[
# (phantom_ped['code_sire'] == 0) & (phantom_ped['BY']  == 1983),'code_sire'] = -8
# phantom_ped.loc[
# (phantom_ped['code_sire'] == 0) & (phantom_ped['BY']  == 1984),'code_sire'] = -8
# phantom_ped.loc[
# (phantom_ped['code_sire'] == 0) & (phantom_ped['BY']  == 1985),'code_sire'] = -9
# phantom_ped.loc[
# (phantom_ped['code_sire'] == 0) & (phantom_ped['BY']  == 1986),'code_sire'] = -9
# phantom_ped.loc[
# (phantom_ped['code_sire'] == 0) & (phantom_ped['BY']  == 1987),'code_sire'] = -10
# phantom_ped.loc[
# (phantom_ped['code_sire'] == 0) & (phantom_ped['BY']  == 1988),'code_sire'] = -10
# phantom_ped.loc[
# (phantom_ped['code_sire'] == 0) & (phantom_ped['BY']  == 1989),'code_sire'] = -11
# phantom_ped.loc[
# (phantom_ped['code_sire'] == 0) & (phantom_ped['BY']  == 1990),'code_sire'] = -11
# phantom_ped.loc[
# (phantom_ped['code_sire'] == 0) & (phantom_ped['BY']  == 1991),'code_sire'] = -12
# phantom_ped.loc[
# (phantom_ped['code_sire'] == 0) & (phantom_ped['BY']  == 1992),'code_sire'] = -12
# phantom_ped.loc[
# (phantom_ped['code_sire'] == 0) & (phantom_ped['BY']  == 1993),'code_sire'] = -13
# phantom_ped.loc[
# (phantom_ped['code_sire'] == 0) & (phantom_ped['BY']  == 1994),'code_sire'] = -13
# phantom_ped.loc[
# (phantom_ped['code_sire'] == 0) & (phantom_ped['BY']  == 1995),'code_sire'] = -14
# phantom_ped.loc[
# (phantom_ped['code_sire'] == 0) & (phantom_ped['BY']  == 1996),'code_sire'] = -14
# phantom_ped.loc[
# (phantom_ped['code_sire'] == 0) & (phantom_ped['BY']  == 1997),'code_sire'] = -15
# phantom_ped.loc[
# (phantom_ped['code_sire'] == 0) & (phantom_ped['BY']  == 1998),'code_sire'] = -15
# phantom_ped.loc[
# (phantom_ped['code_sire'] == 0) & (phantom_ped['BY']  == 1999),'code_sire'] = -16
# phantom_ped.loc[
# (phantom_ped['code_sire'] == 0) & (phantom_ped['BY']  == 2000),'code_sire'] = -16
# phantom_ped.loc[
# (phantom_ped['code_sire'] == 0) & (phantom_ped['BY']  == 2001),'code_sire'] = -17
# phantom_ped.loc[
# (phantom_ped['code_sire'] == 0) & (phantom_ped['BY']  == 2002),'code_sire'] = -17
# phantom_ped.loc[
# (phantom_ped['code_sire'] == 0) & (phantom_ped['BY']  >= 2003)
# ,'code_sire'] = -18
#
# #--------------------------------------------------------------------
# #Phantom dams
# #--------------------------------------------------------------------
# phantom_ped.loc[
# (phantom_ped['code_dam'] == 0) & (phantom_ped['BY']  <= 1970),'code_dam'] = -19
# phantom_ped.loc[
# (phantom_ped['code_dam'] == 0) & (phantom_ped['BY']  == 1971),'code_dam'] = -20
# phantom_ped.loc[
# (phantom_ped['code_dam'] == 0) & (phantom_ped['BY']  == 1972),'code_dam'] = -20
# phantom_ped.loc[
# (phantom_ped['code_dam'] == 0) & (phantom_ped['BY']  == 1973),'code_dam'] = -21
# phantom_ped.loc[
# (phantom_ped['code_dam'] == 0) & (phantom_ped['BY']  == 1974),'code_dam'] = -21
# phantom_ped.loc[
# (phantom_ped['code_dam'] == 0) & (phantom_ped['BY']  == 1975),'code_dam'] = -22
# phantom_ped.loc[
# (phantom_ped['code_dam'] == 0) & (phantom_ped['BY']  == 1976),'code_dam'] = -22
# phantom_ped.loc[
# (phantom_ped['code_dam'] == 0) & (phantom_ped['BY']  == 1977),'code_dam'] = -23
# phantom_ped.loc[
# (phantom_ped['code_dam'] == 0) & (phantom_ped['BY']  == 1978),'code_dam'] = -23
# phantom_ped.loc[
# (phantom_ped['code_dam'] == 0) & (phantom_ped['BY']  == 1979),'code_dam'] = -24
# phantom_ped.loc[
# (phantom_ped['code_dam'] == 0) & (phantom_ped['BY']  == 1980),'code_dam'] = -24
# phantom_ped.loc[
# (phantom_ped['code_dam'] == 0) & (phantom_ped['BY']  == 1981),'code_dam'] = -25
# phantom_ped.loc[
# (phantom_ped['code_dam'] == 0) & (phantom_ped['BY']  == 1982),'code_dam'] = -25
# phantom_ped.loc[
# (phantom_ped['code_dam'] == 0) & (phantom_ped['BY']  == 1983),'code_dam'] = -26
# phantom_ped.loc[
# (phantom_ped['code_dam'] == 0) & (phantom_ped['BY']  == 1984),'code_dam'] = -26
# phantom_ped.loc[
# (phantom_ped['code_dam'] == 0) & (phantom_ped['BY']  == 1985),'code_dam'] = -27
# phantom_ped.loc[
# (phantom_ped['code_dam'] == 0) & (phantom_ped['BY']  == 1986),'code_dam'] = -27
# phantom_ped.loc[
# (phantom_ped['code_dam'] == 0) & (phantom_ped['BY']  == 1987),'code_dam'] = -28
# phantom_ped.loc[
# (phantom_ped['code_dam'] == 0) & (phantom_ped['BY']  == 1988),'code_dam'] = -28
# phantom_ped.loc[
# (phantom_ped['code_dam'] == 0) & (phantom_ped['BY']  == 1989),'code_dam'] = -29
# phantom_ped.loc[
# (phantom_ped['code_dam'] == 0) & (phantom_ped['BY']  == 1990),'code_dam'] = -29
# phantom_ped.loc[
# (phantom_ped['code_dam'] == 0) & (phantom_ped['BY']  == 1991),'code_dam'] = -30
# phantom_ped.loc[
# (phantom_ped['code_dam'] == 0) & (phantom_ped['BY']  == 1992),'code_dam'] = -30
# phantom_ped.loc[
# (phantom_ped['code_dam'] == 0) & (phantom_ped['BY']  == 1993),'code_dam'] = -31
# phantom_ped.loc[
# (phantom_ped['code_dam'] == 0) & (phantom_ped['BY']  == 1994),'code_dam'] = -31
# phantom_ped.loc[
# (phantom_ped['code_dam'] == 0) & (phantom_ped['BY']  == 1995),'code_dam'] = -32
# phantom_ped.loc[
# (phantom_ped['code_dam'] == 0) & (phantom_ped['BY']  == 1996),'code_dam'] = -32
# phantom_ped.loc[
# (phantom_ped['code_dam'] == 0) & (phantom_ped['BY']  == 1997),'code_dam'] = -33
# phantom_ped.loc[
# (phantom_ped['code_dam'] == 0) & (phantom_ped['BY']  == 1998),'code_dam'] = -33
# phantom_ped.loc[
# (phantom_ped['code_dam'] == 0) & (phantom_ped['BY']  == 1999),'code_dam'] = -34
# phantom_ped.loc[
# (phantom_ped['code_dam'] == 0) & (phantom_ped['BY']  == 2000),'code_dam'] = -34
# phantom_ped.loc[
# (phantom_ped['code_dam'] == 0) & (phantom_ped['BY']  == 2001),'code_dam'] = -35
# phantom_ped.loc[
# (phantom_ped['code_dam'] == 0) & (phantom_ped['BY']  == 2002),'code_dam'] = -35
# phantom_ped.loc[
# (phantom_ped['code_dam'] == 0) & (phantom_ped['BY']  >= 2003)
# ,'code_dam'] = -36
#
# dmu_ped_phantom = phantom_ped[['code_id','code_sire','code_dam','code_id2']]
# dmu_ped_phantom.to_csv("../data/dmu_ped_phantom.ped", index=False, header=False, sep=' ')
#
#
# print(phantom_ped.iloc[100:115])
# print(phantom_ped.iloc[50000:50015])
# print(phantom_ped.info())
