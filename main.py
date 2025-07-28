import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

data = yf.download("SPY", start="2005-01-01", end="2025-06-30")
data["SMA"] = data['Close'].rolling(window=20).mean()
data = data[["Close", "SMA"]]
print(data.tail())
