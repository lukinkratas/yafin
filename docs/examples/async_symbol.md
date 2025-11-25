### Chart Endpoint

```python
import asyncio
from yafin import AsyncSymbol

async def main() -> None:

    # opt. 1 use context manager (recommended)
    async with AsyncSymbol('META') as meta:
        meta_1y_chart = await meta.get_chart(interval='1d', period_range='1y')

    # opt. 2 use close to avoid resource leakage
    aapl = AsyncSymbol('AAPL')
    aapl_5d_chart = await aapl.get_chart(
        interval='1h', period_range='5d', include_pre_post=True, include_div=True, include_split=False
    )
    await aapl.close()

if __name__ == '__main__':
    asyncio.run(main())
```

### Quote Endpoint

```python
import asyncio
from yafin import AsyncSymbol

async def main() -> None:

    async with AsyncSymbol('META') as meta:
        meta_quote = await meta.get_quote(include_pre_post=True)

if __name__ == '__main__':
    asyncio.run(main())
```

### Quote Type Endpoint

```python
import asyncio
from yafin import AsyncSymbol

async def main() -> None:

    async with AsyncSymbol('META') as meta:
        meta_quote = await meta.get_quote_type()

if __name__ == '__main__':
    asyncio.run(main())
```

### Quote Summary Endpoint

```python
import asyncio
from yafin import AsyncSymbol

async def main() -> None:

    async with AsyncSymbol('META') as meta:
        meta_quote_summary_all_modules = await meta.get_quote_summary_all_modules()
        meta_asset_profile = await meta.get_asset_profile()
        meta_summary_profile = await meta.get_summary_profile()
        meta_summary_detail = await meta.get_summary_detail()
        meta_price = await meta.get_price()
        meta_default_key_statistics = await meta.get_default_key_statistics()
        meta_financial_data = await meta.get_financial_data()
        meta_calendar_events = await meta.get_calendar_events()
        meta_sec_filings = await meta.get_sec_filings()
        meta_upgrade_downgrade_history = await meta.get_upgrade_downgrade_history()
        meta_institution_ownership = await meta.get_institution_ownership()
        meta_fund_ownership = await meta.get_fund_ownership()
        meta_major_direct_holders = await meta.get_major_direct_holders()
        meta_major_holders_breakdown = await meta.get_major_holders_breakdown()
        meta_insider_transactions = await meta.get_insider_transactions()
        meta_insider_holders = await meta.get_insider_holders()
        meta_net_share_purchase_activity = await meta.get_net_share_purchase_activity()
        meta_earnings = await meta.get_earnings()
        meta_earnings_history = await meta.get_earnings_history()
        meta_earnings_trend = await meta.get_earnings_trend()
        meta_industry_trend = await meta.get_industry_trend()
        meta_index_trend = await meta.get_index_trend()
        meta_sector_trend = await meta.get_sector_trend()
        meta_recommendation_trend = await meta.get_recommendation_trend()
        meta_page_views = await meta.get_page_views()

if __name__ == '__main__':
    asyncio.run(main())
```

### Timeseries Endpoint

```python
import asyncio
from yafin import AsyncSymbol

async def main() -> None:

    async with AsyncSymbol('META') as meta:
        meta_get_income_statement = await meta.get_income_statement(
            frequency='trailing',
            period1=datetime(2020, 1, 1).timestamp(),
            period2=datetime.now().timestamp(),
        )
        meta_get_balance_sheet = await meta.get_balance_sheet(
            frequency='annual', period1=1577833200, period2=1760857217.66133,
        )
        meta_get_cash_flow = await meta.get_cash_flow(frequency='quarterly')

if __name__ == '__main__':
    asyncio.run(main())
```

### Options Endpoint

```python
import asyncio
from yafin import AsyncSymbol

async def main() -> None:

    async with AsyncSymbol('META') as meta:
        meta_options = await meta.get_options()

if __name__ == '__main__':
    asyncio.run(main())
```

### Search Endpoint

```python
import asyncio
from yafin import AsyncSymbol

async def main() -> None:

    async with AsyncSymbol('META') as meta:
        meta_search = await meta.get_search()

if __name__ == '__main__':
    asyncio.run(main())
```

### Recommendations Endpoint

```python
import asyncio
from yafin import AsyncSymbol

async def main() -> None:

    async with AsyncSymbol('META') as meta:
        meta_recommendations = await meta.get_recommendations()

if __name__ == '__main__':
    asyncio.run(main())
```

### Insights Endpoint

```python
import asyncio
from yafin import AsyncSymbol

async def main() -> None:

    async with AsyncSymbol('META') as meta:
        meta_insights = await meta.get_insights()

if __name__ == '__main__':
    asyncio.run(main())
```

### Ratings Endpoint

```python
import asyncio
from yafin import AsyncSymbol

async def main() -> None:

    async with AsyncSymbol('META') as meta:
        meta_ratings = await meta.get_ratings()

if __name__ == '__main__':
    asyncio.run(main())
```
