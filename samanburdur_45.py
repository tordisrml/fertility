saman = pd.read_csv(
    "../data/saman_I_P_G_2001.txt",
    header=None,
    sep=' ',
    names=['id',
        'CR0_I','ICF1_I','ICF2_I','ICF3_I','IFL1_I','IFL2_I','IFL3_I',
        'CR0_P','ICF1_P','ICF2_P','ICF3_P','IFL1_P','IFL2_P','IFL3_P',
        'CI12_I','CI23_I','CI34_I',
        'fertility_1','fertility_2','fertility_3','frjosemi']
    )
