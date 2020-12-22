import re
from datetime import datetime
from datetime import date
import calendar

# import or convert date
dt = datetime.strptime('1/1/2001', '%m/%d/%Y').strftime('%Y-%m-%d')

# US style
str_to_date = lambda x: datetime.strptime(x, '%m/%d/%Y').date()

# European style
str_to_date_E = lambda x: datetime.strptime(x, '%Y-%m-%d').date()


# Calculating last day of month for a row of dataframe
last_day_row = lambda df_row: date(df_row['year'], df_row['month'],
                               calendar.monthrange(df_row['year'],
                                                   df_row['month'])[1])

# Calculating last day of month for index and dataframe
last_day_df = lambda df, i: date(df['year'][i], df['month'][i],
                                 calendar.monthrange(df['year'][i],
                                                     df['month'][i])[1])




def calculate_age(birth_dt, given_dt):
    '''
    calculating age of patient based on his/her birth date for a given date
    :param birth_dt:
    :param given_dt:
    :return:
    '''
    return given_dt.year - birth_dt.year - ((given_dt.month, given_dt.day) < (birth_dt.month, birth_dt.day))


def calculate_age_today(born):
    """
    calculating age of patient based on his/her birth date
    :param born: date of birth
    :return:
    ;example:
        calculate_age(date(2000,9,24))
    """
    today = date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))



def date_conv(date: str, fmt=None)->datetime:
    """
    converting date format module to get different format of choice
    :param
        date: The input String date with different formats
        fmt: Define th output String Format of the conversion can be these forms:
                '%m/%d/%Y'
                '%Y-%m-%d'
                '%b %d %Y'
                ...
    :return:
    ;example:
        Input:
            date_conv('9/21/1989')
            date_conv('19640430')
            date_conv('Mar 12 1951')
            date_conv('2 aug 2015')
            date_conv('2020-12-31')
        Output:
            datetime.date(1989, 9, 21)
            datetime.date(1964, 4, 30)
            datetime.date(1951, 3, 12)
            datetime.date(2015, 8, 2)
            datetime.date(2020, 12, 31)
    """
    dateObj = None
    if re.match(r"^\d{1,2}/\d{1,2}/\d{4}", date):
        dateObj = datetime.strptime(date, '%m/%d/%Y')
    elif re.match(r"^\d{4}\-\d{1,2}\-\d{1,2}", date):
         dateObj = datetime.strptime(date, '%Y-%m-%d')
    elif re.match(r"^\d{8}$", date):
        dateObj = datetime.strptime(date, '%Y%m%d')
    elif re.match(r"^[a-z]{3} \d{1,2} \d{4}", date, re.IGNORECASE):
        dateObj = datetime.strptime(date, '%b %d %Y')
    elif re.match(r"^\d{1,2} [a-z]{3} \d{4}", date, re.IGNORECASE):
        dateObj = datetime.strptime(date, '%d %b %Y')
    else:
        return dateObj
    try:
        if fmt==None:
            return dateObj.date()
        else:
            return dateObj.strftime(fmt)
    except:
        print('ERROR: Cannot convert date ...')



