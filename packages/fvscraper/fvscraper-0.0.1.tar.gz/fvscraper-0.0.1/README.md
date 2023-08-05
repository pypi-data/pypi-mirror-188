# FINVIZ Scraper
A library for interacting with https://finviz.com

## Install

```bash
$ pip install fvscraper
```
*The package name is `fvscraper` but it should be imported as `finscraper`*


## How to use

```python 
from finscraper import Screener

filters = {
    "descriptive": {
        "exchange": "NYSE",
        "industry": "stocksonly"
    },
    "technical": {
        "performance": "1w30o"
    },
}

screener = Screener()

tickers = screener.query(filters=filters)

print(tickers)
#>>> Tickers Bin containing 20 tickers

print(tickers[0].company)
#>>> BIT Mining Limited

print(tickers[0].volume)
#>>> 1122310


tickers.to_csv("scraped.csv")

```
### Filters on the Finviz ui

The filters are split into **Descriptive**, **Fundamental** &  **Technical**

#### Descriptive filters
- Exchange
- Market Cap
- Earnings Rate
- Target Price
- Index
- Dividend Yield
- Average Volume
- IPO Date
- Sector
- Float Short
- Relative Volume
- Shares Outstanding
- Industry
- Analyst Recommendation
- Current Volume
- Float
- Country
- Option/Short
- Price


#### Fundamental
- P/E
- Price/Cash
- EPS growth next 5 years
- Return on Equity
- Debt/Equity
- Insider Ownership
- Forward P/E	
- Price/Free Cash Fl
- Sales growth past 5 years
- Return on Investment
- Gross Margin
- Insider Transactions
- PEG
- EPS growth this year
- EPS growth qtr over qtr
- Current Ratio
- Operating Margin
- Institutional Ownership
- P/S
- EPS growth next year
- Sales growth qtr over qtr
- Quick Ratio
- Net Profit Margin
- Institutional Transactions
- P/B
- EPS growth past 5 years
- Return on Assets
- LT Debt/Equity
- Payout Ratio


#### Technical
- Performance
- 20-Day Simple Moving Average
- 20-Day High/Low
- Beta
- Performance 2
- 50-Day Simple Moving Average
- 50-Day High/Low
- Average True Range
- Volatility
- 200-Day Simple Moving Average
- 52-Week High/Low
- RSI
- Change
- Pattern
- Gap
- Change from Ope
- Candlestick

# TODO
- Proxy to rotate IP's 