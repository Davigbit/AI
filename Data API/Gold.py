import requests
import os
import pandas as pd
from key import api_key_gold
from datetime import datetime, timedelta

start_date = datetime(2022, 1, 1)
end_date = datetime.now()

dates = []
values = []

for year in range(start_date.year, end_date.year + 1):
    year_start = datetime(year, 1, 1)
    year_end = datetime(year, 12, 31) if year < end_date.year else end_date
    url = f"https://api.metalpriceapi.com/v1/timeframe?api_key={api_key_gold}&start_date={year_start.strftime('%Y-%m-%d')}&end_date={year_end.strftime('%Y-%m-%d')}&base=USD&currencies=XAU"
    r = requests.get(url)
    data = r.json()
    for date, rate_data in data['rates'].items():
        dates.append(datetime.strptime(date, '%Y-%m-%d'))
        values.append(rate_data['XAU'])

df_G = pd.DataFrame({'date': dates, 'value': values})

df_G['date'] = pd.to_datetime(df_G['date'])

df_G = df_G.sort_values(by='date')
yesterday = datetime.now() - timedelta(days=1)
yesterday_str = yesterday.strftime('%Y-%m-%d')
filtered_df = df_G[df_G['date'] < yesterday_str]
all_dates = pd.date_range(start=filtered_df['date'].min(), end=yesterday, freq='D')
all_dates_df = pd.DataFrame({'date': all_dates})
merged_df = pd.merge(all_dates_df, df_G, on='date', how='left')
merged_df['value'] = merged_df['value'].fillna(method='ffill')

script_directory = os.path.dirname(os.path.abspath(__file__))
project_directory = os.path.dirname(script_directory)
output_file = os.path.join(project_directory, "Data CSV", "Gold.csv")
merged_df.to_csv(output_file, index=False)