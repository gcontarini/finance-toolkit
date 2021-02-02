"""
Implements a series of financial performance 
indicators used in investments.
"""

import numpy as np
import pandas as pd

def CAGR(data, frequency='Y', only_business=True):
    """ 
    Calculate cummulative annual growth rate (CAGR) for a given series.
    Parameters
    ----------
    data: pd.Series/pd.DataFrame
        Series contaning close prices for an asset. Also possible to input a dataframe,
        must contain a close column.
    frequency: string
        D for daily prices
        W for weekly prices
        M for monthly prices
        Y for yearly prices
    only_business: bool
        When using daily data count only business days.
    Returns
    ----------
    float
        CAGR indicator
    """

    # Handles input data
    if isinstance(data, pd.DataFrame):
        # All possibles names for close column
        possible_cols = ['Close', 'close', 'Adj Close', 'adj close']
        # Select them
        cols = [col for col in data.columns if col in possible_cols]
        # Check if there's only one close column
        if len(cols) > 1:
            raise KeyError('Ambiguous number of possible close prices column.')
        elif len(cols) == 0:
            raise IndexError('No close column. Pass desired column as a pd.Series.')
        # Copy data as series
        series = data[cols[0]].copy()

    elif isinstance(data, pd.Series):
        series = data.copy()
    
    else:
        raise TypeError('Input data is not a pandas Series or DataFrame.')

    # Handles parameter input
    if not frequency in ('D', 'W', 'M', 'Y'): 
        raise ValueError('Invalid option for data frequency.')
    if not isinstance(only_business, bool):
        raise TypeError('Value for only_business must be a boolean.')

    # Map frequency strings to values
    if only_business:
        freq_dict = {'D': 252, 'W': 52, 'M': 12, 'Y': 1}
    else:
        freq_dict = {'D': 365, 'W': 52, 'M': 12, 'Y': 1}
    
    # Factor used to calculate CAGR
    n = (series.shape[0] - 1) / freq_dict[frequency]
    
    # Store temporary values
    tmp_df = pd.DataFrame()

    # Calculate indicator
    tmp_df['returns'] = series.pct_change()
    tmp_df['cum_returns'] = (1 + tmp_df['returns']).cumprod()
    
    CAGR = ((tmp_df['cum_returns'].iloc[-1]) ** (1 / n)) - 1

    return CAGR

def volatility(data, frequency='Y', only_business=True):
    """ 
    Calculate volatility (standard deviation annualized)
    for returns on a given asset.
    Parameters
    ----------
    data: pd.Series/pd.DataFrame
        Series contaning close prices for an asset. Also possible
        to input a dataframe, must contain a close column.
    frequency: string
        D for daily prices
        W for weekly prices
        M for monthly prices
        Y for yearly prices
    only_business: bool
        When using daily data count only business days.
    Returns
    ----------
    float
        volatility
    """
    
    # Handles input data
    if isinstance(data, pd.DataFrame):
        # All possibles names for close column
        possible_cols = ['Close', 'close', 'Adj Close', 'adj close']
        # Select them
        cols = [col for col in data.columns if col in possible_cols]
        # Check if there's only one close column
        if len(cols) > 1:
            raise KeyError('Ambiguous number of possible close prices column.')
        elif len(cols) == 0:
            raise IndexError('No close column. Pass desired column as a pd.Series.')
        # Copy data as series
        series = data[cols[0]].copy()

    elif isinstance(data, pd.Series):
        series = data.copy()
    
    else:
        raise TypeError('Input data is not a pandas Series or DataFrame.')

    # Handles parameter input
    if not frequency in ('D', 'W', 'M', 'Y'): 
        raise ValueError('Invalid option for data frequency.')
    if not isinstance(only_business, bool):
        raise TypeError('Value for only_business must be a boolean.')

    # Map frequency strings to values
    if only_business:
        freq_dict = {'D': 252, 'W': 52, 'M': 12, 'Y': 1}
    else:
        freq_dict = {'D': 365, 'W': 52, 'M': 12, 'Y': 1}

    # Annualization factor
    n_sqrt = np.sqrt(freq_dict[frequency])

    # Store temporary values
    tmp_df = pd.DataFrame()
    
    tmp_df['returns'] = series.pct_change()
    volatility = tmp_df['returns'].std() * n_sqrt
    
    return volatility

def sharpe(data, rf_rate, frequency='Y', only_business=True):
    """ 
    Calculate sharpe ratio.
    Parameters
    ----------
    data: pd.Series/pd.DataFrame
        Series contaning close prices for an asset. Also possible
        to input a dataframe, must contain a close column.
    rf_rate: float
        Risk free rate.
    frequency: string
        D for daily prices
        W for weekly prices
        M for monthly prices
        Y for yearly prices
    Returns
    ----------
    float
        sharpe ratio
    """
    
    # Handles input data
    if isinstance(data, pd.DataFrame):
        # All possibles names for close column
        possible_cols = ['Close', 'close', 'Adj Close', 'adj close']
        # Select them
        cols = [col for col in data.columns if col in possible_cols]
        # Check if there's only one close column
        if len(cols) > 1:
            raise KeyError('Ambiguous number of possible close prices column.')
        elif len(cols) == 0:
            raise IndexError('No close column. Pass desired column as a pd.Series.')
        # Copy data as series
        series = data[cols[0]].copy()

    elif isinstance(data, pd.Series):
        series = data.copy()
    
    else:
        raise TypeError('Input data is not a pandas Series or DataFrame.')

    # Handles parameter input
    if not frequency in ('D', 'W', 'M', 'Y'): 
        raise ValueError('Invalid option for data frequency.')
    if not isinstance(only_business, bool):
        raise TypeError('Value for only_business must be a boolean.')
    if not isinstance(rf_rate, float):
        raise TypeError('rf_rate parameter is not float type.')
    if rf_rate > 1 or rf_rate < 0:
        raise ValueError('rf_rate must positive and equal or less than 1.')

    cagr = CAGR(series, frequency, only_business)
    vol = volatility(series, frequency, only_business)

    # Handles division by zero
    if vol == 0:
        raise ZeroDivisionError('Volatility cannot be equal to zero.')

    sharpe_ratio = (cagr - rf_rate) / vol
    
    return sharpe_ratio

# Something is not right in this logic
# TODO: fix it
# def sortino(data, rf_rate, frequency='Y', only_business=True):
#     """ 
#     Calculate sortino ratio.
#     Parameters
#     ----------
#     data: pd.Series/pd.DataFrame
#         Series contaning close prices for an asset. Also possible
#         to input a dataframe, must contain a close column.
#     rf_rate: float
#         Risk free rate.
#     frequency: string
#         D for daily prices
#         W for weekly prices
#         M for monthly prices
#         Y for yearly prices
#     Returns
#     ----------
#     float
#         sortino ratio
#     """
    
#     # Handles input data
#     if isinstance(data, pd.DataFrame):
#         # All possibles names for close column
#         possible_cols = ['Close', 'close', 'Adj Close', 'adj close']
#         # Select them
#         cols = [col for col in data.columns if col in possible_cols]
#         # Check if there's only one close column
#         if len(cols) > 1:
#             raise KeyError('Ambiguous number of possible close prices column.')
#         elif len(cols) == 0:
#             raise IndexError('No close column. Pass desired column as a pd.Series.')
#         # Copy data as series
#         series = data[cols[0]].copy()

#     elif isinstance(data, pd.Series):
#         series = data.copy()
    
#     else:
#         raise TypeError('Input data is not a pandas Series or DataFrame.')

#     # Handles parameter input
#     if not frequency in ('D', 'W', 'M', 'Y'): 
#         raise ValueError('Invalid option for data frequency.')
#     if not isinstance(only_business, bool):
#         raise TypeError('Value for only_business must be a boolean.')
#     if not isinstance(rf_rate, float):
#         raise TypeError('rf_rate parameter is not float type.')
#     if rf_rate > 1 or rf_rate < 0:
#         raise ValueError('rf_rate must positive and equal or less than 1.')
    
#     # Map frequency strings to values
#     if only_business:
#         freq_dict = {'D': 252, 'W': 52, 'M': 12, 'Y': 1}
#     else:
#         freq_dict = {'D': 365, 'W': 52, 'M': 12, 'Y': 1}

#     tmp_df = pd.DataFrame()

#     tmp_df['returns'] = series.pct_change()
#     # Implement this formula with excel
#     neg_vol = tmp_df.loc[tmp_df['returns'] < 0, 'returns'].std() * np.sqrt(freq_dict[frequency])

#     # Handles division by zero
#     if neg_vol == 0:
#         raise ZeroDivisionError('Volatility cannot be equal to zero.')

#     cagr = CAGR(series, frequency, only_business)

#     sortino_ratio = (cagr - rf_rate) / neg_vol
    
#     return sortino_ratio

def max_dd(data):
    """ 
    Calculate maximum drawdown.
    Parameters
    ----------
    data: pd.Series/pd.DataFrame
        Series contaning close prices for an asset. Also possible to input a dataframe,
        must contain a close column.
    Returns
    ----------
    float
        max drawdown
    """

    # Handles input data
    if isinstance(data, pd.DataFrame):
        # All possibles names for close column
        possible_cols = ['Close', 'close', 'Adj Close', 'adj close']
        # Select them
        cols = [col for col in data.columns if col in possible_cols]
        # Check if there's only one close column
        if len(cols) > 1:
            raise KeyError('Ambiguous number of possible close prices column.')
        elif len(cols) == 0:
            raise IndexError('No close column. Pass desired column as a pd.Series.')
        # Copy data as series
        series = data[cols[0]].copy()

    elif isinstance(data, pd.Series):
        series = data.copy()
    
    else:
        raise TypeError('Input data is not a pandas Series or DataFrame.')

    # Store values
    tmp_df = pd.DataFrame()
    
    # Calculate drawdown
    tmp_df['returns'] = series.pct_change()
    tmp_df['cum_ret'] = (1 + tmp_df['returns']).cumprod()
    tmp_df['cum_max'] = tmp_df['cum_ret'].cummax()
    tmp_df['drawdown'] = tmp_df['cum_max'] - tmp_df['cum_ret']
    tmp_df['dd_pct'] = tmp_df['drawdown'] / tmp_df['cum_max']
    
    max_drawdown = tmp_df['dd_pct'].max()
    
    return max_drawdown

def calmar(data, frequency='Y', only_business=True):
    """ 
    Calculate calmar ratio.
    Parameters
    ----------
    data: pd.Series/pd.DataFrame
        Series contaning close prices for an asset. Also possible to input a dataframe,
        must contain a close column.
    frequency: string
        D for daily prices
        W for weekly prices
        M for monthly prices
        Y for yearly prices
    only_business: bool
        When using daily data count only business days.
    Returns
    ----------
    float
        calmar ratio
    """
    
    # Handles input data
    if isinstance(data, pd.DataFrame):
        # All possibles names for close column
        possible_cols = ['Close', 'close', 'Adj Close', 'adj close']
        # Select them
        cols = [col for col in data.columns if col in possible_cols]
        # Check if there's only one close column
        if len(cols) > 1:
            raise KeyError('Ambiguous number of possible close prices column.')
        elif len(cols) == 0:
            raise IndexError('No close column. Pass desired column as a pd.Series.')
        # Copy data as series
        series = data[cols[0]].copy()

    elif isinstance(data, pd.Series):
        series = data.copy()
    
    else:
        raise TypeError('Input data is not a pandas Series or DataFrame.')

    # Handles parameter input
    if not frequency in ('D', 'W', 'M', 'Y'): 
        raise ValueError('Invalid option for data frequency.')
    if not isinstance(only_business, bool):
        raise TypeError('Value for only_business must be a boolean.')

    calmar_ratio = CAGR(series, frequency, only_business) / max_dd(series)
    
    return calmar_ratio