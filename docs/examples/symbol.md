### Chart Endpoint

```python
from yafin import Symbol

# opt. 1 use context manager (recommended)
with Symbol('META') as meta:
    meta_1y_chart = meta.get_chart(interval='1d', period_range='1y')

# opt. 2 use close to avoid resource leakage
aapl = Symbol('AAPL')
aapl_5d_chart = aapl.get_chart(
    interval='1h', period_range='5d', include_pre_post=True, include_div=True, include_split=False
)
aapl.close()
```

### Quote Endpoint

```python
from yafin import Symbol

with Symbol('META') as meta:
    meta_quote = meta.get_quote(include_pre_post=True)
```

### Quote Type Endpoint

```python
from yafin import Symbol

with Symbol('META') as meta:
    meta_quote = meta.get_quote_type()
```

### Quote Summary Endpoint

```python
from yafin import Symbol

with Symbol('META') as meta:
    meta_quote_summary_all_modules = meta.get_quote_summary_all_modules()
    meta_asset_profile = meta.get_asset_profile()
    meta_summary_profile = meta.get_summary_profile()
    meta_summary_detail = meta.get_summary_detail()
    meta_price = meta.get_price()
    meta_default_key_statistics = meta.get_default_key_statistics()
    meta_financial_data = meta.get_financial_data()
    meta_calendar_events = meta.get_calendar_events()
    meta_sec_filings = meta.get_sec_filings()
    meta_upgrade_downgrade_history = meta.get_upgrade_downgrade_history()
    meta_institution_ownership = meta.get_institution_ownership()
    meta_fund_ownership = meta.get_fund_ownership()
    meta_major_direct_holders = meta.get_major_direct_holders()
    meta_major_holders_breakdown = meta.get_major_holders_breakdown()
    meta_insider_transactions = meta.get_insider_transactions()
    meta_insider_holders = meta.get_insider_holders()
    meta_net_share_purchase_activity = meta.get_net_share_purchase_activity()
    meta_earnings = meta.get_earnings()
    meta_earnings_history = meta.get_earnings_history()
    meta_earnings_trend = meta.get_earnings_trend()
    meta_industry_trend = meta.get_industry_trend()
    meta_index_trend = meta.get_index_trend()
    meta_sector_trend = meta.get_sector_trend()
    meta_recommendation_trend = meta.get_recommendation_trend()
    meta_page_views = meta.get_page_views()
```

### Timeseries Endpoint

```python
from yafin import Symbol

with Symbol('META') as meta:
    meta_get_income_statement = meta.get_income_statement(
        frequency='trailing',
        period1=datetime(2020, 1, 1).timestamp(),
        period2=datetime.now().timestamp(),
    )
    meta_get_balance_sheet = meta.get_balance_sheet(
        frequency='annual', period1=1577833200, period2=1760857217.66133,
    )
    meta_get_cash_flow = meta.get_cash_flow(frequency='quarterly')
```

### Options Endpoint

```python
from yafin import Symbol

with Symbol('META') as meta:
    meta_options = meta.get_options()
```

### Search Endpoint

```python
from yafin import Symbol

with Symbol('META') as meta:
    meta_search = meta.get_search()
```

### Recommendations Endpoint

```python
from yafin import Symbol

with Symbol('META') as meta:
    meta_recommendations = meta.get_recommendations()
```

### Insights Endpoint

```python
from yafin import Symbol

with Symbol('META') as meta:
    meta_insights = meta.get_insights()
```

### Ratings Endpoint

```python
from yafin import Symbol

with Symbol('META') as meta:
    meta_ratings = meta.get_ratings()
```
