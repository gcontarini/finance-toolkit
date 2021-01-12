"""
Implements a series of technical 
indicators used in finance and trading.
"""

import pandas as pd

def ADX(data, ma, full_output=False):
    """ 
    Calculate average directional index (ADX) for a given 
    ohlc dataframe.
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
        With columns adx and dx
        For full output, dm_pos, dm_neg, tr, roll_tr, roll_dmp, 
        roll_dmn, di_pos, di_neg, di_sum, di_diff are shown too
    """
    
    # Handles input data
    if not isinstance(data, pd.DataFrame):
        raise TypeError('Input data is not a pandas DataFrame.')

    if not set(['High', 'Low', 'Close']).issubset(data.columns):
        raise IndexError('Missing necessary columns (High, Low or Close).')

    # Handles parameter input
    if not isinstance(ma, int):
        raise TypeError('ma parameter is not integer type.')

    full_df = pd.DataFrame()

    # Compute true range
    full_df['diff_hl'] = abs(data['High'] - data['Low'])
    full_df['diff_hc'] = abs(data['High'] - data['Close'].shift(1))
    full_df['diff_lc'] = abs(data['Low'] - data['Close'].shift(1))
    full_df['tr'] = full_df[['diff_hl', 'diff_hc', 'diff_lc']].max(axis=1)
    # Delete diff columns
    full_df = full_df.drop(['diff_hl', 'diff_hc', 'diff_lc'], axis=1)
    # Compute directional momentum
    full_df['dm_pos'] = data['High'] - data['High'].shift(1)
    full_df['dm_neg'] = data['Low'].shift(1) - data['Low']
    # Only positive values
    full_df.loc[full_df['dm_pos'] < 0, 'dm_pos'] = 0
    full_df.loc[full_df['dm_neg'] < 0, 'dm_neg'] = 0
    # Take rolling sum
    full_df['roll_tr'] = full_df['tr'].rolling(ma).sum()
    full_df['roll_dmp'] = full_df['dm_pos'].rolling(ma).sum()
    full_df['roll_dmn'] = full_df['dm_neg'].rolling(ma).sum()
    
    # Compute new rolling sum
    roll_tr = [None for i in range(ma)]
    roll_dmp = [None for i in range(ma)]
    roll_dmn = [None for i in range(ma)]
    roll_tr.append(full_df['roll_tr'].iloc[ma])
    roll_dmp.append(full_df['roll_dmp'].iloc[ma])
    roll_dmn.append(full_df['roll_dmn'].iloc[ma])
    # Don't know if there is a vector method to do that
    for i in range(ma+1, full_df.shape[0]):
        temp_tr = (roll_tr[-1] - (roll_tr[-1] / ma) + full_df.iloc[i, -6])
        roll_tr.append(temp_tr)
        
        temp_dmp = (roll_dmp[-1] - (roll_dmp[-1] / ma) + full_df.iloc[i, -5])
        roll_dmp.append(temp_dmp)
        
        temp_dmn = (roll_dmn[-1] - (roll_dmn[-1] / ma) + full_df.iloc[i, -4])
        roll_dmn.append(temp_dmn)
    # Change series in df    
    full_df['roll_tr'] = roll_tr
    full_df['roll_dmp'] = roll_dmp
    full_df['roll_dmn'] = roll_dmn
    
    # Compute directional indicator
    full_df['di_pos'] = 100 * (full_df['roll_dmp'] / full_df['roll_tr'])
    full_df['di_neg'] = 100 * (full_df['roll_dmn'] / full_df['roll_tr'])
    # Compute sum and diff
    full_df['di_sum'] = full_df['di_pos'] + full_df['di_neg']
    full_df['di_diff'] = abs(full_df['di_pos'] - full_df['di_neg'])
    # Compute dx and rolling for adx
    full_df['dx'] = (full_df['di_diff'] / full_df['di_sum']) * 100
    full_df['adx'] = full_df['dx'].rolling(ma).mean()
    
    # Same trick as for roll series
    adx = [None for i in range(2*ma-1)]
    adx.append(full_df['adx'].iloc[2*ma-1])
    for i in range((2*ma), full_df.shape[0]):
        temp = (adx[-1] * (ma - 1) + full_df.iloc[i, -2]) / ma
        adx.append(temp)        
    full_df['adx'] = adx

    # Prepares return df
    if full_output == True:
        df = data.copy()
        df = pd.concat([df, full_df], axis=1)
    else:
        df = full_df[['adx', 'dx']]
    
    return df

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

    if not set(['High', 'Low', 'Close']).issubset(data.columns):
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

def bollband(data, ma, full_output=False):
    '''
    Calculate bollinger bands for a given series.
    Parameters
    ----------
    data: pd.Series/pd.DataFrame
        Series or dataframe to calculate bands.
        If df is passed, it must have a close or
        adjusted close column with the following labels:
           - Close
           - close
           - Adj Close
           - adj close
    ma: int
        Moving average parameter
    Returns
    ----------
    pd.DataFrame
        With columns bollband_up and bollband_low.
        For full output, ma is shown too
    '''

    # Handles input data
    if isinstance(data, pd.DataFrame):
        # All possibles names for close column
        possible_cols = ['Close', 'close', 'Adj Close', 'adj close']
        # Select them
        cols = cols = [col for col in data.columns if col in possible_cols]
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
    if not isinstance(ma, int):
        raise TypeError('ma parameter is not integer type.')

    full_df = pd.DataFrame()

    full_df['ma'] = series.rolling(ma).mean()
    full_df['bollband_up'] = full_df['ma'] + 2 * full_df['ma'].rolling(ma).std()
    full_df['bollband_low'] = full_df['ma'] - 2 * full_df['ma'].rolling(ma).std()

    # Prepares return df
    if full_output == True:
        df = data.copy()
        df = pd.concat([df, full_df], axis=1)
    else:
        df = full_df[['bollband_up', 'bollband_low']]
    
    return df

def MACD(data, slow, fast, ma, full_output=False):
    """ 
    Calculate moving average convergence 
    divergence (MACD) for a given time series 
    (usually close prices).
    Parameters
    ----------
    data: pd.Series/pd.DataFrame
        Series or dataframe to calculate MACD.
        If df is passed, it must have a close or
        adjusted close column with the following labels:
           - Close
           - close
           - Adj Close
           - adj close
    slow: int
        How many observations the slow line will look back
    fast: int
        How many obversations the fast line will look back
    ma: int
        How many obversations will be used to calculate moving average
    full_output: bool
        Returns input data and support series used in calculation
    Returns
    ----------
    pd.DataFrame
        With columns macd_line and macd_signal
        For full output, slow_ma and fast_ma are shown too
    """
    
    # Handles input data
    if isinstance(data, pd.DataFrame):
        # All possibles names for close column
        possible_cols = ['Close', 'close', 'Adj Close', 'adj close']
        # Select them
        cols = cols = [col for col in data.columns if col in possible_cols]
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

    # Handles parameters inputs
    for parameter in [slow, fast, ma]:
        if not isinstance(parameter, int):
            raise TypeError('One or more parameters are not integer type.')
    
    if slow <= fast:
        raise ValueError('Slow line must have a value bigger than fast line')

    full_df = pd.DataFrame()

    # Calculate lines
    full_df['slow_ma'] = series.ewm(span=slow).mean()
    full_df['fast_ma'] = series.ewm(span=fast).mean()
    full_df['macd_line'] = abs(full_df['slow_ma'] - full_df['fast_ma'])
    full_df['macd_signal'] = full_df['macd_line'].ewm(span=ma).mean()
    
    # Prepares return df
    if full_output == True:
        df = data.copy()
        df = pd.concat([df, full_df], axis=1)
    else:
        df = full_df[['macd_line', 'macd_signal']]
    
    return df

def RSI(data, ma, full_output=False):
    """ 
    Calculate RSI indicator for a given series or ohlc data.
    Parameters
    ----------
    data: pd.Series/pd.DataFrame
        Series or dataframe to calculate RSI.
        If df is passed, it must have a close or
        adjusted close column with the following labels:
           - Close
           - close
           - Adj Close
           - adj close
    ma: int
        How many obversations will be used to calculate moving average
    full_output: bool
        Returns input data and support series used in calculation
    Returns
    ----------
    pd.Series/pd.DataFrame
        With rsi values
        For full output, df is returned with gain, loss, av_gain
        and av_loss as well.
    """

    # Handles input data
    if isinstance(data, pd.DataFrame):
        # All possibles names for close column
        possible_cols = ['Close', 'close', 'Adj Close', 'adj close']
        # Select them
        cols = cols = [col for col in data.columns if col in possible_cols]
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
    if not isinstance(ma, int):
        raise TypeError('ma parameter is not integer type.')
    
    full_df = pd.DataFrame()
    
    # Compute gains and losses
    full_df['gain'] = series - series.shift(1)
    full_df['loss'] = series.shift(1) - series
    # For negative values substitute for zero
    full_df.loc[full_df['gain'] < 0, 'gain'] = 0
    full_df.loc[full_df['loss'] < 0, 'loss'] = 0
    # Only needs the first value of the ma series
    full_df['av_gain'] = full_df['gain'].rolling(ma).mean()
    full_df['av_loss'] = full_df['loss'].rolling(ma).mean()
    # all values before index ma must be NaN to preserve original shape
    av_gain = [None for i in range(ma)]
    av_loss = [None for i in range(ma)]
    av_gain.append(full_df['av_gain'].iloc[ma])
    av_loss.append(full_df['av_loss'].iloc[ma])
    
    # The series must be reconstructed recursively
    for i in range(ma+1, series.shape[0]):
        # Index -2 for full_df colums is the gain column
        term_gain = (av_gain[-1] * (ma - 1) + full_df.iloc[i, -2]) / ma
        av_gain.append(term_gain)
        # Index -1 for full_df colums is the loss column
        term_loss = (av_loss[-1] * (ma - 1) + full_df.iloc[i, -1]) / ma
        av_loss.append(term_loss)
    
    # Average columns using recursive rule
    full_df['av_gain'] = av_gain
    full_df['av_loss'] = av_loss
    
    # Compute indicator
    full_df['rsi'] = 100 - (100 / (1 + (full_df['av_gain'] / full_df['av_loss'])))
    
    # Prepares return df
    if full_output == True:
        df = data.copy()
        df = pd.concat([df, full_df], axis=1)
    else:
        df = full_df['rsi']
    
    return df

def OBV(data, full_output=False):
    """ 
    Calculate on balance volume (OBV) for a given 
    ohlc+volume dataframe.
    Parameters
    ----------
    data: pd.DataFrame
        DataFrame containing OHLC+Volume data. Columns must have the
        following labels: Close and Volume.
    full_output: bool
        Returns input data and support series used in calculation
    Returns
    ----------
    pd.DataFrame
        DataFrame with OBV indicator
        For full output, directional and returns are shown too.
    """
    
    # Handles input data
    if not isinstance(data, pd.DataFrame):
        raise TypeError('Input data is not a pandas DataFrame.')

    if not set(['Close', 'Volume']).issubset(data.columns):
        raise IndexError('Missing necessary columns (Close or Volume).')

    full_df = pd.DataFrame()
    
    # Compute OBV
    full_df['returns'] = data['Close'].pct_change()
    
    full_df['directional'] = 0
    
    full_df.loc[full_df['returns'] > 0, 'directional'] = 1
    full_df.loc[full_df['returns'] < 0, 'directional'] = -1
    
    full_df['obv'] = (full_df['directional'] * data['Volume']).cumsum()

    # Prepares return df
    if full_output == True:
        df = data.copy()
        df = pd.concat([df, full_df], axis=1)
    else:
        df = full_df[['obv']]
    
    return df