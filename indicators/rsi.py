import pandas as pd

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