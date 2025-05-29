import os
import sys
import pandas as pd
import numpy as np

# Import stock_short_listing notebook
import stock_data_fetch

# Reload to ensure latest changes
import importlib

# Define global parameters
WINDOW = 10
MIN_DIFF_PCT = 8
MIN_TOUCHES = 2

def identify_strong_reversal_points(df):
    if df is None or df.empty:
        return []

    if len(df) < 2 * WINDOW + 1:
        return []

    df = df.copy()
    df.reset_index(drop=True, inplace=True)

    if "Close" not in df.columns:
        return []

    # **Use rolling windows instead of loops**
    df['Swing_High'] = df['Close'][(df['Close'] == df['Close'].rolling(WINDOW * 2 + 1, center=True).max())]
    df['Swing_Low'] = df['Close'][(df['Close'] == df['Close'].rolling(WINDOW * 2 + 1, center=True).min())]

    # Combine highs & lows into "reversal points"
    reversal_points = pd.concat([df[['Swing_High']], df[['Swing_Low']]], axis=1).stack().values

    # Remove NaN values
    reversal_points = np.sort(reversal_points[~np.isnan(reversal_points)])

    # Merge close levels using vectorized NumPy operations
    if len(reversal_points) == 0:
        return []

    min_price, max_price = df['Close'].min(), df['Close'].max()
    price_range = max_price - min_price
    min_diff = (MIN_DIFF_PCT / 100) * price_range

    merged_levels = []
    count_touches = []

    for level in reversal_points[::-1]:  # Process latest to oldest
        if len(merged_levels) == 0 or abs(level - merged_levels[-1]) > min_diff:
            merged_levels.append(level)
            count_touches.append(1)
        else:
            count_touches[-1] += 1  # Increment touch count for existing level

    # Keep levels with at least 'MIN_TOUCHES'
    strong_levels = [round(merged_levels[i]) for i in range(len(merged_levels)) if count_touches[i] >= MIN_TOUCHES]
    return strong_levels

def calculate_support_resistance(df, symbol):
    
    df_symbol = df[df['Stock'] == symbol]

    if df_symbol.empty:
        return symbol, []

    levels = identify_strong_reversal_points(df_symbol)

    return symbol, levels

if __name__ == "__main__":
   
    df, symbols = stock_data_fetch.fetch_stock_data()

    if "Stock" not in df.columns:
        print("Error: Column 'Stock' not found in DataFrame")
        sys.exit(1)

    results = [calculate_support_resistance(df, symbol) for symbol in symbols]

    df_results = pd.DataFrame(results, columns=['Stock', 'Reversal Levels'])
    df_results.to_csv("support_resistance_levels.csv", index=False)
    

   
