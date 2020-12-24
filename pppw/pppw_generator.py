from .data_processing import DfProcss
from .unos_process import Unos_Prep
import pandas as pd
import numpy as np



class PPPW_Generator(DfProcss):
    def __init__(self, **kwargs):
        self.set_params(**kwargs)
        self.pre_processing()

    def pre_processing(self):
        print('unos_prep ...')
        self.unos_prep()
        # self.unos = pd.read_csv(self.data_path + 'unos_new.csv')
        
        print('unos_merge ...')
        self.data = self.unos_merge(self.iter_methond, file = 'dfs_unos_merge_prep_')
        # self.data = pd.read_csv(self.data_path + 'dfs_unos_merge_prep_all.csv')

    def processings(self, data):
        self.data = data
        print('age calculations ...')
        self.data = self.df_age_calc(file = 'dfs_age_prep_')
        # self.data = pd.read_csv(self.data_path + 'dfs_age_prep_all.csv')


        self.data['Waitlist_Flag'] = None
        self.data['Aux_Wl_Flag'] = None
        self.data = self.data.replace({np.nan: None})
        self.unos = self.unos.replace({np.nan: None})
        print('waitlist calculations ...')
        self.data  = self.waitlist_calc(file = 'dfs_prep_')
        # self.data = pd.read_csv(self.data_path + 'dfs_prep_all.csv')



    def unos_prep(self):
        '''
        preprocessing of unos data before aggregating to dataset
        :return:
        '''
        self.unos = Unos_Prep(df=self.unos).unos_new
        self.unos.to_csv(self.data_path + 'unos_new.csv')
        return self.unos
