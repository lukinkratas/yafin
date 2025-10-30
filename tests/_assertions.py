import warnings
from typing import Any

from tests._const import (
    _ANALYSIS_KEYS,
    _ASSET_PROFILE_KEYS,
    _CALENDAR_EVENTS_EARNING_KEYS,
    _CURRENCY_KEYS,
    _DEFAULT_KEY_STATISTICS_KEYS,
    _EARNINGS_HISTORY_KEYS,
    _EARNINGS_TREND_KEYS,
    _ESG_SCORES_KEYS,
    _FINANCIAL_DATA_KEYS,
    _HOLDER_KEYS,
    _INCOME_STATEMENT_HISTORY_KEYS,
    _INSIGHTS_KEYS,
    _MAJOR_HOLDERS_BREAKDOWN_KEYS,
    _MARKET_SUMMARY_KEYS,
    _NET_SHARE_PURCHASE_ACIVITY_KEYS,
    _OPTIONS_KEYS,
    _OWNERSHIP_KEYS,
    _PRICE_KEYS,
    _QUOTE_KEYS,
    _QUOTE_SUMMARY_QUOTE_TYPE_KEYS,
    _QUOTE_TYPE_KEYS,
    _RECOMMENDATIONS_TREND_KEYS,
    _SEARCH_KEYS,
    _SEC_FILING_KEYS,
    _SUMMARY_DETAIL_KEYS,
    _SUMMARY_PROFILE_KEYS,
    _TRANSACTION_KEYS,
    _TRENDING_KEYS,
    _UPGRADE_DOWNGRADE_HISTORY_KEYS,
)
from yafin.const import (
    ALL_MODULES_SET,
    ANNUAL_BALANCE_SHEET_TYPES_SET,
    ANNUAL_CASH_FLOW_TYPES_SET,
    ANNUAL_INCOME_STATEMENT_TYPES_SET,
)
from yafin.types import ResponseJson, Result


def _assert_contains_keys(data: dict[str, Any] | None, keys: list[str]) -> None:
    """Assert, that all of the keys exist in the data (dict).
    In case the key value is None, warning is raised.

    Args:
        data: dict to be checked
        keys: keys to check in data (dict)
    """
    assert data is not None

    for key in keys:
        assert key in data, f'Key {key} not found.'
        if data[key]:
            warnings.warn(f'Key {key} is empty.')


def _assert_keys_are_not_none(data: dict[str, Any] | None, keys: list[str]) -> None:
    """Assert, that all of the keys axist in the data and are not None.

    Args:
        data: dict to be checked
        keys: keys to check in data (dict)
    """
    assert data is not None

    for key in keys:
        assert data[key], f'Key {key} is empty.'


def _assert_response_json(response_json: ResponseJson, key: str) -> None:
    """Assert, that response json and its' keys."""
    assert response_json
    assert response_json[key]
    assert response_json[key]['error'] is None
    assert response_json[key]['result']


def _assert_quotes(quotes: ResponseJson, tickers: str) -> None:
    """Assertions for quotes response json."""
    tickers_list = tickers.split(',')
    quotes_list = quotes['quoteResponse']['result']
    assert len(quotes_list) == len(tickers_list)
    for ticker, quote in zip(
        sorted(tickers_list), sorted(quotes_list, key=lambda result: result['symbol'])
    ):
        _assert_quote_result(quote, ticker)


def _assert_quote_types(quote_types: ResponseJson, tickers: str) -> None:
    """Assertions for quote types response json."""
    tickers_list = tickers.split(',')
    quote_types_list = quote_types['quoteType']['result']
    assert len(quote_types_list) == len(tickers_list)
    for ticker, quote in zip(
        sorted(tickers_list),
        sorted(quote_types_list, key=lambda result: result['symbol']),
    ):
        _assert_quote_type_result(quote, ticker)


def _assert_insights(insights: ResponseJson, tickers: str) -> None:
    """Assertions for insights response json."""
    tickers_list = tickers.split(',')
    insights_list = insights['finance']['result']
    assert len(insights_list) == len(tickers_list)
    for ticker, insight in zip(
        sorted(tickers_list), sorted(insights_list, key=lambda result: result['symbol'])
    ):
        _assert_insight_result(insight, ticker)


def _assert_recommendations(recommendations: ResponseJson, tickers: str) -> None:
    """Assertions for insights recommendations json."""
    tickers_list = tickers.split(',')
    recommendations_list = recommendations['finance']['result']
    assert len(recommendations_list) == len(tickers_list)
    for ticker, insight in zip(
        sorted(tickers_list),
        sorted(recommendations_list, key=lambda result: result['symbol']),
    ):
        _assert_recommendation_result(insight, ticker)


def _assert_market_summary_results(
    market_summary_results: list[Result],
) -> None:
    """Assertions for result field of market_summaries response json."""
    assert market_summary_results
    for market_summary in market_summary_results:
        _assert_contains_keys(market_summary, _MARKET_SUMMARY_KEYS)


def _assert_trending_result(trending_result: Result) -> None:
    """Assertions for result field of trending response json."""
    assert trending_result
    _assert_contains_keys(trending_result, _TRENDING_KEYS)


def _assert_currencies_results(currencies_results: list[Result]) -> None:
    """Assertions for result field of currencies response json."""
    assert currencies_results
    for currency in currencies_results:
        _assert_contains_keys(currency, _CURRENCY_KEYS)


def _assert_client_calendar_events_result(calendar_events: Result) -> None:
    """Assertions for result field of currencies response json."""
    assert calendar_events
    _assert_contains_keys(calendar_events, ['economicEvents'])


def _assert_chart_result(chart_result: Result, ticker: str) -> None:
    """Assertions for result field of chart response json."""
    assert chart_result
    _assert_keys_are_not_none(chart_result, ['meta', 'timestamp', 'indicators'])
    assert chart_result['meta']['symbol'] == ticker
    _assert_keys_are_not_none(
        chart_result['indicators']['quote'][0],
        ['open', 'close', 'volume', 'low', 'high'],
    )
    assert chart_result['indicators']['adjclose'][0]['adjclose']


def _assert_quote_result(quote_result: Result, ticker: str) -> None:
    """Assertions for result field of quote response json."""
    assert quote_result
    _assert_contains_keys(quote_result, _QUOTE_KEYS)
    assert quote_result['symbol'] == ticker


def _assert_quote_type_result(quote_type_result: Result, ticker: str) -> None:
    assert quote_type_result
    _assert_contains_keys(quote_type_result, _QUOTE_TYPE_KEYS)
    assert quote_type_result['symbol'] == ticker


def _assert_quote_summary_all_modules_result(
    quote_summary_all_modules: Result,
) -> None:
    """Assertions for result field of quote summary with all modules response json."""
    assert quote_summary_all_modules
    assert sorted(quote_summary_all_modules) == sorted(ALL_MODULES_SET)


def _assert_asset_profile(asset_profile: Result) -> None:
    """Assertions for assert profile response json."""
    assert asset_profile
    _assert_contains_keys(asset_profile, _ASSET_PROFILE_KEYS)


def _assert_quote_summary_quote_type(quote_type: Result) -> None:
    """Assertions for quote type response json."""
    assert quote_type
    _assert_contains_keys(quote_type, _QUOTE_SUMMARY_QUOTE_TYPE_KEYS)


def _assert_summary_profile(summary_profile: Result) -> None:
    """Assertions for summary profile response json."""
    assert summary_profile
    _assert_contains_keys(summary_profile, _SUMMARY_PROFILE_KEYS)


def _assert_summary_detail(summary_detail: Result) -> None:
    """Assertions for summary detail response json."""
    assert summary_detail
    _assert_contains_keys(summary_detail, _SUMMARY_DETAIL_KEYS)


def _assert_income_statement_history(
    income_statement_history: list[Result],
) -> None:
    """Assertions for income statement history response json."""
    assert income_statement_history
    for period in income_statement_history:
        _assert_contains_keys(period, _INCOME_STATEMENT_HISTORY_KEYS)


def _assert_income_statement_history_quarterly(
    income_statement_history_quarterly: list[Result],
) -> None:
    """Assertions for income statement quarterly history response json."""
    assert income_statement_history_quarterly
    for period in income_statement_history_quarterly:
        _assert_contains_keys(period, _INCOME_STATEMENT_HISTORY_KEYS)


def _assert_balance_sheet_history(balance_sheet_history: list[Result]) -> None:
    """Assertions for balance sheet history response json."""
    assert balance_sheet_history
    for period in balance_sheet_history:
        _assert_contains_keys(period, ['maxAge', 'endDate'])


def _assert_balance_sheet_history_quarterly(
    balance_sheet_history_quarterly: list[Result],
) -> None:
    """Assertions for balance sheet quarterly history response json."""
    assert balance_sheet_history_quarterly
    for period in balance_sheet_history_quarterly:
        _assert_contains_keys(period, ['maxAge', 'endDate'])


def _assert_cashflow_statement_history(
    cashflow_statement_history: list[Result],
) -> None:
    """Assertions for cash flow history response json."""
    assert cashflow_statement_history
    for period in cashflow_statement_history:
        _assert_contains_keys(period, ['maxAge', 'endDate', 'netIncome'])


def _assert_cashflow_statement_history_quarterly(
    cashflow_statement_history_quarterly: list[Result],
) -> None:
    """Assertions for cash flow quarterly history response json."""
    assert cashflow_statement_history_quarterly
    for period in cashflow_statement_history_quarterly:
        _assert_contains_keys(period, ['maxAge', 'endDate', 'netIncome'])


def _assert_esg_scores(esg_scores: Result) -> None:
    """Assertions for esg scores response json."""
    assert esg_scores
    _assert_contains_keys(esg_scores, _ESG_SCORES_KEYS)


def _assert_price(price: Result) -> None:
    """Assertions for price response json."""
    assert price
    _assert_contains_keys(price, _PRICE_KEYS)


def _assert_default_key_statistics(default_key_statistics: Result) -> None:
    """Assertions for default key statistics response json."""
    assert default_key_statistics
    _assert_contains_keys(default_key_statistics, _DEFAULT_KEY_STATISTICS_KEYS)


def _assert_financial_data(financial_data: Result) -> None:
    """Assertions for financial data response json."""
    assert financial_data
    _assert_contains_keys(financial_data, _FINANCIAL_DATA_KEYS)


def _assert_symbol_calendar_events(calendar_events: Result) -> None:
    """Assertions for calendar events response json."""
    assert calendar_events
    _assert_contains_keys(
        calendar_events, ['maxAge', 'earnings', 'exDividendDate', 'dividendDate']
    )
    _assert_contains_keys(calendar_events['earnings'], _CALENDAR_EVENTS_EARNING_KEYS)


def _assert_sec_filings(sec_filings: Result) -> None:
    """Assertions for sec filings response json."""
    assert sec_filings
    _assert_contains_keys(sec_filings, ['maxAge', 'filings'])
    for sec_filing in sec_filings['filings']:
        _assert_contains_keys(sec_filing, _SEC_FILING_KEYS)


def _assert_upgrade_downgrade_history(upgrade_downgrade_history: list[Result]) -> None:
    """Assertions for upgrade downgrade history response json."""
    assert upgrade_downgrade_history
    for upgrade_downgrade in upgrade_downgrade_history:
        _assert_contains_keys(upgrade_downgrade, _UPGRADE_DOWNGRADE_HISTORY_KEYS)


def _assert_institution_ownership(institution_ownership: list[Result]) -> None:
    """Assertions for institution ownership response json."""
    assert institution_ownership
    for ownership in institution_ownership:
        _assert_contains_keys(ownership, _OWNERSHIP_KEYS)


def _assert_fund_ownership(fund_ownership: list[Result]) -> None:
    """Assertions for fund ownership response json."""
    assert fund_ownership
    for ownership in fund_ownership:
        _assert_contains_keys(ownership, _OWNERSHIP_KEYS)


def _assert_major_direct_holders(major_direct_holders: Result) -> None:
    """Assertions for major direct holders response json."""
    assert major_direct_holders
    _assert_contains_keys(major_direct_holders, ['holders', 'maxAge'])


def _assert_major_holders_breakdown(major_holders_breakdown: Result) -> None:
    """Assertions for major direct breakdown response json."""
    assert major_holders_breakdown
    _assert_contains_keys(major_holders_breakdown, _MAJOR_HOLDERS_BREAKDOWN_KEYS)


def _assert_insider_transactions(insider_transactions: list[Result]) -> None:
    """Assertions for insider transactions response json."""
    assert insider_transactions
    for transaction in insider_transactions:
        _assert_contains_keys(transaction, _TRANSACTION_KEYS)


def _assert_insider_holders(insider_holders: list[Result]) -> None:
    """Assertions for insider holders response json."""
    assert insider_holders
    for holder in insider_holders:
        _assert_contains_keys(holder, _HOLDER_KEYS)


def _assert_net_share_purchase_activity(net_share_purchase_activity: Result) -> None:
    """Assertions for net share purchase activity response json."""
    assert net_share_purchase_activity
    _assert_contains_keys(net_share_purchase_activity, _NET_SHARE_PURCHASE_ACIVITY_KEYS)


def _assert_earnings(earnings: Result) -> None:
    """Assertions for earnings response json."""
    assert earnings
    _assert_contains_keys(
        earnings,
        ['maxAge', 'earningsChart', 'financialsChart', 'financialCurrency'],
    )


def _assert_earnings_history(earnings_history: list[Result]) -> None:
    """Assertions for earnings history response json."""
    assert earnings_history
    for period in earnings_history:
        _assert_contains_keys(period, _EARNINGS_HISTORY_KEYS)


def _assert_earnings_trend(earnings_trend: list[Result]) -> None:
    """Assertions for earnings trend response json."""
    assert earnings_trend
    for trend in earnings_trend:
        _assert_contains_keys(trend, _EARNINGS_TREND_KEYS)


def _assert_industry_trend(industry_trend: Result) -> None:
    """Assertions for industry trend response json."""
    assert industry_trend
    _assert_contains_keys(industry_trend, ['maxAge', 'symbol', 'estimates'])


def _assert_index_trend(index_trend: Result) -> None:
    """Assertions for index trend response json."""
    assert index_trend
    _assert_contains_keys(index_trend, ['maxAge', 'symbol', 'estimates'])


def _assert_sector_trend(sector_trend: Result) -> None:
    """Assertions for sector trend response json."""
    assert sector_trend
    _assert_contains_keys(sector_trend, ['maxAge', 'symbol', 'estimates'])


def _assert_recommendation_trend(recommendation_trend: list[Result]) -> None:
    """Assertions for recommendation trend response json."""
    assert recommendation_trend
    for trend in recommendation_trend:
        _assert_contains_keys(trend, _RECOMMENDATIONS_TREND_KEYS)


def _assert_page_views(page_views: Result) -> None:
    """Assertions for page views response json."""
    assert page_views
    _assert_contains_keys(
        page_views, ['shortTermTrend', 'midTermTrend', 'longTermTrend', 'maxAge']
    )


def _assert_annual_income_stmt_result(annual_income_stmt_result: Result) -> None:
    """Assertions for result field of annual income statement response json."""
    assert annual_income_stmt_result
    assert sorted(ANNUAL_INCOME_STATEMENT_TYPES_SET) == sorted(
        annual_income_stmt_result['meta']['type']
    )


def _assert_annual_balance_sheet_result(annual_balance_sheet_result: Result) -> None:
    """Assertions for result field of annual balance sheet response json."""
    assert annual_balance_sheet_result
    assert sorted(ANNUAL_BALANCE_SHEET_TYPES_SET) == sorted(
        annual_balance_sheet_result['meta']['type']
    )


def _assert_annual_cash_flow_result(annual_cash_flow_result: Result) -> None:
    """Assertions for result field of annual cash flow response json."""
    assert annual_cash_flow_result
    assert sorted(ANNUAL_CASH_FLOW_TYPES_SET) == sorted(
        annual_cash_flow_result['meta']['type']
    )


def _assert_options_result(options_result: Result, ticker: str) -> None:
    """Assertions for result field of options response json."""
    assert options_result
    _assert_contains_keys(options_result, _OPTIONS_KEYS)
    assert options_result['underlyingSymbol'] == ticker
    assert options_result['quote']['symbol'] == ticker


def _assert_recommendation_result(recommendation_result: Result, ticker: str) -> None:
    """Assertions for result field of recommendations response json."""
    assert recommendation_result
    _assert_contains_keys(recommendation_result, ['symbol', 'recommendedSymbols'])
    assert recommendation_result['symbol'] == ticker


def _assert_insight_result(insights_result: Result, ticker: str) -> None:
    """Assertions for result field of insights response json."""
    assert insights_result
    _assert_contains_keys(insights_result, _INSIGHTS_KEYS)
    assert insights_result['symbol'] == ticker


def _assert_search_result(search: ResponseJson) -> None:
    """Assertions for search response json."""
    assert search
    _assert_contains_keys(search, _SEARCH_KEYS)


def _assert_ratings_result(ratings: ResponseJson) -> None:
    """Assertions for search response json."""
    assert ratings
    _assert_contains_keys(ratings, ['dir', 'mm', 'pt', 'fin_score'])


def _assert_analysis_result(analysis: ResponseJson) -> None:
    """Assertions for search response json."""
    assert analysis
    _assert_contains_keys(analysis, _ANALYSIS_KEYS)
