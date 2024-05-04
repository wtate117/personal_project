import sys

import cryptocompare as cp
import pandas as pd
from common_imports import datetime, timedelta, date

# cryptocompare API call
cp.cryptocompare._set_api_key_parameter('d61bdef9c6306d25f3b34e76faf3e2719764a992ae55b655d88ab7e0c446fd8a')
api_key = 'd61bdef9c6306d25f3b34e76faf3e2719764a992ae55b655d88ab7e0c446fd8a'


def pull_crypto_data_daily(currency='BTC', timeframe=30):
    # timeframe *= 365 # Convert a yearly parameter into days
    price_by_day = cp.get_historical_price_day(currency, currency='USD', limit=timeframe)
    # Convert to pandas dataframe
    price_df = pd.DataFrame(price_by_day)
    clean_crypto_data(price_df)

    return clean_crypto_data(price_df)

def pull_crypto_data_hourly(currency='BTC', timeframe=30):
    # Timeframe should be provided in days, convert here to translate into hours
    # timeframe *= 24
    price_by_hour = cp.get_historical_price_hour(currency, currency='USD', limit=timeframe)
    # Convert to pandas dataframe
    price_df = pd.DataFrame(price_by_hour)

    return clean_crypto_data(price_df)


def clean_crypto_data(df):
    # Convert the time column into a legible format
    df['time'] = pd.to_datetime(df['time'], unit='s')
    # Calculate percent change based on the closing price
    df['Pct_Change'] = df['close'].pct_change() * 100
    # Fill in the first NaN value (and others) with 0
    df['Pct_Change'] = df['Pct_Change'].fillna(0)
    return df


import requests
import pandas as pd
from datetime import datetime


def fetch_daily_bitcoin_data(api_key, from_date, to_date, currency):
    # Convert dates to UNIX timestamps
    from_date = datetime_to_string(from_date)
    to_date = datetime_to_string(to_date)
    from_timestamp = int(datetime.strptime(from_date, '%Y-%m-%d').timestamp())
    to_timestamp = int(datetime.strptime(to_date, '%Y-%m-%d').timestamp())


    url = f"https://min-api.cryptocompare.com/data/v2/histohour"
    parameters = {
        'fsym': currency,
        'tsym': 'USD',
        'limit': 1992,  # Adjust based on the number of days in your range
        'toTs': to_timestamp,
        'api_key': api_key
    }

    response = requests.get(url, params=parameters)
    data = response.json()

    # Check if the request was successful
    if data['Response'] == 'Success':
        # Convert the data to a pandas DataFrame
        df = pd.DataFrame(data['Data']['Data'])
        # Convert timestamps to readable dates
        df['time'] = pd.to_datetime(df['time'], unit='s')
        return df
    else:
        print("Error fetching data - we will use a back up dataset with Bitcoin over a 10,000 hours period.")

        return None

# Write a function that creates date ranges until a start date is within bounds

# Write a function to find the difference in hours between two days



def find_day_before(start_date, x_hours):
    """
    Finds the day and time that is x hours before a given start date.

    Parameters:
    - start_date (datetime or str): The start date as a datetime object or a string in format "YYYY-MM-DD HH:MM".
    - x_hours (int): The number of hours before the start date.

    Returns:
    - datetime: The datetime object representing the day and time x hours before the start date.
    """
    try:
        # Assume start_date is already a datetime object and try to use it directly
        result_date = start_date - timedelta(hours=x_hours)
    except TypeError:
        # If start_date is not a datetime object, parse it from the string
        start_date_parsed = datetime.strptime(start_date, "%Y-%m-%d")
        result_date = start_date_parsed - timedelta(hours=x_hours)

    return result_date

def datetime_to_string(date_obj, format_str="%Y-%m-%d"):
    """
    Converts a datetime object into a string with the specified format.

    Parameters:
    - date_obj (datetime): The datetime object to convert.
    - format_str (str): The format string for the output date and time. Default is "%Y-%m-%d %H:%M".

    Returns:
    - str: The formatted date and time as a string.
    """
    return date_obj.strftime(format_str)


# Example usage (commented out to prevent execution in the PCI)
# This would print the datetime for 24 hours before 2024-04-05 15:00, i.e., 2024-04-04 15:00

# Write a function that creates a list of days that backs into the starting date
def data_fetch_dates(start_date, end_date):
    day_list = [end_date]
    increment_day = end_date
    while increment_day > start_date:
        print(increment_day)
        increment_day -= timedelta(hours=1992)
        if(increment_day < start_date):
            increment_day = start_date
        day_list.insert(0, increment_day)
    return day_list



def full_data_pull_process(start_date, end_date, currency):
    # create the list of days for the API calls
    days_list = data_fetch_dates(start_date, end_date)
    print(days_list)

    for day in days_list:
        print(f'day: {datetime_to_string(day)}')

    df = pd.DataFrame()
    # loop over the days to get the hourly data
    for i in range(0,len(days_list) - 1):
        print(i, i+1)
        print(days_list[i], days_list[i+1])

        df2 = fetch_daily_bitcoin_data(api_key, days_list[i], days_list[i+1], currency)
        df = pd.concat([df, df2], ignore_index=True)

    if df.empty == True:
        back_up_df = pd.read_csv('big_pull.csv')
        df = back_up_df.drop(back_up_df.index[0])  # drop the first row

    print(df)
    return df



# full_data_pull_process(find_day_before(date.today(), 4000),date.today(), 'BTC')


"""
df.to_csv('revised_data_pull.csv')


data_to_save = pull_crypto_data_daily('BTC', 30)
data_to_save.to_csv('my_data_pull.csv')
# data_to_save.to_csv('BTC_1_year_by_hour.csv')

'''"""