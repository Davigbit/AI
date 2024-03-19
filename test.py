import pandas as pd
from Data import df_after_2024 as df
import joblib
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt

model = joblib.load('ridge_model.pkl')

df_test = df.loc[:, df.columns != 'BTC (USD)']

model = joblib.load('ridge_model.pkl')

scaler = StandardScaler()
df_test_scaled = scaler.fit_transform(df_test)

Y_pred = model.predict(df_test_scaled)
Y_pred = pd.DataFrame(Y_pred, columns=['Predicted BTC (USD)'])

plt.figure(figsize=(10, 6))
plt.plot(df.index, Y_pred['Predicted BTC (USD)'], label='Predicted Bitcoin Value (USD)', marker='o')
plt.plot(df.index, df['BTC (USD)'], label='Bitcoin Value (USD)', marker='o')
plt.title('Predicted Bitcoin Value and Bitcoin Prices Over Time')
plt.xlabel('Date (yy-mm-dd)')
plt.ylabel('Price (USD)')
plt.legend()
plt.grid(True)
plt.show()