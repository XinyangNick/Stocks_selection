import yfinance as yf

def get_price_dataframe(ticker, start_date, end_date):
    """
    Fetches historical price data for a given ticker between start_date and end_date.

    Parameters:
    ticker (str): The ticker symbol of the stock.
    start_date (str): The start date in the format 'YYYY-MM-DD'.
    end_date (str): The end date in the format 'YYYY-MM-DD'.

    Returns:
    pandas.DataFrame: A dataframe containing the historical price data.
    """
    stock = yf.Ticker(ticker)
    df = stock.history(start=start_date, end=end_date)
    return df

def calculate_macd(df, short_window=12, long_window=26, signal_window=9):
    """
    Calculates the MACD line and signal line.

    Parameters:
    df (pandas.DataFrame): Dataframe containing the historical price data.
    short_window (int): The short window period for the MACD calculation.
    long_window (int): The long window period for the MACD calculation.
    signal_window (int): The window period for the signal line calculation.

    Returns:
    pandas.DataFrame: A dataframe with the MACD line and signal line.
    """
    df['EMA_short'] = df['Close'].ewm(span=short_window, adjust=False).mean()
    df['EMA_long'] = df['Close'].ewm(span=long_window, adjust=False).mean()
    df['MACD'] = df['EMA_short'] - df['EMA_long']
    df['Signal_Line'] = df['MACD'].ewm(span=signal_window, adjust=False).mean()
    return df

def backtest_macd_strategy(df, initial_balance=10000):
    """
    Backtests a simple MACD strategy where you buy when MACD > 0 and sell when MACD < 0.
    Records the balance over time in a new column and allows the balance to be negative.

    Parameters:
    df (pandas.DataFrame): Dataframe containing the historical price data and MACD values.
    initial_balance (float): The initial balance for the backtest.

    Returns:
    pandas.DataFrame: The dataframe with an additional column for balance over time.
    """
    balance = initial_balance
    position = 0  # 0 means no position, positive means holding the stock, negative means shorting the stock
    df['Balance'] = initial_balance

    for i in range(1, len(df)):
        if df['MACD'].iloc[i] > 0 and df['MACD'].iloc[i-1] <= 0:
            # Buy signal
            if position <= 0:
                balance += position * df['Close'].iloc[i]  # Close any short position
                position = balance / df['Close'].iloc[i]
                balance = 0
        elif df['MACD'].iloc[i] < 0 and df['MACD'].iloc[i-1] >= 0:
            # Sell signal
            if position >= 0:
                balance += position * df['Close'].iloc[i]  # Close any long position
                position = -balance / df['Close'].iloc[i]
                balance = 0
        
        # Record the balance at each step
        df['Balance'].iloc[i] = balance if position == 0 else balance + position * df['Close'].iloc[i]

    # If still holding a position at the end, close it
    if position != 0:
        balance += position * df['Close'].iloc[-1]
        df['Balance'].iloc[-1] = balance

    return df


def calculate_returns(df):
    """
    Calculates the returns based on the balance over time.

    Parameters:
    df (pandas.DataFrame): Dataframe containing the historical price data and balance over time.

    Returns:
    pandas.DataFrame: The dataframe with an additional column for returns.
    """
    df['Returns'] = df['Balance'].pct_change().fillna(0)
    return df

# Example usage
if __name__ == "__main__":
    ticker = "APVO"
    start_date = "2013-03-01"
    end_date = "2017-12-01"
    df = get_price_dataframe(ticker, start_date, end_date)
    df = calculate_macd(df)
    final_balance = backtest_macd_strategy(df)
    print(df)
    print(calculate_returns(df))