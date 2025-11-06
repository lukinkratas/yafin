### AsyncSymbol x AsyncClient

`AsyncSymbol` class is more user convenient than `AsyncClient`, because it uses predefined modules for quote summary endpoint and predefined types for timeseries endpoints. It uses `AsyncClient` as a singleton (multiple symbols use shared AsyncClient instance) to save resources. Methods return result field of http response json.

`AsyncClient` class has methods defined according to the API endpoints. It uses `curl_cffi.requests.AsyncSession` under the hood. Methods return full http response json including result and error fields.

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

Quote type data is available in client.get_quote_type (Quote Type Endpoint) and in client.get_quote_summary (Quote Summary Endpoint) with quoteType module, but each endpoint provides different data.

Quote type data is available in symbol.get_quote_type (Quote Type Endpoint) and in symbol.get_quote_summary_quote_type (Quote Summary Endpoint) or symbol.get_quote_summary_all_modules, but each endpoint provides different data.

### Timeseries x Quote Summary Endpoints

Income statement data is available in client.get_timeseries (Timeseries Endpoint) with income statement types and in client.get_quote_summary with incomeStatementHistory or incomeStatementHistoryQuarterly module (Quote Summary Endpoint), but each endpoint provides different data.

Income statement data is available in symbol.get_income_statement (Timeseries Endpoint) and in symbol.get_income_statement_history or symbol.get_income_statement_history_quarterly (Quote Summary Endpoint), but each endpoint provides different data.

Balance sheet data is available in client.get_timeseries with balance sheet types (Timeseries Endpoint) and in client.get_quote_summary with balanceSheetHistory or balanceSheetHistoryQuarterly module (Quote Summary Endpoint), but each endpoint provides different data.

Balance sheet data is available in symbol.get_balance_sheet (Timeseries Endpoint) and in symbol.get_balance_sheet_history or symbol.get_balance_sheet_history_quarterly (Quote Summary Endpoint), but each endpoint provides different data.

Cash flow data is available in client.get_timeseries with cash flow types (Timeseries Endpoint) and in client.get_quote_summary with cashflowStatementHistory or cashflowStatementHistoryQuarterly module (Quote Summary Endpoint), but each endpoint provides different data.

Cash flow data is available in symbol.get_cash_flow (Timeseries Endpoint) and in symbol.get_cashflow_statement_history or symbol.get_cashflow_statement_history_quarterly (Quote Summary Endpoint), but each endpoint provides different data.

### Calendar Events x Quote Summary Endpoints

Calendar events data is available in client.get_calendar_events (Calendar Events Endpoint) and in client.get_quote_summary (Quote Summary Endpoint) with calendarEvents module, but each endpoint provides different data.

Calendar events data is available in symbol.get_calendar_events (Quote Summary Endpoint).

### Response JSON

Most of the client endpoints return response json with result and error fields.

Exception to that are client.get_search, client.get_ratings and client.get_ratings, which return the direct search / ratings / analysis (respectively) results.
