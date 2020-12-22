import pandas as pd
import numpy as np

from pppw import PPPW_Generator, DfProcss, init_params, Unos_Prep

data_source = 'vat'

print('load '+ data_source + ' ...')
sfr_all = pd.read_csv('C:/Project_Data/PPPW/SFR_PWmergeAll.csv')



all_bd = pd.read_csv('C:/Users/iZabett/Downloads/PPPW/All_Pid_BD.csv')

unos_org = pd.read_csv('C:/Users/iZabett/Downloads/PPPW/unos_waitg_lst_202009221849.csv', delimiter='|')

sfr_all = sfr_all.where(pd.notnull(sfr_all), None)
sfr_all['provfs'] = sfr_all['PROVFS']
del sfr_all['PROVFS']

cols = ['patientId', 'provfs', 'year', 'month', 'unos_waitg_lst_id', 'lstg_dt', 'rmvd_dt',
        'unos_waitg_lst_orgn_cd', 'birth_date', 'death_dt', 'W_End']
sfr_all = sfr_all.assign(unos_waitg_lst_id=None,
                         lstg_dt=None,
                         rmvd_dt=None,
                         unos_waitg_lst_orgn_cd=None,
                         birth_date=None,
                         death_dt=None,
                         W_End=None)
sfr_all = sfr_all[cols]
sfr_all = sfr_all[:2000]
# preprocessing ...
pppw_gen = PPPW_Generator(**init_params(data=sfr_all, unos=unos_org, bdate=all_bd))

#############################

# pw_all =  pd.read_csv('C:/Users/iZabett/Downloads/ktv_prep_all.csv')
pw_all = pppw_gen.data



# Reset index
pw_all = pw_all.reset_index()
cols = ['patientId', 'provfs', 'year', 'month', 'birth_date',  'W_End']
pw_all = pw_all[cols]


pppw_gen.processings(pw_all)
# write final data
pppw_gen.data.to_csv(pppw_gen.data_path + data_source + '_final.csv')

