### AsyncSymbol

`AsyncSymbol` class is more user convenient than `AsyncClient`, because it uses predefined modules for quote summary endpoint and predefined types for timeseries endpoints. It uses `AsyncClient` as a singleton (multiple symbols use shared AsyncClient instance) to save resources. Methods return result field of http response json.

### AsyncClient

`AsyncClient` class has methods defined according to the API endpoints. It uses `curl_cffi.requests.AsyncSession` under the hood. Methods return full http response json including result and error fields.

_Note: Market Summary, Trending and Currencies endpoints are only available in the `AsyncClient` class._

### Quote Endpoint

Using client.get_quote and client.get_search you can quote multiple tickers at once.

### Quote Summary Endpoint

In client.get_quote_summary you specify the modules.

Whereas symbol class has predefined methods for each module. Alternatively you can use get_quote_summary_all_modules to obtain result of all modules.

### Timeseries Endpoint

In AsyncClient.get_timeseries you specify the types.

Whereas symbol class has predefined methods for each financial page.