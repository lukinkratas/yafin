`AsyncClient` class has methods defined according to the API endpoints.

It uses `curl_cffi.requests.AsyncSession` under the hood.

Some endpoints are only available in the `AsyncClient` class.

:::src.yafin.AsyncClient
    options:
        members:
        - __init__
        - close 
        - get_quote
        - get_quote_summary
        - get_timeseries
        - get_options
        - get_search
        - get_recommendations
        - get_insights
        - get_market_summaries
        - get_trending
        - get_currencies
