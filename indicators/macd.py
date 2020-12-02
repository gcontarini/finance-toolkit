import pandas as pd

def macd_line(data, slow, fast, ma, full_output=False):
    """ 
    Calculate moving average convergence 
    divergence (MACD) for a given time series 
    (usually close prices).
    Parameters
    ----------
    series: pd.Series/pd.DataFrame
        Series or dataframe to calculate MACD.
        If df is passed, it must have a close or
        adjusted close column in the following column name:
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