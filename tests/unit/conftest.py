import json
import pathlib
from typing import Any

import pytest

FIXTURES_PATH = pathlib.Path(__file__).resolve().parent.joinpath('fixtures')


@pytest.fixture
def chart_json_mock() -> dict[str, Any]:
    """Mock chart response json with data for META, 1y, 1d."""
    return json.loads(FIXTURES_PATH.joinpath('chart.json').read_text())


@pytest.fixture
def quote_json_mock() -> dict[str, Any]:
    """Mock get_quote response json with data for META."""
    return json.loads(FIXTURES_PATH.joinpath('quotes.json').read_text())


@pytest.fixture
def search_json_mock() -> dict[str, Any]:
    """Mock search response json with data for META."""
    return json.loads(FIXTURES_PATH.joinpath('search.json').read_text())


@pytest.fixture
def options_json_mock() -> dict[str, Any]:
    """Mock options response json with data for META."""
    return json.loads(FIXTURES_PATH.joinpath('options.json').read_text())


@pytest.fixture
def recommendations_json_mock() -> dict[str, Any]:
    """Mock recommendations response json with data for META."""
    return json.loads(FIXTURES_PATH.joinpath('recommendations.json').read_text())


@pytest.fixture
def insights_json_mock() -> dict[str, Any]:
    """Mock insights response json with data for META."""
    return json.loads(FIXTURES_PATH.joinpath('insights.json').read_text())


@pytest.fixture
def market_summaries_json_mock() -> dict[str, Any]:
    """Mock market summaries response."""
    return json.loads(FIXTURES_PATH.joinpath('market_summaries.json').read_text())


@pytest.fixture
def trending_json_mock() -> dict[str, Any]:
    """Mock trending response json."""
    return json.loads(FIXTURES_PATH.joinpath('trending.json').read_text())


@pytest.fixture
def currencies_json_mock() -> dict[str, Any]:
    """Mock currencies response json."""
    return json.loads(FIXTURES_PATH.joinpath('currencies.json').read_text())


@pytest.fixture
def quote_summary_all_modules_json_mock() -> dict[str, Any]:
    """Mock quote_summary respons json with all modules data for META."""
    return json.loads(FIXTURES_PATH.joinpath('qs_all_modules.json').read_text())


@pytest.fixture
def timeseries_income_statement_json_mock() -> dict[str, Any]:
    """Mock timeseries response json with annual income statement data for META."""
    return json.loads(FIXTURES_PATH.joinpath('ts_income_statement.json').read_text())


@pytest.fixture
def timeseries_balance_sheet_json_mock() -> dict[str, Any]:
    """Mock timeseries response json with annual balance sheet data for META."""
    return json.loads(FIXTURES_PATH.joinpath('ts_balance_sheet.json').read_text())


@pytest.fixture
def timeseries_cash_flow_json_mock() -> dict[str, Any]:
    """Mock timeseries response json with annual cash flow data for META."""
    return json.loads(FIXTURES_PATH.joinpath('ts_cash_flow.json').read_text())


@pytest.fixture
def asset_profile_json_mock() -> dict[str, Any]:
    """Mock quote summary response json with asset profile data for META."""
    return json.loads(FIXTURES_PATH.joinpath('qs_asset_profile.json').read_text())


@pytest.fixture
def quote_type_json_mock() -> dict[str, Any]:
    """Mock quote summary response json with quote type data for META."""
    return json.loads(FIXTURES_PATH.joinpath('qs_quote_type.json').read_text())


@pytest.fixture
def summary_profile_json_mock() -> dict[str, Any]:
    """Mock quote summary response json with summary profile data for META."""
    return json.loads(FIXTURES_PATH.joinpath('qs_summary_profile.json').read_text())


@pytest.fixture
def summary_detail_json_mock() -> dict[str, Any]:
    """Mock quote summary response json with summary detail data for META."""
    return json.loads(FIXTURES_PATH.joinpath('qs_summary_detail.json').read_text())


@pytest.fixture
def income_statement_history_json_mock() -> dict[str, Any]:
    """Mock quote summary response json with income statement history data for META."""
    return json.loads(
        FIXTURES_PATH.joinpath('qs_income_statement_history.json').read_text()
    )


@pytest.fixture
def income_statement_history_quarterly_json_mock() -> dict[str, Any]:
    """Mock quote summary response json with income statement history quarterly data for META."""  # noqa: E501
    return json.loads(
        FIXTURES_PATH.joinpath('qs_income_statement_history_quarterly.json').read_text()
    )


@pytest.fixture
def balance_sheet_history_json_mock() -> dict[str, Any]:
    """Mock quote summary response json with balance sheet history data for META."""
    return json.loads(
        FIXTURES_PATH.joinpath('qs_balance_sheet_history.json').read_text()
    )


@pytest.fixture
def balance_sheet_history_quarterly_json_mock() -> dict[str, Any]:
    """Mock quote summary response json with balance sheet history quarterly data for META."""  # noqa: E501
    return json.loads(
        FIXTURES_PATH.joinpath('qs_balance_sheet_history_quarterly.json').read_text()
    )


@pytest.fixture
def cashflow_statement_history_json_mock() -> dict[str, Any]:
    """Mock quote summary response json with cash flow history data for META."""
    return json.loads(
        FIXTURES_PATH.joinpath('qs_cashflow_statement_history.json').read_text()
    )


@pytest.fixture
def cashflow_statement_history_quarterly_json_mock() -> dict[str, Any]:
    """Mock quote summary response json with cash flow history quarterly data for META."""  # noqa: E501
    return json.loads(
        FIXTURES_PATH.joinpath(
            'qs_cashflow_statement_history_quarterly.json'
        ).read_text()
    )


@pytest.fixture
def esg_scores_json_mock() -> dict[str, Any]:
    """Mock quote summary response json with esg scores data for META."""
    return json.loads(FIXTURES_PATH.joinpath('qs_esg_scores.json').read_text())


@pytest.fixture
def price_json_mock() -> dict[str, Any]:
    """Mock quote summary response json with price data for META."""
    return json.loads(FIXTURES_PATH.joinpath('qs_price.json').read_text())


@pytest.fixture
def default_key_statistics_json_mock() -> dict[str, Any]:
    """Mock quote summary response json with default key statistics data for META."""
    return json.loads(
        FIXTURES_PATH.joinpath('qs_default_key_statistics.json').read_text()
    )


@pytest.fixture
def financial_data_json_mock() -> dict[str, Any]:
    """Mock quote summary response json with financial data for META."""
    return json.loads(FIXTURES_PATH.joinpath('qs_financial_data.json').read_text())


@pytest.fixture
def calendar_events_json_mock() -> dict[str, Any]:
    """Mock quote summary response json with calendar events data for META."""
    return json.loads(FIXTURES_PATH.joinpath('qs_calendar_events.json').read_text())


@pytest.fixture
def sec_filings_json_mock() -> dict[str, Any]:
    """Mock quote summary response json with sec filings data for META."""
    return json.loads(FIXTURES_PATH.joinpath('qs_sec_filings.json').read_text())


@pytest.fixture
def upgrade_downgrade_history_json_mock() -> dict[str, Any]:
    """Mock quote summary response json with upgrade downgrade history data for META."""
    return json.loads(
        FIXTURES_PATH.joinpath('qs_upgrade_downgrade_history.json').read_text()
    )


@pytest.fixture
def institution_ownership_json_mock() -> dict[str, Any]:
    """Mock quote summary response json with institution ownership data for META."""
    return json.loads(
        FIXTURES_PATH.joinpath('qs_institution_ownership.json').read_text()
    )


@pytest.fixture
def fund_ownership_json_mock() -> dict[str, Any]:
    """Mock quote summary response json with fund ownership data for META."""
    return json.loads(FIXTURES_PATH.joinpath('qs_fund_ownership.json').read_text())


@pytest.fixture
def major_direct_holders_json_mock() -> dict[str, Any]:
    """Mock quote summary response json with major direct holders data for META."""
    return json.loads(
        FIXTURES_PATH.joinpath('qs_major_direct_holders.json').read_text()
    )


@pytest.fixture
def major_holders_breakdown_json_mock() -> dict[str, Any]:
    """Mock quote summary response json with major holders breakdown data for META."""
    return json.loads(
        FIXTURES_PATH.joinpath('qs_major_holders_breakdown.json').read_text()
    )


@pytest.fixture
def insider_transactions_json_mock() -> dict[str, Any]:
    """Mock quote summary response json with insider transactions data for META."""
    return json.loads(
        FIXTURES_PATH.joinpath('qs_insider_transactions.json').read_text()
    )


@pytest.fixture
def insider_holders_json_mock() -> dict[str, Any]:
    """Mock quote summary response json with insider holders data for META."""
    return json.loads(FIXTURES_PATH.joinpath('qs_insider_holders.json').read_text())


@pytest.fixture
def net_share_purchase_activity_json_mock() -> dict[str, Any]:
    """Mock quote summary response json with net share purchase activity data for META."""  # noqa: E501
    return json.loads(
        FIXTURES_PATH.joinpath('qs_net_share_purchase_activity.json').read_text()
    )


@pytest.fixture
def earnings_json_mock() -> dict[str, Any]:
    """Mock quote summary response json with net earnings data for META."""
    return json.loads(FIXTURES_PATH.joinpath('qs_earnings.json').read_text())


@pytest.fixture
def earnings_history_json_mock() -> dict[str, Any]:
    """Mock quote summary response json with net earnings history data for META."""
    return json.loads(FIXTURES_PATH.joinpath('qs_earnings_history.json').read_text())


@pytest.fixture
def earnings_trend_json_mock() -> dict[str, Any]:
    """Mock quote summary response json with net earnings trend data for META."""
    return json.loads(FIXTURES_PATH.joinpath('qs_earnings_trend.json').read_text())


@pytest.fixture
def industry_trend_json_mock() -> dict[str, Any]:
    """Mock quote summary response json with net industry trend data for META."""
    return json.loads(FIXTURES_PATH.joinpath('qs_industry_trend.json').read_text())


@pytest.fixture
def index_trend_json_mock() -> dict[str, Any]:
    """Mock quote summary response json with net index trend data for META."""
    return json.loads(FIXTURES_PATH.joinpath('qs_index_trend.json').read_text())


@pytest.fixture
def sector_trend_json_mock() -> dict[str, Any]:
    """Mock quote summary response json with net sector trend data for META."""
    return json.loads(FIXTURES_PATH.joinpath('qs_sector_trend.json').read_text())


@pytest.fixture
def recommendation_trend_json_mock() -> dict[str, Any]:
    """Mock quote summary response json with net recommendations trend data for META."""
    return json.loads(
        FIXTURES_PATH.joinpath('qs_recommendation_trend.json').read_text()
    )


@pytest.fixture
def page_views_json_mock() -> dict[str, Any]:
    """Mock quote summary response json with net page views data for META."""
    return json.loads(FIXTURES_PATH.joinpath('qs_page_views.json').read_text())
