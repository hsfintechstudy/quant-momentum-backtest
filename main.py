
import pandas as pd
import yfinance as yf

def main(): 
  print("quant-momentum-backtest initialized") 
  tickers = ["SPY", "TLT"]
  start_date = "2010-01-01"

  prices = yf.download(tickers, start = start_date)["Adj Close"]
  monthly_prices = prices.resample("M").last()

  momentum = monthly_prices.pct_change(3)
  signal = momentum.idxmax(axis=1).shift(1)
  
  print(signal.tail(12))

if __name__ == "__main__":
  main()
