import pandas as pd
import numpy as np
import yfinance as yf
import plotly.graph_objects as go
from plotly.subplots import make_subplots


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


def MA(history:pd.DataFrame, N):
    """
    Return the current Moving Average N
    """
    col = 'MA'+str(N)
    if col not in history.columns:
        MA_Adding(history, [N])
    return history[col][-1]


def Stage2_Confirmed_Criteria(history:pd.DataFrame, 
                              Benchmark:pd.DataFrame, 
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
    #3
    slope = (history['MA200'][-1] - history['MA200'][-MA200UP]) / MA200UP
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
    if RS_rating(history, Benchmark) >= RS_score:
        Counter.append(8)  
    # Check if meet all 8 Criteria
    if len(Counter) == 8:
        return True, Counter
    else:
        return False, Counter


#The RS rating >=70 is great
def RS_rating(hisotry:pd.DataFrame, benchmark:pd.DataFrame):
    """
    Return the RS ratio
    """
    stock_price_change = (hisotry['Close'].iloc[-1] / hisotry['Close'].iloc[-250]) - 1
    benchmark_price_change = (benchmark['Adj Close'].iloc[-1] / benchmark['Adj Close'].iloc[-250]) - 1
    rs_score = (stock_price_change / benchmark_price_change) * 100
    return rs_score


#Plot
def Kline_Plot(Ticker:yf.Ticker, data:pd.DataFrame):
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, 
                    vertical_spacing=0.03, subplot_titles=(f'Candlestick Chart for {Ticker}', 'Volume'), 
                    row_width=[0.2, 0.7])

    # Add candlestick chart in the first row
    fig.add_trace(go.Candlestick(x=data.index,
                                open=data['Open'],
                                high=data['High'],
                                low=data['Low'],
                                close=data['Close'],
                                name='Price'), row=1, col=1)

    # Add volume bars in the second row
    fig.add_trace(go.Bar(x=data.index, y=data['Volume'], showlegend=False, name='Volume'), row=2, col=1)

    # Update layout
    fig.update_layout(title=f'{Ticker} Candlestick Chart with Volume',
                    xaxis_title='Date',
                    yaxis_title='Price (USD)',
                    xaxis_rangeslider_visible=False)

    # Show the plot
    fig.show()


