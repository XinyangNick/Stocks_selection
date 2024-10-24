import yfinance as yf
import pandas as pd
import selection_function as sf



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

def backtest_macd_strategy(df, initial_cash=10000):
    """
    Backtests a simple MACD strategy where you buy when MACD > 0 and sell when MACD < 0.
    Records the balance, cash, and position over time in new columns.

    Parameters:
    df (pandas.DataFrame): Dataframe containing the historical price data and MACD values.
    initial_cash (float): The initial cash for the backtest.

    Returns:
    pandas.DataFrame: The dataframe with additional columns for balance, cash, and position over time.
    """
    cash = initial_cash
    position = 0  # Number of shares held
    df['Cash'] = initial_cash
    df['Position'] = 0
    df['Balance'] = initial_cash


    df['Cash'] = df['Cash'].astype(float)
    df['Balance'] = df['Balance'].astype(float)
    df.reset_index(inplace=True)

    for i, row in df.iterrows():
        if i == 0:
            continue  # Skip the first row
        cash = df.at[i-1, 'Cash']  # Update cash from the previous row
        position = df.at[i-1, 'Position']  # Update position from the previous row

        if df['MACD'].iloc[i] > 0 and df['MACD'].iloc[i-1] <= 0:
            # Buy signal
            if cash > 0:
                position = cash // df['Close'].iloc[i]
                cash = cash - position * df['Close'].iloc[i]
        elif df['MACD'].iloc[i] < 0 and df['MACD'].iloc[i-1] >= 0:
            # Sell signal
            if position > 0:
                cash = cash + position * df['Close'].iloc[i]
                position = 0

        # Calculate balance
        balance = cash + position * df['Close'].iloc[i]
        if balance < 0:
            break  # Stop the backtest if balance is negative

        # Record the values
        df.at[i, 'Cash'] = cash
        df.at[i, 'Position'] = position
        df.at[i, 'Balance'] = balance

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
    df['Cumulative_Returns'] = (1 + df['Returns']).cumprod() - 1
    return df['Cumulative_Returns'].iloc[-1]  # Return the final cumulative return


# Example usage
if __name__ == "__main__":
    ticker = "AAPL"
    start_date = "2020-01-01"
    end_date = "2020-12-01"
    df = yf.download(ticker, start=start_date, end=end_date)
    df = calculate_macd(df)
    final_df = backtest_macd_strategy(df)
    final_df
