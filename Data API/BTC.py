import requests
import os
import pandas as pd
from key import api_key
from datetime import datetime, timedelta

symbol = "BTC"
url = f'https://www.alphavantage.co/query?function=DIGITAL_CURRENCY_DAILY&symbol={symbol}&market=USD&outputsize=full&apikey={api_key}'
r = requests.get(url)
data = r.json().get("Time Series (Digital Currency Daily)", {})

df_BTC = pd.DataFrame([
    {"date": date,
    "value": float(data[date]["4b. close (USD)"]),
    "volume": float(data[date]["5. volume"])}
    for date in data
])

df_BTC['date'] = pd.to_datetime(df_BTC['date'])

df_BTC = df_BTC.sort_values(by='date')
yesterday = datetime.now() - timedelta(days=1)
yesterday_str = yesterday.strftime('%Y-%m-%d')
filtered_df = df_BTC[df_BTC['date'] < yesterday_str]
all_dates = pd.date_range(start=filtered_df['date'].min(), end=yesterday, freq='D')
all_dates_df = pd.DataFrame({'date': all_dates})
merged_df = pd.merge(all_dates_df, df_BTC, on='date', how='left')
merged_df['value'] = merged_df['value'].fillna(method='ffill')
merged_df['volume'] = merged_df['volume'].fillna(method='ffill')

script_directory = os.path.dirname(os.path.abspath(__file__))
project_directory = os.path.dirname(script_directory)
output_file = os.path.join(project_directory, "Data CSV", "BTC.csv")
merged_df.to_csv(output_file, index=False)