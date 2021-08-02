#Program to check which animals have their own observations in SOL files
#Also checks bulls with daughters with their own obs

#Reading in id codes to replace in SOL files
code_df = pd.read_csv(
    "../data/id_code.txt",
    header=None,
    sep = ' ',
    names=['id','code_id']
    )

#Reading in DMU observation file
df = pd.read_csv(
    "../data/dmu_fertility.txt",
    header=None,
    sep = ' ',
    names=['code_id','H_BY','HC1','HC2','HC3','IYM0','IYM1','IYM2',
        'IYM3','AGEi_h','AGEc_1','AGEc_2','AGEc_3','tech_h',
        'CRh','ICF1','ICF2','ICF3','IFL1','IFL2','IFL3']
    )
