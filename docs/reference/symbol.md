`AsyncSymbol` class is more user convinient, than `AsyncClient` and uses predefined modules for quote summary endpoint and predefined types for timeseries endpoints.

It uses `AsyncClient` as a singleton (multiple symbols use shared AsyncClient instance) to save resources.

::: src.yafin.AsyncSymbol
    options:
        members:
        - __init__
        - close
        - get_chart
        - get_quote
        - get_quote_summary_all_modules
        - get_quote_type
        - get_asset_profile
        - get_summary_profile
        - get_summary_detail
        - get_income_statement_history
        - get_income_statement_history_quarterly
        - get_balance_sheet_history
        - get_balance_sheet_history_quarterly
        - get_cashflow_statement_history
        - get_cashflow_statement_history_quarterly
        - get_esg_scores
        - get_price
        - get_default_key_statistics
        - get_financial_data
        - get_calendar_events
        - get_sec_filings
        - get_upgrade_downgrade_history
        - get_institution_ownership
        - get_fund_ownership
        - get_major_direct_holders
        - get_major_holders_breakdown
        - get_insider_transactions
        - get_insider_holders
        - get_net_share_purchase_activity
        - get_earnings
        - get_earnings_history
        - get_earnings_trend
        - get_industry_trend
        - get_index_trend
        - get_sector_trend
        - get_recommendation_trend
        - get_page_views
        - get_income_statement
        - get_balance_sheet
        - get_cash_flow
        - get_options
        - get_search
        - get_recommendations
        - get_insights
