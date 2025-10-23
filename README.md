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
