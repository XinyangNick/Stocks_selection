

def get_quarterly_fundamental(Ticker:str, time:str='Q')->pd.DataFrame:
    """
    return the quarterly fundamental of the stock by
    """
    df = pd.DataFrame()
    income_sts_df = get_income_statement(Ticker, time)
    EPS_df = get_EPS(Ticker, time)
    merge_df = pd.merge(income_sts_df, EPS_df, how='outer', on='fiscalDateEnding')
    # merge_df['fiscalDateEnding'] = merge_df['fiscalDateEnding'].astype('datetime64')
    # merge_df['quarter'] = merge_df['fiscalDateEnding'].dt.quarter

    merge_df['fiscalDateEnding'] = pd.to_datetime(merge_df['fiscalDateEnding'])
    merge_df['reportedEPS'] = pd.to_numeric(merge_df['reportedEPS'], errors='coerce').fillna(0).astype(float)
    merge_df['estimatedEPS'] = pd.to_numeric(merge_df['estimatedEPS'], errors='coerce').fillna(0).astype(float)
    merge_df['surprise'] = pd.to_numeric(merge_df['surprise'], errors='coerce').fillna(0).astype(float)
    merge_df['totalRevenue'] = pd.to_numeric(merge_df['totalRevenue'], errors='coerce').fillna(0).astype(float)
    merge_df['netIncome'] = pd.to_numeric(merge_df['netIncome'], errors='coerce').fillna(0).astype(float)

    df = pd.concat([df, merge_df['fiscalDateEnding']], axis=1)
    df = pd.concat([df, merge_df['reportedEPS']], axis=1)
    # add percentage change of EPS
    df['EPS_pct_change'] = (df['reportedEPS'] - df['reportedEPS'].shift(1)) / df['reportedEPS'].shift(1).replace(0, 1)
    df = pd.concat([df, merge_df['estimatedEPS']], axis=1)
    df = pd.concat([df, merge_df['surprise']], axis=1)
    # add percentage change of revenue
    df = pd.concat([df, merge_df['totalRevenue']], axis=1)
    df['revenue_pct_change'] = (df['totalRevenue'] - df['totalRevenue'].shift(1)) / df['totalRevenue'].shift(1).replace(0, 1)
    # add percentage change of net margin
    df = pd.concat([df, merge_df['netIncome']], axis=1)
    df['netIncome_pct_change'] = (df['netIncome'] - df['netIncome'].shift(1)) / df['netIncome'].shift(1).replace(0, 1)
    # add percentage change of Net Profit Margin
    df['netProfitMargin'] = df['netIncome'] / df['totalRevenue']
    df['netProfitMargin_pct_change'] = (df['netProfitMargin'] - df['netProfitMargin'].shift(1)) / df['netProfitMargin'].shift(1).replace(0, 1)

    return df