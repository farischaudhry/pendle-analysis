import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import math

sns.set_style('whitegrid')

# delta = dPT/dS
def calculate_delta(df):
    if 'pt_open' in df.columns and 'underlying_open' in df.columns:
        df['pt_change'] = df['pt_open'].diff().fillna(0)
        df['underlying_change'] = df['underlying_open'].diff().fillna(0)
        df['delta'] = df['pt_change'] / df['underlying_change'].replace(0, method='ffill')  # Replace zero to avoid division by zero
    return df

# gamma = d^2PT/dS^2
def calculate_gamma(df):
    if 'delta' in df.columns and 'underlying_open' in df.columns:
        df['delta_change'] = df['delta'].diff().fillna(0)
        df['gamma'] = df['delta_change'] / df['underlying_change'].replace(0, method='ffill')  # Replace zero to avoid division by zero
    return df

# vega = dPT/dvolatility
def calculate_vega(df):
    if 'pt_open' in df.columns:
        df['volatility'] = df['pt_open'].pct_change().rolling(window=30).std()
        df['30d_pt_volatility'] = df['pt_open'].pct_change().rolling(window=30).std()
        df['volatility_change'] = df['volatility'].diff().fillna(0)
        df['vega'] = df['pt_change'] / df['volatility_change'].replace(0, method='ffill')  # Replace zero to avoid division by zero
    return df

def calculate_implied_apy(prices_df, expiry_date):
    # Convert PT and YT prices from USD to ETH using the underlying price
    prices_df['pt_open_eth'] = prices_df['pt_open'] / prices_df['underlying_open']
    prices_df['yt_open_eth'] = prices_df['yt_open'] / prices_df['underlying_open']
    prices_df['pt_high_eth'] = prices_df['pt_high'] / prices_df['underlying_high']
    prices_df['yt_high_eth'] = prices_df['yt_high'] / prices_df['underlying_high']
    prices_df['pt_low_eth'] = prices_df['pt_low'] / prices_df['underlying_low']
    prices_df['yt_low_eth'] = prices_df['yt_low'] / prices_df['underlying_low']
    prices_df['pt_close_eth'] = prices_df['pt_close'] / prices_df['underlying_open']
    prices_df['yt_close_eth'] = prices_df['yt_close'] / prices_df['underlying_open']

    prices_df['implied_apy'] = (1 + prices_df['yt_open'] / prices_df['pt_open']) ** (365 / prices_df['days_to_expiry']) - 1
    prices_df['daily_implied_rate'] = (1 + 0.03) ** (1/365) - 1
    prices_df['expected_yield'] = prices_df['daily_implied_rate'] * prices_df['underlying_open']
    prices_df['yearly_expected_yield'] = prices_df['implied_apy'] * prices_df['underlying_open']
    return prices_df

# Don't mind all the volatility calculations, most of them are legacy and not used.
# Main importance is the 30d_ewm_volatility variables
def calculate_volatility(df):
    df['daily_pt_change'] = df['pt_open_eth'].pct_change()
    df['daily_yt_change'] = df['yt_open_eth'].pct_change()
    df['pt_change'] = df['pt_open_eth'].pct_change()
    df['yt_change'] = df['yt_open_eth'].pct_change()
    df['underlying_change'] = df['yt_open_eth'].pct_change()
    df['daily_returns'] = df['underlying_open'].pct_change()
    df['volatility'] = df['daily_returns'].rolling(window=30).std() * np.sqrt(252)  # Annualized Volatility
    df['30d_volatility'] = df['daily_pt_change'].rolling(window=30).std() * np.sqrt(365)  # Annualized Volatility
    df['7d_volatility'] = df['daily_pt_change'].rolling(window=7).std() * np.sqrt(365)  # Annualized Volatility
    df['5d_volatility'] = df['daily_pt_change'].rolling(window=5).std() * np.sqrt(365)  # Annualized Volatility
    df['30d_ewm_volatility'] = df['daily_pt_change'].ewm(span=30).std() * np.sqrt(365)  # Annualized Exponentially Weighted Volatility
    df['30d_ewm_pt_volatility'] = df['daily_pt_change'].ewm(span=30).std() * np.sqrt(365)  # Annualized Exponentially Weighted Volatility
    df['30d_ewm_yt_volatility'] = df['daily_yt_change'].ewm(span=30).std() * np.sqrt(365)  # Annualized Exponentially Weighted Volatility
    df['30d_ewm_underlying_volatility'] = df['daily_underlying_change'].ewm(span=30).std() * np.sqrt(365)  # Annualized Exponentially Weighted Volatility

    return df

def calculate_fixed_yield(prices_df, expiry_date):
    # Calculate the fixed yield
    prices_df['fixed_yield'] = (prices_df['underlying_open'] / prices_df['pt_open']) ** (365 / prices_df['days_to_expiry']) - 1
    # prices_df['fixed_yield'] = -365 / prices_df['days_to_expiry'] * np.log(prices_df['pt_open'] / prices_df['underlying_open'])
    return prices_df

def calculate_theoretical_pt_yt(prices_df, start_date, expiry_date):
    # Calculate the fixed yield rate r based on the initial PT price
    days_to_expiry_initial = (expiry_date - start_date).days

    # Theoretical PT value calculation using the calculated r
    # prices_df['theoretical_pt_eth'] = 1 / (1 + prices_df['fixed_yield']) ** (prices_df['days_to_expiry'] / 365)
    prices_df['theoretical_pt_eth'] = np.exp(-prices_df['fixed_yield'] * (prices_df['days_to_expiry'] / 365))
    prices_df['theoretical_yt_eth'] = 1 - prices_df['theoretical_pt_eth']
    return prices_df

def iterate_yield_price_convergence(prices_df, iterations=10):
    def calculate_fixed_yield_iterative(prices_df):
        # This function recalculates the fixed yield based on current PT and underlying prices
        prices_df['iterative_fixed_yield'] = (1 / prices_df['theoretical_pt_eth']) ** (365 / prices_df['days_to_expiry']) - 1
        return prices_df['iterative_fixed_yield']

    def calculate_theoretical_prices(prices_df):
        prices_df['theoretical_pt_eth'] = 1 / (1 + prices_df['iterative_fixed_yield']) ** (prices_df['days_to_expiry'] / 365)
        prices_df['theoretical_yt_eth'] = 1 - prices_df['theoretical_pt_eth']
        return prices_df

    prices_df['theoretical_pt_eth'] = prices_df['pt_open_eth']
    prices_df['theoretical_yt_eth'] = prices_df['yt_open_eth']

    for i in range(iterations):
        # Calculate fixed yield
        yield_rate = calculate_fixed_yield_iterative(prices_df)

        # Update theoretical prices based on the current yield
        prices_df = calculate_theoretical_prices(prices_df)

    return prices_df


def calculate_normal_changes(df):
    df['theta'] = df['fixed_yield'] * df['pt_open_eth']
    df['residual_change'] = df['pt_open_eth'] - df['theta']
    df['residual_change_pct'] = df['residual_change'].pct_change()
    return df

def prepare_token_data(underlying_path, yt_path, pt_path, start_date, expiry_date, tvl_path=None):
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
    prices_df = pt_df[['open', 'volume', 'high', 'low', 'close']].join(yt_df[['open', 'volume', 'high', 'low', 'close']], lsuffix='_pt', rsuffix='_yt', how='inner').join(underlying_df[['open', 'volume', 'high', 'low']], rsuffix='_underlying', how='inner')

    # Rename the columns
    prices_df.columns = ['pt_open', 'pt_volume', 'pt_high', 'pt_low', 'pt_close', 'yt_open', 'yt_volume', 'yt_high', 'yt_low', 'yt_close', 'underlying_open', 'underlying_volume', 'underlying_high', 'underlying_low']

    # Filter the data by start and expiry dates
    prices_df = prices_df[(prices_df.index >= start_date) & (prices_df.index <= expiry_date)]

    prices_df['days_to_expiry'] = (expiry_date - prices_df.index).days
    prices_df = calculate_implied_apy(prices_df, expiry_date)
    prices_df = calculate_fixed_yield(prices_df, expiry_date)
    prices_df['implied_apy_minus_fixed_yield'] = prices_df['implied_apy'] - prices_df['fixed_yield']
    prices_df['pct_maturity_left'] = prices_df['days_to_expiry'] / (expiry_date - start_date).days
    prices_df = calculate_theoretical_pt_yt(prices_df, start_date, expiry_date)
    # prices_df = iterate_yield_price_convergence(prices_df, iterations=1)
    prices_df['daily_underlying_change'] = prices_df['underlying_open'].pct_change()
    prices_df = calculate_volatility(prices_df)

    prices_df = calculate_delta(prices_df)
    prices_df = calculate_gamma(prices_df)
    prices_df = calculate_vega(prices_df)
    prices_df = calculate_normal_changes(prices_df)

    if tvl_path:
        tvl_df = pd.read_csv(tvl_path)
        # Remove unnamed columns
        tvl_df = tvl_df.loc[:, ~tvl_df.columns.str.contains('^Unnamed')]
        tvl_df.columns = tvl_df.columns.str.lower()
        tvl_df['date'] = pd.to_datetime(tvl_df['date'], format='%d/%m/%Y')
        tvl_df.set_index('date', inplace=True)
        prices_df = prices_df.join(tvl_df, how='left')
        prices_df['tvl_change'] = prices_df['tvl'].pct_change()

    return prices_df[(prices_df.index <= expiry_date - pd.Timedelta(days=1))] # Exclude the last day of the data since yt will be 0 for that day

def prepare_price_data(path):
    df = pd.read_csv(path)
    df.columns = df.columns.str.lower()
    try:
        df['date'] = pd.to_datetime(df['date'], format='%m/%d/%Y')
    except ValueError:
        df['date'] = pd.to_datetime(df['date'], format='%d/%m/%Y')
    df.set_index('date', inplace=True)
    return df
