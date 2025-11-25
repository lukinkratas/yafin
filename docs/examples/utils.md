### Timeseries Endpoint

```python
import asyncio
from yafin import AsyncClient
from yafin.utils import get_types_with_frequency

async def main() -> None:

    async with AsyncClient() as client:

        aapl_annual_income_stmt = await client.get_timeseries(
            ticker='AAPL',
            types=get_types_with_frequency(
                frequency='annual', typ='income_statement'
            )
        )

        aapl_quarterly_balance_sheet = await client.get_timeseries(
            ticker='AAPL',
            types=get_types_with_frequency(
                frequency='quarterly', typ='balance_sheet'
            )
        )

        aapl_ttm_cash_flow = await client.get_timeseries(
            ticker='AAPL',
            types=get_types_with_frequency(
                frequency='trailing', typ='cash_flow'
            )
        )

        aapl_other = await client.get_timeseries(
            ticker='AAPL', types=get_types_with_frequency(typ='other')
        )

if __name__ == '__main__':
    asyncio.run(main())
```
