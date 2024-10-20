import pandas as pd
from datetime import datetime
import os

PATH = '/Users/nick0o0o0/Library/Mobile Documents/com~apple~CloudDocs/gxyfile/Trading/Stocks_selection/data'
PATH2 = '/Users/nick0o0o0/Library/Mobile Documents/com~apple~CloudDocs/gxyfile/Trading/Stocks_selection'
CURRENT_MONTH = datetime.now().strftime('%Y-%m')

def clean_quarterly_fundamental(Ticker:str, current_month:str=CURRENT_MONTH, n:int=4)->pd.DataFrame:
    """
    Ticker: str, ex: 'AAPL'
    current_month: str, ex :2001-12format
    n: int, number of quarters to return
    return the quarterly fundamental of the stock by
    """
    important_columns = ['fiscalDateEnding', 'quarter', 
                         'reportedEPS', 'EPS_YOY_pct_change', 
                         'estimatedEPS', 'surprise', 
                         'totalRevenue', 'revenue_YOY_pct_change', 
                         'netIncome', 'netIncome_YOY_pct_change', 
                         'netProfitMargin', 'netProfitMargin_YOY_pct_change']
    income_sts_df = pd.read_csv(f'{PATH}/{current_month}/{Ticker}_quarter_income.csv')
    EPS_df = pd.read_csv(f'{PATH}/{current_month}/{Ticker}_quarter_EPS.csv')
    # merge the two dataframes
    merge_df = pd.merge(income_sts_df, EPS_df, how='outer', on='fiscalDateEnding')
    # convert the date to datetime format
    merge_df['fiscalDateEnding'] = pd.to_datetime(merge_df['fiscalDateEnding'])
    merge_df = merge_df.sort_values(by='fiscalDateEnding', ascending=False)
    merge_df['quarter'] = merge_df['fiscalDateEnding'].dt.to_period('Q').astype(str).str.replace(' ', '')
    # add percentage change of EPS
    merge_df['EPS_YOY_pct_change'] = merge_df['reportedEPS'].pct_change(periods=n, fill_method=None).replace(0, 1)
    # add percentage change of revenue
    merge_df['revenue_YOY_pct_change'] = merge_df['totalRevenue'].pct_change(periods=n, fill_method=None).replace(0, 1)
    # add percentage change of net income
    merge_df['netIncome_YOY_pct_change'] = merge_df['netIncome'].pct_change(periods=n, fill_method=None).replace(0, 1)
    # add net profit margin
    merge_df['netProfitMargin'] = merge_df['netIncome'] / merge_df['totalRevenue']
    # add percentage change of net profit margin
    merge_df['netProfitMargin_YOY_pct_change'] = merge_df['netProfitMargin'].pct_change(periods=n, fill_method=None).replace(0, 1)
    # Convert percentage changes to percentage format (multiply by 100) and round to no decimal
    merge_df['EPS_YOY_pct_change'] = (merge_df['EPS_YOY_pct_change'] * 100).round(0).apply(lambda x: f"{x:+}")
    merge_df['revenue_YOY_pct_change'] = (merge_df['revenue_YOY_pct_change'] * 100).round(0).apply(lambda x: f"{x:+}")
    merge_df['netIncome_YOY_pct_change'] = (merge_df['netIncome_YOY_pct_change'] * 100).round(0).apply(lambda x: f"{x:+}")
    merge_df['netProfitMargin_YOY_pct_change'] = (merge_df['netProfitMargin_YOY_pct_change'] * 100).round(0).apply(lambda x: f"{x:+}")
    # Shift the percentage change columns to the next row
    merge_df['EPS_YOY_pct_change'] = merge_df['EPS_YOY_pct_change'].shift(-n)
    merge_df['revenue_YOY_pct_change'] = merge_df['revenue_YOY_pct_change'].shift(-n)
    merge_df['netIncome_YOY_pct_change'] = merge_df['netIncome_YOY_pct_change'].shift(-n)
    merge_df['netProfitMargin_YOY_pct_change'] = merge_df['netProfitMargin_YOY_pct_change'].shift(-n)


    return merge_df, merge_df[important_columns]

def generate_fundamental(Ticker:str, current_month:str=CURRENT_MONTH, n:int=4)->pd.DataFrame:
    data_file_name = f'{Ticker}_quarter_income.csv'
    data_file_name2 = f'{Ticker}_quarter_EPS.csv'

    if (data_file_name not in os.listdir(f'{PATH}/{current_month}')) or (data_file_name2 not in os.listdir(f'{PATH}/{current_month}')):
        print(f'{data_file_name} or {data_file_name2} not found in {PATH}/{current_month}')
        return None
    else:
        df1, df2 = clean_quarterly_fundamental(Ticker, current_month, n)

        if not os.path.exists(f'{PATH2}/report/{current_month}'):
            os.makedirs(f'{PATH2}/report/{current_month}', exist_ok=True)
        df1.to_csv(f'{PATH2}/report/{current_month}/{Ticker}_bigfundamental.csv', index=False)
        df2.to_csv(f'{PATH2}/report/{current_month}/{Ticker}_smallfundamental.csv', index=False)
        return df1, df2
    

#example
# example = generate_fundamental('HROW')
# example[1]