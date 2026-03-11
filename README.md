# Mean Reversion Strategy

This is a simple trading strategy project where I test whether stock or ETF prices tend to revert back to their average over time.

The idea is that when prices move too far away from their recent mean, they may eventually move back toward it.

## What the strategy does

- Calculates a 20-day simple moving average (SMA)
- Measures the percentage deviation of price from the SMA
- Buys when price drops significantly below the average
- Sells when price moves significantly above the average
- Signals are shifted by one day to avoid look-ahead bias

## Performance evaluation

The strategy is compared to a simple buy-and-hold benchmark.

Metrics included in the analysis:

- Total return
- Sharpe ratio
- Maximum drawdown
- Number of trades
- Win rate

Transaction costs are also included in the strategy returns.

## Data

Market data is downloaded using **yfinance**.

Example assets tested:
- SPY
- QQQ
- IWM
- DIA
- EFA
- TLT

Data period:
2005 – 2025

## Tools

- Python
- pandas
- numpy
- matplotlib
- yfinance

## Status

Work in progress.  
Future improvements may include parameter testing, better signal rules, and more realistic backtesting assumptions.
