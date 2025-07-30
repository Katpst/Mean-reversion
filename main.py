import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

yf_data = yf.download("SPY", start="2005-01-01", end="2025-06-30")
data = pd.DataFrame()
data["Close"] = yf_data["Close"]
data["SMA"] = data["Close"].rolling(window=20).mean() #Simple moving average 

data["Deviation"] = (data["Close"] - data["SMA"]) / data["SMA"] * 100 #% deviation from the SMA
data["Direction"] = 0
data.loc[data["Deviation"] < -3, "Direction"] = 1 #Buy
data.loc[data["Deviation"] > 3, "Direction"] = -1 #Sell
data["Shifted_direction"] = data["Direction"].shift(1) #Shift direction by 1 day to avoid lookahead bias

data["Return"] = data["Close"].pct_change()
data["SMA_return"] = data["Return"] * data["Shifted_direction"]

data["Buy_Hold"] = (1 + data["Return"]).cumprod() #% return from Buy & Hold
data["SMA_strategy"] = (1 + data["SMA_return"]).cumprod() #% return from SMA strategy

print("Buy & Hold return: {:.2f}%".format((data["Buy_Hold"].iloc[-1] - 1) * 100))
print("SMA Strategy return: {:.2f}%".format((data["SMA_strategy"].iloc[-1] - 1) * 100))

import matplotlib.pyplot as plt

plt.figure(figsize=(10, 4))
plt.plot(data.index, data["Buy_Hold"], label="Buy & Hold")
plt.plot(data.index, data["SMA_strategy"], label="Mean Reversion Strategy")
plt.title("SMA Strategy vs Buy & Hold Performance")
plt.xlabel("Date")
plt.ylabel("Return")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

#Sharpe ratios
trading_days = 252 #Trading days in a year

strategy_sharpe = (
    data["SMA_return"].mean() / data["SMA_return"].std()
) * (trading_days**0.5)

buyhold_sharpe = (
    data["Return"].mean() / data["Return"].std()
) * (trading_days**0.5)

print("Buy & Hold Sharpe ratio: {:.2f}".format(buyhold_sharpe))
print("Strategy Sharpe ratio: {:.2f}".format(strategy_sharpe))
