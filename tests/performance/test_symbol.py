import json
import pathlib
from typing import Any, Generator

import pandas as pd
import pytest
from curl_cffi import requests
from pytest_benchmark.fixture import BenchmarkFixture
from pytest_mock import MockerFixture
from yfinance import Ticker

from tests._utils import _mock_200_response
from yafin import Symbol


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
    """Mock chart response json."""
    json_path = pathlib.Path(__file__).resolve().parent.joinpath('meta.json')
    return json.loads(json_path.read_text())


@pytest.fixture(scope='session')
def expected_chart_df() -> pd.DataFrame:
    """Mock chart response json."""
    csv_path = pathlib.Path(__file__).resolve().parent.joinpath('meta.csv')
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
        _mock_200_response(
            mocker,
            patched_method='yafin.client.Session.get',
            response_json=chart_json_mock,
        )

        def run() -> pd.DataFrame:
            chart = symbol.get_chart(interval='1d', period_range='1y')
            return process_chart_like_yfinance(chart)

        result_df = benchmark.pedantic(run, rounds=10, iterations=1, warmup_rounds=1)

        assert result_df.columns.to_list() == expected_chart_df.columns.to_list()
        assert result_df.index.to_list() == expected_chart_df.index.to_list()
        assert result_df.compare(expected_chart_df).empty


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
        _mock_200_response(
            mocker,
            patched_method='curl_cffi.requests.Session.get',
            response_json=chart_json_mock,
        )

        def run() -> pd.DataFrame:
            return ticker.history(period='1y', interval='1d')

        result_df = benchmark.pedantic(run, rounds=10, iterations=1, warmup_rounds=1)
        result_df.to_csv('yfinance.csv')
        expected_chart_df.to_csv('expected.csv')

        assert result_df.columns.to_list() == expected_chart_df.columns.to_list()
        assert result_df.index.to_list() == expected_chart_df.index.to_list()
        assert result_df.compare(expected_chart_df).empty
