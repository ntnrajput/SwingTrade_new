import pandas as pd
import numpy as np
from support_resistance import calculate_support_resistance  # Fixed import
import stock_data_fetch
import smtplib
from email.message import EmailMessage
import os


# Parameters
PROXIMITY_PCT = 2 # Percentage threshold for considering price "close" to a level
CROSSING_PCT = 1.5  # Percentage threshold for considering price "crossing" a level

def send_email_with_attachment(recipient, subject, body, attachment_path):
    sender_email = "criobd.rites@gmail.com"           # Replace with your email
    sender_password = "exel gmiq fcdq rlkl"      # Use App Password if Gmail 2FA is on

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = recipient
    msg.set_content(body)

    # Attach the CSV file
    with open(attachment_path, "rb") as f:
        file_data = f.read()
        filename = os.path.basename(attachment_path)
        msg.add_attachment(file_data, maintype="application", subtype="octet-stream", filename=filename)

    # Send email via SMTP
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(sender_email, sender_password)
        smtp.send_message(msg)



def find_stocks_near_levels(df, symbols):
    """
    Identify stocks where current price is near or crossing support/resistance levels.
    
    Args:
        df: DataFrame containing stock data
        symbols: List of stock symbols to analyze
        
    Returns:
        DataFrame with stocks near/crossing levels and relevant information
    """
    results = []
    
    for symbol in symbols:
        # Get current price (latest close)
        symbol_data = df[df['Stock'] == symbol]
        if symbol_data.empty:
            continue
            
        current_price = symbol_data.iloc[-2]['Close']
        
        # Calculate support/resistance levels
        _, levels = calculate_support_resistance(df, symbol)
        if not levels:
            continue
            
        # Check proximity to each level
        for level in levels:
            if level == 0:  # Skip zero levels which might be invalid
                continue
                
            diff_pct = abs(current_price - level) / level * 100
            
            if diff_pct <= PROXIMITY_PCT:
                relation = "Near"
                if diff_pct <= CROSSING_PCT and current_price > level:
                    relation = "Crossing"
                
                # Determine if it's support or resistance
                level_type = "Support" if current_price > level else "Resistance"
                
                results.append({
                    'Stock': symbol,
                    'Current Price': current_price,
                    'Level': level,
                    'Level Type': level_type,
                    'Relation': relation,
                    'Distance %': round(diff_pct, 2),
                    'Price Above Level': current_price > level
                })
    
    return pd.DataFrame(results)

def main():
    # Fetch stock data
    df, symbols = stock_data_fetch.fetch_stock_data()
    
    if df.empty:
        print("No stock data available")
        return
    
    # Find stocks near levels
    near_levels_df = find_stocks_near_levels(df, symbols)
    
    if near_levels_df.empty:
        print("No stocks found near support/resistance levels")
        return
    
    # Sort by distance percentage (closest first)
    near_levels_df = near_levels_df.sort_values(by='Distance %')
    
    # Save results
    output_file = "stocks_near_levels.csv"
    near_levels_df.to_csv(output_file, index=False)
    print(f"Found {len(near_levels_df)} stocks near support/resistance levels")
    print(near_levels_df.head())

    send_email_with_attachment(
        recipient="ntn.rajput89@gmail.com",
        subject="Stocks Near Support/Resistance Levels",
        body="Please find attached the latest stock analysis report.",
        attachment_path=output_file
    )
    
    return near_levels_df

if __name__ == "__main__":
    main()