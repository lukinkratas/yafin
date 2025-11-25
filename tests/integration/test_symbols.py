from typing import AsyncGenerator, Generator

import pytest
import pytest_asyncio

from tests._assertions import (
    _assert_chart_result_list,
    _assert_insights_result_list,
    _assert_options_result_list,
    _assert_quote_summary_result_list,
    _assert_quote_types_result_list,
    _assert_quotes_result_list,
    _assert_ratings_result_list,
    _assert_recommendations_result_list,
    _assert_search_result,
    _assert_timeseries_result_list,
)
from yafin import AsyncSymbols, Symbols
from yafin.const import (
    ANNUAL_BALANCE_SHEET_TYPES,
    ANNUAL_CASH_FLOW_TYPES,
    ANNUAL_INCOME_STATEMENT_TYPES,
    QUOTE_SUMMARY_MODULES,
)


class TestUnitSymbols:
    """Integration tests for yafin.Symbols."""

    @pytest.fixture
    def symbols(self, tickers: str) -> Generator[Symbols, None, None]:
        """Fixture for Symbols."""
        with Symbols(tickers) as symbols:
            yield symbols

    @pytest.mark.integration
    def test_get_chart(
        self, symbols: Symbols, interval: str, period_range: str
    ) -> None:
        """Test get_chart method."""
        chart_result_list = symbols.get_chart(interval, period_range)
        _assert_chart_result_list(chart_result_list, symbols.tickers)

    @pytest.mark.integration
    def test_get_quote(self, symbols: Symbols) -> None:
        """Test get_quote method."""
        quotes_result_list = symbols.get_quote()
        _assert_quotes_result_list(quotes_result_list, symbols.tickers)

    @pytest.mark.integration
    def test_get_quote_type(self, symbols: Symbols) -> None:
        """Test get_quote_type method."""
        quote_types_result_list = symbols.get_quote_type()
        _assert_quote_types_result_list(quote_types_result_list, symbols.tickers)

    @pytest.mark.integration
    def test_get_quote_summary_all_modules(self, symbols: Symbols) -> None:
        """Test get_quote_summary_all_modules method."""
        quote_summary_all_modules = symbols.get_quote_summary_all_modules()
        _assert_quote_summary_result_list(
            quote_summary_all_modules, symbols.tickers, QUOTE_SUMMARY_MODULES
        )

    @pytest.mark.integration
    def test_get_income_statement(self, symbols: Symbols) -> None:
        """Test get_income_statement method."""
        frequency = 'annual'
        annual_income_stmt_list = symbols.get_income_statement(frequency)
        _assert_timeseries_result_list(
            annual_income_stmt_list,
            symbols.tickers,
            ANNUAL_INCOME_STATEMENT_TYPES,
        )

    @pytest.mark.integration
    def test_get_balance_sheet(self, symbols: Symbols) -> None:
        """Test get_balance_sheet method."""
        frequency = 'annual'
        annual_balance_sheets_list = symbols.get_balance_sheet(frequency)
        _assert_timeseries_result_list(
            annual_balance_sheets_list,
            symbols.tickers,
            ANNUAL_BALANCE_SHEET_TYPES,
        )

    @pytest.mark.integration
    def test_get_cash_flow(self, symbols: Symbols) -> None:
        """Test get_cash_flow method."""
        frequency = 'annual'
        annual_cash_flows_list = symbols.get_cash_flow(frequency)
        _assert_timeseries_result_list(
            annual_cash_flows_list, symbols.tickers, ANNUAL_CASH_FLOW_TYPES
        )

    @pytest.mark.integration
    def test_get_options(self, symbols: Symbols) -> None:
        """Test get_options method."""
        options_result_list = symbols.get_options()
        _assert_options_result_list(options_result_list, symbols.tickers)

    @pytest.mark.integration
    def test_get_search(self, symbols: Symbols) -> None:
        """Test get_search method."""
        search = symbols.get_search()
        _assert_search_result(search)

    @pytest.mark.integration
    def test_get_recommendations(self, symbols: Symbols) -> None:
        """Test get_recommendations method."""
        recommendations_result_list = symbols.get_recommendations()
        _assert_recommendations_result_list(
            recommendations_result_list, symbols.tickers
        )

    @pytest.mark.integration
    def test_get_insights(self, symbols: Symbols) -> None:
        """Test get_insights method."""
        insights_result_list = symbols.get_insights()
        _assert_insights_result_list(insights_result_list, symbols.tickers)

    @pytest.mark.integration
    def test_get_ratings(self, symbols: Symbols) -> None:
        """Test get_ratings method."""
        ratings_result_list = symbols.get_ratings()
        _assert_ratings_result_list(ratings_result_list, symbols.tickers)


class TestUnitAsyncSymbols:
    """Integration tests for yafin.AsyncSymbols."""

    @pytest_asyncio.fixture
    async def async_symbols(self, tickers: str) -> AsyncGenerator[AsyncSymbols, None]:
        """Fixture for AsyncSymbols."""
        async with AsyncSymbols(tickers) as async_symbols:
            yield async_symbols

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_get_chart(
        self, async_symbols: AsyncSymbols, interval: str, period_range: str
    ) -> None:
        """Test get_chart method."""
        chart_result_list = await async_symbols.get_chart(interval, period_range)
        _assert_chart_result_list(chart_result_list, async_symbols.tickers)

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_get_quote(self, async_symbols: AsyncSymbols) -> None:
        """Test get_quote method."""
        quotes_result_list = await async_symbols.get_quote()
        _assert_quotes_result_list(quotes_result_list, async_symbols.tickers)

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_get_quote_type(self, async_symbols: AsyncSymbols) -> None:
        """Test get_quote_type method."""
        quote_types_result_list = await async_symbols.get_quote_type()
        _assert_quote_types_result_list(quote_types_result_list, async_symbols.tickers)

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_get_quote_summary_all_modules(
        self, async_symbols: AsyncSymbols
    ) -> None:
        """Test get_quote_summary_all_modules method."""
        quote_summary_all_modules = await async_symbols.get_quote_summary_all_modules()
        _assert_quote_summary_result_list(
            quote_summary_all_modules, async_symbols.tickers, QUOTE_SUMMARY_MODULES
        )

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_get_income_statement(self, async_symbols: AsyncSymbols) -> None:
        """Test get_income_statement method."""
        frequency = 'annual'
        annual_income_stmt_list = await async_symbols.get_income_statement(frequency)
        _assert_timeseries_result_list(
            annual_income_stmt_list,
            async_symbols.tickers,
            ANNUAL_INCOME_STATEMENT_TYPES,
        )

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_get_balance_sheet(self, async_symbols: AsyncSymbols) -> None:
        """Test get_balance_sheet method."""
        frequency = 'annual'
        annual_balance_sheets_list = await async_symbols.get_balance_sheet(frequency)
        _assert_timeseries_result_list(
            annual_balance_sheets_list,
            async_symbols.tickers,
            ANNUAL_BALANCE_SHEET_TYPES,
        )

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_get_cash_flow(self, async_symbols: AsyncSymbols) -> None:
        """Test get_cash_flow method."""
        frequency = 'annual'
        annual_cash_flows_list = await async_symbols.get_cash_flow(frequency)
        _assert_timeseries_result_list(
            annual_cash_flows_list, async_symbols.tickers, ANNUAL_CASH_FLOW_TYPES
        )

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_get_options(self, async_symbols: AsyncSymbols) -> None:
        """Test get_options method."""
        options_result_list = await async_symbols.get_options()
        _assert_options_result_list(options_result_list, async_symbols.tickers)

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_get_search(self, async_symbols: AsyncSymbols) -> None:
        """Test get_search method."""
        search = await async_symbols.get_search()
        _assert_search_result(search)

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_get_recommendations(self, async_symbols: AsyncSymbols) -> None:
        """Test get_recommendations method."""
        recommendations_result_list = await async_symbols.get_recommendations()
        _assert_recommendations_result_list(
            recommendations_result_list, async_symbols.tickers
        )

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_get_insights(self, async_symbols: AsyncSymbols) -> None:
        """Test get_insights method."""
        insights_result_list = await async_symbols.get_insights()
        _assert_insights_result_list(insights_result_list, async_symbols.tickers)

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_get_ratings(self, async_symbols: AsyncSymbols) -> None:
        """Test get_ratings method."""
        ratings_result_list = await async_symbols.get_ratings()
        _assert_ratings_result_list(ratings_result_list, async_symbols.tickers)
