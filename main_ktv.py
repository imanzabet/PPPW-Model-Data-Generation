import pandas as pd
import numpy as np

from pppw import PPPW_Generator, init_params

data_source = 'ktv'


print('load '+ data_source + ' ...')
ktv = pd.read_csv('C:/Users/iZabett/Downloads/part-00000-8e7df0ed-7e74-476d-8645-f244ca0db1e6-c000.csv')

print('Delete unnecessary columns:')
del ktv['AVF'];
del ktv['AVF_f'];
del ktv['bmilt185'];
del ktv['bmi185to249'];
del ktv['bmigt249'];
del ktv['inNH_prevYr'];
del ktv['ESRD_vintagele1'];
del ktv['ESRD_vintage1to5'];
del ktv['ESRD_vintage5to9'];
del ktv['ESRD_vintagegt9'];
del ktv['pre_NEPHCARE'];
del ktv['prim_diab'];
del ktv['noprim_diab'];
del ktv['CHF'];
del ktv['CAD'];
del ktv['CVA'];
del ktv['PVASC'];
del ktv['PULMON'];
del ktv['DRUG'];
del ktv['inc_noambtrn'];
del ktv['Anemia'];
del ktv['NonVAInf'];
del ktv['medcov_6m']

# ktv.to_csv('C:/Users/iZabett/Downloads/KtV_1.csv')


##########################333
# adding DOB from all_pid_bd.csv to ktv.csv
# ktv_all = pd.read_csv('C:/Users/iZabett/Downloads/PPPW/KtV_1.csv')
ktv_all = ktv
all_bd = pd.read_csv('C:/Users/iZabett/Downloads/PPPW/All_Pid_BD.csv')
# unos = pd.read_csv('C:/Users/iZabett/Downloads/PPPW/unos_new.csv')

unos_org = pd.read_csv('C:/Users/iZabett/Downloads/PPPW/unos_waitg_lst_202009221849.csv', delimiter='|')



# unos_new = pd.read_csv('C:/Users/iZabett/Downloads/PPPW/unos_new.csv')



# ?del ktv_all['Unnamed: 0']

ktv_all['unos_waitg_lst_id'] = None
ktv_all['lstg_dt'] = None
ktv_all['rmvd_dt'] = None
ktv_all['unos_waitg_lst_orgn_cd'] = None
ktv_all['birth_date'] = None
ktv_all['death_dt'] = None
ktv_all['W_End'] = None
cols = ['patientId', 'provfs', 'year', 'month', 'unos_waitg_lst_id', 'lstg_dt', 'rmvd_dt', 'unos_waitg_lst_orgn_cd'
    , 'Fistpatients11', 'age18to24', 'age25to59', 'age60to74', 'agege75', 'birth_date', 'death_dt', 'W_End']
ktv_all = ktv_all[cols]
# remove pid records of ktv which are not in unos
# ktv_all = ktv_all[ktv_all['patientId'].isin(list(unos['ptnt_id']))]
# ktv_all = ktv_all[:32500]


# preprocessing ...
pppw_gen = PPPW_Generator(**init_params(data=ktv_all, unos=unos_org, bdate=all_bd))

#############################

# pw_all =  pd.read_csv('C:/Users/iZabett/Downloads/ktv_prep_all.csv')
pw_all = pppw_gen.data


# Filter out Fistpatients11 Flag==0
pw_all = pw_all[pw_all['Fistpatients11'] == 1]
# Filter out agege75 Flag==1 (meaning age>75)
pw_all = pw_all[pw_all['agege75'] == 0]

# Reset index
pw_all = pw_all.reset_index()
cols = ['patientId', 'provfs', 'year', 'month', 'birth_date',  'W_End']
pw_all = pw_all[cols]


pppw_gen.processings(pw_all)
# write final data
pppw_gen.data.to_csv(pppw_gen.data_path + data_source + '_final.csv')



# for i in range(len(pw)):
# if calendar.monthrange(pw['year'][i], pw['month'][i])[1]

