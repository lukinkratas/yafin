from datetime import datetime
from typing import Any

import pytest

from tests._utils import _get_json_fixture


@pytest.fixture(scope='session')
def params() -> dict[str, Any]:
    """Params used for mocks fetching."""
    return _get_json_fixture(file_name='params.json')


@pytest.fixture(scope='session')
def ticker(params: dict[str, Any]) -> str:
    """Fresh new instance of ticker for each tests."""
    return params.get('ticker', 'META')


@pytest.fixture(scope='session')
def tickers() -> str:
    """Fresh new instance of tickers for each tests."""
    return 'META,AAPL'


@pytest.fixture(params=[None, int, float], scope='session')
def period1(request: pytest.FixtureRequest, params: dict[str, Any]) -> int | float | None:
    """Fresh new instance of period1 for each tests."""
    if request.param is None:
        return None

    period1_ts = params.get('period1', datetime.now().timestamp())
    # return in request type
    return request.param(period1_ts)


@pytest.fixture(params=[None, int, float], scope='session')
def period2(request: pytest.FixtureRequest, params: dict[str, Any]) -> int | float | None:
    """Fresh new instance of period2 for each tests."""
    if request.param is None:
        return None

    period2_ts = params.get('period1', datetime(2020, 1, 1).timestamp())
    # return in request type
    return request.param(period2_ts)


@pytest.fixture(scope='session')
def chart_json_mock(ticker: str) -> dict[str, Any]:
    """Mock chart response json with data for 1y, 1d."""
    return _get_json_fixture(file_name=f'{ticker.lower()}_1d_1y.json', folder_name='chart')


@pytest.fixture(scope='session')
def options_json_mock(ticker: str) -> dict[str, Any]:
    """Mock options response json with data."""
    return _get_json_fixture(file_name=f'{ticker.lower()}.json', folder_name='options')


@pytest.fixture(scope='session')
def ratings_json_mock(ticker: str) -> dict[str, Any]:
    """Mock ratings response json with data."""
    return _get_json_fixture(file_name=f'{ticker.lower()}.json', folder_name='ratings')


@pytest.fixture(scope='session')
def market_summaries_json_mock() -> dict[str, Any]:
    """Mock market summaries response."""
    return _get_json_fixture(file_name='market_summaries.json')


@pytest.fixture(scope='session')
def trending_json_mock() -> dict[str, Any]:
    """Mock trending response json."""
    return _get_json_fixture(file_name='trending.json')


@pytest.fixture(scope='session')
def currencies_json_mock() -> dict[str, Any]:
    """Mock currencies response json."""
    return _get_json_fixture(file_name='currencies.json')


@pytest.fixture(scope='session')
def client_calendar_events_json_mock() -> dict[str, Any]:
    """Mock currencies response json."""
    return _get_json_fixture(file_name='calendar_events.json')


@pytest.fixture(scope='session')
def timeseries_income_statement_json_mock(ticker: str) -> dict[str, Any]:
    """Mock timeseries response json with annual income statement data."""
    return _get_json_fixture(file_name=f'income_statement_{ticker.lower()}.json', folder_name='timeseries')


@pytest.fixture(scope='session')
def timeseries_balance_sheet_json_mock(ticker: str) -> dict[str, Any]:
    """Mock timeseries response json with annual balance sheet data."""
    return _get_json_fixture(file_name=f'balance_sheet_{ticker.lower()}.json', folder_name='timeseries')


@pytest.fixture(scope='session')
def timeseries_cash_flow_json_mock(ticker: str) -> dict[str, Any]:
    """Mock timeseries response json with annual cash flow data."""
    return _get_json_fixture(file_name=f'cash_flow_{ticker.lower()}.json', folder_name='timeseries')


@pytest.fixture(scope='session')
def quote_summary_all_modules_json_mock(ticker: str) -> dict[str, Any]:
    """Mock quote_summary respons json with all modules data."""
    return _get_json_fixture(file_name=f'all_modules_{ticker.lower()}.json', folder_name='quote_summary')


@pytest.fixture(scope='session')
def asset_profile_json_mock(ticker: str) -> dict[str, Any]:
    """Mock quote summary response json with asset profile data."""
    return _get_json_fixture(file_name=f'asset_profile_{ticker.lower()}.json', folder_name='quote_summary')


@pytest.fixture(scope='session')
def summary_profile_json_mock(ticker: str) -> dict[str, Any]:
    """Mock quote summary response json with summary profile data."""
    return _get_json_fixture(file_name=f'summary_profile_{ticker.lower()}.json', folder_name='quote_summary')


@pytest.fixture(scope='session')
def summary_detail_json_mock(ticker: str) -> dict[str, Any]:
    """Mock quote summary response json with summary detail data."""
    return _get_json_fixture(file_name=f'summary_detail_{ticker.lower()}.json', folder_name='quote_summary')


@pytest.fixture(scope='session')
def esg_scores_json_mock(ticker: str) -> dict[str, Any]:
    """Mock quote summary response json with esg scores data."""
    return _get_json_fixture(file_name=f'esg_scores_{ticker.lower()}.json', folder_name='quote_summary')


@pytest.fixture(scope='session')
def price_json_mock(ticker: str) -> dict[str, Any]:
    """Mock quote summary response json with price data."""
    return _get_json_fixture(file_name=f'price_{ticker.lower()}.json', folder_name='quote_summary')


@pytest.fixture(scope='session')
def default_key_statistics_json_mock(ticker: str) -> dict[str, Any]:
    """Mock quote summary response json with default key statistics data."""
    return _get_json_fixture(file_name=f'default_key_statistics_{ticker.lower()}.json', folder_name='quote_summary')


@pytest.fixture(scope='session')
def financial_data_json_mock(ticker: str) -> dict[str, Any]:
    """Mock quote summary response json with financial data."""
    return _get_json_fixture(file_name=f'financial_data_{ticker.lower()}.json', folder_name='quote_summary')


@pytest.fixture(scope='session')
def symbol_calendar_events_json_mock(ticker: str) -> dict[str, Any]:
    """Mock quote summary response json with calendar events data."""
    return _get_json_fixture(file_name=f'calendar_events_{ticker.lower()}.json', folder_name='quote_summary')


@pytest.fixture(scope='session')
def sec_filings_json_mock(ticker: str) -> dict[str, Any]:
    """Mock quote summary response json with sec filings data."""
    return _get_json_fixture(file_name=f'sec_filings_{ticker.lower()}.json', folder_name='quote_summary')


@pytest.fixture(scope='session')
def upgrade_downgrade_history_json_mock(ticker: str) -> dict[str, Any]:
    """Mock quote summary response json with upgrade downgrade history data."""
    return _get_json_fixture(file_name=f'upgrade_downgrade_history_{ticker.lower()}.json', folder_name='quote_summary')


@pytest.fixture(scope='session')
def institution_ownership_json_mock(ticker: str) -> dict[str, Any]:
    """Mock quote summary response json with institution ownership data."""
    return _get_json_fixture(file_name=f'institution_ownership_{ticker.lower()}.json', folder_name='quote_summary')


@pytest.fixture(scope='session')
def fund_ownership_json_mock(ticker: str) -> dict[str, Any]:
    """Mock quote summary response json with fund ownership data."""
    return _get_json_fixture(file_name=f'fund_ownership_{ticker.lower()}.json', folder_name='quote_summary')


@pytest.fixture(scope='session')
def major_direct_holders_json_mock(ticker: str) -> dict[str, Any]:
    """Mock quote summary response json with major direct holders data."""
    return _get_json_fixture(file_name=f'major_direct_holders_{ticker.lower()}.json', folder_name='quote_summary')


@pytest.fixture(scope='session')
def major_holders_breakdown_json_mock(ticker: str) -> dict[str, Any]:
    """Mock quote summary response json with major holders breakdown data."""
    return _get_json_fixture(file_name=f'major_holders_breakdown_{ticker.lower()}.json', folder_name='quote_summary')


@pytest.fixture(scope='session')
def insider_transactions_json_mock(ticker: str) -> dict[str, Any]:
    """Mock quote summary response json with insider transactions data."""
    return _get_json_fixture(file_name=f'insider_transactions_{ticker.lower()}.json', folder_name='quote_summary')


@pytest.fixture(scope='session')
def insider_holders_json_mock(ticker: str) -> dict[str, Any]:
    """Mock quote summary response json with insider holders data."""
    return _get_json_fixture(file_name=f'insider_holders_{ticker.lower()}.json', folder_name='quote_summary')


@pytest.fixture(scope='session')
def net_share_purchase_activity_json_mock(ticker: str) -> dict[str, Any]:
    """Mock quote summary response json with net share purchase activity data."""  # noqa: E501
    return _get_json_fixture(file_name=f'net_share_purchase_activity_{ticker.lower()}.json', folder_name='quote_summary')


@pytest.fixture(scope='session')
def earnings_json_mock(ticker: str) -> dict[str, Any]:
    """Mock quote summary response json with net earnings data."""
    return _get_json_fixture(file_name=f'earnings_{ticker.lower()}.json', folder_name='quote_summary')


@pytest.fixture(scope='session')
def earnings_history_json_mock(ticker: str) -> dict[str, Any]:
    """Mock quote summary response json with net earnings history data."""
    return _get_json_fixture(file_name=f'earnings_history_{ticker.lower()}.json', folder_name='quote_summary')


@pytest.fixture(scope='session')
def earnings_trend_json_mock(ticker: str) -> dict[str, Any]:
    """Mock quote summary response json with net earnings trend data."""
    return _get_json_fixture(file_name=f'earnings_trend_{ticker.lower()}.json', folder_name='quote_summary')


@pytest.fixture(scope='session')
def industry_trend_json_mock(ticker: str) -> dict[str, Any]:
    """Mock quote summary response json with net industry trend data."""
    return _get_json_fixture(file_name=f'industry_trend_{ticker.lower()}.json', folder_name='quote_summary')


@pytest.fixture(scope='session')
def index_trend_json_mock(ticker: str) -> dict[str, Any]:
    """Mock quote summary response json with net index trend data."""
    return _get_json_fixture(file_name=f'index_trend_{ticker.lower()}.json', folder_name='quote_summary')


@pytest.fixture(scope='session')
def sector_trend_json_mock(ticker: str) -> dict[str, Any]:
    """Mock quote summary response json with net sector trend data."""
    return _get_json_fixture(file_name=f'sector_trend_{ticker.lower()}.json', folder_name='quote_summary')


@pytest.fixture(scope='session')
def recommendation_trend_json_mock(ticker: str) -> dict[str, Any]:
    """Mock quote summary response json with net recommendations trend data."""
    return _get_json_fixture(file_name=f'recommendation_trend_{ticker.lower()}.json', folder_name='quote_summary')


@pytest.fixture(scope='session')
def page_views_json_mock(ticker: str) -> dict[str, Any]:
    """Mock quote summary response json with net page views data."""
    return _get_json_fixture(file_name=f'page_views_{ticker.lower()}.json', folder_name='quote_summary')
