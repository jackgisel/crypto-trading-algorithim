from discord import send_discord
import cbpro
import pandas as pd 
from datetime import datetime
from slack import send_message
from discord import send_discord

cb = cbpro.PublicClient()

def evaluate(ticker):
  data = cb.get_product_historic_rates(ticker, granularity=3600)
  dates = []
  if len(data) < 200:
    return
  for d in data:
    dates.append(datetime.fromtimestamp(d[0]))
  df = pd.DataFrame(data, index=dates, columns=['time', 'low', 'high', 'open', 'close', 'volume'])
  df['MA200'] = df['close'].rolling(window=200).mean()
  df['price change'] = df['close'].pct_change()
  df['Upmove'] = df['price change'].apply(lambda x: x if x > 0 else 0)
  df['Downmove'] = df['price change'].apply(lambda x: abs(x) if x < 0 else 0)
  df['avg Up'] = df['Upmove'].ewm(span=19).mean()
  df['avg Down'] = df['Downmove'].ewm(span=19).mean()
  df = df.dropna()
  df['RS'] = df['avg Up']/df['avg Down']
  df['RSI'] = df['RS'].apply(lambda x: 100-(100/(x+1)))
  df.loc[(df['close'] > df['MA200']) & (df['RSI'] < 30), 'Buy'] = 'Yes'
  df.loc[(df['close'] < df['MA200']) | (df['RSI'] > 30), 'Buy'] = 'No'
  df.sort_values(by=['time'])
  if df['Buy'].iloc[0] == "Yes":
    return ticker

def check_products():
  products = cb.get_products()
  currencies = []
  buys = []
  for prod in products:
    if '-USD' in prod['id']:
      if '-USDC' not in prod['id']:
        currencies.append(prod['id'])
  for i in currencies:
    buys.append(evaluate(i))

print(check_products())
