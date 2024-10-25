import pandas as pd
import yfinance as yf
import os
import sys
sys.path.append('/Users/nick0o0o0/Library/Mobile Documents/com~apple~CloudDocs/gxyfile/Trading/Stocks_selection/Nick_Module')
from Nick_Module import selection_function as sf
from Nick_Module import back_test as bt



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



# Create folder if it doesn't exist
output_folder = 'CompanyIDs'
os.makedirs(output_folder, exist_ok=True)

output_path = os.path.join(output_folder, 'company_results.csv')

# Check if the file exists
if not os.path.exists(output_path):
    # Create a DataFrame with company_id and a new column with zeros
    company_df = pd.DataFrame(company_id, columns=['PERMNO'])
    company_df['NewColumn'] = 0

    # Save the DataFrame to a CSV file
    company_df.to_csv(output_path, index=False)
else:
    # Read the existing CSV file
    company_df = pd.read_csv(output_path)



for ID, group in df.groupby('PERMNO'):
    merged_df = pd.merge(group, small_benchmark, on='date', how='left')
    print(merged_df.head(3))  # Display the first 3 rows of the merged DataFrame
    merged_df['Stage2'] = 0  # Add a new column with zeros
    merged_df = bt.calculate_macd(merged_df)  # Calculate MACD

    for i in range(merged_df.shape[0]):
        temp_df = merged_df.iloc[:i]
        try:
            if sf.Stage2_DF_Criteria(temp_df, temp_df)[0]:  # Check criteria
                merged_df.at[i, 'Stage2'] = 1 # Update the 'Stage2' column
        except Exception as e:
            print(f"Error at index {i}: {e}")
            continue 
        
    print(merged_df.head(1000))
    break
    








print(df.head(3))