import pandas as pd

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