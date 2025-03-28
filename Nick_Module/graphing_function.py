import plotly.graph_objects as go
from plotly.subplots import make_subplots
import yfinance as yf


#Plot
def Kline_Plot(Ticker: str, time: str = '1y'):
    """
    Graph candlestick chart for the given Ticker from -days to now
    """
    # Fetch historical data for the given ticker
    data = yf.Ticker(Ticker).history(period=f'{time}')
    
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, 
                        vertical_spacing=0.03, subplot_titles=(f'Candlestick Chart for {Ticker}', 'Volume'), 
                        row_width=[0.3, 0.7])

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


def Industry_Plot(Ticker: str, time: str = '1y'):
    """
    Graph line chart for the industry of the given Ticker from -days to now
    """
    # Fetch industry data for the given ticker
    ticker_info = yf.Ticker(Ticker).info
    industry_key = ticker_info.get('industryKey')
    
    if not industry_key:
        raise ValueError(f"Industry data not found for ticker {Ticker}")
    
    industry = yf.Industry(industry_key)
    industry_ticker = industry.ticker
    
    # Fetch historical data for the industry ticker
    data = industry_ticker.history(period=f'{time}')
    
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, 
                        vertical_spacing=0.03, subplot_titles=(f'Line Chart for {industry_key} Industry', 'Volume'), 
                        row_width=[0.3, 0.7])

    # Add line chart in the first row
    fig.add_trace(go.Scatter(x=data.index,
                             y=data['Close'],
                             mode='lines',
                             name='Price'), row=1, col=1)

    # Add volume bars in the second row
    fig.add_trace(go.Bar(x=data.index, y=data['Volume'], showlegend=False, name='Volume'), row=2, col=1)

    # Update layout
    fig.update_layout(title=f'{industry_key} Industry Line Chart with Volume',
                      xaxis_title='Date',
                      yaxis_title='Price (USD)',
                      xaxis_rangeslider_visible=False)

    # Show the plot
    fig.show()


def Benchmark_Plot(benchmark: str = '^GSPC', time: str = '1y'):
    """
    Graph line chart for the benchmark index from -days to now
    """
    # Fetch historical data for the benchmark index
    data = yf.download(benchmark, period=f'{time}')
    
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, 
                        vertical_spacing=0.03, subplot_titles=(f'Line Chart for {benchmark}', 'Volume'), 
                        row_width=[0.3, 0.7])

    # Add line chart in the first row
    fig.add_trace(go.Scatter(x=data.index,
                             y=data['Close'],
                             mode='lines',
                             name='Price'), row=1, col=1)

    # Add volume bars in the second row
    fig.add_trace(go.Bar(x=data.index, y=data['Volume'], showlegend=False, name='Volume'), row=2, col=1)

    # Update layout
    fig.update_layout(title=f'{benchmark} Line Chart with Volume',
                      xaxis_title='Date',
                      yaxis_title='Price (USD)',
                      xaxis_rangeslider_visible=False)

    # Show the plot
    fig.show()




def graph_together(Ticker: str, Benchmark: str='^GSPC', time: str='1y'):
    Kline_Plot(Ticker, time)
    Industry_Plot(Ticker, time)
    Benchmark_Plot(Benchmark, time)



def graph_move_together(Ticker: str, benchmark: str='^GSPC', time: str = '5y'):
    """
    Plots three graphs together with the same height using Plotly.
    
    Parameters:
    kline_data (pd.DataFrame): Data for the Kline graph, with volume
    data1 (pd.DataFrame): Data for the industry graph.
    data2 (pd.DataFrame): Data for the benchmark graph.
    
    """
    klinedata = yf.Ticker(Ticker).history(period=f'{time}')
    ticker_info = yf.Ticker(Ticker).info
    industry_key = ticker_info.get('industryKey')

    if not industry_key:
        raise ValueError(f"Industry data not found for ticker {Ticker}")
    industry = yf.Industry(industry_key)
    industry_ticker = industry.ticker
    # Fetch historical data for the industry ticker
    data1 = industry_ticker.history(period=f'{time}')
    #benchmark data
    data2 = yf.download(benchmark, period=f'{time}')


    # Create subplots
    fig = make_subplots(rows=4, cols=1, shared_xaxes=True, vertical_spacing=0)
    # Plot only the volume for Kline
    fig.add_trace(go.Candlestick(x=klinedata.index,
                                 open=klinedata['Open'],
                                 high=klinedata['High'],
                                 low=klinedata['Low'],
                                 close=klinedata['Close'],
                                 name=Ticker), row=1, col=1)
    fig.add_trace(go.Bar(x=klinedata.index, y=klinedata['Volume'], showlegend=False, name='Volume'), row=2, col=1)
    # Plot the industry graph
    fig.add_trace(go.Scatter(x=data1.index,
                             y=data1['Close'],
                             mode='lines',
                             name=industry_key), row=3, col=1)

    # Plot the Benchmark graph
    fig.add_trace(go.Scatter(x=data2.index,
                             y=data2['Close'],
                             mode='lines',
                             name=benchmark), row=4, col=1)
    
    # Update layout
    fig.update_layout(title_text="{0} Kline, {1} Industry, {2} Benchmark".format(Ticker, industry_key, benchmark))
    
    # Show plot
    fig.show()

# Example usage:
#graph_move_together('HROW', time='5Y')