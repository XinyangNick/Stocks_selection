import pandas as pd
import yfinance as yf
#import selection_function as sf
import requests

API = 'L9YXXXRSY2IFLQQ3'


def get_EPS(Ticker:str, time:str='Q')->pd.DataFrame:
    """
    time: str which can be 'A' or 'Q' for annual or quarterly EPS
    return the EPS of the stock by
    """
    url = 'https://www.alphavantage.co/query?function=EARNINGS&symbol=' + Ticker + '&apikey=' + API
    r = requests.get(url)
    data = r.json()
    if time == 'A':
        earnings_df = pd.DataFrame(data['annualEarnings'])
    elif time == 'Q':
        earnings_df = pd.DataFrame(data['quarterlyEarnings'])
    return earnings_df

def get_income_statement(Ticker:str, time:str='Q')->pd.DataFrame:
    """
    time: str which can be 'A' or 'Q' for annual or quarterly income statement
    return the income statement of the stock by
    """
    url = 'https://www.alphavantage.co/query?function=INCOME_STATEMENT&symbol=' + Ticker + '&apikey=' + API
    r = requests.get(url)
    data = r.json()
    if time == 'A':
        income_df = pd.DataFrame(data['annualReports'])
    elif time == 'Q':
        income_df = pd.DataFrame(data['quarterlyReports'])
    return income_df

def get_quarterly_fundamental(Ticker:str)->pd.DataFrame:
    """
    return the quarterly fundamental of the stock by
    """
    df = pd.DataFrame()
    income_sts_df = get_income_statement(Ticker)
    EPS_df = get_EPS(Ticker)
    merge_df = pd.merge(income_sts_df, EPS_df, how='outer', on='fiscalDateEnding')
    merge_df['fiscalDateEnding'] = merge_df['fiscalDateEnding'].astype('datetime64')
    merge_df['quarter'] = merge_df['fiscalDateEnding'].dt.quarter

    df = pd.concat([df, merge_df['fiscalDateEnding']], axis=1)
    df = pd.concat([df, merge_df['quarter']], axis=1)
    df = pd.concat([df, merge_df['reportedEPS']], axis=1)
    #add percentage change of EPS
    df['EPS_pct_change'] = df['reportedEPS'] - df['reportedEPS'].shift(1)/ df['reportedEPS'].shift(1)
    df = pd.concat([df, merge_df['estimatedEPS']], axis=1)
    df = pd.concat([df, merge_df['surprise']], axis=1)
    #add percentage change of revenue
    df = pd.concat([df, merge_df['totalRevenue']], axis=1)
    df['revenue_pct_change'] = df['totalRevenue'] - df['totalRevenue'].shift(1)/ df['totalRevenue'].shift(1)
    #add percentage change of net margin
    df = pd.concat([df, merge_df['netIncome']], axis=1)
    df['netIncome_pct_change'] = df['netIncome'] - df['netIncome'].shift(1)/ df['netIncome'].shift(1)
    #add percentage change of Net Profit Margin
    df['netProfitMargin'] = df['netIncome']/df['totalRevenue']
    df['netProfitMargin_pct_change'] = df['netProfitMargin'] - df['netProfitMargin'].shift(1)/ df['netProfitMargin'].shift(1)

    return df


def generate_result(path, Ticker:str):
    df = get_quarterly_fundamental(Ticker)
    df.to_csv(path + Ticker)
    return df

