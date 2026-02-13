
import yfinance as yf

def main(): 
  print("quant-momentum-backtest initialized") 
  tickers = ["SPY", "TLT"]
  start_date = "2010-01-01"

  data = yf.download(tickers, start = start_date)
  print(data.tail())

if __name__ == "__main__":
  main()
