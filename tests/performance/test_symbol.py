import pathlib
import json
from typing import Any, Generator
from pytest_benchmark.fixture import BenchmarkFixture
import pandas as pd
import pytest
from pytest_mock import MockerFixture
from yfinance import Ticker
from curl_cffi import requests

from tests._utils import _mock_200_response
from yafin import Symbol
from yafin.const import (
    ANNUAL_BALANCE_SHEET_TYPES,
    ANNUAL_CASH_FLOW_TYPES,
    ANNUAL_INCOME_STATEMENT_TYPES,
    QUOTE_SUMMARY_MODULES,
)


def process_chart_like_yfinance(chart: dict[str, Any]) -> pd.DataFrame:
    """Process chart response json into pandas dataframe, exact as yfinance."""
    dividends = chart['events'].get('dividends')
    dividends_df = pd.DataFrame(
        dividends.values() if dividends else {'date': [], 'amount': []}
    ).rename(columns={'amount': 'dividends'})

    splits = chart['events'].get('splits')
    splits_df = pd.DataFrame(
        splits.values()
        if splits
        else {'date': [], 'numerator': [], 'denominator': [], 'splitRatio': []}
    )
    splits_df['splits'] = splits_df['numerator'] / splits_df['denominator']

    chart_df = (
        pd.DataFrame({'date': chart['timestamp'], **chart['indicators']['quote'][0]})
        .set_index('date')
        .join(dividends_df.set_index('date').loc[:, 'dividends'])
        .join(splits_df.set_index('date').loc[:, 'splits'])
        .fillna(value={'dividends': 0, 'splits': 0})
    )
    chart_df.index = pd.to_datetime(chart_df.index, unit='s')
    chart_df.columns = chart_df.columns.str.capitalize()
    chart_df = chart_df.rename(columns={'Splits': 'Stock Splits'})
    return chart_df.loc[
        :,
        ['Open', 'High', 'Low', 'Close', 'Volume', 'Dividends', 'Stock Splits'],
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
    def symbol(selfr) -> Generator[Symbol, None, None]:
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
        expected_chart_df: pd.DataFrame
    ) -> None:
        """Test get_chart method."""
        
        _mock_200_response(mocker, patched_method='yafin.client.Session.get', response_json=chart_json_mock)

        def run() -> pd.DataFrame:
            chart = symbol.get_chart(interval='1d', period_range='1y')
            return process_chart_like_yfinance(chart)
         
        result_df = benchmark.pedantic(run, rounds=10, iterations=1, warmup_rounds=1)
        print('result_df')
        print(result_df)
        print('expected_chart_df')
        print(expected_chart_df)

        assert result_df.equals(expected_chart_df)
        assert result_df.columns == expected_chart_df.columns
        assert result_df.index == expected_chart_df.index

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
        self, ticker: Ticker, mocker: MockerFixture, benchmark: BenchmarkFixture, chart_json_mock: dict[str, Any], expected_chart_df: pd.DataFrame
    ) -> None:
        """Test history method."""

        _mock_200_response(mocker, patched_method='curl_cffi.requests.Session.get', response_json=chart_json_mock)

        def run() -> pd.DataFrame:
            return ticker.history(period='1y', interval='1d')

        result_df = benchmark.pedantic(run, rounds=10, iterations=1, warmup_rounds=1)
        print('result_df')
        print(result_df)
        print('expected_chart_df')
        print(expected_chart_df)

        assert result_df.equals(expected_chart_df)
        assert result_df.columns == expected_chart_df.columns
        assert result_df.index == expected_chart_df.index
