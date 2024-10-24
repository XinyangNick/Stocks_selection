import pandas as pd
import yfinance as yf
import selection_function as sf
import os


START_DATE = '2018-01-01'
END_DATE = '2020-01-01'
#The path to the directory where the CSV files are stored
os.chdir('/Users/nick0o0o0/Library/Mobile Documents/com~apple~CloudDocs/gxyfile/Trading/BackTest')

# Read the list of tickers from a CSV file
Ticker_df = pd.read_csv('/Users/nick0o0o0/Library/Mobile Documents/com~apple~CloudDocs/gxyfile/Trading/Tickers.csv')
Big_tickers = Ticker_df['Symbol']

# Check if the Stage 2 Ticker list CSV file exists
if not os.path.exists(f'{END_DATE}Stage2.csv'):
    Ticker_list = []
else:
    # Read the existing tickers from the CSV file
    Ticker_list = pd.read_csv(f'{END_DATE}Stage2.csv')['Ticker'].tolist()

# Determine the starting index for processing remaining tickers
if Ticker_list:
    last_ticker = Ticker_list[-1]
    start_index = Big_tickers[Big_tickers == last_ticker].index[0] + 1
else:
    start_index = 0

# Get the list of remaining tickers to process
Remain_ticker = Big_tickers[start_index:]

# Check Stage 2 Confirm Criteria
counter = 0
for ticker in Remain_ticker:
    if counter >= 50:
        break
    try:
        result = sf.Stage2_Confirmed_Criteria(Ticker=ticker, start_date=START_DATE, end_date=END_DATE)
        print(result)
        if result[0]:
            Ticker_list.append(ticker)
    except:
        print(f"Error processing ticker {ticker}")
        continue
    finally:
        counter += 1

print(Ticker_list)


Ticker_list_df = pd.DataFrame(Ticker_list, columns=['Ticker'])
Ticker_list_df.to_csv(f'{END_DATE}Stage2.csv', index=False)