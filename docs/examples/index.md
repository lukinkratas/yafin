Below are example for each endpoint.

Output example JSONs can be found in [unit test fixtures](https://github.com/lukinkratas/yafin/tree/main/tests/unit/fixtures). If needed, they can be reproduced with [fetch_mocks.py](https://github.com/lukinkratas/yafin/blob/main/scripts/fetch_mocks.py) script.

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
