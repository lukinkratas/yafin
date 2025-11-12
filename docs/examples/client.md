### Chart Endpoint

```python
from yafin import Client

def main() -> None:

    # opt. 1 use context manager (recommended)
    with Client() as client:
        aapl_5d_chart = client.get_chart(ticker='AAPL', interval='1h', period_range='5d', events='div,split')

    # opt. 2 use close to avoid resource leakage
    client = Client()
    meta_1y_chart = client.get_chart(ticker='META', interval='1d', period_range='1y')
    client.close()

if __name__ == '__main__':
    main()
```

### Quote Endpoint

```python
from yafin import Client

def main() -> None:

    with Client() as client:
        aapl_meta_quotes = client.get_quote(tickers='AAPL,META')

if __name__ == '__main__':
    main()
```

### Quote Type Endpoint

```python
from yafin import Client

def main() -> None:

    with Client() as client:
        aapl_meta_quotes = client.get_quote_type(tickers='AAPL,META')

if __name__ == '__main__':
    main()
```

### Quote Summary Endpoint

```python
from yafin import Client

def main() -> None:

    with Client() as client:
        meta_quote_summary = client.get_quote_summary(
            ticker='META', modules='assetProfile,price,defaultKeyStatistics,calendarEvents'
        )

if __name__ == '__main__':
    main()
```

### Timeseries Endpoint

```python
from yafin import Client

def main() -> None:

    with Client() as client:
        aapl_ttm_income_stmt = client.get_timeseries(
            ticker='AAPL',
            types='trailingNetIncome,trailingPretaxIncome,trailingEBIT,trailingEBITDA,trailingGrossProfit'
        )
        meta_annual_balance_sheet = client.get_timeseries(
            ticker='META',
            types='annualNetDebt,annualTotalDebt',
            period1=datetime(2020, 1, 1).timestamp(),
            period2=datetime.now().timestamp(),
        )
        aapl_quarterly_cash_flow = client.get_timeseries(
            ticker='AAPL', types='quarterlyFreeCashFlow,quarterlyOperatingCashFlow'
        )

if __name__ == '__main__':
    main()
```

### Options Endpoint

```python
from yafin import AsyncClien

def main() -> None:

    with Client() as client:
        meta_options = client.get_options(ticker='META')

if __name__ == '__main__':
    main()
```

### Search Endpoint

```python
from yafin import AsyncSymbol

def main() -> None:

    with Client() as client:
        aapl_meta_search = client.get_search(tickers='AAPL,META')

if __name__ == '__main__':
    main()
```

### Recommendations Endpoint

```python
from yafin import Client

def main() -> None:

    with Client() as client:
        meta_recommendations = client.get_recommendations(ticker='META')

if __name__ == '__main__':
    main()
```

### Insights Endpoint

```python
from yafin import Client

def main() -> None:

    with Client() as client:
        aapl_meta_insights = client.get_insights(tickers='AAPL,META')

if __name__ == '__main__':
    main()
```

### Ratings Endpoint

```python
from yafin import Client

def main() -> None:

    with Client() as client:
        meta_ratings = client.get_ratings(ticker='META')

if __name__ == '__main__':
    main()
```

### Market Summary Endpoint

```python
from yafin import Client

def main() -> None:

    with Client() as client:
        market_summaries = client.get_market_summaries()

if __name__ == '__main__':
    main()
```

### Trending Endpoint

```python
from yafin import Client

def main() -> None:

    with Client() as client:
        trending = client.get_trending()

if __name__ == '__main__':
    main()
```

### Currencies Endpoint

```python
from yafin import Client

def main() -> None:

    with Client() as client:
        currencies = client.get_currencies()

if __name__ == '__main__':
    main()
```

### Calendas Events Endpoint

```python
from yafin import Client

def main() -> None:

    with Client() as client:
        currencies = client.get_calendar_events()

if __name__ == '__main__':
    main()
```
