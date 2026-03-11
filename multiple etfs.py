import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

etfs = ["SPY", "QQQ", "IWM", "DIA", "EFA", "TLT"]
results = []

for ticker in etfs:
    print(f"Processing {ticker}")
    
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

    # Transaction cost assumption
    cost_per_trade = 0.001
    data["Trade"] = data["Shifted_direction"].diff().abs()
    data["Trade"] = data["Trade"].fillna(0)

    data["SMA_return"] = data["Return"] * data["Shifted_direction"]
    data["SMA_return_after_cost"] = data["SMA_return"] - (data["Trade"] * cost_per_trade)

    data.dropna(inplace=True)

    # Cumulative returns
    data["Buy_Hold"] = (1 + data["Return"]).cumprod()
    data["SMA_strategy"] = (1 + data["SMA_return_after_cost"]).cumprod()

    # Sharpe ratio
    trading_days = 252
    sharpe_buy = (data["Return"].mean() / data["Return"].std()) * (trading_days**0.5)
    sharpe_strategy = (data["SMA_return_after_cost"].mean() / data["SMA_return_after_cost"].std()) * (trading_days**0.5)

    # Max drawdown
    data["BuyHoldPeak"] = data["Buy_Hold"].cummax()
    data["StrategyPeak"] = data["SMA_strategy"].cummax()
    max_dd_buyhold = ((data["Buy_Hold"] - data["BuyHoldPeak"]) / data["BuyHoldPeak"]).min()
    max_dd_strategy = ((data["SMA_strategy"] - data["StrategyPeak"]) / data["StrategyPeak"]).min()

    # Trade statistics
    number_of_trades = (data["Trade"] > 0).sum()
    winning_days = (data["SMA_return_after_cost"] > 0).sum()
    total_trading_days = (data["Shifted_direction"] != 0).sum()

    if total_trading_days > 0:
        win_rate = winning_days / total_trading_days * 100
    else:
        win_rate = 0

    # Save results
    results.append({
        "Ticker": ticker,
        "Buy & Hold return (%)": (data["Buy_Hold"].iloc[-1] - 1) * 100,
        "Strategy return (%)": (data["SMA_strategy"].iloc[-1] - 1) * 100,
        "Buy & Hold sharpe": sharpe_buy,
        "Strategy sharpe": sharpe_strategy,
        "Buy & Hold max drawdown (%)": max_dd_buyhold * 100,
        "Strategy max drawdown (%)": max_dd_strategy * 100,
        "Number of trades": number_of_trades,
        "Win rate (%)": win_rate,
    })

summary_df = pd.DataFrame(results)
print("Strategy Summary:")
print(summary_df)
