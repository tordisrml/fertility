
#This a file where python code I've tried to use or used at one point in
#the programs but removed is stored.

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

# #Creating fixed effect Herd - Birth year / Calving years
# s = cows_df['herd'] * 100
# cows_df['H_BY'] = s + cows_df['birth'].dt.year
# cows_df['HC1'] = s + cows_df['calv1'].dt.year
# cows_df['HC2'] = s + cows_df['calv2'].dt.year
# cows_df['HC3'] = s + cows_df['calv3'].dt.year
# cows_df[['H_BY','HC1','HC2','HC3']] = cows_df[
#     ['H_BY','HC1','HC2','HC3']].fillna(0, downcast='infer')

    s = cows_df['herd'] * 100
    cows_df['H_BY'] = s + cows_df['birth'].dt.strftime('%y').replace('NaT', '0').astype(int)
    cows_df['HC1'] = s + cows_df['calv1'].dt.strftime('%y').replace('NaT', '0').astype(int)
    cows_df['HC2'] = s + cows_df['calv2'].dt.strftime('%y').replace('NaT', '0').astype(int)
    cows_df['HC3'] = s + cows_df['calv3'].dt.strftime('%y').replace('NaT', '0').astype(int)
    cows_df[['H_BY','HC1','HC2','HC3']] = cows_df[
        ['H_BY','HC1','HC2','HC3']].fillna(0, downcast='infer')


dmu_fertility[['birth','calv1','calv2','calv3']] = dmu_fertility[
    ['birth','calv1','calv2','calv3']
    ].apply(
    lambda x: pd.to_datetime(x, format='%Y-%m-%d'))




fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1, sharex=True)

ax1.plot(
    (saman.groupby('BY')['ICF_I'].mean()),
    label='ICF_I',
    color='mediumslateblue',
    linewidth=3)

ax1.plot(
    (saman.groupby('BY')['ICF_P'].mean()),
    label='ICF_P',
    color='blue',
    linestyle='--',
    linewidth=3)

ax2 = ax1.twinx()

ax2.plot(
    (saman.groupby('BY')['frjosemi'].mean()),
    label='frjosemi',
    color='red')

#Show legends of plotted values, names are in 'label' above
ax1.legend()

#Labels for x and y
ax2.set_xlabel('Birth Year')
ax1.set_ylabel('EBV')
#Title of plot
ax1.set_title('Estimated breeding values for ICF and IFL by Birth year')

#Style of plot
#plt.style.use('Solarize_Light2')
#Print to see avalable styles
# print(plt.style.available) mediumslateblue

# plt.plot((saman2001.groupby('BY')['ICF1_I'].mean()), label='ICF1_I', color='mediumslateblue')
# plt.plot((saman2001.groupby('BY')['ICF2_I'].mean()), label='ICF2_I', color='royalblue' )
# plt.plot((saman2001.groupby('BY')['ICF3_I'].mean()), label='ICF3_I', color='navy')
# plt.plot((saman2001.groupby('BY')['ICF1_P'].mean()), label='ICF1_P', color='cornflowerblue')
# plt.plot((saman2001.groupby('BY')['ICF2_P'].mean()), label='ICF2_P', color='mediumblue')
# # plt.plot((saman2001.groupby('BY')['ICF3_P'].mean()), label='ICF3_P', color='slateblue')
# plt.plot((saman2001.groupby('BY')['ICF_I'].mean()), label='ICF_I', color='mediumslateblue', linewidth=4)
# plt.plot((saman2001.groupby('BY')['ICF_P'].mean()), label='ICF_P', color='blue', linewidth=4)
#
# # plt.plot((saman2001.groupby('BY')['IFL1_I'].mean()), label='IFL1_I', color='green')
# # plt.plot((saman2001.groupby('BY')['IFL2_I'].mean()), label='IFL2_I', color='forestgreen')
# # plt.plot((saman2001.groupby('BY')['IFL3_I'].mean()), label='IFL3_I', color='mediumseagreen')
# # plt.plot((saman2001.groupby('BY')['IFL1_P'].mean()), label='IFL1_P', color='springgreen')
# # plt.plot((saman2001.groupby('BY')['IFL2_P'].mean()), label='IFL2_P', color='aquamarine')
# # plt.plot((saman2001.groupby('BY')['IFL3_P'].mean()), label='IFL3_P', color='seagreen')
# plt.plot((saman2001.groupby('BY')['IFL_I'].mean()), label='IFL_I', color='lime', linewidth=4)
# plt.plot((saman2001.groupby('BY')['IFL_P'].mean()), label='IFL_P', color='limegreen', linewidth=4)
#
# plt.plot((saman2001.groupby('BY')['CR0_I'].mean()), label='CR0_I', color='slategrey', linewidth=4)
# plt.plot((saman2001.groupby('BY')['CR0_P'].mean()), label='CR0_P', color='black', linewidth=4)
#
# plt.plot((saman2001.groupby('BY')['new_I'].mean()), label='new_I', color='orchid', linewidth=4)
# plt.plot((saman2001.groupby('BY')['new_P'].mean()), label='new_P', color='deeppink', linewidth=4)
# plt.plot((saman2001.groupby('BY')['CI_I'].mean()), label='CI_I', color='yellow', linewidth=4)
# plt.plot((saman2001.groupby('BY')['frjosemi'].mean()), label='frjosemi', color='red')


saman[[
    'BLUP_ICF1','BLUP_ICF2','BLUP_ICF3', 'BLUP_ICF',
    'BLUP_IFL1','BLUP_IFL2','BLUP_IFL3', 'BLUP_IFL',
    'fertility_1','fertility_2','fertility_3','frjosemi']] = saman[[
    'BLUP_ICF1','BLUP_ICF2','BLUP_ICF3', 'BLUP_ICF',
    'BLUP_IFL1','BLUP_IFL2','BLUP_IFL3', 'BLUP_IFL',
    'fertility_1','fertility_2','fertility_3','frjosemi']].astype(float).round().astype(int)

Print Summary statistics
print(saman[[
    'BLUP_ICF1','BLUP_ICF2','BLUP_ICF3',
    'BLUP_IFL1','BLUP_IFL2','BLUP_IFL3',
    'fertility_1','fertility_2','fertility_3','frjosemi']].describe())

# print(sires50.groupby("BY").describe())

describe = sires50.groupby("BY").describe().to_csv("my_description.csv")


# saman[[
#     'BLUP_ICF1','BLUP_ICF2','BLUP_ICF3', 'BLUP_ICF',
#     'BLUP_IFL1','BLUP_IFL2','BLUP_IFL3', 'BLUP_IFL',
#     'fertility_1','fertility_2','fertility_3','frjosemi']] = saman[[
#     'BLUP_ICF1','BLUP_ICF2','BLUP_ICF3', 'BLUP_ICF',
#     'BLUP_IFL1','BLUP_IFL2','BLUP_IFL3', 'BLUP_IFL',
#     'fertility_1','fertility_2','fertility_3','frjosemi']].astype(float).round().astype(int)

#Print Summary statistics
# print(saman[[
#     'BLUP_ICF1','BLUP_ICF2','BLUP_ICF3',
#     'BLUP_IFL1','BLUP_IFL2','BLUP_IFL3',
#     'fertility_1','fertility_2','fertility_3','frjosemi']].describe())    
