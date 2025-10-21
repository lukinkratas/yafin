from typing import AsyncGenerator

import pytest
import pytest_asyncio

from tests.assertions import (
    assert_annual_balance_sheet_result,
    assert_annual_cash_flow_result,
    assert_annual_income_stmt_result,
    assert_chart_result,
    assert_insights_result,
    assert_options_result,
    assert_quote_result,
    assert_quote_summary_all_modules_result,
    assert_recommendations_result,
    assert_search,
)
from yafin import AsyncSymbol


class TestUnitSymbol:
    """Integration tests for yafin.symbol module."""

    @pytest_asyncio.fixture
    async def symbol(self) -> AsyncGenerator[AsyncSymbol, None]:
        """Fixture for AsyncSymbol."""
        async with AsyncSymbol('META') as symbol:
            yield symbol

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_get_chart(self, symbol: AsyncSymbol) -> None:
        """Test get_chart method."""
        chart = await symbol.get_chart(period_range='1y', interval='1d')
        assert_chart_result(chart, symbol.ticker)

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_get_quote(self, symbol: AsyncSymbol) -> None:
        """Test get_quote method."""
        quote = await symbol.get_quote()
        assert_quote_result(quote, symbol.ticker)

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_get_quote_summary_all_modules(self, symbol: AsyncSymbol) -> None:
        """Test get_quote_summary_all_modules method."""
        quote_summary_all_modules = await symbol.get_quote_summary_all_modules()
        assert_quote_summary_all_modules_result(quote_summary_all_modules)

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_get_income_statement(self, symbol: AsyncSymbol) -> None:
        """Test get_income_statement method."""
        frequency = 'annual'
        annual_income_stmt = await symbol.get_income_statement(frequency)
        assert_annual_income_stmt_result(annual_income_stmt)

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_get_balance_sheet(self, symbol: AsyncSymbol) -> None:
        """Test get_balance_sheet method."""
        frequency = 'annual'
        annual_balance_sheet = await symbol.get_balance_sheet(frequency)
        assert_annual_balance_sheet_result(annual_balance_sheet)

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_get_cash_flow(self, symbol: AsyncSymbol) -> None:
        """Test get_cash_flow method."""
        frequency = 'annual'
        annual_cash_flow = await symbol.get_cash_flow(frequency)
        assert_annual_cash_flow_result(annual_cash_flow)

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_get_options(self, symbol: AsyncSymbol) -> None:
        """Test get_options method."""
        options = await symbol.get_options()
        assert_options_result(options, symbol.ticker)

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_get_search(self, symbol: AsyncSymbol) -> None:
        """Test get_search method."""
        search = await symbol.get_search()
        assert_search(search)

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_get_recommendations(self, symbol: AsyncSymbol) -> None:
        """Test get_recommendations method."""
        recommendations = await symbol.get_recommendations()
        assert_recommendations_result(recommendations, symbol.ticker)

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_get_insights(self, symbol: AsyncSymbol) -> None:
        """Test get_insights method."""
        insights = await symbol.get_insights()
        assert_insights_result(insights, symbol.ticker)
