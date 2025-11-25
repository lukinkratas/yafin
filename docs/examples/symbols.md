### Chart Endpoint

```python
from yafin import Symbols

# opt. 1 use context manager (recommended)
with Symbols('META,AAPL') as meta_aapl:
    meta_aapl_1y_chart = meta_aapl.get_chart(interval='1d', period_range='1y')

# opt. 2 use close to avoid resource leakage
googl_msft = Symbols('GOOGL,MSFT')
googl_msft_5d_chart = googl_msft.get_chart(
    interval='1h', period_range='5d', include_pre_post=True, include_div=True, include_split=False
)
googl_msft.close()
```

### Quote Endpoint

```python
from yafin import Symbols

with Symbols('META,AAPL') as meta_aapl:
    meta_aapl_quote = meta_aapl.get_quote(include_pre_post=True)
```

### Quote Type Endpoint

```python
from yafin import Symbols

with Symbols('META,AAPL') as meta_aapl:
    meta_aapl_quote = meta_aapl.get_quote_type()
```

### Quote Summary Endpoint

```python
from yafin import Symbols

with Symbols('META,AAPL') as meta_aapl:
    meta_aapl_quote_summary_all_modules = meta_aapl.get_quote_summary_all_modules()
    meta_aapl_asset_profile = meta_aapl.get_asset_profile()
    meta_aapl_summary_profile = meta_aapl.get_summary_profile()
    meta_aapl_summary_detail = meta_aapl.get_summary_detail()
    meta_aapl_price = meta_aapl.get_price()
    meta_aapl_default_key_statistics = meta_aapl.get_default_key_statistics()
    meta_aapl_financial_data = meta_aapl.get_financial_data()
    meta_aapl_calendar_events = meta_aapl.get_calendar_events()
    meta_aapl_sec_filings = meta_aapl.get_sec_filings()
    meta_aapl_upgrade_downgrade_history = meta_aapl.get_upgrade_downgrade_history()
    meta_aapl_institution_ownership = meta_aapl.get_institution_ownership()
    meta_aapl_fund_ownership = meta_aapl.get_fund_ownership()
    meta_aapl_major_direct_holders = meta_aapl.get_major_direct_holders()
    meta_aapl_major_holders_breakdown = meta_aapl.get_major_holders_breakdown()
    meta_aapl_insider_transactions = meta_aapl.get_insider_transactions()
    meta_aapl_insider_holders = meta_aapl.get_insider_holders()
    meta_aapl_net_share_purchase_activity = meta_aapl.get_net_share_purchase_activity()
    meta_aapl_earnings = meta_aapl.get_earnings()
    meta_aapl_earnings_history = meta_aapl.get_earnings_history()
    meta_aapl_earnings_trend = meta_aapl.get_earnings_trend()
    meta_aapl_industry_trend = meta_aapl.get_industry_trend()
    meta_aapl_index_trend = meta_aapl.get_index_trend()
    meta_aapl_sector_trend = meta_aapl.get_sector_trend()
    meta_aapl_recommendation_trend = meta_aapl.get_recommendation_trend()
    meta_aapl_page_views = meta_aapl.get_page_views()
```

### Timeseries Endpoint

```python
from yafin import Symbols

with Symbols('META,AAPL') as meta_aapl:
    meta_aapl_get_income_statement = meta_aapl.get_income_statement(
        frequency='trailing',
        period1=datetime(2020, 1, 1).timestamp(),
        period2=datetime.now().timestamp(),
    )
    meta_aapl_get_balance_sheet = meta_aapl.get_balance_sheet(
        frequency='annual', period1=1577833200, period2=1760857217.66133,
    )
    meta_aapl_get_cash_flow = meta_aapl.get_cash_flow(frequency='quarterly')
```

### Options Endpoint

```python
from yafin import Symbols

with Symbols('META,AAPL') as meta_aapl:
    meta_aapl_options = meta_aapl.get_options()
```

### Search Endpoint

```python
from yafin import Symbols

with Symbols('META,AAPL') as meta_aapl:
    meta_aapl_search = meta_aapl.get_search()
```

### Recommendations Endpoint

```python
from yafin import Symbols

with Symbols('META,AAPL') as meta_aapl:
    meta_aapl_recommendations = meta_aapl.get_recommendations()
```

### Insights Endpoint

```python
from yafin import Symbols

with Symbols('META,AAPL') as meta_aapl:
    meta_aapl_insights = meta_aapl.get_insights()
```

### Ratings Endpoint

```python
from yafin import Symbols

with Symbols('META,AAPL') as meta_aapl:
    meta_aapl_ratings = meta_aapl.get_ratings()
```
