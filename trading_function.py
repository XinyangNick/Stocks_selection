import pandas as pd
import numpy as np
import yfinance as yf
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def MA(history:pd.DataFrame, N:int):
    """
    MA = sum(Pn)/n, where Pn is Clsoed price
    """
    history['MA'+str(N)] = history['Close'].rolling(N).sum() / N
    

def TransStage2_price_Criteria(history:pd.DataFrame, n=0.8):
    """
    52-week low
    """
    low52week = history['Close'].min()
    last_price = history['Close'].iloc[-1]

    return last_price >= low52week * (1+n)




#Plot
def Kline_Plot(Ticker:yf.Ticker, data:pd.DataFrame):
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, 
                    vertical_spacing=0.03, subplot_titles=(f'Candlestick Chart for {ticker}', 'Volume'), 
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


