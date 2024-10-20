import pandas as pd
from datetime import datetime
import os

PATH = '/Users/nick0o0o0/Library/Mobile Documents/com~apple~CloudDocs/gxyfile/Trading/Stocks_selection/data'
PATH2 = '/Users/nick0o0o0/Library/Mobile Documents/com~apple~CloudDocs/gxyfile/Trading/Stocks_selection/report'
CURRENT_MONTH = datetime.now().strftime('%Y-%m')

def clean_quarterly_fundamental(Ticker:str, current_month:str=CURRENT_MONTH)->pd.DataFrame:
    """
    current_month: str, ex :2001-12format
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

    merge_df['fiscalDateEnding'] = pd.to_datetime(merge_df['fiscalDateEnding'])
    merge_df = merge_df.sort_values(by='fiscalDateEnding', ascending=False)
    merge_df['quarter'] = merge_df['fiscalDateEnding'].dt.to_period('Q').astype(str).str.replace(' ', '')

    merge_df['reportedEPS'] = pd.to_numeric(merge_df['reportedEPS'], errors='coerce').fillna(0).astype(float)
    merge_df['estimatedEPS'] = pd.to_numeric(merge_df['estimatedEPS'], errors='coerce').fillna(0).astype(float)
    merge_df['surprise'] = pd.to_numeric(merge_df['surprise'], errors='coerce').fillna(0).astype(float)
    merge_df['totalRevenue'] = pd.to_numeric(merge_df['totalRevenue'], errors='coerce').fillna(0).astype(float)
    merge_df['netIncome'] = pd.to_numeric(merge_df['netIncome'], errors='coerce').fillna(0).astype(float)

    # add percentage change of EPS
    merge_df['EPS_YOY_pct_change'] = merge_df['reportedEPS'].pct_change(periods=4).replace(0, 1)
    # add percentage change of revenue
    merge_df['revenue_YOY_pct_change'] = merge_df['totalRevenue'].pct_change(periods=4).replace(0, 1)
    # add percentage change of net income
    merge_df['netIncome_YOY_pct_change'] = merge_df['netIncome'].pct_change(periods=4).replace(0, 1)
    # add net profit margin
    merge_df['netProfitMargin'] = merge_df['netIncome'] / merge_df['totalRevenue']
    # add percentage change of net profit margin
    merge_df['netProfitMargin_YOY_pct_change'] = merge_df['netProfitMargin'].pct_change(periods=4).replace(0, 1)

    return merge_df, merge_df[important_columns]

def generate_fundamental(Ticker:str, current_month:str=CURRENT_MONTH)->pd.DataFrame:
    data_file_name = f'{Ticker}_quarter_income.csv'
    if data_file_name not in os.listdir(f'{PATH}/{current_month}'):
        print(f'{data_file_name} not found in {PATH}/{current_month}')
        return None
    else:
        df1 = clean_quarterly_fundamental(Ticker, current_month)[0]
        df2 = clean_quarterly_fundamental(Ticker, current_month)[1]

        if not os.path.exists(f'{PATH2}/{current_month}'):
            os.makedirs(f'{PATH2}/{current_month}', exist_ok=True)
        df1.to_csv(f'{PATH2}/{current_month}/{Ticker}_bigfundamental.csv', index=False)
        df2.to_csv(f'{PATH2}/{current_month}/{Ticker}_smallfundamental.csv', index=False)
        return df1, df2
    

#example
example = generate_fundamental('HROW')
example[1]