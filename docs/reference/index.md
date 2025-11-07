### AsyncSymbol x AsyncClient

`AsyncSymbol` class is high level and more user convenient than `AsyncClient`, because it uses predefined modules for quote summary endpoint and predefined types for timeseries endpoints. It uses `AsyncClient` as a singleton (multiple symbols use shared AsyncClient instance) to save resources. Methods return result field of http response json.

`AsyncClient` class is low level http client class, which has methods defined according to the API endpoints. It uses `curl_cffi.requests.AsyncSession` under the hood. Methods return full http response json including result and error fields.

_Note: Market Summary, Trending, Currencies and Calendar Events endpoints are only available in the `AsyncClient` class._

### Query multiple symbols

Using client.get_quote, get_quote_type, client.get_search, client.get_insights and client.get_recommendations you can quote multiple tickers at once natively.

### Quote Summary Endpoint Modules

In client.get_quote_summary you specify the modules.

Whereas symbol class has predefined methods for each module. Alternatively you can use get_quote_summary_all_modules to obtain result of all modules.

### Timeseries Endpoint Types

In AsyncClient.get_timeseries you specify the types.

Whereas symbol class has predefined methods for each financial page.

### Quote Type x Quote Summary Endpoints

Client class provides quote type data in either client.get_quote_type (Quote Type Endpoint) or in client.get_quote_summary (Quote Summary Endpoint) with quoteType module. Each endpoint provides different data.

Symbol class provides quote type data in either symbol.get_quote_type (Quote Type Endpoint) or symbol.get_quote_summary_all_modules (Quote Summary Endpoint). Each endpoint provides different data.
To avoid confusion with quote type endpoint quote summary data with quoteType module are not provided as separate method in symbol class.

### Timeseries x Quote Summary Endpoints

Client class provides income statement data in either client.get_timeseries (Timeseries Endpoint) with income statement types or in client.get_quote_summary with incomeStatementHistory and incomeStatementHistoryQuarterly module (Quote Summary Endpoint). Each endpoint provides different data.

Symbol class provides income statement data in either symbol.get_income_statement (Timeseries Endpoint) or in symbol.get_quote_summary_all_modules (Quote Summary Endpoint). Each endpoint provides different data.
To avoid confusion with timeseries endpoint quote summary data with incomeStatementHistory and incomeStatementHistoryQuarterly modules are not provided as separate methods in symbol class.

Client class provides balance sheet data in either client.get_timeseries with balance sheet types (Timeseries Endpoint) or in client.get_quote_summary with balanceSheetHistory and balanceSheetHistoryQuarterly module (Quote Summary Endpoint). Each endpoint provides different data.

Symbol class provides balance sheet data in either symbol.get_balance_sheet (Timeseries Endpoint) or symbol.get_quote_summary_all_modules (Quote Summary Endpoint). Each endpoint provides different data.
To avoid confusion with timeseries endpoint quote summary data with balanceSheetHistory and balanceSheetHistoryQuarterly modules are not provided as separate methods in symbol class.

Client class provides cash flow data in eitherclient.get_timeseries with cash flow types (Timeseries Endpoint) or in client.get_quote_summary with cashflowStatementHistory and cashflowStatementHistoryQuarterly module (Quote Summary Endpoint). Each endpoint provides different data.

Symbol class provides cash flow data in either symbol.get_cash_flow (Timeseries Endpoint) or symbol.get_quote_summary_all_modules (Quote Summary Endpoint). Each endpoint provides different data.
To avoid confusion with timeseries endpoint quote summary data with cashflowStatementHistory and cashflowStatementHistoryQuarterly modules are not provided as separate methods in symbol class.

### Calendar Events x Quote Summary Endpoints

Client class provides calendar events data in either client.get_calendar_events (Calendar Events Endpoint) or in client.get_quote_summary (Quote Summary Endpoint) with calendarEvents module. Each endpoint provides different data.

Symbol class provides calendar events data in symbol.get_calendar_events (Quote Summary Endpoint).

### Response JSON

Most of the client endpoints return response json with result and error fields.

Exception to that are client.get_search, client.get_ratings and client.get_ratings, which return the direct search / ratings / analysis (respectively) results.
