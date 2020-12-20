import pandas as pd

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