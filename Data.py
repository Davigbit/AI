import os
import pandas as pd

files = ['BTC.csv', 'Interests.csv', 'S&P 500.csv', 'Gold.csv']

dfs = {}

for file in files:
    df_name = f'df_{file.replace(" ", "_").replace(".", "_")}'
    dfs[df_name] = pd.read_csv(os.path.join('./Data CSV/', file), parse_dates=['date'])
    dfs[df_name] = dfs[df_name].sort_values(by='date', ascending=False)
    dfs[df_name] = dfs[df_name][dfs[df_name]['date'] >= '2021-06-24']

for key, df in dfs.items():
    if key != 'df_BTC_csv':
        df['value'] = df['value'].shift(-1)

dfs['df_BTC_csv']['volume'] = dfs['df_BTC_csv']['volume'].shift(-1)

for key, df in dfs.items():
    dfs[key] = df.reset_index(drop=True)

dfs['df_BTC_csv'] = dfs['df_BTC_csv'].rename(columns={'date': 'Date', 'value': 'BTC (USD)', 'volume': 'BTC Volume'})
dfs['df_Interests_csv'] = dfs['df_Interests_csv'].rename(columns={'value': 'Interest Rate (%)'})
dfs['df_S&P_500_csv'] = dfs['df_S&P_500_csv'].rename(columns={'value': 'S&P 500 (USD)'})
dfs['df_Gold_csv'] = dfs['df_Gold_csv'].rename(columns={'value': 'Gold (USD)'})

result_df = pd.concat([dfs['df_BTC_csv']['Date'], dfs['df_BTC_csv']['BTC (USD)'], dfs['df_BTC_csv']['BTC Volume'], 
                       dfs['df_Interests_csv']['Interest Rate (%)'], dfs['df_S&P_500_csv']['S&P 500 (USD)'], dfs['df_Gold_csv']['Gold (USD)']], axis=1)

result_df = result_df.dropna()

latest_date = result_df['Date'].max()

df_before_2024 = result_df.loc[result_df['Date'] <= '2024-03-01']
df_after_2024 = result_df.loc[result_df['Date'] > '2024-03-01']

df_before_2024.set_index('Date', inplace=True)
df_after_2024.set_index('Date', inplace=True)