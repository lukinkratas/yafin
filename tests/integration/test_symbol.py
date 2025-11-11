from typing import AsyncGenerator

import pytest
import pytest_asyncio

from tests._assertions import (
    _assert_chart_result,
    _assert_insight_result,
    _assert_options_result,
    _assert_quote_result,
    _assert_quote_summary_result,
    _assert_quote_type_result,
    _assert_ratings_response_json,
    _assert_recommendation_result,
    _assert_search_response_json,
    _assert_timeseries_result,
)
from yafin import AsyncSymbol
from yafin.const import (
    ANNUAL_BALANCE_SHEET_TYPES,
    ANNUAL_CASH_FLOW_TYPES,
    ANNUAL_INCOME_STATEMENT_TYPES,
    QUOTE_SUMMARY_MODULES,
)


class TestUnitSymbol:
    """Integration tests for yafin.symbol module."""

    @pytest_asyncio.fixture
    async def symbol(self, ticker: str) -> AsyncGenerator[AsyncSymbol, None]:
        """Fixture for AsyncSymbol."""
        async with AsyncSymbol(ticker) as symbol:
            yield symbol

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_get_chart(self, symbol: AsyncSymbol) -> None:
        """Test get_chart method."""
        chart_result = await symbol.get_chart(interval='1d', period_range='1y')
        _assert_chart_result(chart_result, symbol.ticker)

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_get_quote(self, symbol: AsyncSymbol) -> None:
        """Test get_quote method."""
        quote_result = await symbol.get_quote()
        _assert_quote_result(quote_result, symbol.ticker)

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_get_quote_type(self, symbol: AsyncSymbol) -> None:
        """Test get_quote_type method."""
        quote_type_result = await symbol.get_quote_type()
        _assert_quote_type_result(quote_type_result, symbol.ticker)

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_get_quote_summary_all_modules(self, symbol: AsyncSymbol) -> None:
        """Test get_quote_summary_all_modules method."""
        quote_summary_all_modules = await symbol.get_quote_summary_all_modules()
        _assert_quote_summary_result(
            quote_summary_all_modules, modules=QUOTE_SUMMARY_MODULES
        )

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_get_income_statement(self, symbol: AsyncSymbol) -> None:
        """Test get_income_statement method."""
        frequency = 'annual'
        annual_income_stmt = await symbol.get_income_statement(frequency)
        _assert_timeseries_result(
            annual_income_stmt,
            types=ANNUAL_INCOME_STATEMENT_TYPES,
            ticker=symbol.ticker,
        )

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_get_balance_sheet(self, symbol: AsyncSymbol) -> None:
        """Test get_balance_sheet method."""
        frequency = 'annual'
        annual_balance_sheet = await symbol.get_balance_sheet(frequency)
        _assert_timeseries_result(
            annual_balance_sheet, types=ANNUAL_BALANCE_SHEET_TYPES, ticker=symbol.ticker
        )

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_get_cash_flow(self, symbol: AsyncSymbol) -> None:
        """Test get_cash_flow method."""
        frequency = 'annual'
        annual_cash_flow = await symbol.get_cash_flow(frequency)
        _assert_timeseries_result(
            annual_cash_flow, types=ANNUAL_CASH_FLOW_TYPES, ticker=symbol.ticker
        )

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_get_options(self, symbol: AsyncSymbol) -> None:
        """Test get_options method."""
        options = await symbol.get_options()
        _assert_options_result(options, symbol.ticker)

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_get_search(self, symbol: AsyncSymbol) -> None:
        """Test get_search method."""
        search = await symbol.get_search()
        _assert_search_response_json(search)

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_get_recommendations(self, symbol: AsyncSymbol) -> None:
        """Test get_recommendations method."""
        recommendations = await symbol.get_recommendations()
        _assert_recommendation_result(recommendations, symbol.ticker)

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_get_insights(self, symbol: AsyncSymbol) -> None:
        """Test get_insights method."""
        insights = await symbol.get_insights()
        _assert_insight_result(insights, symbol.ticker)

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_get_ratings(self, symbol: AsyncSymbol) -> None:
        """Test get_ratings method."""
        ratings = await symbol.get_ratings()
        _assert_ratings_response_json(ratings)
