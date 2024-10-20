import pandas as pd
import yfinance as yf
#import selection_function as sf
import requests
from datetime import datetime
import os

#API = 'L9YXXXRSY2IFLQQ3'
API = '2ID6DFGA46EO9NEI'
PATH = '/Users/nick0o0o0/Library/Mobile Documents/com~apple~CloudDocs/gxyfile/Trading/Stocks_selection'

def get_EPS(Ticker:str)->pd.DataFrame:
    """
    return the EPS of the stock
    """
    url = 'https://www.alphavantage.co/query?function=EARNINGS&symbol=' + Ticker + '&apikey=' + API
    r = requests.get(url)
    data = r.json()
    quarter_data = pd.DataFrame(data['quarterlyEarnings'])
    year_data = pd.DataFrame(data['annualEarnings'])
    return quarter_data, year_data

def get_income_statement(Ticker:str)->pd.DataFrame:
    """
    return the income statement of the stock by
    """
    url = 'https://www.alphavantage.co/query?function=INCOME_STATEMENT&symbol=' + Ticker + '&apikey=' + API
    r = requests.get(url)
    data = r.json()
    quarter_data = pd.DataFrame(data['quarterlyReports'])
    year_data = pd.DataFrame(data['annualReports'])
    return quarter_data, year_data


def save_raw(Ticker:str, path:str=PATH):
    """
    save the raw data of the stock
    """
    quarter_income_df, annual_income_df = get_income_statement(Ticker)
    quarter_EPS_df, annual_EPS_df = get_EPS(Ticker)
    current_date = datetime.now().strftime("%Y-%m")
    if path is None:
        path = os.getcwd()
    path = os.path.join(path, 'data', current_date)
    os.makedirs(path, exist_ok=True)
    base_path = os.path.join(path, Ticker)
    quarter_income_df.to_csv(base_path + '_quarter_income.csv')
    annual_income_df.to_csv(base_path + '_annual_income.csv')
    quarter_EPS_df.to_csv(base_path + '_quarter_EPS.csv')
    annual_EPS_df.to_csv(base_path + '_annual_EPS.csv')


save_raw('TXRH')