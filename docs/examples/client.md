### Chart Endpoint

```python
import asyncio

from yafin import AsyncClient

async def main() -> None:

    # opt. 1 use context manager (recommended)
    async with AsyncClient() as client:
        aapl_5d_chart = await client.get_chart(ticker='AAPL', period_range='5d', interval='1h', events='div,split')

    # opt. 2 use close to avoid resource leakage
    client = AsyncClient()
    meta_1y_chart = await client.get_chart(ticker='META', period_range='1y', interval='1d')
    await client.close()

if __name__ == '__main__':
    asyncio.run(main())
```

### Quote Endpoint

```python
import asyncio

from yafin import AsyncClient

async def main() -> None:

    async with AsyncClient() as client:
        aapl_meta_quotes = await client.get_quote(tickers='AAPL,META')

if __name__ == '__main__':
    asyncio.run(main())
```

### Quote Summary Endpoint

```python
import asyncio

from yafin import AsyncClient

async def main() -> None:

    async with AsyncClient() as client:
        meta_quote_summary = await client.get_quote_summary(
            ticker='META', modules='assetProfile,price,defaultKeyStatistics,calendarEvents'
        )

if __name__ == '__main__':
    asyncio.run(main())
```

### Timeseries Endpoint

```python
import asyncio

from yafin import AsyncClient

async def main() -> None:

    async with AsyncClient() as client:
        aapl_ttm_income_stmt = await client.get_timeseries(
            ticker='AAPL',
            types='trailingNetIncome,trailingPretaxIncome,trailingEBIT,trailingEBITDA,trailingGrossProfit'
        )
        meta_annual_balance_sheet = await client.get_timeseries(
            ticker='META',
            types='annualNetDebt,annualTotalDebt',
            period1=datetime(2020, 1, 1).timestamp(),
            period2=datetime.now().timestamp(),
        )
        aapl_quarterly_cash_flow = await client.get_timeseries(
            ticker='AAPL', types='quarterlyFreeCashFlow,quarterlyOperatingCashFlow'
        )

if __name__ == '__main__':
    asyncio.run(main())
```

### Options Endpoint

```python
import asyncio

from yafin import AsyncClien

async def main() -> None:

    async with AsyncClient() as client:
        meta_options = await client.get_options(ticker='META')

if __name__ == '__main__':
    asyncio.run(main())
```

### Search Endpoint

```python
import asyncio

from yafin import AsyncSymbol

async def main() -> None:

    async with AsyncClient() as client:
        meta_search = await client.get_search(tickers='AAPL,META')

if __name__ == '__main__':
    asyncio.run(main())
```

### Recommendations Endpoint

```python
import asyncio

from yafin import AsyncClient

async def main() -> None:

    async with AsyncClient() as client:
        meta_recommendations = await client.get_recommendations(ticker='META')

if __name__ == '__main__':
    asyncio.run(main())
```

### Insights Endpoint

```python
import asyncio

from yafin import AsyncClient

async def main() -> None:

    async with AsyncClient() as client:
        meta_insights = await client.get_insights(ticker='META')

if __name__ == '__main__':
    asyncio.run(main())
```

### Market Summary Endpoint

```python
import asyncio

from yafin import AsyncClient

async def main() -> None:

    async with AsyncClient() as client:
        market_summaries = await client.get_market_summaries()

if __name__ == '__main__':
    asyncio.run(main())
```

### Trending Endpoint

```python
import asyncio

from yafin import AsyncClient

async def main() -> None:

    async with AsyncClient() as client:
        trending = await client.get_trending()

if __name__ == '__main__':
    asyncio.run(main())
```

### Currencies Endpoint

```python
import asyncio

from yafin import AsyncClient

async def main() -> None:

    async with AsyncClient() as client:
        currencies = await client.get_currencies()

if __name__ == '__main__':
    asyncio.run(main())
```
