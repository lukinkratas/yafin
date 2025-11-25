### Chart Endpoint

```python
import asyncio
from yafin import AsyncSymbols

async def main() -> None:

    # opt. 1 use context manager (recommended)
    async with AsyncSymbols('META,AAPL') as meta_aapl:
        meta_aapl_1y_chart = await meta_aapl.get_chart(interval='1d', period_range='1y')

    # opt. 2 use close to avoid resource leakage
    googl_msft = AsyncSymbol('GOOGL,MSFT')
    googl_msft_5d_chart = await googl_msft.get_chart(
        interval='1h', period_range='5d', include_pre_post=True, include_div=True, include_split=False
    )
    await googl_msft.close()

if __name__ == '__main__':
    asyncio.run(main())
```

### Quote Endpoint

```python
import asyncio
from yafin import AsyncSymbols

async def main() -> None:

    async with AsyncSymbols('META,AAPL') as meta_aapl:
        meta_aapl_quote = await meta_aapl.get_quote(include_pre_post=True)

if __name__ == '__main__':
    asyncio.run(main())
```

### Quote Type Endpoint

```python
import asyncio
from yafin import AsyncSymbols

async def main() -> None:

    async with AsyncSymbols('META,AAPL') as meta_aapl:
        meta_aapl_quote = await meta_aapl.get_quote_type()

if __name__ == '__main__':
    asyncio.run(main())
```

### Quote Summary Endpoint

```python
import asyncio
from yafin import AsyncSymbols

async def main() -> None:

    async with AsyncSymbols('META,AAPL') as meta_aapl:
        meta_aapl_quote_summary_all_modules = await meta_aapl.get_quote_summary_all_modules()
        meta_aapl_asset_profile = await meta_aapl.get_asset_profile()
        meta_aapl_summary_profile = await meta_aapl.get_summary_profile()
        meta_aapl_summary_detail = await meta_aapl.get_summary_detail()
        meta_aapl_price = await meta_aapl.get_price()
        meta_aapl_default_key_statistics = await meta_aapl.get_default_key_statistics()
        meta_aapl_financial_data = await meta_aapl.get_financial_data()
        meta_aapl_calendar_events = await meta_aapl.get_calendar_events()
        meta_aapl_sec_filings = await meta_aapl.get_sec_filings()
        meta_aapl_upgrade_downgrade_history = await meta_aapl.get_upgrade_downgrade_history()
        meta_aapl_institution_ownership = await meta_aapl.get_institution_ownership()
        meta_aapl_fund_ownership = await meta_aapl.get_fund_ownership()
        meta_aapl_major_direct_holders = await meta_aapl.get_major_direct_holders()
        meta_aapl_major_holders_breakdown = await meta_aapl.get_major_holders_breakdown()
        meta_aapl_insider_transactions = await meta_aapl.get_insider_transactions()
        meta_aapl_insider_holders = await meta_aapl.get_insider_holders()
        meta_aapl_net_share_purchase_activity = await meta_aapl.get_net_share_purchase_activity()
        meta_aapl_earnings = await meta_aapl.get_earnings()
        meta_aapl_earnings_history = await meta_aapl.get_earnings_history()
        meta_aapl_earnings_trend = await meta_aapl.get_earnings_trend()
        meta_aapl_industry_trend = await meta_aapl.get_industry_trend()
        meta_aapl_index_trend = await meta_aapl.get_index_trend()
        meta_aapl_sector_trend = await meta_aapl.get_sector_trend()
        meta_aapl_recommendation_trend = await meta_aapl.get_recommendation_trend()
        meta_aapl_page_views = await meta_aapl.get_page_views()

if __name__ == '__main__':
    asyncio.run(main())
```

### Timeseries Endpoint

```python
import asyncio
from yafin import AsyncSymbols

async def main() -> None:

    async with AsyncSymbols('META,AAPL') as meta_aapl:
        meta_aapl_get_income_statement = await meta_aapl.get_income_statement(
            frequency='trailing',
            period1=datetime(2020, 1, 1).timestamp(),
            period2=datetime.now().timestamp(),
        )
        meta_aapl_get_balance_sheet = await meta_aapl.get_balance_sheet(
            frequency='annual', period1=1577833200, period2=1760857217.66133,
        )
        meta_aapl_get_cash_flow = await meta_aapl.get_cash_flow(frequency='quarterly')

if __name__ == '__main__':
    asyncio.run(main())
```

### Options Endpoint

```python
import asyncio
from yafin import AsyncSymbols

async def main() -> None:

    async with AsyncSymbols('META,AAPL') as meta_aapl:
        meta_aapl_options = await meta_aapl.get_options()

if __name__ == '__main__':
    asyncio.run(main())
```

### Search Endpoint

```python
import asyncio
from yafin import AsyncSymbols

async def main() -> None:

    async with AsyncSymbols('META,AAPL') as meta_aapl:
        meta_aapl_search = await meta_aapl.get_search()

if __name__ == '__main__':
    asyncio.run(main())
```

### Recommendations Endpoint

```python
import asyncio
from yafin import AsyncSymbols

async def main() -> None:

    async with AsyncSymbols('META,AAPL') as meta_aapl:
        meta_aapl_recommendations = await meta_aapl.get_recommendations()

if __name__ == '__main__':
    asyncio.run(main())
```

### Insights Endpoint

```python
import asyncio
from yafin import AsyncSymbols

async def main() -> None:

    async with AsyncSymbols('META,AAPL') as meta_aapl:
        meta_aapl_insights = await meta_aapl.get_insights()

if __name__ == '__main__':
    asyncio.run(main())
```

### Ratings Endpoint

```python
import asyncio
from yafin import AsyncSymbols

async def main() -> None:

    async with AsyncSymbols('META,AAPL') as meta_aapl:
        meta_aapl_ratings = await meta_aapl.get_ratings()

if __name__ == '__main__':
    asyncio.run(main())
```
