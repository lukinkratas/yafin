### Chart Endpoint

```python
from yafin import Client

# opt. 1 use context manager (recommended)
with Client() as client:
    aapl_5d_chart = client.get_chart(ticker='AAPL', interval='1h', period_range='5d', events='div,split')

# opt. 2 use close to avoid resource leakage
client = Client()
meta_1y_chart = client.get_chart(ticker='META', interval='1d', period_range='1y')
client.close()
```

### Quote Endpoint

```python
from yafin import Client

with Client() as client:
    aapl_meta_quotes = client.get_quote(tickers='AAPL,META')
```

### Quote Type Endpoint

```python
from yafin import Client

with Client() as client:
    aapl_meta_quotes = client.get_quote_type(tickers='AAPL,META')
```

### Quote Summary Endpoint

```python
from yafin import Client

with Client() as client:
    meta_quote_summary = client.get_quote_summary(
        ticker='META', modules='assetProfile,price,defaultKeyStatistics,calendarEvents'
    )
```

### Timeseries Endpoint

```python
from yafin import Client

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
```

### Options Endpoint

```python
from yafin import Client

with Client() as client:
    meta_options = client.get_options(ticker='META')
```

### Search Endpoint

```python
from yafin import Client

with Client() as client:
    aapl_meta_search = client.get_search(tickers='AAPL,META')
```

### Recommendations Endpoint

```python
from yafin import Client

with Client() as client:
    meta_recommendations = client.get_recommendations(ticker='META')
```

### Insights Endpoint

```python
from yafin import Client

with Client() as client:
    aapl_meta_insights = client.get_insights(tickers='AAPL,META')
```

### Ratings Endpoint

```python
from yafin import Client

with Client() as client:
    meta_ratings = client.get_ratings(ticker='META')
```

### Market Summary Endpoint

```python
from yafin import Client

with Client() as client:
    market_summaries = client.get_market_summaries()
```

### Trending Endpoint

```python
from yafin import Client

with Client() as client:
    trending = client.get_trending()
```

### Currencies Endpoint

```python
from yafin import Client

with Client() as client:
    currencies = client.get_currencies()
```

### Calendas Events Endpoint

```python
from yafin import Client

with Client() as client:
    currencies = client.get_calendar_events()
```
