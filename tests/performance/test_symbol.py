from typing import Any, Generator

import pandas as pd
import pytest
from curl_cffi import requests
from curl_cffi.requests import Response
from curl_cffi.requests.exceptions import HTTPError
from pytest_benchmark.fixture import BenchmarkFixture
from pytest_mock import MockerFixture
from yfinance import Ticker

from tests._utils import _get_fixture_path, _get_json_fixture, _mock_response
from yafin import Symbol

BENCHMARK_KWARGS = dict(rounds=10, iterations=1, warmup_rounds=1)


# def _mock_yfinance_response(
#     mocker: MockerFixture,
#     status_code: int = 200,
#     response_json: dict[str, Any] | None = None,
#     text: str | None = None,
#     async_mock: bool = False,
# ) -> None:
#     """Mock response with status code 200."""
#     mock_response = mocker.Mock(spec=Response)
#     mock_response.status_code = status_code
#     mock_response.raise_for_status = mocker.Mock()

#     if status_code == 404:
#         mock_response.raise_for_status.side_effect = HTTPError(
#             '404 Client Error: Not Found for url'
#         )

#     if response_json:
#         mock_response.json.return_value = response_json

#     if text:
#         mock_response.text = text

#     mock_class = mocker.AsyncMock if async_mock else mocker.Mock
#     patched_method = 'curl_cffi.requests.Session.get'
#     mocker.patch(patched_method, new=mock_class(return_value=mock_response))


def process_chart_like_yfinance(chart: dict[str, Any]) -> pd.DataFrame:
    """Process chart response json into pandas dataframe, exact as yfinance."""
    chart_df = pd.DataFrame(
        {**chart['indicators']['quote'][0]}, index=chart['timestamp']
    ).rename(
        columns={
            'open': 'Open',
            'volume': 'Volume',
            'close': 'Close',
            'low': 'Low',
            'high': 'High',
        }
    )

    tz = '-01:00'
    chart_df['Date'] = pd.to_datetime(chart_df.index.values, unit='s', utc=True)
    chart_df['Date'] = chart_df['Date'].dt.tz_convert(tz)

    dividends = chart['events'].get('dividends')
    dividends_df = (
        pd.DataFrame(
            dividends.values() if dividends is not None else {'date': [], 'amount': []}
        )
        .set_index('date')
        .rename(columns={'amount': 'Dividends'})
    )
    chart_df = chart_df.join(dividends_df).fillna(value={'Dividends': 0})

    splits = chart['events'].get('splits')
    splits_df = (
        pd.DataFrame(
            splits.values() if splits is not None else {'date': [], 'numerator': []}
        )
        .set_index('date')
        .rename(columns={'numerator': 'Stock Splits'})
    )
    chart_df = chart_df.join(splits_df['Stock Splits']).fillna(
        value={'Stock Splits': 0}
    )

    return chart_df.reset_index().loc[
        :,
        ['Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'Dividends', 'Stock Splits'],
    ]


@pytest.fixture(scope='session')
def chart_json_mock() -> dict[str, Any]:
    """Chart response json mock."""
    return _get_json_fixture(file_name='meta.json', folder_name='performance')


@pytest.fixture(scope='session')
def expected_chart_df() -> pd.DataFrame:
    """Expected Chart DataFrame ficture."""
    csv_path = _get_fixture_path(file_name='meta.csv', folder_name='performance')
    return pd.read_csv(csv_path)


class TestPerformanceSymbol:
    """Unit tests for yafin.Symbol."""

    @pytest.fixture
    def symbol(self) -> Generator[Symbol, None, None]:
        """Fresh new instance of Symbol for each tests."""
        with Symbol('META') as symbol:
            yield symbol

    @pytest.mark.performance
    def test_get_chart(
        self,
        symbol: Symbol,
        mocker: MockerFixture,
        benchmark: BenchmarkFixture,
        chart_json_mock: dict[str, Any],
        expected_chart_df: pd.DataFrame,
    ) -> None:
        """Test get_chart method."""

        def run() -> pd.DataFrame:
            chart = symbol.get_chart(interval='1d', period_range='1y')
            return process_chart_like_yfinance(chart)

        # _mock_response(mocker, response_json=chart_json_mock)

        result_df = benchmark.pedantic(run, **BENCHMARK_KWARGS)

        # assert result_df.columns.to_list() == expected_chart_df.columns.to_list()
        # assert result_df.index.to_list() == expected_chart_df.index.to_list()
        # assert result_df.compare(expected_chart_df).empty


class TestPerformanceYFinance:
    """Performance tests for yafin.stonk module."""

    @pytest.fixture
    def ticker(self) -> Generator[Ticker, None, None]:
        """Fixture for Ticker."""
        session = requests.Session(impersonate='chrome')
        yield Ticker('META', session=session)
        session.close()

    @pytest.mark.performance
    def test_get_chart_yfinance(
        self,
        ticker: Ticker,
        mocker: MockerFixture,
        benchmark: BenchmarkFixture,
        chart_json_mock: dict[str, Any],
        expected_chart_df: pd.DataFrame,
    ) -> None:
        """Test history method."""

        def run() -> pd.DataFrame:
            return ticker.history(period='1y', interval='1d')

        # _mock_yfinance_response(mocker, response_json=chart_json_mock)

        result_df = benchmark.pedantic(run, **BENCHMARK_KWARGS)
        # result_df.to_csv('yfinance.csv')
        # expected_chart_df.to_csv('expected.csv')

        # assert result_df.columns.to_list() == expected_chart_df.columns.to_list()
        # assert result_df.index.to_list() == expected_chart_df.index.to_list()
        # assert result_df.compare(expected_chart_df).empty
