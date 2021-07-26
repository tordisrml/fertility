
#wrong observations printed into a datafile
wrong2_df.to_csv("wrong2.txt", index=False, sep="\t")


np.savetxt('wrong2.txt', wrong2_df, fmt='%+15s %+8s %+4s %+7s %+8s %+8s %+8s %+8s %+8s %+8s %+1s %+2s ')
np.savetxt('wrong1.txt', wrong1_df, fmt='%+15s %+7s %+8s %+8s %+8s %+8s %+8s %+8s %+1s ')

# item = df["ins_lact"].value_counts()
# print(item)

#wrong = df.loc[df["calv4"] == 2015090]
#print(wrong)

#ÞEGAR EG ER KOMIN MEÐ DAGASKJALIÐ!
df.describe()


#Number of calvings in data counted
df["no_calv"] = df[["calv1","calv2","calv3","calv4"]].notna().sum(axis = 1)
#FINNUR EKKI VILLUR EF VANTAR BURÐ INN Á MILLI!

#from tabulate import tabulate
def to_fwf(df, fname):
    content = tabulate(df.values.tolist(), list(df.columns), tablefmt="plain")
    open(fname, "w").write(content)




#Year - month lact 1 ins
cows_df['IYM1'] = (pd.DatetimeIndex(cows_df['first_1']).year.astype(str) +
   pd.DatetimeIndex(cows_df['first_1']).month.astype(str)
   )

# #Year - month lact 2 ins
# cows_df['IYM2'] = (pd.DatetimeIndex(cows_df['first_2']).year.astype(str) +
#    pd.DatetimeIndex(cows_df['first_2']).month.astype(str)
#    )
#Year - month lact 2 ins
# cows_df['IYM2'] = ((cows_df['first_2']).dt.year.astype(str).str.strip(".0")
#     + (cows_df['first_2']).dt.month.astype(str).str.strip(".0")
#     ).where(df["first_2"].notnull())
# #Year - month lact 2 ins
# cows_df['IYM2'] = (cows_df['first_2']).dt.month.astype(str)

#Year - month lact 3 ins
# cows_df['IYM3'] = ((pd.DatetimeIndex(cows_df['first_3']).year).astype(int)*100 +
#    (pd.DatetimeIndex(cows_df['first_3']).month).astype(int)
#    )



#virkaði ekki
# cows_df['IYM0'] = (cows_df['first_h'].dt.year.astype(str).str.strip('.0')
#              + '0'
#              + cows_df['first_h'].dt.month.astype(str).str.strip('.0')
#             ).where(cows_df['first_h'].notnull())


#PASSAR EKKI ÞEGAR VANTAR ANNAÐ HVORT!!!!!
#Creating herd - year fixed effects
#Herd - birth year
# cows_df['H_BY'] = (cows_df['herd'].astype(str) +
#    pd.DatetimeIndex(cows_df['birth']).year.astype(str)
#    )
# #Herd - calving year 1
# cows_df['H_C1Y'] = (cows_df['herd'].astype(str) +
#    pd.DatetimeIndex(cows_df['calv1']).year.astype(str)
#    )
# #Herd - calving year 2
# cows_df['H_C2Y'] = (cows_df['herd'].astype(str) +
#    pd.DatetimeIndex(cows_df['calv2']).year.astype(str)
#    )
# #Herd - calving year 3
# cows_df['H_C3Y'] = (
#
#     cows_df['herd'].astype(str) +
#
#     pd.DatetimeIndex(cows_df['calv3']).year.astype(str)
#
#     )


#virkar ekki
cows_df[['H_BY','H_C3Y','H_C2Y','H_C3Y']] =((cows_df[
    ['herd','herd','herd','herd']
    ].apply(
    lambda s: s * 10000
    ))
    +
    (cows_df[
    ['birth','calv1','calv2','calv3']
    ].apply(
    lambda x: x.dt.strftime('%Y').replace('NaT', '0').astype(int)
    ))
)


wrongins_df = df[
    (df['ins_lact'] != 0.0) & (df['ins_lact'] != 7.0) & (df['ins_lact'] != 1.0)
    & (df['ins_lact'] != 2.0) & (df['ins_lact'] != 3.0)
    ]
#wrong observations printed into a datafile
wrongins_df.to_csv('wrongins.csv', index=False)


wrongcalv_df = cows_df[
    (cows_df['no_calv'] != 0) & (cows_df['no_calv'] != 1) & (cows_df['no_calv'] != 2)
    & (cows_df['no_calv'] != 3) & (cows_df['no_calv'] != 4)
    ]
#wrongcalv_df.to_csv('wrongcalv.csv', index=False)

wrong_df = (
    cows_df.loc[
    (cows_df['wrong'].notnull().astype(int) == 1) |
    (cows_df['wrong1'].notnull().astype(int) == 1) |
    (cows_df['wrong2'].notnull().astype(int) == 1) |
    (cows_df['wrong3'].notnull().astype(int) == 1) ]
)


# cows_df['AGEi_h'] = (cows_df['AGEi_h'] / 30.5
#     ).apply(np.ceil).fillna(0).astype(int)
# cows_df['AGEc_1'] = (cows_df['AGEc_1'] / 30.5
#     ).apply(np.ceil).fillna(0).astype(int)
# cows_df['AGEc_2'] = (cows_df['AGEc_2'] / 30.5
#     ).apply(np.ceil).fillna(0).astype(int)
# cows_df['AGEc_3'] = (cows_df['AGEc_3'] / 30.5
#     ).apply(np.ceil).fillna(0).astype(int)



#---------------------------------------------------------------------------
#Datafile 1, info about inseminations. One line for every ins.
#---------------------------------------------------------------------------
widths_ins = [15,9,4,]
ins_df = pd.read_fwf(
    'saedingar.txt',
    widths=widths_ins,
    header=None,
    names=['id','ins','tech']
    )
#---------------------------------------------------------------------------
#Datafile 2, info about cows. One line for every cow.
#---------------------------------------------------------------------------
widths_cows = [15,8,9,9,9,9,9,9,]
cows_df = pd.read_fwf(
    'gripalisti.txt',
    widths=widths_cows,
    header=None,
    names=['id','herd','birth','death','calv1','calv2','calv3','calv4']
    )
