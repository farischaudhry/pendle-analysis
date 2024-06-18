import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_style('whitegrid')

def calculate_implied_apy(prices_df, expiry_date):
    # Calculate the remaining days to expiry
    # prices_df['days_to_expiry'] = (expiry_date - prices_df.index).days

    # # Convert PT and YT prices from USD to ETH using the underlying price
    # prices_df['pt_open_eth'] = prices_df['pt_open'] / prices_df['underlying_open']
    # prices_df['yt_open_eth'] = prices_df['yt_open'] / prices_df['underlying_open']

    # Calculate the implied APY using ETH prices
    # prices_df['implied_apy_eth'] = (1 + prices_df['yt_open_eth'] / prices_df['pt_open_eth']) ** (365 / prices_df['days_to_expiry']) - 1
    prices_df['implied_apy_usd'] = (1 + prices_df['yt_open'] / prices_df['pt_open']) ** (365 / prices_df['days_to_expiry']) - 1

    return prices_df


def calculate_fixed_yield(prices_df, expiry_date):
    # Calculate the fixed yield using ETH prices
    prices_df['fixed_yield'] = (prices_df['underlying_open'] / prices_df['pt_open']) ** (365 / prices_df['days_to_expiry']) - 1
    return prices_df

def prepare_token_data(underlying_path, yt_path, pt_path, start_date, expiry_date):
    # Load the data
    pt_df = pd.read_csv(pt_path)
    yt_df = pd.read_csv(yt_path)
    underlying_df = pd.read_csv(underlying_path)

    # Convert column names to lowercase
    pt_df.columns = pt_df.columns.str.lower()
    yt_df.columns = yt_df.columns.str.lower()
    underlying_df.columns = underlying_df.columns.str.lower()

    # Convert the timestamp to datetime
    pt_df['time'] = pd.to_datetime(pt_df['time'])
    yt_df['time'] = pd.to_datetime(yt_df['time'])
    underlying_df['date'] = pd.to_datetime(underlying_df['date'])

    pt_df.set_index('time', inplace=True)
    yt_df.set_index('time', inplace=True)
    underlying_df.set_index('date', inplace=True)

    # Inner join the dataframes on 'time'
    prices_df = pt_df[['open']].join(yt_df[['open']], lsuffix='_pt', rsuffix='_yt', how='inner').join(underlying_df[['open']], how='inner')

    # Rename the columns
    prices_df.columns = ['pt_open', 'yt_open', 'underlying_open']

    prices_df = prices_df[(prices_df.index >= start_date) & (prices_df.index <= expiry_date)]

    prices_df['days_to_expiry'] = (expiry_date - prices_df.index).days
    prices_df = calculate_implied_apy(prices_df, expiry_date)
    prices_df = calculate_fixed_yield(prices_df, expiry_date)
    prices_df['yield_diff'] = prices_df['implied_apy_usd'] - prices_df['fixed_yield']
    prices_df['pct_maturity_left'] = prices_df['days_to_expiry'] / (expiry_date - start_date).days

    # Filter the data by start and expiry dates
    return prices_df

def prepare_price_data(path):
    df = pd.read_csv(path)
    df.columns = df.columns.str.lower()
    try:
        df['date'] = pd.to_datetime(df['date'], format='%m/%d/%Y')
    except ValueError:
        df['date'] = pd.to_datetime(df['date'], format='%d/%m/%Y')
    df.set_index('date', inplace=True)
    return df
