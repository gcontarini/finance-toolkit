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