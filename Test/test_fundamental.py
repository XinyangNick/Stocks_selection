import sys
Path = '/Users/nick0o0o0/Library/Mobile Documents/com~apple~CloudDocs/gxyfile/Trading/Stocks_selection'
sys.path.insert(0, Path)

import pandas as pd
import yfinance as yf
from Nick_Module import fundamental_function as ff


ticker = 'HROW'

ff.get_fundamental_data(ticker)