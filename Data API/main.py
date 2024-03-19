import subprocess

variables = ['BTC.py', 'Interests.py', 'SPY.py', 'Gold.py']

for filename in variables:
    subprocess.run(['python', filename])