import sys
Path = 'D:/NickFiles/Stocks/Stocks_selection'
sys.path.insert(0, Path)

import pandas as pd
import yfinance as yf
from Nick_Module import selection_function as sf

SP500_data = sf.Benchmark_Data()

GOOG = 'GOOG'
AAPL = 'AAPL'
MSFT = 'MSFT'
HROW = 'HROW'

GOOG_hist = sf.Stock_Data(GOOG)
print(GOOG_hist)