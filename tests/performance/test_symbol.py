from typing import Any, Generator

import pandas as pd
import pytest
import yahooquery as yq
import yfinance as yf
from curl_cffi import requests
from pytest_benchmark.fixture import BenchmarkFixture
from pytest_mock import MockerFixture

import yafin
from tests._utils import _get_fixture_path, _get_json_fixture, _mock_response

BENCHMARK_KWARGS = dict(rounds=100, iterations=1, warmup_rounds=1)


def _process_chart_like_yfinance(chart: dict[str, Any]) -> pd.DataFrame:
    """Process chart response json into pandas dataframe, exact as yfinance."""
    timestamps = chart['timestamp']
    ohlcvs = chart['indicators']['quote'][0]
    # adjcloses = chart['indicators']['adjclose'][0]['adjclose']

    chart_df = pd.DataFrame({**ohlcvs}, index=timestamps).rename(
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

    return chart_df.set_index('Date').loc[
        :,
        ['Open', 'High', 'Low', 'Close', 'Volume', 'Dividends', 'Stock Splits'],
    ]


def _assert_chart_df(chart_df: pd.DataFrame, expected_df: pd.DataFrame) -> None:
    """Assertions for chart dataframe."""
    assert not chart_df.empty

    assert chart_df.columns.to_list() == expected_df.columns.to_list()
    assert len(chart_df) == len(expected_df)
    # for col in chart_df.columns:
    #     assert chart_df[col].to_list() == expected_df[col].to_list()

@pytest.fixture(scope='session')
def chart_json_mock() -> dict[str, Any]:
    """Chart response json mock."""
    return _get_json_fixture(file_name='meta.json', folder_name='performance')


@pytest.fixture(scope='session')
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

    def run_get_chart(self, symbol: yafin.Symbol) -> pd.DataFrame:
        """Run get_chart method."""
        chart = symbol.get_chart(period_range='1y', interval='1d')
        return _process_chart_like_yfinance(chart)

    def benchmark_chart(
        self, symbol: yafin.Symbol, benchmark: BenchmarkFixture
    ) -> pd.DataFrame:
        """Benchmark get_chart method."""
        return benchmark.pedantic(self.run_get_chart, args=[symbol], **BENCHMARK_KWARGS)  # type: ignore[no-untyped-call, unused-ignore]

    @pytest.mark.performance
    def test_get_chart(
        self,
        symbol: yafin.Symbol,
        mocker: MockerFixture,
        benchmark: BenchmarkFixture,
        chart_json_mock: dict[str, Any],
        expected_chart_df: pd.DataFrame,
    ) -> None:
        """Test get_chart method."""
        _mock_response(
            mocker,
            patched_method='yafin.client.Session.get',
            response_json=chart_json_mock,
        )
        chart_df = self.benchmark_chart(symbol, benchmark)
        _assert_chart_df(chart_df, expected_chart_df)


class TestPerformanceYfinance:
    """Performance tests for yfinance.Ticker."""

    @pytest.fixture
    def ticker(self) -> Generator[yf.Ticker, None, None]:
        """Fixture for Ticker."""
        session: requests.Session[Any] = requests.Session(impersonate='chrome')
        yield yf.Ticker('META', session=session)
        session.close()

    def run_get_chart(self, ticker: yf.Ticker) -> pd.DataFrame:
        """Run history method."""
        return ticker.history(period='1y', interval='1d')

    def benchmark_chart(
        self,
        ticker: yf.Ticker,
        benchmark: BenchmarkFixture,
    ) -> pd.DataFrame:
        """Benchmark history method."""
        return benchmark.pedantic(
            self.run_get_chart, args=[ticker], **BENCHMARK_KWARGS
        )  # type: ignore[no-untyped-call, unused-ignore]

    @pytest.mark.performance
    def test_get_chart_yfinance(
        self,
        ticker: yf.Ticker,
        mocker: MockerFixture,
        benchmark: BenchmarkFixture,
        chart_json_mock: dict[str, Any],
        expected_chart_df: pd.DataFrame,
    ) -> None:
        """Test history method."""
        _mock_response(
            mocker,
            patched_method='yfinance.data.YfData.get',
            response_json=chart_json_mock,
            text='',
        )
        chart_df = self.benchmark_chart(ticker, benchmark)
        _assert_chart_df(chart_df, expected_chart_df)
