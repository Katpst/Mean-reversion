import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

etfs = ["SPY", "QQQ", "IWM", "DIA", "EFA", "TLT"]
results = []

for ticker in etfs:
    print("Processing {ticker}")
    
    # Download data
    yf_data = yf.download(ticker, start="2005-01-01", end="2025-06-30")
    data = pd.DataFrame()
    data["Close"] = yf_data["Close"]
    data["SMA"] = data["Close"].rolling(window=20).mean()
    data["Deviation"] = (data["Close"] - data["SMA"]) / data["SMA"] * 100

    data["Direction"] = 0
    data.loc[data["Deviation"] < -3, "Direction"] = 1
    data.loc[data["Deviation"] > 3, "Direction"] = -1
    data["Shifted_direction"] = data["Direction"].shift(1)

    data["Return"] = data["Close"].pct_change()
    data["SMA_return"] = data["Return"] * data["Shifted_direction"]

    data.dropna(inplace=True)

    # Cumulative returns
    data["Buy_Hold"] = (1 + data["Return"]).cumprod()
    data["SMA_strategy"] = (1 + data["SMA_return"]).cumprod()

    # Sharpe ratio
    trading_days = 252
    sharpe_buy = (data["Return"].mean() / data["Return"].std()) * (trading_days**0.5)
    sharpe_strategy = (data["SMA_return"].mean() / data["SMA_return"].std()) * (trading_days**0.5)

    # Max drawdown
    data["BuyHoldPeak"] = data["Buy_Hold"].cummax()
    data["StrategyPeak"] = data["SMA_strategy"].cummax()
    max_dd_buyhold = ((data["Buy_Hold"] - data["BuyHoldPeak"]) / data["BuyHoldPeak"]).min()
    max_dd_strategy = ((data["SMA_strategy"] - data["StrategyPeak"]) / data["StrategyPeak"]).min()

    # Save results
    results.append({
        "Ticker": ticker,
        "Buy & Hold return (%)": (data["Buy_Hold"].iloc[-1] - 1) * 100,
        "Strategy return (%)": (data["SMA_strategy"].iloc[-1] - 1) * 100,
        "Buy & Hold sharpe": sharpe_buy,
        "Strategy sharpe": sharpe_strategy,
        "Buy & Hold max drawdown (%)": max_dd_buyhold * 100,
        "Strategy max drawdown (%)": max_dd_strategy * 100,
    })
summary_df = pd.DataFrame(results)
print("Strategy Summary:")
print(summary_df)
