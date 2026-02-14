import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt 

def main():
    print("quant-momentum-backtest initialized")

    tickers = ["SPY", "TLT"]
    start_date = "2010-01-01"

    df = yf.download(tickers, start=start_date)
    prices = df["Close"]

    monthly_prices = prices.resample("ME").last().dropna(how="all")
    monthly_returns = monthly_prices.pct_change()
    momentum = monthly_prices.pct_change(3)

    signal = momentum.apply(
        lambda row: row.idxmax() if row.notna().any() else np.nan,
        axis=1
    ).shift(1)

    strategy_returns = pd.Series(index=monthly_returns.index, dtype=float)
    for date in monthly_returns.index:
        asset = signal.loc[date]
        if pd.notna(asset):
            strategy_returns.loc[date] = monthly_returns.loc[date, asset]

    cumulative_strategy = (1 + strategy_returns.fillna(0)).cumprod()
    cumulative_spy = (1 + monthly_returns["SPY"].fillna(0)).cumprod()

    sharpe = (strategy_returns.mean() / strategy_returns.std()) * np.sqrt(12)
    cum_max = cumulative_strategy.cummax()
    drawdown = cumulative_strategy / cum_max - 1
    mdd = drawdown.min()

    print("Sharpe Ratio:", round(sharpe, 3))
    print("Maximum Drawdown:", round(mdd, 3))
    
    plt.figure(figsize=(10,6))
    plt.plot(cumulative_strategy, label="Momentum Strategy")
    plt.plot(cumulative_spy, label="SPY Buy & Hold")
    plt.legend()
    plt.title("Momentum Rotation Backtest")
    plt.tight_layout()
    plt.savefig("momentum_backtest.png", dpi=300)
    plt.show()

if __name__ == "__main__":
    main()
