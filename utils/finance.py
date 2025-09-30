# utils/finance.py
import yfinance as yf
import pandas as pd

def get_stock_price(ticker: str):
    """
    Fetch the latest stock price and daily % change for the given ticker.
    """
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period="2d")  # last 2 days for comparison
        if hist.empty:
            return None, None
        latest = hist['Close'].iloc[-1]
        prev = hist['Close'].iloc[-2] if len(hist) > 1 else latest
        pct_change = ((latest - prev) / prev) * 100 if prev else 0
        return round(latest, 2), round(pct_change, 2)
    except Exception as e:
        print(f"Finance fetch error: {e}")
        return None, None

def get_stock_history(ticker: str, period="7d", interval="1h"):
    """
    Fetch historical stock prices for plotting.
    """
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period=period, interval=interval)
        return hist.reset_index()[["Datetime", "Close"]]
    except Exception as e:
        print(f"Finance history error: {e}")
        return pd.DataFrame()
