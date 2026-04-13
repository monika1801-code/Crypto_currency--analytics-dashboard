#import required data
from data_loader import all_data

#change coin here anytime to get the candlestick plot for that coin
coin = 'bitcoin' 
data = all_data[coin]
#print(all_data.keys())

# To generate a candlestick plot, get the data for the open(first price of the day), high(max price of the day), low(min price of the day), and close(last price of the day) for the last 30 days.
candlestick_data = data.groupby(data.index.date).agg({'price': ['first', 'max', 'min', 'last']})

# use plotly to create a candlestick plot
import plotly.graph_objects as go
import plotly.offline as pyo

fig = go.Figure(data=[go.Candlestick(
                x=candlestick_data.index,
                open=candlestick_data['price']['first'],
                high=candlestick_data['price']['max'],
                low=candlestick_data['price']['min'],
                close=candlestick_data['price']['last']
)])

fig.update_layout(
    xaxis_rangeslider_visible=False, 
    xaxis_title='Date', 
    yaxis_title='Price (USD)', 
    title=f'{coin} Price Candlestick Chart over past 30 days'
)

pyo.plot(fig, filename=f'{coin}_chart.html', auto_open=True)