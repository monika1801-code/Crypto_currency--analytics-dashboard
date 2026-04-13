#import required libraries and import the data from data_loader.py
import streamlit as st
import plotly.graph_objects as go
from data_loader import all_data

# Set the title of the app
st.title("Cryptocurrency Dashboard")
st.write("Select a cryptocurrency from the dropdown menu to view its price candlestick chart over the past 30 days.")

# To create a dropdown menu to select the cryptocurrency, we will use the selectbox function from streamlit. The options for the dropdown will be the keys of the all_data dictionary, which are the names of the cryptocurrencies.
coin = st.selectbox(
    "select a cryptocurrency",
    list(all_data.keys())
)

days = st.selectbox(
    "select the number of days to view the data",
    [7, 14, 30], index=2
)

# Get the data for the selected cryptocurrency
data = all_data[coin].copy()

# Get the data for the selected number of days.
data = data.last(f"{days}D")

# To calculate the 7-day moving average, we will use the rolling function from pandas. We will create a new column in the data dataframe called 'MA_7' which will contain the 7-day moving average of the price.
data['MA_7'] = data['price'].rolling(window=7).mean()

# metric to show the current price, highest price, and lowest price of the selected cryptocurrency in the last 30 days
current_price = all_data[coin]['price'].iloc[-1]
highest_price = data['price'].max()
lowest_price = data['price'].min()

col1, col2, col3 = st.columns(3)

col1.metric("Current Price (USD)", f"${current_price:.2f}")
col2.metric("Highest Price (USD)", f"${highest_price:.2f}")
col3.metric("Lowest Price (USD)", f"${lowest_price:.2f}")


# To generate a candlestick plot, get the data for the open(first price of the day), high(max price of the day), low(min price of the day), and close(last price of the day) for the last 30 days.
candlestick_data = data.groupby(data.index.date).agg({'price': ['first', 'max', 'min', 'last']})

# To calculate the daily moving average, we will group the data by date and calculate the mean of the 'MA_7' column for each day.
ma_daily = data.groupby(data.index.date)['MA_7'].mean()

# use plotly to create a candlestick plot and define the layout of the plot
fig = go.Figure()

# use plotly to create a candlestick plot and define the layout of the plot
fig.add_trace(go.Candlestick(
    x = candlestick_data.index,
    open = candlestick_data['price']['first'],
    high = candlestick_data['price']['max'],
    low = candlestick_data['price']['min'],
    close = candlestick_data['price']['last'],
    name = 'Candlestick'
))

# Add a line trace for the 7-day moving average
fig.add_trace(go.Scatter(
    x = ma_daily.index,
    y = ma_daily.values,
    mode = 'lines',
    name = '7-day Moving Average',
    line = dict(color='blue', width=2)
))

# Update the layout of the plot to add titles and labels
fig.update_layout(
    xaxis_rangeslider_visible=False, 
    xaxis_title='Date', 
    yaxis_title='Price (USD)', 
    title=f'{coin.capitalize()} Price Chart - over last {days} days'
)

# Display the plot in the streamlit app
st.plotly_chart(fig, use_container_width=True)

# To display price line chart
st.subheader("Price Trend")

line_fig = go.Figure()

line_fig.add_trace(go.Scatter(
    x = data.index,
    y = data['price'],
    mode = 'lines',
    name = 'price'
))

line_fig.add_trace(go.Scatter(
    x = data.index,
    y = data['MA_7'],
    mode = 'lines',
    name = "7-day Moving Average"
))

line_fig.update_layout(
    xaxis_title='Date', 
    yaxis_title='Price (USD)'  
)

st.plotly_chart(line_fig, use_container_width=True)