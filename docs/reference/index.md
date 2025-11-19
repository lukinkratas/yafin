### (Async)Symbol x (Async)Client

`(Async)Symbol` class is high level and more user convenient than `(Async)Client`, because it uses predefined modules for quote summary endpoint and predefined types for timeseries endpoints. It uses `(Async)Client` as a singleton (multiple symbols use shared AsyncClient instance) to save resources. Methods return result field of http response json.

`(Async)Client` class is low level http client class, which has methods defined according to the API endpoints. It uses `curl_cffi.requests.AsyncSession` under the hood. Methods return full http response json including result and error fields.

*Note: Market Summary, Trending, Currencies and Calendar Events endpoints are only available in the `(Async)Client` class.*

### Query multiple symbols

Using `(Async)Client.get_quote`, `(Async)Client.get_quote_type`, `(Async)Client.get_search`, `(Async)Client.get_insights` and `(Async)Client.get_recommendations` you can quote multiple tickers at once natively.

### Quote Summary Endpoint Modules

In `(Async)Client.get_quote_summary` you specify the modules.

Whereas `(Async)Symbol` class has defined methods for each module separately. Alternatively you can use `(Async)Symbol.get_quote_summary_all_modules` to obtain result of all modules.

### Timeseries Endpoint Types

In `(Async)Client.get_timeseries` you specify the types.

Whereas `(Async)Symbol.get_income_statement`, `(Async)Symbol.get_balance_sheet` and `(Async)Symbol.get_cash_flow` class have predefined types.

### Quote Type x Quote Summary Endpoints

`(Async)Client` class provides quote type data in either `(Async)Client.get_quote_type` (Quote Type Endpoint) or in `(Async)Client.get_quote_summary` (Quote Summary Endpoint) with quoteType module. Each endpoint provides different data.

`(Async)Symbol` class provides quote type data in either `(Async)Symbol.get_quote_type` (Quote Type Endpoint) or `(Async)Symbol.get_quote_summary_all_modules` (Quote Summary Endpoint). Each endpoint provides different data.
To avoid confusion with quote type endpoint quote summary data with quoteType module are not provided as separate method in `(Async)Symbol` class.

### Timeseries x Quote Summary Endpoints

`(Async)Client` class provides income statement data in either `(Async)Client.get_timeseries` (Timeseries Endpoint) with income statement types or in `(Async)Client.get_quote_summary` with incomeStatementHistory and incomeStatementHistoryQuarterly module (Quote Summary Endpoint). Each endpoint provides different data.

`(Async)Symbol` class provides income statement data in either `(Async)Symbol.get_income_statement` (Timeseries Endpoint) or in `(Async)Symbol.get_quote_summary_all_modules` (Quote Summary Endpoint). Each endpoint provides different data.
To avoid confusion with timeseries endpoint quote summary data with incomeStatementHistory and incomeStatementHistoryQuarterly modules are not provided as separate methods in `(Async)Symbol` class.

`(Async)Client` class provides balance sheet data in either `(Async)Client.get_timeseries` with balance sheet types (Timeseries Endpoint) or in `(Async)Client.get_quote_summary` with balanceSheetHistory and balanceSheetHistoryQuarterly module (Quote Summary Endpoint). Each endpoint provides different data.

`(Async)Symbol` class provides balance sheet data in either `(Async)Symbol.get_balance_sheet` (Timeseries Endpoint) or `(Async)Symbol.get_quote_summary_all_modules` (Quote Summary Endpoint). Each endpoint provides different data.
To avoid confusion with timeseries endpoint quote summary data with balanceSheetHistory and balanceSheetHistoryQuarterly modules are not provided as separate methods in `(Async)Symbol` class.

`(Async)Client` class provides cash flow data in either `(Async)Client.get_timeseries` with cash flow types (Timeseries Endpoint) or in `(Async)Client.get_quote_summary` with cashflowStatementHistory and cashflowStatementHistoryQuarterly module (Quote Summary Endpoint). Each endpoint provides different data.

`(Async)Symbol` class provides cash flow data in either `(Async)Symbol.get_cash_flow` (Timeseries Endpoint) or `(Async)Symbol.get_quote_summary_all_modules` (Quote Summary Endpoint). Each endpoint provides different data.
To avoid confusion with timeseries endpoint quote summary data with cashflowStatementHistory and cashflowStatementHistoryQuarterly modules are not provided as separate methods in `(Async)Symbol` class.

### Calendar Events x Quote Summary Endpoints

`(Async)Client` class provides calendar events data in either `(Async)Client.get_calendar_events` (Calendar Events Endpoint) or in `(Async)Client.get_quote_summary` (Quote Summary Endpoint) with calendarEvents module. Each endpoint provides different data.

`(Async)Symbol` class provides calendar events data in `(Async)Symbol.get_calendar_events` (Quote Summary Endpoint).

### Response JSON

Most of the `(Async)Client` endpoints return response json with result and error fields.

Exception to that are `(Async)Client.get_search`, `(Async)Client.get_ratings` and `(Async)Client.get_ratings`, which return the direct search / ratings / analysis (respectively) results.
