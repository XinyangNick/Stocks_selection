import pandas as pd
import yfinance as yf
import os
import sys
sys.path.append('/Users/nick0o0o0/Library/Mobile Documents/com~apple~CloudDocs/gxyfile/Trading/Stocks_selection/Nick_Module')
from Nick_Module import selection_function as sf
from Nick_Module import back_test as bt


#Can be reused:
os.chdir('/Users/nick0o0o0/Library/Mobile Documents/com~apple~CloudDocs/gxyfile/Trading')
PATH = '/Users/nick0o0o0/Library/Mobile Documents/com~apple~CloudDocs/gxyfile/Trading/BackTestData/small2015_2023.csv'

df = pd.read_csv(PATH)
df.rename(columns={'PRC': 'Close'}, inplace=True)

company_id = df['PERMNO'].unique()
banchmark = pd.read_csv('/Users/nick0o0o0/Library/Mobile Documents/com~apple~CloudDocs/gxyfile/Trading/BackTestData/benchmark2015-2023.csv')
banchmark.reset_index(inplace=True)
banchmark.rename(columns={'Date': 'date'}, inplace=True)
small_benchmark = banchmark[['date', 'Adj Close']]
print(small_benchmark.head(3))


output_file = 'MACDandStage2.csv'
# Create folder if it doesn't exist
output_folder = 'CompanyIDs'
os.makedirs(output_folder, exist_ok=True)

output_path = os.path.join(output_folder, output_file)
#Can be reused:

# Check if the file exists
if not os.path.exists(output_path):
    # Create a DataFrame with company_id and a new column with zeros
    company_df = pd.DataFrame(company_id, columns=['PERMNO'])
    company_df['Tested'] = 0 #is it tested?
    company_df['Returns'] = 0 #returns

    # Save the DataFrame to a CSV file
    company_df.to_csv(output_path, index=False)
else:
    # Read the existing CSV file
    company_df = pd.read_csv(output_path)


initial_cash = 10000

for ID, group in df.groupby('PERMNO'):
    if company_df.loc[company_df['PERMNO'] == ID, 'Tested'].values[0] == 1:
        continue
    ticker = group['TICKER'].iloc[0]  # Get the ticker for the current group

    merged_df = pd.merge(group, small_benchmark, on='date', how='left')
    print(merged_df.head(3))  # Display the first 3 rows of the merged DataFrame
    merged_df['Stage2'] = 0  # Add a new column with zeros
    merged_df = bt.calculate_macd(merged_df)  # Calculate MACD
    
    position = 0  # Number of shares held
    merged_df['Cash'] = initial_cash
    merged_df['Position'] = 0
    merged_df['Balance'] = initial_cash
    
    stage2_days = 0  # Counter for Stage 2 days
    for i in range(merged_df.shape[0]):
        temp_df = merged_df.iloc[:i]
        
        try:
            if sf.Stage2_DF_Criteria(temp_df, temp_df)[0]:  # Check criteria
                merged_df.at[i, 'Stage2'] = 1 # Update the 'Stage2' column
                stage2_days += 1
        except Exception as e:
            print(f"Error at index {i}: {e}")
            continue
        finally:
            if i == 0:
                continue  # Skip the first row
            cash = merged_df.at[i-1, 'Cash']  # Update cash from the previous row
            position = merged_df.at[i-1, 'Position'] # Update position from the previous row

            if merged_df.at[i, 'Stage2'] == 1:
                if (merged_df['MACD'].iloc[i] > 0 and merged_df['MACD'].iloc[i-1] <= 0):
                    # Buy signal
                    if cash > 0:
                        position = cash // merged_df['Close'].iloc[i]
                        cash = cash - position * merged_df['Close'].iloc[i]
                elif merged_df['MACD'].iloc[i] < 0 and merged_df['MACD'].iloc[i-1] >= 0:
                    # Sell signal
                    if position > 0:
                        cash = cash + position * merged_df['Close'].iloc[i]
                        position = 0
            else:
                # If not in Stage 2, do not trade
                cash = cash + position * merged_df['Close'].iloc[i]
                position = 0

            # Calculate balance
            balance = cash + position * df['Close'].iloc[i]
            if pd.isna(balance):
                balance = merged_df.at[i-1, 'Balance']
            if balance < 0:
                merged_df.at[i, 'Balance'] = balance
                break  # Stop the backtest if balance is negative

            # Record the values
            merged_df.at[i, 'Cash'] = cash
            merged_df.at[i, 'Position'] = position
            merged_df.at[i, 'Balance'] = balance
    returns = (merged_df['Balance'].iloc[-1] - initial_cash) / initial_cash * 100  # Calculate returns

    merged_df.to_csv(f'Strategy_Results/{ID}{ticker}.csv', index=False)

    # Update the company_df with the returns
    company_df.loc[company_df['PERMNO'] == ID, 'Tested'] = 1
    company_df.loc[company_df['PERMNO'] == ID, 'Returns'] = returns

    # Save the updated company_df to the output file
    company_df.to_csv(output_path, index=False)

        
    print(ID, ticker, returns)  # Print the results for each company
    break
    






