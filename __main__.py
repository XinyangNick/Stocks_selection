from Nick_Module import graphing_function, selection_function, clean_data as gf, sf, cd

Ticker = 'TXRH'
print(sf.Stage2_Confirmed_Criteria(Ticker))
gf.graph_move_together(Ticker, time='1y')
cd.generate_fundamental(Ticker)