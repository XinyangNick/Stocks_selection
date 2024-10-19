import sys
Path = 'D:/NickFiles/Stocks/Stocks_selection'
sys.path.insert(0, Path)

import pandas as pd
import yfinance as yf
from Nick_Module import selection_function, fundamental_function as sf, ff