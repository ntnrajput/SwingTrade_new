# fetch the historical data for all stocks that are technically bullish
import os
import sys
import pandas as pd
import yfinance as yf
import stock_short_listed
import importlib

stock_short_listing = importlib.reload(stock_short_listed)


def fetch_stock_data():
    
    symbols = stock_short_listing.get_bullish_stocks()

    dfs = []
    problematic_stocks = []

    for symbol in symbols:
        try:
            data = yf.download(symbol, period="1y", interval="1d", progress=False)
            if data.empty:
                print(f"⚠️ No data found for {symbol}. Skipping...")
                problematic_stocks.append(symbol)
                continue

            if isinstance(data.columns, pd.MultiIndex):
                data.columns = data.columns.get_level_values(0)

            data.reset_index(inplace=True)
            data["Stock"] = symbol
            data = data[['Date', 'Stock', 'Open', 'High', 'Low', 'Close', 'Volume']]
            dfs.append(data)

        except Exception as e:
            print(f"⚠️ Error fetching {symbol}: {e}")
            problematic_stocks.append(symbol)

    if not dfs:
        print("❌ No valid data fetched.")
        return pd.DataFrame()

    final_df = pd.concat(dfs, ignore_index=True)
    final_df = final_df.sort_values(by=['Stock', 'Date']).reset_index(drop=True)

    print(f"\n✅ Code 2: Successfully fetched data for {len(symbols) - len(problematic_stocks)} stocks.")
    print(f"⚠️ from Code 2:  Problematic stocks: {problematic_stocks}")

    return final_df, symbols

if __name__ == "__main__":
    final_df = fetch_stock_data()

    
