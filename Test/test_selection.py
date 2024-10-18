import os
# Path = '/Users/nick0o0o0/Library/Mobile Documents/com~apple~CloudDocs/gxyfile/Trading/Nick_Module'
# os.chdir(Path)
import pandas as pd
import yfinance as yf
from ..Nick_Module import selection_function as sf 


SP500_data = sf.Benchmark_Data()

GOOG = 'GOOG'
AAPL = 'AAPL'
MSFT = 'MSFT'
HROW = 'HROW'

GOOG_hist = sf.Stock_Data(GOOG)
print(GOOG_hist)