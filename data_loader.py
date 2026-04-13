# import pandas and CoinGeckoAPI
from pycoingecko import CoinGeckoAPI
import pandas as pd

# create a client object cg
cg = CoinGeckoAPI()


coins = ['bitcoin', 'ethereum', 'solana']

all_data = {}

for coin in coins:
    # use function get_coin_market_chart_by_id to get the market data for bitcoin in the last 30 days
    coin_data = cg.get_coin_market_chart_by_id(
        id = coin,
        vs_currency='usd',
        days=30
    )

    # as the price data is required for the analysis, we will convert the price data into a pandas dataframe
    data = pd.DataFrame(coin_data['prices'], columns=['timestamp', 'price'])

    # convert the timestamp to datetime format and set it as the index of the dataframe
    data['Date'] = pd.to_datetime(data['timestamp'], unit='ms')
    data.set_index('Date', inplace=True)
    data.drop('timestamp', axis=1, inplace=True)

    # store the dataframe in the all_data dictionary with the coin name as the key
    all_data[coin] = data

print(all_data['bitcoin'].head())
    




