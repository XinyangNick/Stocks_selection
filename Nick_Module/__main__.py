import graphing_function as gf
import selection_function as sf
import clean_data as cd

Ticker = 'IRMD'
print(sf.Stage2_Confirmed_Criteria(Ticker))
gf.graph_move_together(Ticker, time='1y')
cd.generate_fundamental(Ticker)