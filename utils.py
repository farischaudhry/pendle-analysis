import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import math

sns.set_style('whitegrid')

def calculate_implied_apy(prices_df, expiry_date):
    # Convert PT and YT prices from USD to ETH using the underlying price
    prices_df['pt_open_eth'] = prices_df['pt_open'] / prices_df['underlying_open']
    prices_df['yt_open_eth'] = prices_df['yt_open'] / prices_df['underlying_open']

    prices_df['implied_apy'] = (1 + prices_df['yt_open'] / prices_df['pt_open']) ** (365 / prices_df['days_to_expiry']) - 1
    return prices_df


def calculate_fixed_yield(prices_df, expiry_date):
    # Calculate the fixed yield
    prices_df['fixed_yield'] = (prices_df['underlying_open'] / prices_df['pt_open']) ** (365 / prices_df['days_to_expiry']) - 1
    # prices_df['fixed_yield'] = -365 / prices_df['days_to_expiry'] * np.log(prices_df['pt_open'] / prices_df['underlying_open'])
    return prices_df

def calculate_theoretical_pt_yt(prices_df, start_date, expiry_date):
    # Calculate the fixed yield rate r based on the initial PT price
    days_to_expiry_initial = (expiry_date - start_date).days

    # Theoretical PT value calculation using the calculated r
    prices_df['theoretical_pt_eth'] = np.exp(-((1 / prices_df['pt_open_eth']) ** (1 / days_to_expiry_initial) - 1) * prices_df['days_to_expiry'])
    prices_df['theoretical_yt_eth'] = 1 - prices_df['theoretical_pt_eth']
    return prices_df

def calculate_volatility(df):
    df['daily_returns'] = df['pt_open'].pct_change()
    df['volatility'] = df['daily_returns'].rolling(window=30).std() * np.sqrt(252)  # Annualized Volatility
    return df

# def iterate_yield_price_convergence(prices_df, iterations=1):
#     def calculate_fixed_yield_iterative(prices_df):
#         # This function recalculates the fixed yield based on current PT and underlying prices
#         prices_df['iterative_fixed_yield'] = (1 / prices_df['theoretical_pt_eth']) ** (365 / prices_df['days_to_expiry']) - 1
#         return prices_df['iterative_fixed_yield']

#     def calculate_theoretical_prices(prices_df):
#         prices_df['theoretical_pt_eth'] = np.exp(-prices_df['iterative_fixed_yield'] * prices_df['days_to_expiry'])
#         prices_df['theoretical_yt_eth'] = 1 - prices_df['theoretical_pt_eth']
#         return prices_df

#     prices_df['theoretical_pt_eth'] = prices_df['pt_open_eth']
#     prices_df['theoretical_yt_eth'] = prices_df['yt_open_eth']

#     for i in range(iterations):
#         # Calculate fixed yield
#         yield_rate = calculate_fixed_yield_iterative(prices_df)

#         # Update theoretical prices based on the current yield
#         prices_df = calculate_theoretical_prices(prices_df)

#     return prices_df

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
    prices_df['implied_apy_minus_fixed_yield'] = prices_df['implied_apy'] - prices_df['fixed_yield']
    prices_df['pct_maturity_left'] = prices_df['days_to_expiry'] / (expiry_date - start_date).days
    prices_df = calculate_theoretical_pt_yt(prices_df, start_date, expiry_date)
    # prices_df = iterate_yield_price_convergence(prices_df, iterations=10)
    prices_df = calculate_volatility(prices_df)

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
