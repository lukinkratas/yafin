from typing import AsyncGenerator, Generator

import pytest
import pytest_asyncio

from tests._assertions import (
    _assert_chart_result,
    _assert_insights_result,
    _assert_options_result,
    _assert_quote_summary_result,
    _assert_quote_types_result,
    _assert_quotes_result,
    _assert_ratings_result,
    _assert_recommendations_result,
    _assert_search_result,
    _assert_timeseries_result,
)
from yafin import AsyncSymbol, Symbol
from yafin.const import (
    ANNUAL_BALANCE_SHEET_TYPES,
    ANNUAL_CASH_FLOW_TYPES,
    ANNUAL_INCOME_STATEMENT_TYPES,
    QUOTE_SUMMARY_MODULES,
)


class TestUnitSymbol:
    """Integration tests for yafin.Symbol."""

    @pytest.fixture
    def symbol(self, ticker: str) -> Generator[Symbol, None, None]:
        """Fixture for Symbol."""
        with Symbol(ticker) as symbol:
            yield symbol

    @pytest.mark.integration
    def test_get_chart(self, symbol: Symbol, interval: str, period_range: str) -> None:
        """Test get_chart method."""
        chart_result = symbol.get_chart(interval, period_range)
        _assert_chart_result(chart_result, symbol.ticker)

    @pytest.mark.integration
    def test_get_quote(self, symbol: Symbol) -> None:
        """Test get_quote method."""
        quotes_result = symbol.get_quote()
        _assert_quotes_result(quotes_result, symbol.ticker)

    @pytest.mark.integration
    def test_get_quote_type(self, symbol: Symbol) -> None:
        """Test get_quote_type method."""
        quote_types_result = symbol.get_quote_type()
        _assert_quote_types_result(quote_types_result, symbol.ticker)

    @pytest.mark.integration
    def test_get_quote_summary_all_modules(self, symbol: Symbol) -> None:
        """Test get_quote_summary_all_modules method."""
        quote_summary_all_modules = symbol.get_quote_summary_all_modules()
        _assert_quote_summary_result(
            quote_summary_all_modules, modules=QUOTE_SUMMARY_MODULES
        )

    @pytest.mark.integration
    def test_get_income_statement(self, symbol: Symbol) -> None:
        """Test get_income_statement method."""
        frequency = 'annual'
        annual_income_stmt = symbol.get_income_statement(frequency)
        _assert_timeseries_result(
            annual_income_stmt, symbol.ticker, ANNUAL_INCOME_STATEMENT_TYPES
        )

    @pytest.mark.integration
    def test_get_balance_sheet(self, symbol: Symbol) -> None:
        """Test get_balance_sheet method."""
        frequency = 'annual'
        annual_balance_sheet = symbol.get_balance_sheet(frequency)
        _assert_timeseries_result(
            annual_balance_sheet, symbol.ticker, ANNUAL_BALANCE_SHEET_TYPES
        )

    @pytest.mark.integration
    def test_get_cash_flow(self, symbol: Symbol) -> None:
        """Test get_cash_flow method."""
        frequency = 'annual'
        annual_cash_flow = symbol.get_cash_flow(frequency)
        _assert_timeseries_result(
            annual_cash_flow, symbol.ticker, ANNUAL_CASH_FLOW_TYPES
        )

    @pytest.mark.integration
    def test_get_options(self, symbol: Symbol) -> None:
        """Test get_options method."""
        options = symbol.get_options()
        _assert_options_result(options, symbol.ticker)

    @pytest.mark.integration
    def test_get_search(self, symbol: Symbol) -> None:
        """Test get_search method."""
        search = symbol.get_search()
        _assert_search_result(search)

    @pytest.mark.integration
    def test_get_recommendations(self, symbol: Symbol) -> None:
        """Test get_recommendations method."""
        recommendations_result = symbol.get_recommendations()
        _assert_recommendations_result(recommendations_result, symbol.ticker)

    @pytest.mark.integration
    def test_get_insights(self, symbol: Symbol) -> None:
        """Test get_insights method."""
        insights_result = symbol.get_insights()
        _assert_insights_result(insights_result, symbol.ticker)

    @pytest.mark.integration
    def test_get_ratings(self, symbol: Symbol) -> None:
        """Test get_ratings method."""
        ratings = symbol.get_ratings()
        _assert_ratings_result(ratings, symbol.ticker)


class TestUnitAsyncSymbol:
    """Integration tests for yafin.AsyncSymbol."""

    @pytest_asyncio.fixture
    async def async_symbol(self, ticker: str) -> AsyncGenerator[AsyncSymbol, None]:
        """Fixture for AsyncSymbol."""
        async with AsyncSymbol(ticker) as async_symbol:
            yield async_symbol

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_get_chart(
        self, async_symbol: AsyncSymbol, interval: str, period_range: str
    ) -> None:
        """Test get_chart method."""
        chart_result = await async_symbol.get_chart(interval, period_range)
        _assert_chart_result(chart_result, async_symbol.ticker)

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_get_quote(self, async_symbol: AsyncSymbol) -> None:
        """Test get_quote method."""
        quotes_result = await async_symbol.get_quote()
        _assert_quotes_result(quotes_result, async_symbol.ticker)

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_get_quote_type(self, async_symbol: AsyncSymbol) -> None:
        """Test get_quote_type method."""
        quote_types_result = await async_symbol.get_quote_type()
        _assert_quote_types_result(quote_types_result, async_symbol.ticker)

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_get_quote_summary_all_modules(
        self, async_symbol: AsyncSymbol
    ) -> None:
        """Test get_quote_summary_all_modules method."""
        quote_summary_all_modules = await async_symbol.get_quote_summary_all_modules()
        _assert_quote_summary_result(
            quote_summary_all_modules, modules=QUOTE_SUMMARY_MODULES
        )

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_get_income_statement(self, async_symbol: AsyncSymbol) -> None:
        """Test get_income_statement method."""
        frequency = 'annual'
        annual_income_stmt = await async_symbol.get_income_statement(frequency)
        _assert_timeseries_result(
            annual_income_stmt, async_symbol.ticker, ANNUAL_INCOME_STATEMENT_TYPES
        )

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_get_balance_sheet(self, async_symbol: AsyncSymbol) -> None:
        """Test get_balance_sheet method."""
        frequency = 'annual'
        annual_balance_sheet = await async_symbol.get_balance_sheet(frequency)
        _assert_timeseries_result(
            annual_balance_sheet, async_symbol.ticker, ANNUAL_BALANCE_SHEET_TYPES
        )

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_get_cash_flow(self, async_symbol: AsyncSymbol) -> None:
        """Test get_cash_flow method."""
        frequency = 'annual'
        annual_cash_flow = await async_symbol.get_cash_flow(frequency)
        _assert_timeseries_result(
            annual_cash_flow, async_symbol.ticker, ANNUAL_CASH_FLOW_TYPES
        )

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_get_options(self, async_symbol: AsyncSymbol) -> None:
        """Test get_options method."""
        options = await async_symbol.get_options()
        _assert_options_result(options, async_symbol.ticker)

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_get_search(self, async_symbol: AsyncSymbol) -> None:
        """Test get_search method."""
        search = await async_symbol.get_search()
        _assert_search_result(search)

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_get_recommendations(self, async_symbol: AsyncSymbol) -> None:
        """Test get_recommendations method."""
        recommendations_result = await async_symbol.get_recommendations()
        _assert_recommendations_result(recommendations_result, async_symbol.ticker)

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_get_insights(self, async_symbol: AsyncSymbol) -> None:
        """Test get_insights method."""
        insights_result = await async_symbol.get_insights()
        _assert_insights_result(insights_result, async_symbol.ticker)

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_get_ratings(self, async_symbol: AsyncSymbol) -> None:
        """Test get_ratings method."""
        ratings_result = await async_symbol.get_ratings()
        _assert_ratings_result(ratings_result, async_symbol.ticker)
