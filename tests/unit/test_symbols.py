from typing import Any, Generator

import pytest
from pytest_mock import MockerFixture

from tests._assertions import (
    _assert_insights_results,
    _assert_quote_types_results,
    _assert_quotes_results,
    _assert_recommendations_results,
    _assert_search_response_json,
)
from tests._utils import _get_json_fixture, _mock_response
from yafin import Symbols


@pytest.fixture
def quote_json_mock(tickers_name: str) -> dict[str, Any]:
    """Quote response json mock."""
    return _get_json_fixture(file_name=f'{tickers_name}.json', folder_name='quote')


@pytest.fixture
def quote_type_json_mock(tickers_name: str) -> dict[str, Any]:
    """Quote_type response json mock."""
    return _get_json_fixture(file_name=f'{tickers_name}.json', folder_name='quote_type')


@pytest.fixture
def search_json_mock(tickers_name: str) -> dict[str, Any]:
    """Search response json mock."""
    return _get_json_fixture(file_name=f'{tickers_name}.json', folder_name='search')


@pytest.fixture
def recommendations_json_mock(tickers_name: str) -> dict[str, Any]:
    """Recommendations response json mock."""
    return _get_json_fixture(
        file_name=f'{tickers_name}.json', folder_name='recommendations'
    )


@pytest.fixture
def insights_json_mock(tickers_name: str) -> dict[str, Any]:
    """Insights response json mock."""
    return _get_json_fixture(file_name=f'{tickers_name}.json', folder_name='insights')


class TestUnitSymbols:
    """Unit tests for yafin.Symbols."""

    def test_client(self) -> None:
        """Test client attribute."""
        symbols = Symbols('NETA,AAPL')
        assert symbols._client is None

        symbols._get_client()
        assert symbols._client

        symbols.close()
        assert symbols._client is None

        with Symbols('NETA,AAPL') as symbols:
            assert symbols._client

        assert symbols._client is None

    def test_client_singleton(self) -> None:
        """Test client attribute singleton pattern."""
        meta_aapl = Symbols('NETA,AAPL')
        googl_msft = Symbols('GOOGL,MSFT')

        meta_aapl._get_client()
        googl_msft._get_client()

        # test it is singleton
        assert meta_aapl._client is googl_msft._client

        meta_aapl.close()
        googl_msft.close()

    def test_close(self) -> None:
        """Test client attribute singleton pattern."""
        meta_aapl = Symbols('NETA,AAPL')
        googl_msft = Symbols('GOOGL,MSFT')

        meta_aapl._get_client()
        googl_msft._get_client()

        assert meta_aapl._client
        assert googl_msft._client

        # meta close should not close the aapl client
        meta_aapl.close()
        assert meta_aapl._client is None
        assert googl_msft._client

        googl_msft.close()
        assert meta_aapl._client is None
        assert googl_msft._client is None

    @pytest.fixture
    def symbols(self, tickers: str) -> Generator[Symbols, None, None]:
        """Fresh new instance of Symbol for each tests."""
        with Symbols(tickers) as symbols:
            yield symbols

    def test_get_quote(
        self,
        symbols: Symbols,
        mocker: MockerFixture,
        quote_json_mock: dict[str, Any],
    ) -> None:
        """Test get_quote method."""
        _mock_response(
            mocker,
            patched_method='yafin.client.Session.get',
            response_json=quote_json_mock,
        )
        quotes_results = symbols.get_quote()
        _assert_quotes_results(quotes_results, symbols.tickers)

    def test_get_quote_type(
        self,
        symbols: Symbols,
        mocker: MockerFixture,
        quote_type_json_mock: dict[str, Any],
    ) -> None:
        """Test get_quote_type method."""
        _mock_response(
            mocker,
            patched_method='yafin.client.Session.get',
            response_json=quote_type_json_mock,
        )
        quote_types_results = symbols.get_quote_type()
        _assert_quote_types_results(quote_types_results, symbols.tickers)

    def test_get_search(
        self,
        symbols: Symbols,
        mocker: MockerFixture,
        search_json_mock: dict[str, Any],
    ) -> None:
        """Test get_search method."""
        _mock_response(
            mocker,
            patched_method='yafin.client.Session.get',
            response_json=search_json_mock,
        )
        search = symbols.get_search()
        _assert_search_response_json(search)

    def test_get_recommendations(
        self,
        symbols: Symbols,
        mocker: MockerFixture,
        recommendations_json_mock: dict[str, Any],
    ) -> None:
        """Test get_recommendations method."""
        _mock_response(
            mocker,
            patched_method='yafin.client.Session.get',
            response_json=recommendations_json_mock,
        )
        recommendations_results = symbols.get_recommendations()
        _assert_recommendations_results(recommendations_results, symbols.tickers)

    def test_get_insights(
        self,
        symbols: Symbols,
        mocker: MockerFixture,
        insights_json_mock: dict[str, Any],
    ) -> None:
        """Test get_insights method."""
        _mock_response(
            mocker,
            patched_method='yafin.client.Session.get',
            response_json=insights_json_mock,
        )
        insights_results = symbols.get_insights()
        _assert_insights_results(insights_results, symbols.tickers)
