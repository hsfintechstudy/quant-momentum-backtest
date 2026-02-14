import pandas as pd
import numpy as np
import yfinance as yf

def main():
    print("quant-momentum-backtest initialized")

    tickers = ["SPY", "TLT"]
    start_date = "2010-01-01"

    df = yf.download(tickers, start=start_date)
    prices = df["Close"]

    monthly_prices = prices.resample("ME").last().dropna(how="all")

    momentum = monthly_prices.pct_change(3)

    signal = momentum.apply(
        lambda row: row.idxmax() if row.notna().any() else np.nan,
        axis=1
    ).shift(1)

    print(signal.tail(12))

if __name__ == "__main__":
    main()
