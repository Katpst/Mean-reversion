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

# Transaction cost assumption
cost_per_trade = 0.001 #0.1% per trade
data["Trade"] = data["Shifted_direction"].diff().abs()
data["Trade"] = data["Trade"].fillna(0)

data["SMA_return"] = data["Return"] * data["Shifted_direction"]
data["SMA_return_after_cost"] = data["SMA_return"] - (data["Trade"] * cost_per_trade)

data.dropna(inplace=True)

data["Buy_Hold"] = (1 + data["Return"]).cumprod() #% return from Buy & Hold
data["SMA_strategy"] = (1 + data["SMA_return_after_cost"]).cumprod() #% return from SMA strategy

print("Buy & Hold return: {:.2f}%".format((data["Buy_Hold"].iloc[-1] - 1) * 100))
print("SMA Strategy return: {:.2f}%".format((data["SMA_strategy"].iloc[-1] - 1) * 100))

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
    data["SMA_return_after_cost"].mean() / data["SMA_return_after_cost"].std()
) * (trading_days**0.5)

buyhold_sharpe = (
    data["Return"].mean() / data["Return"].std()
) * (trading_days**0.5)

print("Buy & Hold Sharpe ratio: {:.2f}".format(buyhold_sharpe))
print("Strategy Sharpe ratio: {:.2f}".format(strategy_sharpe))

# Max drawdown
data["BuyHoldPeak"] = data["Buy_Hold"].cummax()
data["StrategyPeak"] = data["SMA_strategy"].cummax()

max_dd_buyhold = ((data["Buy_Hold"] - data["BuyHoldPeak"]) / data["BuyHoldPeak"]).min()
max_dd_strategy = ((data["SMA_strategy"] - data["StrategyPeak"]) / data["StrategyPeak"]).min()

print("Buy & Hold max drawdown: {:.2f}%".format(max_dd_buyhold * 100))
print("Strategy max drawdown: {:.2f}%".format(max_dd_strategy * 100))

# Trade statistics
number_of_trades = (data["Trade"] > 0).sum()
winning_days = (data["SMA_return_after_cost"] > 0).sum()
total_trading_days = (data["Shifted_direction"] != 0).sum()

if total_trading_days > 0:
    win_rate = winning_days / total_trading_days * 100
else:
    win_rate = 0

print("Number of trades: {}".format(number_of_trades))
print("Win rate: {:.2f}%".format(win_rate))
