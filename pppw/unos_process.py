from datetime import date
import pandas as pd
import numpy as np
from tqdm import tqdm

from .data_processing import DfProcss
from .utils import str_to_date_E


class Unos_Prep():
    def __init__(self, df):
        self. unos_new = self.W_End_calc(df)

    # define correct removed date
    def W_End_calc(self, df):
        '''
        calculating and combining W_End col based on a proposed algorithm into unos dataset
        :param df: unos dataframe
        :return:
        '''
        df['W_End'] = None
        df = df.replace({np.nan: None})
        for i in tqdm(range(len(df))):
            if (df['death_dt'][i] != None):
                if str_to_date_E(df['rmvd_dt'][i]) > str_to_date_E(df['death_dt'][i]):
                    df.loc[i, 'W_End'] = df['death_dt'][i]
                else:
                    df.loc[i, 'W_End'] = df['rmvd_dt'][i]
            else:
                df.loc[i, 'W_End'] = df['rmvd_dt'][i]

            if df.loc[i, 'W_End'] == None:
                df.loc[i, 'W_End'] = date(2020,12,31).strftime('%m/%d/%Y')
            else:
                df.loc[i, 'W_End'] = str_to_date_E(df.loc[i, 'W_End']).strftime('%m/%d/%Y')
        return df

        # df.to_csv('C:/Users/iZabett/Downloads/unos_new.csv')