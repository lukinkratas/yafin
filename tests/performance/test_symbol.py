from typing import Any, Generator

import pandas as pd
import pytest
import yfinance as yf
from curl_cffi import requests
from pytest_benchmark.fixture import BenchmarkFixture
from pytest_mock import MockerFixture

import yafin
from tests._utils import (
    _get_fixture_path,
    _get_json_fixture,
    _mock_response,
    _process_chart_like_yfinance,
)

BENCHMARK_KWARGS = dict(rounds=10, iterations=10, warmup_rounds=10)


def _assert_chart_df(chart_df: pd.DataFrame, expected_df: pd.DataFrame) -> None:
    """Assertions for chart dataframe."""
    assert not chart_df.empty

    assert chart_df.columns.to_list() == expected_df.columns.to_list()
    assert len(chart_df) == len(expected_df)
    # for col in chart_df.columns:
    #     assert chart_df[col].to_list() == expected_df[col].to_list()


@pytest.fixture
def chart_json_mock() -> dict[str, Any]:
    """Chart response json mock."""
    return _get_json_fixture(file_name='meta_1d_1y.json', folder_name='chart')


@pytest.fixture
def expected_chart_df() -> pd.DataFrame:
    """Expected Chart DataFrame ficture."""
    csv_path = _get_fixture_path(file_name='meta.csv', folder_name='performance')
    return pd.read_csv(csv_path).set_index('Date')


class TestPerformanceSymbol:
    """Unit tests for yafin.Symbol."""

    @pytest.fixture
    def symbol(self) -> Generator[yafin.Symbol, None, None]:
        """Fresh new instance of Symbol for each tests."""
        with yafin.Symbol('META') as symbol:
            yield symbol

    def run_get_chart(
        self, symbol: yafin.Symbol, interval: str, period_range: str
    ) -> pd.DataFrame:
        """Run get_chart method."""
        chart = symbol.get_chart(interval, period_range)
        return _process_chart_like_yfinance(chart)

    def benchmark_chart(
        self,
        symbol: yafin.Symbol,
        benchmark: BenchmarkFixture,
        interval: str,
        period_range: str,
    ) -> pd.DataFrame:
        """Benchmark get_chart method."""
        return benchmark.pedantic(
            self.run_get_chart,
            args=[symbol, interval, period_range],
            **BENCHMARK_KWARGS,
        )  # type: ignore[no-untyped-call, unused-ignore]

    @pytest.mark.performance
    def test_get_chart(
        self,
        symbol: yafin.Symbol,
        mocker: MockerFixture,
        benchmark: BenchmarkFixture,
        interval: str,
        period_range: str,
        chart_json_mock: dict[str, Any],
        expected_chart_df: pd.DataFrame,
    ) -> None:
        """Test get_chart method."""
        _mock_response(
            mocker,
            patched_method='yafin.client.Session.get',
            response_jsons=[chart_json_mock],
        )
        chart_df = self.benchmark_chart(symbol, benchmark, interval, period_range)
        _assert_chart_df(chart_df, expected_chart_df)


class TestPerformanceYfinance:
    """Performance tests for yfinance.Ticker."""

    @pytest.fixture
    def ticker(self) -> Generator[yf.Ticker, None, None]:
        """Fixture for Ticker."""
        session: requests.Session[Any] = requests.Session(impersonate='chrome')
        yield yf.Ticker('META', session=session)
        session.close()

    def run_get_chart(
        self, ticker: yf.Ticker, interval: str, period_range: str
    ) -> pd.DataFrame:
        """Run history method."""
        return ticker.history(period=period_range, interval=interval)

    def benchmark_chart(
        self,
        ticker: yf.Ticker,
        benchmark: BenchmarkFixture,
        interval: str,
        period_range: str,
    ) -> pd.DataFrame:
        """Benchmark history method."""
        return benchmark.pedantic(
            self.run_get_chart,
            args=[ticker, interval, period_range],
            **BENCHMARK_KWARGS,
        )  # type: ignore[no-untyped-call, unused-ignore]

    @pytest.mark.performance
    def test_get_chart_yfinance(
        self,
        ticker: yf.Ticker,
        mocker: MockerFixture,
        benchmark: BenchmarkFixture,
        interval: str,
        period_range: str,
        chart_json_mock: dict[str, Any],
        expected_chart_df: pd.DataFrame,
    ) -> None:
        """Test history method."""
        _mock_response(
            mocker,
            patched_method='yfinance.data.YfData.get',
            response_jsons=[chart_json_mock],
            text='',
        )
        chart_df = self.benchmark_chart(ticker, benchmark, interval, period_range)
        _assert_chart_df(chart_df, expected_chart_df)
