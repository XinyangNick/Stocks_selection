import pandas as pd
import yfinance as yf
import statsmodels.api as sm

DEFULT_START_DATE = '2000-01-01'
CURRENT_DATE = pd.Timestamp.now().strftime('%Y-%m-%d')


def Stock_Data(Ticker:str, period:str='2y', start_date:str=None, end_date:str=None):
    if start_date is None or end_date is None:
        data = yf.Ticker(Ticker).history(period)
    else:
        data = yf.Ticker(Ticker).history(start=start_date, end=end_date)
    return data

def Industry_Data(Ticker:str, period:str='2y'):
    ticker_info = yf.Ticker(Ticker).info
    industry_key = ticker_info.get('industryKey')
    if not industry_key:
        raise ValueError(f"Industry data not found for ticker {Ticker}")
    industry = yf.Industry(industry_key)
    industry_ticker = industry.ticker
    # Fetch historical data for the industry ticker
    data = industry_ticker.history(period=period)
    return data

def Benchmark_Data(benchmark:str='^GSPC', start_date:str=DEFULT_START_DATE, end_date:str=CURRENT_DATE):
    if start_date is None or end_date is None:
        SP500 = yf.download(benchmark)
    else:
        SP500 = yf.download(benchmark, start=start_date, end=end_date)
    return SP500

def Risk_Free_Data(Ticker:str='^TNX', start_date:str=DEFULT_START_DATE, end_date:str=CURRENT_DATE):
    """
    Return the risk free rate using the 10-year US Treasury yield.
    """
    if start_date is None or end_date is None:
        treasury_data = yf.download(Ticker)
    else:
        treasury_data = yf.download(Ticker, start=start_date, end=end_date)
    return treasury_data

def Stock_Returns(Ticker:str, period:str='2y', n:int=1):
    """
    Date is ascending order
    n is the number of days of shift to calculate the returns
    Return the stock return
    """
    data = Stock_Data(Ticker, period)
    data['Stock_Return'] = (data['Close']-data['Close'].shift(n))/data['Close'].shift(n)
    return data

def Industry_Returns(Ticker:str, period:str='2y', n:int=1):
    """
    n is the number of days of shift to calculate the returns
    Return the industry return
    """
    data = Industry_Data(Ticker, period)
    data['Industry_Return'] = (data['Close']-data['Close'].shift(n))/data['Close'].shift(n)
    return data

def Benchmark_Returns(benchmark:str='^GSPC', start_date:str=DEFULT_START_DATE, end_date:str=CURRENT_DATE, n:int=1):
    """
    n is the number of days of shift to calculate the returns
    Reutrn the benchmark return
    """
    data = Benchmark_Data(benchmark, start_date, end_date)
    data['Benchmark_Return'] = (data['Adj Close']-data['Adj Close'].shift(n))/data['Adj Close'].shift(n)
    return data

def Risk_Free_Return(Ticker:str='^TNX', start_date:str=DEFULT_START_DATE, end_date:str=CURRENT_DATE, n:int=1):
    """
    Return the risk free rate using the 10-year US Treasury yield.
    """
    data = Risk_Free_Data(Ticker, start_date, end_date)
    data['Risk_Free_Return'] = data['Adj Close']/100
    return data


def MA_Adding(history:pd.DataFrame, lst=[20, 50, 100, 150, 200]):
    """
    MA = sum(Pn)/n, where Pn is Clsoed price
    return the current MA
    """
    for N in lst:
        history['MA'+str(N)] = history['Close'].rolling(N).sum() / N


def MA(history: pd.DataFrame, N: int, Day: int = -1)->float:
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
                              start_date:str=None,
                              end_date:str=None,
                              MA200UP:int=30, 
                              LOW52UP:int=30,
                              RS_score:int=70)->tuple:
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

    history = Stock_Data(Ticker, start_date=start_date, end_date=end_date)
    if Benchmark is None:
        Benchmark = Benchmark_Data(start_date=start_date, end_date=end_date)
    else:
        Benchmark = Benchmark_Data(Benchmark, start_date=start_date, end_date=end_date)

    if len(history) < 250:
        raise ValueError("Not enough data to compute 52-week high/low and last price.")
    
    high52week = history['Close'].iloc[-250:].max()
    low52week = history['Close'].iloc[-250:].min()
    last_price = history['Close'].iloc[-1]

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
def RS_rating(hisotry:pd.DataFrame, benchmark:pd.DataFrame)->float:
    """
    Return the RS ratio
    """
    stock_price_change = (hisotry['Close'].iloc[-1] / hisotry['Close'].iloc[-250]) - 1
    benchmark_price_change = (benchmark['Adj Close'].iloc[-1] / benchmark['Adj Close'].iloc[-250]) - 1
    rs_score = (stock_price_change / benchmark_price_change) * 100
    return rs_score


def Regression_Analysis(Ticker:str, 
                        Benchmark:str='^GSPC', 
                        Risk_free:str='^TNX', 
                        period:str='max',
                        start_date:str=None, 
                        end_date:str=None, 
                        n:int=1):
    """
    Ticker: is the stock ticker
    Benchmark: is the benchmark ticker
    Risk_free: is the risk free ticker
    Peiod: is the time period for the Stock, Industry, Benchmark
    Start_date: is the start date for the Risk_free rate
    End_date: is the end date for the Risk_free rate
    n: is the number of days of shift to calculate the returns

    Return the regression analysis
    """
    Stock_R = Stock_Returns(Ticker, period, n)['Stock_Return']
    Industry_R= Industry_Returns(Ticker, period, n)['Industry_Return']
    Benchmark_R = Benchmark_Returns(Benchmark, start_date, end_date, n)['Benchmark_Return']
    Risk_free_r = Risk_Free_Return(Risk_free, start_date, end_date, n)['Risk_Free_Return']

    #Change the date to the same format
    Stock_R.index = Stock_R.index.tz_localize(None)
    Industry_R.index = Industry_R.index.tz_localize(None)
    Benchmark_R.index = Benchmark_R.index.tz_localize(None)
    Risk_free_r.index = Risk_free_r.index.tz_localize(None)

    # Merge the data
    data = pd.merge(Stock_R, Industry_R, how='inner', left_index=True, right_index=True)
    data = pd.merge(data, Benchmark_R, how='inner', left_index=True, right_index=True)
    data = pd.merge(data, Risk_free_r, how='inner', left_index=True, right_index=True)
    data.dropna(inplace=True)
    
    data['Risk_Free_Return_daily'] = (1 + data['Risk_Free_Return']) ** (1/252) - 1
    #Change annul return to daily return
    Rf = data['Risk_Free_Return_daily']
    Rm = data['Benchmark_Return']
    Ri = data['Industry_Return']
    Rs = data['Stock_Return']
    data['R_stock-Rf'] = Rs - Rf
    data['Ri - Rf'] = Ri - Rf
    data['Rm - Rf'] = Rm - Rf
    print(data)

    # Regression Analysis
    X1 = sm.add_constant(data['Ri - Rf']) # Industry
    X2 = sm.add_constant(data['Rm - Rf']) # Benchmark
    
    Y = data['R_stock-Rf'] # Stock
    model1 = sm.OLS(Y, X1).fit() # Industry Regression
    model2 = sm.OLS(Y, X2).fit() # Benchmark Regression

    return model1.summary(), model2.summary()

    

#example
print(Stage2_Confirmed_Criteria('TXRH',start_date='2010-12-01', end_date='2015-11-1'))
#Regression_Analysis('HROW')


x = Stock_Data('AAPL', start_date='2010-12-01', end_date='2015-11-1') # Example usage of the Stock_Data function
print(x)