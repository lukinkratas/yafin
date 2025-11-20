from typing import Generator

import pytest

from tests._assertions import (
    _assert_insights_results,
    _assert_quote_types_results,
    _assert_quotes_results,
    _assert_recommendations_results,
    _assert_search_response_json,
)
from yafin import Symbols

class TestUnitSymbols:
    """Integration tests for yafin.Symbol."""

    @pytest.fixture
    def symbols(self, tickers: str) -> Generator[Symbols, None, None]:
        """Fixture for Symbols."""
        with Symbols(tickers) as symbols:
            yield symbols

    @pytest.mark.integration
    def test_get_quote(self, symbols: Symbols) -> None:
        """Test get_quote method."""
        quotes_results = symbols.get_quote()
        _assert_quotes_results(quotes_results, symbols.tickers)

    @pytest.mark.integration
    def test_get_quote_type(self, symbols: Symbols) -> None:
        """Test get_quote_type method."""
        quote_types_results = symbols.get_quote_type()
        _assert_quote_types_results(quote_types_results, symbols.tickers)

    @pytest.mark.integration
    def test_get_search(self, symbols: Symbols) -> None:
        """Test get_search method."""
        search = symbols.get_search()
        _assert_search_response_json(search)

    @pytest.mark.integration
    def test_get_recommendations(self, symbols: Symbols) -> None:
        """Test get_recommendations method."""
        recommendations_results = symbols.get_recommendations()
        _assert_recommendations_results(recommendations_results, symbols.tickers)

    @pytest.mark.integration
    def test_get_insights(self, symbols: Symbols) -> None:
        """Test get_insights method."""
        insights_results = symbols.get_insights()
        _assert_insights_results(insights_results, symbols.tickers)
