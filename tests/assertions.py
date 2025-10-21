import warnings
from typing import Any

from tests.const import (
    ASSET_PROFILE_KEYS,
    CALENDAR_EVENTS_EARNING_KEYS,
    CURRENCY_KEYS,
    DEFAULT_KEY_STATISTICS_KEYS,
    EARNINGS_HISTORY_KEYS,
    EARNINGS_TREND_KEYS,
    ESG_SCORES_KEYS,
    FINANCIAL_DATA_KEYS,
    HOLDER_KEYS,
    INCOME_STATEMENT_HISTORY_KEYS,
    INSIGHTS_KEYS,
    MAJOR_HOLDERS_BREAKDOWN_KEYS,
    MARKET_SUMMARY_KEYS,
    NET_SHARE_PURCHASE_ACIVITY_KEYS,
    OPTIONS_KEYS,
    OWNERSHIP_KEYS,
    PRICE_KEYS,
    QUOTE_KEYS,
    QUOTE_TYPE_KEYS,
    RECOMMENDATIONS_TREND_KEYS,
    SEARCH_KEYS,
    SEC_FILING_KEYS,
    SUMMARY_DETAIL_KEYS,
    SUMMARY_PROFILE_KEYS,
    TRANSACTION_KEYS,
    TRENDING_KEYS,
    UPGRADE_DOWNGRADE_HISTORY_KEYS,
)
from yafin.const import ALL_MODULES
from yafin.utils import get_types_with_frequency


def assert_contains_keys(data: dict[str, Any], keys: list[str]) -> None:
    """Assert, that all of the keys exist in the data (dict).
    In case the key value is None, warning is raised.

    Args:
        data: dict to be checked
        keys: keys to check in data (dict)
    """
    for key in keys:
        assert key in data, f'Key {key} not found.'
        if data[key]:
            warnings.warn(f'Key {key} is empty.')


def assert_keys_are_not_none(data: dict[str, Any], keys: list[str]) -> None:
    """Assert, that all of the keys axist in the data and are not None.

    Args:
        data: dict to be checked
        keys: keys to check in data (dict)
    """
    for key in keys:
        assert data[key], f'Key {key} is empty.'


def assert_response_json(response_json: dict[str, Any], key: str) -> None:
    """Assert, that response json and its' keys."""
    assert response_json
    assert response_json[key]
    assert response_json[key]['error'] is None
    assert response_json[key]['result']


def assert_search(search: dict[str, Any]) -> None:
    """Assertions for search response json."""
    assert search
    assert_contains_keys(search, SEARCH_KEYS)


def assert_quotes(quotes: dict[str, Any], tickers: str) -> None:
    """Assertions for quotes response json."""
    tickers_list = tickers.split(',')
    quotes_list = quotes['quoteResponse']['result']
    assert len(quotes_list) == len(tickers_list)
    for ticker, quote in zip(
        sorted(tickers_list), sorted(quotes_list, key=lambda result: result['symbol'])
    ):
        assert_quote_result(quote, ticker)


def assert_market_summaries_result(
    market_summaries_result: list[dict[str, Any]],
) -> None:
    """Assertions for result field of market_summaries response json."""
    assert market_summaries_result
    for market_summary in market_summaries_result:
        assert_contains_keys(market_summary, MARKET_SUMMARY_KEYS)


def assert_trending_result(trending_result: dict[str, Any]) -> None:
    """Assertions for result field of trending response json."""
    assert trending_result
    assert_contains_keys(trending_result, TRENDING_KEYS)


def assert_currencies_result(currencies_result: list[dict[str, Any]]) -> None:
    """Assertions for result field of currencies response json."""
    assert currencies_result
    for currency in currencies_result:
        assert_contains_keys(currency, CURRENCY_KEYS)


def assert_chart_result(chart_result: dict[str, Any], ticker: str) -> None:
    """Assertions for result field of chart response json."""
    assert chart_result
    assert_keys_are_not_none(chart_result, ['meta', 'timestamp', 'indicators'])
    assert chart_result['meta']['symbol'] == ticker
    assert_keys_are_not_none(
        chart_result['indicators']['quote'][0],
        ['open', 'close', 'volume', 'low', 'high'],
    )
    assert chart_result['indicators']['adjclose'][0]['adjclose']


def assert_quote_result(quote_result: dict[str, Any], ticker: str) -> None:
    """Assertions for result field of quote response json."""
    assert quote_result
    assert_contains_keys(quote_result, QUOTE_KEYS)
    assert quote_result['symbol'] == ticker


def assert_quote_summary_all_modules_result(
    quote_summary_all_modules: dict[str, Any],
) -> None:
    """Assertions for result field of quote summary with all modules response json."""
    assert quote_summary_all_modules
    assert sorted(quote_summary_all_modules) == sorted(ALL_MODULES)


def assert_asset_profile(asset_profile: dict[str, Any]) -> None:
    """Assertions for assert profile response json."""
    assert asset_profile
    assert_contains_keys(asset_profile, ASSET_PROFILE_KEYS)


def assert_quote_type(quote_type: dict[str, Any]) -> None:
    """Assertions for quote type response json."""
    assert quote_type
    assert_contains_keys(quote_type, QUOTE_TYPE_KEYS)


def assert_summary_profile(summary_profile: dict[str, Any]) -> None:
    """Assertions for summary profile response json."""
    assert summary_profile
    assert_contains_keys(summary_profile, SUMMARY_PROFILE_KEYS)


def assert_summary_detail(summary_detail: dict[str, Any]) -> None:
    """Assertions for summary detail response json."""
    assert summary_detail
    assert_contains_keys(summary_detail, SUMMARY_DETAIL_KEYS)


def assert_income_statement_history(
    income_statement_history: list[dict[str, Any]],
) -> None:
    """Assertions for income statement history response json."""
    assert income_statement_history
    for period in income_statement_history:
        assert_contains_keys(period, INCOME_STATEMENT_HISTORY_KEYS)


def assert_income_statement_history_quarterly(
    income_statement_history_quarterly: list[dict[str, Any]],
) -> None:
    """Assertions for income statement quarterly history response json."""
    assert income_statement_history_quarterly
    for period in income_statement_history_quarterly:
        assert_contains_keys(period, INCOME_STATEMENT_HISTORY_KEYS)


def assert_balance_sheet_history(balance_sheet_history: list[dict[str, Any]]) -> None:
    """Assertions for balance sheet history response json."""
    assert balance_sheet_history
    for period in balance_sheet_history:
        assert_contains_keys(period, ['maxAge', 'endDate'])


def assert_balance_sheet_history_quarterly(
    balance_sheet_history_quarterly: list[dict[str, Any]],
) -> None:
    """Assertions for balance sheet quarterly history response json."""
    assert balance_sheet_history_quarterly
    for period in balance_sheet_history_quarterly:
        assert_contains_keys(period, ['maxAge', 'endDate'])


def assert_cashflow_statement_history(
    cashflow_statement_history: list[dict[str, Any]],
) -> None:
    """Assertions for cash flow history response json."""
    assert cashflow_statement_history
    for period in cashflow_statement_history:
        assert_contains_keys(period, ['maxAge', 'endDate', 'netIncome'])


def assert_cashflow_statement_history_quarterly(
    cashflow_statement_history_quarterly: list[dict[str, Any]],
) -> None:
    """Assertions for cash flow quarterly history response json."""
    assert cashflow_statement_history_quarterly
    for period in cashflow_statement_history_quarterly:
        assert_contains_keys(period, ['maxAge', 'endDate', 'netIncome'])


def assert_esg_scores(esg_scores: dict[str, Any]) -> None:
    """Assertions for esg scores response json."""
    assert esg_scores
    assert_contains_keys(esg_scores, ESG_SCORES_KEYS)


def assert_price(price: dict[str, Any]) -> None:
    """Assertions for price response json."""
    assert price
    assert_contains_keys(price, PRICE_KEYS)


def assert_default_key_statistics(
    default_key_statistics: dict[str, Any],
) -> None:
    """Assertions for default key statistics response json."""
    assert default_key_statistics
    assert_contains_keys(default_key_statistics, DEFAULT_KEY_STATISTICS_KEYS)


def assert_financial_data(financial_data: dict[str, Any]) -> None:
    """Assertions for financial data response json."""
    assert financial_data
    assert_contains_keys(financial_data, FINANCIAL_DATA_KEYS)


def assert_calendar_events(calendar_events: dict[str, Any]) -> None:
    """Assertions for calendar events response json."""
    assert calendar_events
    assert_contains_keys(
        calendar_events, ['maxAge', 'earnings', 'exDividendDate', 'dividendDate']
    )
    assert_contains_keys(calendar_events['earnings'], CALENDAR_EVENTS_EARNING_KEYS)


def assert_sec_filings(sec_filings: dict[str, Any]) -> None:
    """Assertions for sec filings response json."""
    assert sec_filings
    assert_contains_keys(sec_filings, ['maxAge', 'filings'])
    for sec_filing in sec_filings['filings']:
        assert_contains_keys(sec_filing, SEC_FILING_KEYS)


def assert_upgrade_downgrade_history(
    upgrade_downgrade_history: list[dict[str, Any]],
) -> None:
    """Assertions for upgrade downgrade history response json."""
    assert upgrade_downgrade_history
    for upgrade_downgrade in upgrade_downgrade_history:
        assert_contains_keys(upgrade_downgrade, UPGRADE_DOWNGRADE_HISTORY_KEYS)


def assert_institution_ownership(institution_ownership: list[dict[str, Any]]) -> None:
    """Assertions for institution ownership response json."""
    assert institution_ownership
    for ownership in institution_ownership:
        assert_contains_keys(ownership, OWNERSHIP_KEYS)


def assert_fund_ownership(fund_ownership: list[dict[str, Any]]) -> None:
    """Assertions for fund ownership response json."""
    assert fund_ownership
    for ownership in fund_ownership:
        assert_contains_keys(ownership, OWNERSHIP_KEYS)


def assert_major_direct_holders(major_direct_holders: dict[str, Any]) -> None:
    """Assertions for major direct holders response json."""
    assert major_direct_holders
    assert_contains_keys(major_direct_holders, ['holders', 'maxAge'])


def assert_major_holders_breakdown(
    major_holders_breakdown: dict[str, Any],
) -> None:
    """Assertions for major direct breakdown response json."""
    assert major_holders_breakdown
    assert_contains_keys(major_holders_breakdown, MAJOR_HOLDERS_BREAKDOWN_KEYS)


def assert_insider_transactions(insider_transactions: list[dict[str, Any]]) -> None:
    """Assertions for insider transactions response json."""
    assert insider_transactions
    for transaction in insider_transactions:
        assert_contains_keys(transaction, TRANSACTION_KEYS)


def assert_insider_holders(insider_holders: list[dict[str, Any]]) -> None:
    """Assertions for insider holders response json."""
    assert insider_holders
    for holder in insider_holders:
        assert_contains_keys(holder, HOLDER_KEYS)


def assert_net_share_purchase_activity(
    net_share_purchase_activity: dict[str, Any],
) -> None:
    """Assertions for net share purchase activity response json."""
    assert net_share_purchase_activity
    assert_contains_keys(net_share_purchase_activity, NET_SHARE_PURCHASE_ACIVITY_KEYS)


def assert_earnings(earnings: dict[str, Any]) -> None:
    """Assertions for earnings response json."""
    assert earnings
    assert_contains_keys(
        earnings,
        ['maxAge', 'earningsChart', 'financialsChart', 'financialCurrency'],
    )


def assert_earnings_history(earnings_history: list[dict[str, Any]]) -> None:
    """Assertions for earnings history response json."""
    assert earnings_history
    for period in earnings_history:
        assert_contains_keys(period, EARNINGS_HISTORY_KEYS)


def assert_earnings_trend(earnings_trend: list[dict[str, Any]]) -> None:
    """Assertions for earnings trend response json."""
    assert earnings_trend
    for trend in earnings_trend:
        assert_contains_keys(trend, EARNINGS_TREND_KEYS)


def assert_industry_trend(industry_trend: dict[str, Any]) -> None:
    """Assertions for industry trend response json."""
    assert industry_trend
    assert_contains_keys(industry_trend, ['maxAge', 'symbol', 'estimates'])


def assert_index_trend(index_trend: dict[str, Any]) -> None:
    """Assertions for index trend response json."""
    assert index_trend
    assert_contains_keys(index_trend, ['maxAge', 'symbol', 'estimates'])


def assert_sector_trend(sector_trend: dict[str, Any]) -> None:
    """Assertions for sector trend response json."""
    assert sector_trend
    assert_contains_keys(sector_trend, ['maxAge', 'symbol', 'estimates'])


def assert_recommendation_trend(recommendation_trend: list[dict[str, Any]]) -> None:
    """Assertions for recommendation trend response json."""
    assert recommendation_trend
    for trend in recommendation_trend:
        assert_contains_keys(trend, RECOMMENDATIONS_TREND_KEYS)


def assert_page_views(page_views: dict[str, Any]) -> None:
    """Assertions for page views response json."""
    assert page_views
    assert_contains_keys(
        page_views, ['shortTermTrend', 'midTermTrend', 'longTermTrend', 'maxAge']
    )


def assert_annual_income_stmt_result(
    annual_income_stmt_result: list[dict[str, Any]],
) -> None:
    """Assertions for result field of annual income statement response json."""
    assert annual_income_stmt_result
    types = get_types_with_frequency(frequency='annual', typ='income_statement')
    expected_types_list = types.split(',')
    annual_income_stmt_types_list = [
        field['meta']['type'][0] for field in annual_income_stmt_result
    ]
    assert sorted(expected_types_list) == sorted(annual_income_stmt_types_list)


def assert_annual_balance_sheet_result(
    annual_balance_sheet_result: list[dict[str, Any]],
) -> None:
    """Assertions for result field of annual balance sheet response json."""
    assert annual_balance_sheet_result
    types = get_types_with_frequency(frequency='annual', typ='balance_sheet')
    expected_types_list = types.split(',')
    annual_balance_sheet_types_list = [
        field['meta']['type'][0] for field in annual_balance_sheet_result
    ]
    assert sorted(expected_types_list) == sorted(annual_balance_sheet_types_list)


def assert_annual_cash_flow_result(
    annual_cash_flow_result: list[dict[str, Any]],
) -> None:
    """Assertions for result field of annual cash flow response json."""
    assert annual_cash_flow_result
    types = get_types_with_frequency(frequency='annual', typ='cash_flow')
    expected_types_list = types.split(',')
    annual_cash_flow_types_list = [
        field['meta']['type'][0] for field in annual_cash_flow_result
    ]
    assert sorted(expected_types_list) == sorted(annual_cash_flow_types_list)


def assert_options_result(options_result: dict[str, Any], ticker: str) -> None:
    """Assertions for result field of options response json."""
    assert options_result
    assert_contains_keys(options_result, OPTIONS_KEYS)
    assert options_result['underlyingSymbol'] == ticker
    assert options_result['quote']['symbol'] == ticker


def assert_recommendations_result(
    recommendations_result: dict[str, Any], ticker: str
) -> None:
    """Assertions for result field of recommendations response json."""
    assert recommendations_result
    assert_contains_keys(recommendations_result, ['symbol', 'recommendedSymbols'])
    assert recommendations_result['symbol'] == ticker


def assert_insights_result(insights_result: dict[str, Any], ticker: str) -> None:
    """Assertions for result field of insights response json."""
    assert insights_result
    assert_contains_keys(insights_result, INSIGHTS_KEYS)
    assert insights_result['symbol'] == ticker
