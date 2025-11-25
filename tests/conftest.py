from datetime import datetime
from typing import Any

import pytest

from tests._utils import _get_json_fixture
from yafin.exceptions import TrailingBalanceSheetError


@pytest.fixture(scope='session')
def params() -> dict[str, Any]:
    """Params used for mocks fetching."""
    return _get_json_fixture(file_name='params.json')


@pytest.fixture(scope='session')
def tickers(params: dict[str, Any]) -> str:
    """Fresh new instance of tickers for each test."""
    return params.get('tickers', 'META,AAPL')


@pytest.fixture(scope='session')
def tickers_name(tickers: str) -> str:
    """Fresh new instance of tickers for each test."""
    return tickers.replace(',', '_').lower()


@pytest.fixture(params=['META', 'AAPL'], scope='session')
def ticker(request: pytest.FixtureRequest) -> str:
    """Fresh new instance of ticker for each test."""
    return request.param


@pytest.fixture(scope='session')
def interval(params: dict[str, Any]) -> str:
    """Fresh new instance of interval for each test."""
    return params.get('interval', '1d')


@pytest.fixture(scope='session')
def period_range(params: dict[str, Any]) -> str:
    """Fresh new instance of period_range for each test."""
    return params.get('period_range', '1y')


@pytest.fixture(params=[None, int, float], scope='session')
def period1(
    request: pytest.FixtureRequest, params: dict[str, Any]
) -> int | float | None:
    """Fresh new instance of period1 for each test."""
    if request.param is None:
        return None

    period1_ts = params.get('period1', datetime.now().timestamp())
    # return in request type
    return request.param(period1_ts)


@pytest.fixture(params=[None, int, float], scope='session')
def period2(
    request: pytest.FixtureRequest, params: dict[str, Any]
) -> int | float | None:
    """Fresh new instance of period2 for each test."""
    if request.param is None:
        return None

    period2_ts = params.get('period1', datetime(2020, 1, 1).timestamp())
    # return in request type
    return request.param(period2_ts)


@pytest.fixture(scope='session')
def chart_json_mock(ticker: str) -> dict[str, Any]:
    """Chart response json mock with data for 1y, 1d."""
    return _get_json_fixture(
        file_name=f'{ticker.lower()}_1d_1y.json', folder_name='chart'
    )


@pytest.fixture(scope='session')
def options_json_mock(ticker: str) -> dict[str, Any]:
    """Options response json mock."""
    return _get_json_fixture(file_name=f'{ticker.lower()}.json', folder_name='options')


@pytest.fixture(scope='session')
def ratings_json_mock(ticker: str) -> dict[str, Any]:
    """Ratings response json mock."""
    return _get_json_fixture(file_name=f'{ticker.lower()}.json', folder_name='ratings')


@pytest.fixture(scope='session')
def market_summaries_json_mock() -> dict[str, Any]:
    """Market summaries response mock."""
    return _get_json_fixture(file_name='market_summaries.json')


@pytest.fixture(scope='session')
def trending_json_mock() -> dict[str, Any]:
    """Trending response json mock."""
    return _get_json_fixture(file_name='trending.json')


@pytest.fixture(scope='session')
def currencies_json_mock() -> dict[str, Any]:
    """Currencies response json mock."""
    return _get_json_fixture(file_name='currencies.json')


@pytest.fixture(scope='session')
def timeseries_income_statement_json_mock(ticker: str) -> dict[str, Any]:
    """Timeseries response json mock with annual income statement data."""
    return _get_json_fixture(
        file_name=f'income_statement_{ticker.lower()}.json', folder_name='timeseries'
    )


@pytest.fixture(scope='session')
def timeseries_balance_sheet_json_mock(ticker: str) -> dict[str, Any]:
    """Timeseries response json mock with annual balance sheet data."""
    return _get_json_fixture(
        file_name=f'balance_sheet_{ticker.lower()}.json', folder_name='timeseries'
    )


@pytest.fixture(scope='session')
def timeseries_cash_flow_json_mock(ticker: str) -> dict[str, Any]:
    """Timeseries response json mock with annual cash flow data."""
    return _get_json_fixture(
        file_name=f'cash_flow_{ticker.lower()}.json', folder_name='timeseries'
    )


@pytest.fixture(scope='session')
def quote_summary_all_modules_json_mock(ticker: str) -> dict[str, Any]:
    """Quote_summary response json mock with all modules data."""
    return _get_json_fixture(
        file_name=f'all_modules_{ticker.lower()}.json', folder_name='quote_summary'
    )


@pytest.fixture(
    params=[
        dict(),
        dict(include_pre_post=True),
        dict(include_div=True),
        dict(include_split=True),
        dict(include_earn=True),
        dict(include_capital_gain=True),
        dict(
            include_pre_post=True,
            include_div=True,
            include_split=True,
            include_earn=True,
            include_capital_gain=True,
        ),
    ],
    scope='session',
)
def chart_kwargs(request: pytest.FixtureRequest) -> dict[str, Any]:
    """Fresh new instance of kwargs for chart for each test."""
    return request.param


@pytest.fixture(
    params=[
        (dict(period_range='xxx', interval='1d'), ValueError),
        (dict(period_range='1y', interval='xxx'), ValueError),
    ],
    scope='session',
)
def invalid_chart_kwargs_err_tuple(
    request: pytest.FixtureRequest,
) -> tuple[dict[str, Any], type[Exception]]:
    """Fresh new instance of invalid kwargs, err tuple for chart for each test."""
    return request.param


@pytest.fixture(
    params=[
        (dict(frequency='trailing'), TrailingBalanceSheetError),
        (dict(frequency='xxx'), ValueError),
    ],
)
def invalid_balance_sheet_kwargs_err_tuple(
    request: pytest.FixtureRequest,
) -> tuple[dict[str, Any], type[Exception]]:
    """Fresh new instance of invalid kwargs, err tuple for balance sheet for each
    test.
    """
    return request.param
