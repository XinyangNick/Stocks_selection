import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import yfinance as yf


#Plot
def Kline_Plot(Ticker:yf.Ticker, data:pd.DataFrame, days:int=250):
    """
    graph caddle chart from -days to now
    """
    data = data[-days:]
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
