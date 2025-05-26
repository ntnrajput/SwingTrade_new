import requests
from bs4 import BeautifulSoup

def get_stock_data(symbol):
    url = f"https://www.screener.in/company/{symbol}/consolidated/"
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code != 200:
            print(f"Failed to fetch data for {symbol}")
            return None

        soup = BeautifulSoup(response.text, 'html.parser')
        ratios = {}

        # Look for all li tags that hold ratio name and value
        ratio_items = soup.select("ul.ratios li")

        def find_ratio(label):
            for item in ratio_items:
                if label.lower() in item.text.lower():
                    try:
                        value_text = item.find("span", class_="number").text.replace('%', '').strip()
                        return float(value_text)
                    except:
                        return None
            return None

        ratios['ROE'] = find_ratio("Return on equity")
        ratios['ROCE'] = find_ratio("Return on capital employed")
        ratios['Debt to equity'] = find_ratio("Debt to equity")
        ratios['Current ratio'] = find_ratio("Current ratio")
        ratios['Profit growth 5Years'] = find_ratio("Profit growth 5Years")

        return ratios
    except Exception as e:
        print(f"Error fetching data for {symbol}: {e}")
        return None

def is_fundamentally_strong(ratios):
    try:
        return (
            ratios['ROE'] and ratios['ROE'] > 15 and
            ratios['ROCE'] and ratios['ROCE'] > 15 and
            ratios['Debt to equity'] is not None and ratios['Debt to equity'] < 0.5 and
            ratios['Current ratio'] and ratios['Current ratio'] > 1.5 and
            ratios['Profit growth 5Years'] and ratios['Profit growth 5Years'] > 0
        )
    except:
        return False

def check_stocks(symbols):
    results = {}
    for symbol in symbols:
        print(f"Checking {symbol}...")
        data = get_stock_data(symbol)
        if data:
            strong = is_fundamentally_strong(data)
            results[symbol] = {"Strong": strong, "Data": data}
        else:
            results[symbol] = {"Strong": False, "Data": None}
    return results

# Example usage
stock_symbols = ["TCS", "INFY", "RELIANCE", "YESBANK"]
results = check_stocks(stock_symbols)

for sym, res in results.items():
    print(f"\n{sym}: {'✅ Fundamentally Strong' if res['Strong'] else '❌ Not Strong'}")
    print(f"Data: {res['Data']}")
