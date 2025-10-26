### Quote Summary Endpoint

```python
import asyncio

from yafin import AsyncClient
from yafin.const import ALL_MODULES_CSV

async def main() -> None:

    async with AsyncClient() as client:
        meta_quote_summary = await client.get_quote_summary(
            ticker='META', modules=ALL_MODULES_CSV
        )

if __name__ == '__main__':
    asyncio.run(main())
```

### Timeseries Endpoint

```python
import asyncio

from yafin import AsyncClient
from yafin.const import (
    ANNUAL_INCOME_STATEMENT_TYPES_CSV,
    QUARTERLY_BALANCE_SHEET_TYPES_CSV,
    TRAILING_CASH_FLOW_TYPES_CSV,
)

async def main() -> None:

    async with AsyncClient() as client:

        aapl_annual_income_stmt = await client.get_timeseries(
            ticker='AAPL', types=ANNUAL_INCOME_STATEMENT_TYPES_CSV
        )

        aapl_quarterly_balance_sheet = await client.get_timeseries(
            ticker='AAPL', types=QUARTERLY_BALANCE_SHEET_TYPES_CSV
        )

        aapl_ttm_cash_flow = await client.get_timeseries(
            ticker='AAPL', types=TRAILING_CASH_FLOW_TYPES_CSV
        )

if __name__ == '__main__':
    asyncio.run(main())
```
