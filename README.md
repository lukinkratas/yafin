# Yafin

Unofficial [Yahoo!Ⓡ finance](https://finance.yahoo.com) API asynchronous client.

- not affiliated with Yahoo, Inc.
- oss that uses publicly available APIs.
- intended for research, educational purposes and personal use only.
- asynchronous.
- not returning pandas dataframes (because why?).

## Example usage

Below are example for each endpoint.

`AsyncClient` class has methods defined according to the API endpoints. It uses `curl_cffi.requests.AsyncSession` under the hood.
s
`AsyncSymbol` class is more user friendly and uses predefined modules for quote summary endpoint and predefined types for timeseries endpoints. It uses `AsyncClient` as a singleton (meaning multiple symbols use the AsyncClient instance) under the hood.

Some endpoints are only available in the `AsyncClient` class.

Both use http resources, so do not forget to close them after use to avoid resource leakage or use context manager.

Output example JSONs can be found in [unit test fixtures](tests/unit/fixtures).

If needed, they can be reproduced with [fetch_mocks.py](scripts/fetch_mocks.py) script.

### chart endpoint

```python
import asyncio

from yafin import AsyncClient, AsyncSymbol

async def main() -> None:

    client = AsyncClient()
    meta_1y_chart = await client.get_chart(ticker='META', period_range='1y', interval='1d')
    await client.close()

    async with AsyncClient() as client:
        aapl_5d_chart = await client.get_chart(ticker='AAPL', period_range='5d', interval='1h', events='div,split')

    aapl = AsyncSymbol('AAPL')
    aapl_5d_chart = await aapl.get_chart(period_range='5d', interval='1h', include_div=True, include_split=False)
    await aapl.close()

    async with AsyncSymbol('META') as meta:
        meta_1y_chart = await meta.get_chart(period_range='1y', interval='1d')

if __name__ == '__main__':
    asyncio.run(main())
```

### quote endpoint

In client.get_quote you can quote multiple tickers at once.

```python
import asyncio

from yafin import AsyncClient, AsyncSymbol

async def main() -> None:

    async with AsyncClient() as client:
        aapl_meta_quotes = await client.get_quote(tickers='AAPL,META')

    async with AsyncSymbol('META') as meta:
        meta_quote = await meta.get_quote()

    aapl = AsyncSymbol('AAPL')
    aapl_quote = await aapl.get_quote()
    await aapl.close()

if __name__ == '__main__':
    asyncio.run(main())
```

### quote summary endpoint

In client.get_quote_summary you specify the modules.

Whereas symbol class has predefined methods for each module. Alternatively you can use get_quote_summary_all_modules to obtain result of all modules.

```python
import asyncio

from yafin import AsyncClient, AsyncSymbol

async def main() -> None:

    async with AsyncClient() as client:
        meta_quote_summary = await client.get_quote_summary(
            ticker='META', modules='assetProfile,price,defaultKeyStatistics,calendarEvents'
        )

    async with AsyncSymbol('META') as meta:
        meta_quote_summary_all_modules = await meta.get_quote_summary_all_modules()
        meta_quote_type = await meta.get_quote_type()
        meta_asset_profile = await meta.get_asset_profile()
        meta_summary_profile = await meta.get_summary_profile()
        meta_summary_detail = await meta.get_summary_detail()
        meta_income_statement_history = await meta.get_income_statement_history()
        meta_income_statement_history_quarterly = await meta.get_income_statement_history_quarterly()
        meta_balance_sheet_history = await meta.get_balance_sheet_history()
        meta_balance_sheet_history_quarterly = await meta.get_balance_sheet_history_quarterly()
        meta_cashflow_statement_history = await meta.get_cashflow_statement_history()
        meta_cashflow_statement_history_quarterly = await meta.get_cashflow_statement_history_quarterly()
        meta_esg_scores = await meta.get_esg_scores()
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

### timeseries endpoint

In AsyncClient.get_timeseries you specify the types.

Whereas symbol class has predefined methods for each financial page.

```python
import asyncio

from yafin import AsyncClient, AsyncSymbol

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

### options endpoint

```python
import asyncio

from yafin import AsyncClient, AsyncSymbol

async def main() -> None:

    async with AsyncClient() as client:
        meta_options = await client.get_options(ticker='META')

    async with AsyncSymbol('META') as meta:
        meta_options = await meta.get_options()

if __name__ == '__main__':
    asyncio.run(main())
```

### search endpoint

```python
import asyncio

from yafin import AsyncClient, AsyncSymbol

async def main() -> None:

    async with AsyncClient() as client:
        meta_search = await client.get_search(tickers='META')

    async with AsyncSymbol('META') as meta:
        meta_search = await meta.get_search()

if __name__ == '__main__':
    asyncio.run(main())
```

### recommendations endpoint

```python
import asyncio

from yafin import AsyncClient, AsyncSymbol

async def main() -> None:

    async with AsyncClient() as client:
        meta_recommendations = await client.get_recommendations(ticker='META')

    async with AsyncSymbol('META') as meta:
        meta_recommendations = await meta.get_recommendations()

if __name__ == '__main__':
    asyncio.run(main())
```

### insights endpoint

```python
import asyncio

from yafin import AsyncClient, AsyncSymbol

async def main() -> None:

    async with AsyncClient() as client:
        meta_insights = await client.get_insights(ticker='META')

    async with AsyncSymbol('META') as meta:
        meta_insights = await meta.get_insights()

if __name__ == '__main__':
    asyncio.run(main())
```

### market summary endpoint

```python
import asyncio

from yafin import AsyncClient

async def main() -> None:

    async with AsyncClient() as client:
        market_summaries = await client.get_market_summaries()

if __name__ == '__main__':
    asyncio.run(main())
```

### trending endpoint

```python
import asyncio

from yafin import AsyncClient

async def main() -> None:

    async with AsyncClient() as client:
        trending = await client.get_trending()

if __name__ == '__main__':
    asyncio.run(main())
```

### currencies endpoint

```python
import asyncio

from yafin import AsyncClient

async def main() -> None:

    async with AsyncClient() as client:
        currencies = await client.get_currencies()

if __name__ == '__main__':
    asyncio.run(main())
```

### Set custom curl cffi async session in AsyncClient or custom AsyncClient in AsyncSymbol [WIP]

Not yet implemented - solve after closing session / client assignment

```python
import asyncio

from yafin import AsyncClient, AsyncSymbol

async def main() -> None:

    session = AsyncSession(impersonate='chrome')
    client = AsyncClient(session=session)
    symbol = AsyncSymbol('META', client=client)

    ...

    await symbol.close()
    await client.close()
    await session.close()

if __name__ == '__main__':
    asyncio.run(main())
```

## Research

### yfinances
https://github.com/ranaroussi/yfinance
https://ranaroussi.github.io/yfinance/

### yahooquery
https://github.com/dpguthrie/yahooquery
https://yahooquery.dpguthrie.com/

### gh open api
https://github.com/pasdam/yahoo-finance-openapi/blob/main/query2.yml
https://github.com/pasdam/yahoo-finance-openapi/blob/main/query1.yml

### gh yahoo-finance-api-collection (bruno collection)
https://github.com/Scarvy/yahoo-finance-api-collection
