from sklearn.preprocessing import StandardScaler
import subprocess
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_percentage_error
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import r2_score
from sklearn.linear_model import Ridge
from sklearn.model_selection import GridSearchCV
import joblib

subprocess.run(['python', 'Data.py'])

from Data import df_before_2024 as df

X = df.drop('BTC (USD)', axis=1)
Y = df['BTC (USD)'].astype(int)

X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

alphas = np.logspace(-3, 3, 2000)
param_grid = {'alpha': alphas}

grid_search = GridSearchCV(Ridge(), param_grid, cv=5)
grid_search.fit(X_train_scaled, Y_train)

best_alpha = grid_search.best_params_['alpha']

ridge_model = Ridge(alpha=best_alpha)
ridge_model.fit(X_train_scaled, Y_train)

Y_pred = ridge_model.predict(X_test_scaled)

print(f'Mean Absolute Percentage Error: {mean_absolute_percentage_error(Y_test, Y_pred):.3f}%')
print(f'Mean Absolute Error: {mean_absolute_error(Y_test, Y_pred):.3f}')
print(f'R2 Score: {r2_score(Y_test, Y_pred):.3f}')

joblib.dump(ridge_model, 'ridge_model.pkl')