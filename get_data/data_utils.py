"""
This module is for defining functions used in data handling processes
Yu Mu
Dec. 26th, 2017
"""
import pandas as pd
import numpy as np


def revise_single_stock_name(address, new_name):
    """
    revise single stock name with new names

    Returns
    -------
    renamed_data: DataFrame
    ticker_name: str
    """
    renamed_data = pd.read_csv(address, encoding='GBK').rename(index=str, columns=new_name)
    ticker_name = str(renamed_data['ticker code'].unique()[0])
    return renamed_data, ticker_name


def read_single_column(address, column_name):
    """
    read single column of one stock, change the column name to ticker name
    Parameters
    ----------
    address: file full address; str
    column_name: str
    Return
    ------
    price: DataFrame
    """
    one_stock_data = pd.read_csv(address, encoding='GBK')
    ticker_name = str(one_stock_data['ticker code'].unique()[0])
    price = one_stock_data[[column_name]].rename(index=one_stock_data['dates'],
                                                         columns={column_name: ticker_name})
    return price


def read_single_column_tushare(address, column_name):
    """
    read single column from one stock dataframe, change the column name to ticker name
    Parameters
    ----------
    address: file full address; str
    column_name: str

    Return
    ------
    adjusted close price: DataFrame
    """
    one_stock_data = pd.read_csv(address)
    # ticker_name = str(one_stock_data['code'].unique()[0])
    ticker_name = address[-10:-4]
    if len(ticker_name) < 6:
        import pdb; pdb.set_trace()  # breakpoint 4a02aff3 //
    price = one_stock_data[[column_name]].rename(index=one_stock_data['date'],
                                                 columns={column_name: ticker_name})
    return price


def find_first_day_of_month(current_date, list_dates):
    """
    given list of dates and current date to find first date of current month
    """
    current_month = current_date[0:7]
    days_of_month = [s for s in list_dates if current_month in s]
    return days_of_month[0]


def extract_universe(first_day, window_size, all_dvolumes, all_dates, threshold):
    """
    extract universe
    """
    # get sub data from windowsize
    current_index = all_dates.index(first_day)
    start_day = all_dates[current_index-window_size]
    sub_data = all_dvolumes.loc[start_day:first_day, :]
    # remove those stocks having too much nan values
    nan_values = sub_data.isnull()
    good_stocks = nan_values.sum(axis=0) < 10
    non_empty_universe = good_stocks[good_stocks].index.tolist()
    # fill empty point with zero
    non_empty_universe_data = sub_data.loc[:, non_empty_universe].fillna(0.0)
    # chose stock with large adv
    average_dvolumes = np.mean(non_empty_universe_data, axis=0)
    cut = np.percentile(average_dvolumes, threshold)
    universe = average_dvolumes[average_dvolumes>cut].index.tolist()
    return universe