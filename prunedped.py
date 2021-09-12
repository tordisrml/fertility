#This program takes a pruned pedigree file and created a ped file for dmu

import pandas as pd
import numpy as np


code = pd.read_csv(
    "/home/thordis/data/id_code.txt",
    header=None,
    sep = ' ',
    names=['id','code_id']
    )

widths = [15,16,16,]
ped = pd.read_fwf(
    '/home/thordis/data/5gen.ped',
    widths=widths,
    header=None,
    names=['id','sire','dam']
    )

phantom_ped = pd.merge(left=ped, right=code, on='id', how='left')

#renaming the columns for a pedigree file with code id's
code.columns = ['sire', 'code_sire']
#sire code id's merged with a pedigree file
phantom_ped = pd.merge(left=phantom_ped, right=code, on='sire', how='left').fillna(0, downcast='infer')

#renaming the columns for a pedigree file with code id's
code.columns = ['dam', 'code_dam']
#dam code id's merged with a pedigree file
phantom_ped = pd.merge(left=phantom_ped, right=code, on='dam', how='left').fillna(0, downcast='infer')

#The pedigree file for DMU needs 4 columns, column 4 will be the code id's again
phantom_ped['code_id2'] = phantom_ped['code_id']

phantom_ped = phantom_ped.sort_values(by=['code_id'])

phantom_ped['BY'] = (phantom_ped.id.astype(str).str[:4]).astype(int)

#All parents from animals older than 1970 go into same group
#--------------------------------------------------------------------
#Phantom sires
phantom_ped.loc[
(phantom_ped['code_sire'] == 0) & (phantom_ped['BY']  <= 1970)
,'code_sire'] = -1
phantom_ped.loc[
(phantom_ped['code_sire'] == 0) & (phantom_ped['BY']  == 1971),'code_sire'] = -2
phantom_ped.loc[
(phantom_ped['code_sire'] == 0) & (phantom_ped['BY']  == 1972),'code_sire'] = -2
phantom_ped.loc[
(phantom_ped['code_sire'] == 0) & (phantom_ped['BY']  == 1973),'code_sire'] = -2
phantom_ped.loc[
(phantom_ped['code_sire'] == 0) & (phantom_ped['BY']  == 1974),'code_sire'] = -2
phantom_ped.loc[
(phantom_ped['code_sire'] == 0) & (phantom_ped['BY']  == 1975),'code_sire'] = -3
phantom_ped.loc[
(phantom_ped['code_sire'] == 0) & (phantom_ped['BY']  == 1976),'code_sire'] = -3
phantom_ped.loc[
(phantom_ped['code_sire'] == 0) & (phantom_ped['BY']  == 1977),'code_sire'] = -3
phantom_ped.loc[
(phantom_ped['code_sire'] == 0) & (phantom_ped['BY']  == 1978),'code_sire'] = -3
phantom_ped.loc[
(phantom_ped['code_sire'] == 0) & (phantom_ped['BY']  == 1979),'code_sire'] = -4
phantom_ped.loc[
(phantom_ped['code_sire'] == 0) & (phantom_ped['BY']  == 1980),'code_sire'] = -4
phantom_ped.loc[
(phantom_ped['code_sire'] == 0) & (phantom_ped['BY']  == 1981),'code_sire'] = -4
phantom_ped.loc[
(phantom_ped['code_sire'] == 0) & (phantom_ped['BY']  == 1982),'code_sire'] = -4
phantom_ped.loc[
(phantom_ped['code_sire'] == 0) & (phantom_ped['BY']  == 1983),'code_sire'] = -5
phantom_ped.loc[
(phantom_ped['code_sire'] == 0) & (phantom_ped['BY']  == 1984),'code_sire'] = -5
phantom_ped.loc[
(phantom_ped['code_sire'] == 0) & (phantom_ped['BY']  == 1985),'code_sire'] = -5
phantom_ped.loc[
(phantom_ped['code_sire'] == 0) & (phantom_ped['BY']  == 1986),'code_sire'] = -5
phantom_ped.loc[
(phantom_ped['code_sire'] == 0) & (phantom_ped['BY']  == 1987),'code_sire'] = -6
phantom_ped.loc[
(phantom_ped['code_sire'] == 0) & (phantom_ped['BY']  == 1988),'code_sire'] = -6
phantom_ped.loc[
(phantom_ped['code_sire'] == 0) & (phantom_ped['BY']  == 1989),'code_sire'] = -6
phantom_ped.loc[
(phantom_ped['code_sire'] == 0) & (phantom_ped['BY']  == 1990),'code_sire'] = -6
phantom_ped.loc[
(phantom_ped['code_sire'] == 0) & (phantom_ped['BY']  == 1991),'code_sire'] = -7
phantom_ped.loc[
(phantom_ped['code_sire'] == 0) & (phantom_ped['BY']  == 1992),'code_sire'] = -7
phantom_ped.loc[
(phantom_ped['code_sire'] == 0) & (phantom_ped['BY']  == 1993),'code_sire'] = -7
phantom_ped.loc[
(phantom_ped['code_sire'] == 0) & (phantom_ped['BY']  == 1994),'code_sire'] = -7
phantom_ped.loc[
(phantom_ped['code_sire'] == 0) & (phantom_ped['BY']  == 1995),'code_sire'] = -8
phantom_ped.loc[
(phantom_ped['code_sire'] == 0) & (phantom_ped['BY']  == 1996),'code_sire'] = -8
phantom_ped.loc[
(phantom_ped['code_sire'] == 0) & (phantom_ped['BY']  == 1997),'code_sire'] = -8
phantom_ped.loc[
(phantom_ped['code_sire'] == 0) & (phantom_ped['BY']  == 1998),'code_sire'] = -8
phantom_ped.loc[
(phantom_ped['code_sire'] == 0) & (phantom_ped['BY']  == 1999),'code_sire'] = -9
phantom_ped.loc[
(phantom_ped['code_sire'] == 0) & (phantom_ped['BY']  == 2000),'code_sire'] = -9
phantom_ped.loc[
(phantom_ped['code_sire'] == 0) & (phantom_ped['BY']  == 2001),'code_sire'] = -9
phantom_ped.loc[
(phantom_ped['code_sire'] == 0) & (phantom_ped['BY']  == 2002),'code_sire'] = -9
phantom_ped.loc[
(phantom_ped['code_sire'] == 0) & (phantom_ped['BY']  == 2003),'code_sire'] = -10
phantom_ped.loc[
(phantom_ped['code_sire'] == 0) & (phantom_ped['BY']  == 2004),'code_sire'] = -10
phantom_ped.loc[
(phantom_ped['code_sire'] == 0) & (phantom_ped['BY']  == 2005),'code_sire'] = -10
phantom_ped.loc[
(phantom_ped['code_sire'] == 0) & (phantom_ped['BY']  == 2006),'code_sire'] = -10
phantom_ped.loc[
(phantom_ped['code_sire'] == 0) & (phantom_ped['BY']  == 2007),'code_sire'] = -11
phantom_ped.loc[
(phantom_ped['code_sire'] == 0) & (phantom_ped['BY']  == 2008),'code_sire'] = -11
phantom_ped.loc[
(phantom_ped['code_sire'] == 0) & (phantom_ped['BY']  == 2009),'code_sire'] = -11
phantom_ped.loc[
(phantom_ped['code_sire'] == 0) & (phantom_ped['BY']  == 2010),'code_sire'] = -11
phantom_ped.loc[
(phantom_ped['code_sire'] == 0) & (phantom_ped['BY']  == 2011),'code_sire'] = -12
phantom_ped.loc[
(phantom_ped['code_sire'] == 0) & (phantom_ped['BY']  == 2012),'code_sire'] = -12
phantom_ped.loc[
(phantom_ped['code_sire'] == 0) & (phantom_ped['BY']  == 2013),'code_sire'] = -12
phantom_ped.loc[
(phantom_ped['code_sire'] == 0) & (phantom_ped['BY']  == 2014),'code_sire'] = -12
phantom_ped.loc[
(phantom_ped['code_sire'] == 0) & (phantom_ped['BY']  == 2015),'code_sire'] = -13
phantom_ped.loc[
(phantom_ped['code_sire'] == 0) & (phantom_ped['BY']  == 2016),'code_sire'] = -13
phantom_ped.loc[
(phantom_ped['code_sire'] == 0) & (phantom_ped['BY']  == 2017),'code_sire'] = -13
phantom_ped.loc[
(phantom_ped['code_sire'] == 0) & (phantom_ped['BY']  == 2018),'code_sire'] = -13
phantom_ped.loc[

(phantom_ped['code_sire'] == 0) & (phantom_ped['BY']  >= 2019)
,'code_sire'] = -14

#--------------------------------------------------------------------
#Phantom dams
#--------------------------------------------------------------------
phantom_ped.loc[
(phantom_ped['code_dam'] == 0) & (phantom_ped['BY']  <= 1970),'code_dam'] = -15
phantom_ped.loc[
(phantom_ped['code_dam'] == 0) & (phantom_ped['BY']  == 1971),'code_dam'] = -16
phantom_ped.loc[
(phantom_ped['code_dam'] == 0) & (phantom_ped['BY']  == 1972),'code_dam'] = -16
phantom_ped.loc[
(phantom_ped['code_dam'] == 0) & (phantom_ped['BY']  == 1973),'code_dam'] = -16
phantom_ped.loc[
(phantom_ped['code_dam'] == 0) & (phantom_ped['BY']  == 1974),'code_dam'] = -16
phantom_ped.loc[
(phantom_ped['code_dam'] == 0) & (phantom_ped['BY']  == 1975),'code_dam'] = -17
phantom_ped.loc[
(phantom_ped['code_dam'] == 0) & (phantom_ped['BY']  == 1976),'code_dam'] = -17
phantom_ped.loc[
(phantom_ped['code_dam'] == 0) & (phantom_ped['BY']  == 1977),'code_dam'] = -17
phantom_ped.loc[
(phantom_ped['code_dam'] == 0) & (phantom_ped['BY']  == 1978),'code_dam'] = -17
phantom_ped.loc[
(phantom_ped['code_dam'] == 0) & (phantom_ped['BY']  == 1979),'code_dam'] = -18
phantom_ped.loc[
(phantom_ped['code_dam'] == 0) & (phantom_ped['BY']  == 1980),'code_dam'] = -18
phantom_ped.loc[
(phantom_ped['code_dam'] == 0) & (phantom_ped['BY']  == 1981),'code_dam'] = -18
phantom_ped.loc[
(phantom_ped['code_dam'] == 0) & (phantom_ped['BY']  == 1982),'code_dam'] = -18
phantom_ped.loc[
(phantom_ped['code_dam'] == 0) & (phantom_ped['BY']  == 1983),'code_dam'] = -19
phantom_ped.loc[
(phantom_ped['code_dam'] == 0) & (phantom_ped['BY']  == 1984),'code_dam'] = -19
phantom_ped.loc[
(phantom_ped['code_dam'] == 0) & (phantom_ped['BY']  == 1985),'code_dam'] = -19
phantom_ped.loc[
(phantom_ped['code_dam'] == 0) & (phantom_ped['BY']  == 1986),'code_dam'] = -19
phantom_ped.loc[
(phantom_ped['code_dam'] == 0) & (phantom_ped['BY']  == 1987),'code_dam'] = -20
phantom_ped.loc[
(phantom_ped['code_dam'] == 0) & (phantom_ped['BY']  == 1988),'code_dam'] = -20
phantom_ped.loc[
(phantom_ped['code_dam'] == 0) & (phantom_ped['BY']  == 1989),'code_dam'] = -20
phantom_ped.loc[
(phantom_ped['code_dam'] == 0) & (phantom_ped['BY']  == 1990),'code_dam'] = -20
phantom_ped.loc[
(phantom_ped['code_dam'] == 0) & (phantom_ped['BY']  == 1991),'code_dam'] = -21
phantom_ped.loc[
(phantom_ped['code_dam'] == 0) & (phantom_ped['BY']  == 1992),'code_dam'] = -21
phantom_ped.loc[
(phantom_ped['code_dam'] == 0) & (phantom_ped['BY']  == 1993),'code_dam'] = -21
phantom_ped.loc[
(phantom_ped['code_dam'] == 0) & (phantom_ped['BY']  == 1994),'code_dam'] = -21
phantom_ped.loc[
(phantom_ped['code_dam'] == 0) & (phantom_ped['BY']  == 1995),'code_dam'] = -22
phantom_ped.loc[
(phantom_ped['code_dam'] == 0) & (phantom_ped['BY']  == 1996),'code_dam'] = -22
phantom_ped.loc[
(phantom_ped['code_dam'] == 0) & (phantom_ped['BY']  == 1997),'code_dam'] = -22
phantom_ped.loc[
(phantom_ped['code_dam'] == 0) & (phantom_ped['BY']  == 1998),'code_dam'] = -22
phantom_ped.loc[
(phantom_ped['code_dam'] == 0) & (phantom_ped['BY']  == 1999),'code_dam'] = -23
phantom_ped.loc[
(phantom_ped['code_dam'] == 0) & (phantom_ped['BY']  == 2000),'code_dam'] = -23
phantom_ped.loc[
(phantom_ped['code_dam'] == 0) & (phantom_ped['BY']  == 2001),'code_dam'] = -23
phantom_ped.loc[
(phantom_ped['code_dam'] == 0) & (phantom_ped['BY']  == 2002),'code_dam'] = -23
phantom_ped.loc[
(phantom_ped['code_dam'] == 0) & (phantom_ped['BY']  == 2003),'code_dam'] = -24
phantom_ped.loc[
(phantom_ped['code_dam'] == 0) & (phantom_ped['BY']  == 2004),'code_dam'] = -24
phantom_ped.loc[
(phantom_ped['code_dam'] == 0) & (phantom_ped['BY']  == 2005),'code_dam'] = -24
phantom_ped.loc[
(phantom_ped['code_dam'] == 0) & (phantom_ped['BY']  == 2006),'code_dam'] = -24
phantom_ped.loc[
(phantom_ped['code_dam'] == 0) & (phantom_ped['BY']  == 2007),'code_dam'] = -25
phantom_ped.loc[
(phantom_ped['code_dam'] == 0) & (phantom_ped['BY']  == 2008),'code_dam'] = -25
phantom_ped.loc[
(phantom_ped['code_dam'] == 0) & (phantom_ped['BY']  == 2009),'code_dam'] = -25
phantom_ped.loc[
(phantom_ped['code_dam'] == 0) & (phantom_ped['BY']  == 2010),'code_dam'] = -25
phantom_ped.loc[
(phantom_ped['code_dam'] == 0) & (phantom_ped['BY']  == 2011),'code_dam'] = -26
phantom_ped.loc[
(phantom_ped['code_dam'] == 0) & (phantom_ped['BY']  == 2012),'code_dam'] = -26
phantom_ped.loc[
(phantom_ped['code_dam'] == 0) & (phantom_ped['BY']  == 2013),'code_dam'] = -26
phantom_ped.loc[
(phantom_ped['code_dam'] == 0) & (phantom_ped['BY']  == 2014),'code_dam'] = -26
phantom_ped.loc[
(phantom_ped['code_dam'] == 0) & (phantom_ped['BY']  == 2015),'code_dam'] = -27
phantom_ped.loc[
(phantom_ped['code_dam'] == 0) & (phantom_ped['BY']  == 2016),'code_dam'] = -27
phantom_ped.loc[
(phantom_ped['code_dam'] == 0) & (phantom_ped['BY']  == 2017),'code_dam'] = -27
phantom_ped.loc[
(phantom_ped['code_dam'] == 0) & (phantom_ped['BY']  == 2018),'code_dam'] = -27
phantom_ped.loc[
(phantom_ped['code_dam'] == 0) & (phantom_ped['BY']  >= 2019)
,'code_dam'] = -28

#Creation of a pedigree file with code id's to be used in DMU
dmu_ped_code = phantom_ped[['code_id','code_sire','code_dam','code_id2']]
dmu_ped_code.to_csv("../data/dmu_ped_code_5gen.ped", index=False, header=False, sep=' ')


print(dmu_ped_code.info())
