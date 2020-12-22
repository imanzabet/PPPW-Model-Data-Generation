import calendar
from datetime import datetime, date

import numpy as np
import pandas as pd
from tqdm import tqdm

from pppw.utils import last_day_row, str_to_date_E, str_to_date, calculate_age
# from unos_process import add_W_End_period


class DfProcss():
    def __init__(self, **kwargs):

        self.set_params(**kwargs)



    def unos_merge(self, method, file):
        '''
        preperation phase on merging unos data w.r.t. to the constraints to generate auxiliary cols in dataset
        :param method:
        :return:
        '''
        for i in range(self.df_len // self.df_index + 1):
            lower_b = i * self.df_index
            higher_b = min(lower_b + self.df_index, self.df_len)
            dfs = self.data[lower_b:higher_b]
            print('')
            if method==2:
                for _, row1 in tqdm(self.bdate.iterrows()):
                    for index2, row2 in dfs[dfs['patientId'] == row1['patient_id']].iterrows():
                        dfs.loc[index2, row2['birth_date']] = row1['Date_of_Birth']

            if method==1:
                # iterrows() implementation
                for dfs_idx, dfs_row in tqdm(dfs.iterrows()):
                    pid = dfs_row['patientId']
                    for bc_idx, bd_row in self.bdate[self.bdate['patient_id'] == pid].iterrows():
                        dfs.at[dfs_idx, 'birth_date'] = bd_row['Date_of_Birth']
                    for unos_idx, unos_row in self.unos[self.unos['ptnt_id'] == pid].iterrows():
                        dfs.at[dfs_idx, 'unos_waitg_lst_id'] = unos_row['unos_waitg_lst_id']
                        dfs.at[dfs_idx, 'lstg_dt'] = unos_row['lstg_dt']
                        dfs.at[dfs_idx, 'rmvd_dt'] = unos_row['rmvd_dt']
                        dfs.at[dfs_idx, 'unos_waitg_lst_orgn_cd'] = unos_row['unos_waitg_lst_orgn_cd']
                        dfs.at[dfs_idx, 'birth_date'] = unos_row['birth_dt']
                        dfs.at[dfs_idx, 'death_dt'] = unos_row['death_dt']
                        dfs.at[dfs_idx, 'W_End'] = unos_row['W_End']

            if method==3:
                # itertuples() implementation
                for dfs_row in tqdm(dfs.itertuples()):
                    for bd_row in self.bdate[self.bdate['patient_id'] == dfs_row.patientId].itertuples():
                        dfs.loc[dfs_row.Index, dfs_row.birth_date] = bd_row.Date_of_Birth

            if method==4:
                # list implementation
                self.bdate_pid = list(self.bdate['patient_id'])
                self.bdate_dob = list(self.bdate['Date_of_Birth'])
                dfs_pid = list(dfs['patientId'])
                dfs_dob = [None] * len(dfs_pid)
                for pid in tqdm(self.bdate_pid):
                    try:
                        dfs_dob[dfs_pid.index(pid)] = self.bdate_dob.index(pid)
                        pass
                    except:
                        pass
            if method==5:
                # list numpy implementation
                self.bdate_pid = self.bdate['patient_id'].to_numpy()
                self.bdate_dob = self.bdate['Date_of_Birth'].to_numpy()
                dfs_pid = dfs['patientId'].to_numpy()
                dfs_dob = [None] * len(dfs_pid)
                for pid in tqdm(self.bdate_pid):
                    try:
                        dfs_dob[dfs_pid.index(pid)] = self.bdate_dob(int(np.where(self.bdate_pid == pid)[0]))
                        pass
                    except:
                        pass
            if method==6:
                # vectorization implementation 1 (Series)
                # if we have only 1-dimension of data
                def series_np_vectorization(df):
                    np_arr = df.to_numpy()
                    return pd.Series(np_arr, index=df.index)

            if method==7:
                # vectorization implementation 2 (just Numpy)
                def just_np_vectorization(df):
                    return df.to_numpy()

            if method==8:
                pid_dob_map = dict(zip(self.bdate.patient_id, self.bdate.Date_of_Birth))
                set_dfs_pid = set(dfs['patientId'])
                for pid in tqdm(self.bdate.patient_id):
                    # pid = self.bdate.patient_id[idx]
                    if pid in set_dfs_pid:
                        sub_df = dfs[dfs['patientId'] == pid]
                        for j in range(len(sub_df)):
                            dfs.loc[sub_df.index[j], 'birth_date'] = pid_dob_map[pid]

            # dfs.loc[dfs_pid.index(pid), dfs_row['birth_date']] = self.bdate_dob.index(pid)

            dfs.to_csv(self.data_path+ file + str(i) + '.csv')


        dfw = (pd.read_csv(f) for f in [self.data_path + file + str(i) + '.csv' for i in range(self.df_len // self.df_index + 1)])
        df_all = pd.concat(dfw)
        df_all.reset_index()
        df_all.to_csv(self.data_path + file + 'all.csv')
        return df_all

    def df_age_calc(self, data=None, method=None, file=None):
        '''
        calculating age of patients within a column
        :return:
        '''
        ex_count = 0
        for i in range(self.df_len // self.df_index + 1):
            lower_b = i * self.df_index
            higher_b = min(lower_b + self.df_index, self.df_len)
            dfs = self.data[lower_b:higher_b].copy()


            for dfs_idx, dfs_row in tqdm(dfs.iterrows()):  # i in tqdm(range(0, len(dfs))):
                if dfs_row['birth_date'] != None:
                    try:
                        dfs.loc[dfs_idx, 'Age'] = calculate_age(
                            datetime.strptime(dfs_row['birth_date'], '%m/%d/%Y').date()
                            , date(dfs_row['year'], dfs_row['month'],
                                   calendar.monthrange(dfs_row['year'], dfs_row['month'])[1]))
                    except:
                        try:
                            dfs.loc[dfs_idx, 'Age'] = calculate_age(
                                datetime.strptime(dfs_row['birth_date'], '%Y-%m-%d').date()
                                , date(dfs_row['year'], dfs_row['month'],
                                       calendar.monthrange(dfs_row['year'], dfs_row['month'])[1]))
                        except:
                            ex_count += 1

            dfs.to_csv(self.data_path+ file + str(i) + '.csv')


        print('Age Calculation is done with ' + str(ex_count) + ' exceptions')

        dfw = (pd.read_csv(f) for f in [self.data_path + file + str(i) + '.csv' for i in range(self.df_len // self.df_index + 1)])
        df_all = pd.concat(dfw)
        df_all.reset_index()
        cols = ['patientId', 'provfs', 'year', 'month', 'birth_date', 'W_End', 'Age']
        df_all = df_all[cols]
        df_all.to_csv(self.data_path + file +'all.csv')
        return df_all


    def df_writecsv(self, data, path=None, file=None):
        '''
        writing CSV file module from dataframe
        :param data: dataframe
        :param path:
        :param file:
        :return:
        '''
        if path==None:
            path = self.data_path
        if file==None:
            raise ValueError( "filename hasn't been specified for writing csv")
        data.to_csv(self.data_path + file +'all.csv')

    def df_readcsv(self, path=None, file=None)->pd.DataFrame:
        '''
        reading CSV file module to a dataframe
        :param path:
        :param file:
        :return:
        '''
        if path==None:
            path = self.data_path
        if file==None:
            raise ValueError( "filename hasn't been specified for reading csv")
        return pd.read_csv(path+file)


    def waitlist_calc(self, data=None, index=None, file=None):
        '''
        compute the watilist and add to a column in data
        :param :
        :return:
        '''

        for i in range(self.df_len // self.df_index + 1):
            lower_b = i * self.df_index
            higher_b = min(lower_b + self.df_index, self.df_len)
            dfs = self.data[lower_b:higher_b].copy()

            for dfs_idx, dfs_row in tqdm(dfs.iterrows()):  # i in tqdm(range(0, len(dfs))):

                sub_unos = self.unos[self.unos['ptnt_id'] == dfs['patientId'][dfs_idx]].reset_index()
                for j in range(len(sub_unos)):
                    dfs.loc[dfs_idx, 'W_End'] = sub_unos['W_End'][j]
                    if dfs.loc[dfs_idx, 'Waitlist_Flag'] != 1:
                        if last_day_row(dfs_row) >= str_to_date_E(sub_unos['lstg_dt'][j]) and \
                                last_day_row(dfs_row) <= str_to_date(sub_unos['W_End'][j]):
                            dfs.loc[dfs_idx, 'Waitlist_Flag'] = 1
                        else:
                            dfs.loc[dfs_idx, 'Waitlist_Flag'] = 0


            del dfs['birth_date']

            # Filter out all records withou age
            dfs = dfs[dfs['Age'] >= 0]

            # Copy original Unos Waitlist_Flags to Aux_Wl_Flag
            dfs['Aux_Wl_Flag'] = dfs['Waitlist_Flag'].copy()

            # Fill All other Waitlist Flag with Zero
            a = dfs['Waitlist_Flag'].to_numpy().copy()
            a[a == None] = 0
            dfs['Waitlist_Flag'] = a

            dfs = dfs.replace({np.nan: None})
            dfs.to_csv(self.data_path + file + str(i) + '.csv')

        dfw = (pd.read_csv(f) for f in [self.data_path + file + str(i) + '.csv' for i in range(self.df_len // self.df_index + 1)])
        df_all = pd.concat(dfw)
        df_all.reset_index()
        cols = ['patientId', 'provfs', 'year', 'month', 'W_End', 'Age', 'Waitlist_Flag', 'Aux_Wl_Flag']
        df_all = df_all[cols]
        df_all.to_csv(self.data_path + file +'all.csv')
        return df_all

    def set_params(self, **kwargs):

        """
         Take in of parameters.
         If a parameter is not provided, it takes its default value.

         :param data: Number of clusters to be produced. Should be greater than 2.
         :type data: `df`
         :param df_index: Clustering method to use
         :type df_index: `int`
         :param df_len: Number of dimensions to project on
         :type df_len: `int`

         """
        # Save specific parameters
        # super(DfProcss, self).set_params(**kwargs)

        try:
            self.data = pd.DataFrame(kwargs['data'])
        except:
            raise ValueError( "Data can't be convert to Pandas DataFrame")
        if self.data._typ != 'dataframe':
            raise ValueError("Wrong Data format. The format is: " + str(type(self.data)))
        self.df_len = len(self.data)
        if self.df_len <=0 :
            raise ValueError("Wrong data input: " + self.df_len)
        try:
            self.df_index = int(kwargs['index'])
        except:
            self.df_index = 50000
        if self.df_index <= 0 or self.df_index > self.df_len:
            raise ValueError("Wrong number of df_index ")
        try:
            self.iter_methond = int(kwargs['iter_method'])
        except:
            self.iter_methond=1
        self.data_path = kwargs['data_path']
        self.bdate = kwargs['bdate']
        self.unos = kwargs['unos']
        return True


