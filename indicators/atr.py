import pandas as pd

def ATR(data, ma, full_output=False):
    """ 
    Calculate average true range (ATR) for a given ohlc data.
    Parameters
    ----------
    data: pd.DataFrame
        DataFrame containing OHLC data. Columns must have the
        following labels: High, Low, Close. Open column is not mandatory.
    ma: int
        How many obversations will be used to calculate moving average
    full_output: bool
        Returns input data and support series used in calculation
    Returns
    ----------
    pd.DataFrame
        With columns atr and tr (true range)
        For full output, dff_hl, dff_hc and dff_lc are shown too
    """
    # Handles input data
    if not isinstance(data, pd.DataFrame):
        raise TypeError('Input data is not a pandas DataFrame.')

    # Check this condition
    if not (['High', 'Low', 'Close'] in data.columns).all():
        raise IndexError('Missing necessary columns (High, Low or Close).')

    # Handles parameter input
    if not isinstance(ma, int):
        raise TypeError('ma parameter is not integer type.')

    full_df = pd.DataFrame()

    # Compute ranges
    full_df['dff_hl'] = abs(data['High'] - data['Low'])
    full_df['dff_hc'] = abs(data['High'] - data['Close'].shift(1))
    full_df['dff_lc'] = abs(data['Low'] - data['Close'].shift(1))
    full_df['tr'] = full_df[['dff_hl', 'dff_hc', 'dff_lc']].max(axis=1)
    full_df['atr'] = full_df['tr'].rolling(ma).mean()
    
    # Prepares return df
    if full_output == True:
        df = data.copy()
        df = pd.concat([df, full_df], axis=1)
    else:
        df = full_df[['atr', 'tr']]
    
    return df