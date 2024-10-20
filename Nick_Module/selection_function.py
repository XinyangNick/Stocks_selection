import pandas as pd
import numpy as np
import yfinance as yf


def Stock_Data(Ticker:str, period:str='2y'):
    data = yf.Ticker(Ticker).history(period)
    return data

def Benchmark_Data(benchmark:str='^GSPC'):
    SP500 = yf.download(benchmark, period='2y')
    return SP500


def MA_Adding(history:pd.DataFrame, lst=[20, 50, 100, 150, 200]):
    """
    MA = sum(Pn)/n, where Pn is Clsoed price
    return the current MA
    """
    for N in lst:
        history['MA'+str(N)] = history['Close'].rolling(N).sum() / N



def MA(history: pd.DataFrame, N: int, Day: int = -1):
    """
    Returns the Moving Average over N periods for the specified Day in the 'history' DataFrame.
    
    Parameters:
    - history: DataFrame with at least a 'Close' column for closing prices.
    - N: The window size for calculating the moving average.
    - Day: The index (negative or positive) of the day for which to return the moving average.
    
    Returns:
    - The moving average value for the given day.
    """
    close_price = history['Close']
    
    # Handle if Day is negative, to count from the end of the series
    target_day = Day if Day >= 0 else len(close_price) + Day
    
    # Ensure the target day is within a valid range
    if target_day < N - 1:
        raise ValueError(f"Not enough data to compute a {N}-period moving average on day {Day}.")
    
    # Slice the relevant portion of the close_price for the given day and N periods before it
    relevant_data = close_price.iloc[target_day - N + 1 : target_day + 1]
    
    # Calculate the moving average only for the sliced data
    moving_avg = relevant_data.mean()
    
    return moving_avg



def Stage2_Confirmed_Criteria(Ticker:str, 
                              Benchmark:str=None, 
                              MA200UP:int=30, 
                              LOW52UP:int=30,
                              RS_score:int=70):
    """
    MA200UP: is the number of day that MA200 is uptrend
    (should be at least 30days)
    LOW52UP: is the percent that current price higher than the 52 Weeks low
    (should be at least 30% better 100%200%)
    RS_score: is the performance of the stock compare to the market
    (should be at least 70 better >80, 90)

    1. The current stock price is above both the 150-day (30-week) and t
    he 200-day (40-week) moving average price lines. 
    2. The 150-day moving average is above the 200-day moving average. 
    3. The 200-day moving average line is trending up for at least 1
    month (preferably 4 to 5 months minimum in most cases). 
    4. The 50-day (10-week) moving average is above both the 150-day 
    and 200-day moving averages. 
    5. The current stock price is trading above the 50-day moving average. 
    6. The current stock price is at least 30 percent above its 52-week low. 
    (Many of the best selections will be 100 percent, 300 percent, or greater 
    above their 52-week low before they emerge from a solid consolidation 
    period and mount a large scale advance.) 
    7. The current stock price is within at least 25 percent of its 52-week 
    high (the closer to a new high the better). 
    8. The relative strength ranking (RSI)(as reported in Investor’s Business 
    Daily) is no less than 70, and preferably in the 80s or 90s, which will 
    generally be the case with the better selections. 

    """

    history = Stock_Data(Ticker)
    if Benchmark is None:
        Benchmark = Benchmark_Data()
    else:
        Benchmark = Benchmark_Data(Benchmark)

    high52week = history['Close'][-250:].max()
    low52week = history['Close'][-250:].min()
    last_price = history['Close'][-1]

    Counter = []
    #1
    if last_price >= MA(history, 150) and last_price >= MA(history, 200):
        Counter.append(1)
    #2
    if MA(history, 150) >= MA(history, 200):
        Counter.append(2)
    #3 (history['MA200'][-1] - history['MA200'][-MA200UP]) / MA200UP
    slope = (MA(history, 200) - MA(history, 200, -MA200UP)) / MA200UP
    if slope > 0:
        Counter.append(3)
    #4
    if MA(history, 50) >= MA(history, 150) and MA(history, 50) >= MA(history, 200):
        Counter.append(4)
    #5
    if last_price >= MA(history, 50):
        Counter.append(5)
    #6
    if last_price >= low52week * (1 + LOW52UP / 100):
        Counter.append(6)
    #7
    if last_price >= high52week * 0.75:
        Counter.append(7)
    #8
    RS_score = RS_rating(history, Benchmark)
    if RS_score >= RS_score:
        Counter.append(8)  
    # Check if meet all 8 Criteria
    return len(Counter) == 8, Counter, RS_score


#The RS rating >=70 is great
def RS_rating(hisotry:pd.DataFrame, benchmark:pd.DataFrame):
    """
    Return the RS ratio
    """
    stock_price_change = (hisotry['Close'].iloc[-1] / hisotry['Close'].iloc[-250]) - 1
    benchmark_price_change = (benchmark['Adj Close'].iloc[-1] / benchmark['Adj Close'].iloc[-250]) - 1
    rs_score = (stock_price_change / benchmark_price_change) * 100
    return rs_score


Stage2_Confirmed_Criteria('IRMD')

