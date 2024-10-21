from Nick_Module import graphing_function as gf
from Nick_Module import selection_function as sf
from Nick_Module import clean_data as cd
from Nick_Module import api_fundamental_function as aff

# selection_function
"""
DEFULT_START_DATE = '2000-01-01'
CURRENT_DATE = pd.Timestamp.now().strftime('%Y-%m-%d')

Stage2_Confirmed_Criteria(Stage2_Confirmed_Criteria(Ticker:str, 
                              Benchmark:str=None, 
                              MA200UP:int=30, 
                              LOW52UP:int=30,
                              RS_score:int=70)->tuple:)
This function is used to determine if a stock has met the criteria for a Stage 2 Confirmed uptrend.

Regression_Analysis(Ticker:str, 
                    Benchmark:str='^GSPC', 
                    Risk_free:str='^TNX', 
                    period:str='max',
                    start_date:str=None, 
                    end_date:str=None, 
                    n:int=1):
This function is used to perform a regression analysis on a stock.
"""
#api_fundamental_function
"""
API = '2ID6DFGA46EO9NEI'
PATH = '/Users/nick0o0o0/Library/Mobile Documents/com~apple~CloudDocs/gxyfile/Trading/Stocks_selection'

def save_raw(Ticker:str, path:str=PATH, api:str=API):
This function is used to save the raw data of a stock to a csv file.
"""
#clean_data
"""
PATH = '/Users/nick0o0o0/Library/Mobile Documents/com~apple~CloudDocs/gxyfile/Trading/Stocks_selection/data'
PATH2 = '/Users/nick0o0o0/Library/Mobile Documents/com~apple~CloudDocs/gxyfile/Trading/Stocks_selection'
CURRENT_MONTH = datetime.now().strftime('%Y-%m')

generate_fundamental(Ticker:str, current_month:str=CURRENT_MONTH, n:int=-4)->pd.DataFrame:
This function is used to generate the fundamental data of a stock.(It needs save_raw() to be run first)
"""
#graphing_function
"""
graph_move_together(Ticker: str, benchmark: str='^GSPC', time: str = '5y')
Plots stock, industy, benchmark graphs together with the same height using Plotly.
"""
GUIDANCE = ("""
1.sf.Stage2_Confirmed_Criteria(Stage2_Confirmed_Criteria(Ticker:str, 
                              Benchmark:str=None, 
                              MA200UP:int=30, 
                              LOW52UP:int=30,
                              RS_score:int=70)->tuple:)\n
2.sf.Regression_Analysis(Ticker:str, 
                    Benchmark:str='^GSPC', 
                    Risk_free:str='^TNX', 
                    period:str='max',
                    start_date:str=None, 
                    end_date:str=None, 
                    n:int=1)\n
3.aff.save_raw(Ticker:str, path:str=PATH, api:str=API)\n
4.cd.generate_fundamental(Ticker:str, current_month:str=CURRENT_MONTH, n:int=-4)->pd.DataFrame:\n
5.gf.graph_move_together(Ticker: str, benchmark: str='^GSPC', time: str = '5y')\n
""")
Ticker = input('Enter the ticker: ')
Choice = input(f"""
Current Ticker: {Ticker}\n
1. Stage2_Confirmed_Criteria\n
2. Regression_Analysis\n
3. save_raw\n
4. generate_fundamental\n
5. graph_move_together\n
6. Re-enter the ticker\n
7. Guidance\n
8. Exit\n
Enter the number of the function you want to run: """)
while Choice != '':
    if Choice == '1':
        print(sf.Stage2_Confirmed_Criteria(Ticker))
    elif Choice == '2':
        print(sf.Regression_Analysis(Ticker))
    elif Choice == '3':
        confirm = input(f'Are you sure to get the raw data of {Ticker}? \n(y/n):')
        if confirm == 'y':
            aff.save_raw(Ticker)
    elif Choice == '4':
        cd.generate_fundamental(Ticker)
    elif Choice == '5':
        gf.graph_move_together(Ticker)
    elif Choice == '6':
        Ticker = input('Enter the ticker: ')
    elif Choice == '7':
        print(GUIDANCE)
    elif Choice == '8':
        print('Nick is a genius')
        break
    else:
        print('Invalid choice')
        
    Choice = input(f"""
Current Ticker: {Ticker}\n
1. Stage2_Confirmed_Criteria\n
2. Regression_Analysis\n
3. save_raw\n
4. generate_fundamental\n
5. graph_move_together\n
6. Re-enter the ticker\n
7. Guidance\n
8. Exit\n
Enter the number of the function you want to run: """)


# Ticker = 'TXRH'
# print(sf.Stage2_Confirmed_Criteria(Ticker))
# gf.graph_move_together(Ticker, time='1y')
# cd.generate_fundamental(Ticker)