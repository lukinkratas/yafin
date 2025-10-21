from typing import AsyncGenerator

import pytest
import pytest_asyncio

from tests.assertions import (
    assert_annual_income_stmt_result,
    assert_chart_result,
    assert_currencies_result,
    assert_insights_result,
    assert_market_summaries_result,
    assert_options_result,
    assert_quote_summary_all_modules_result,
    assert_quotes,
    assert_recommendations_result,
    assert_response_json,
    assert_search,
    assert_trending_result,
)
from yafin import AsyncClient
from yafin.const import ALL_MODULES_CSV
from yafin.utils import get_types_with_frequency


class TestIntegrationClient:
    """Integration tests for yafin.client module."""

    @pytest_asyncio.fixture
    async def client(self) -> AsyncGenerator[AsyncClient, None]:
        """Fixture for AsyncClient."""
        async with AsyncClient() as client:
            yield client

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_get_chart(self, client: AsyncClient) -> None:
        """Test get_chart method."""
        ticker = 'META'
        chart = await client.get_chart(ticker, period_range='1y', interval='1d')
        assert_response_json(chart, 'chart')
        assert_chart_result(chart['chart']['result'][0], ticker)

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_get_quote(self, client: AsyncClient) -> None:
        """Test get_quote method."""
        tickers = 'META,AAPL,MSFT,AMZN,GOOGL,NVDA'
        quotes = await client.get_quote(tickers)
        assert_response_json(quotes, 'quoteResponse')
        assert_quotes(quotes, tickers)

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_get_quote_summary(self, client: AsyncClient) -> None:
        """Test get_quote_summary method."""
        ticker = 'META'
        modules = ALL_MODULES_CSV
        quote_summary = await client.get_quote_summary(ticker, modules)
        assert_response_json(quote_summary, 'quoteSummary')
        assert_quote_summary_all_modules_result(
            quote_summary['quoteSummary']['result'][0]
        )

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_get_timeseries(self, client: AsyncClient) -> None:
        """Test get_timeseries method."""
        types = get_types_with_frequency(frequency='annual', typ='income_statement')
        timeseries = await client.get_timeseries(ticker='META', types=types)
        assert_response_json(timeseries, 'timeseries')
        assert_annual_income_stmt_result(timeseries['timeseries']['result'])

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_get_options(self, client: AsyncClient) -> None:
        """Test get_options method."""
        ticker = 'META'
        options = await client.get_options(ticker)
        assert_response_json(options, 'optionChain')
        assert_options_result(options['optionChain']['result'][0], ticker)

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_get_search(self, client: AsyncClient) -> None:
        """Test get_search method."""
        search = await client.get_search(tickers='META')
        assert_search(search)

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_get_recommendations(self, client: AsyncClient) -> None:
        """Test get_recommendations method."""
        ticker = 'META'
        recommendations = await client.get_recommendations(ticker)
        assert_response_json(recommendations, 'finance')
        assert_recommendations_result(recommendations['finance']['result'][0], ticker)

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_get_insights(self, client: AsyncClient) -> None:
        """Test get_insights method."""
        ticker = 'META'
        insights = await client.get_insights(ticker)
        assert_response_json(insights, 'finance')
        assert_insights_result(insights['finance']['result'], ticker)

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_get_market_summaries(self, client: AsyncClient) -> None:
        """Test get_market_summaries method."""
        market_summaries = await client.get_market_summaries()
        assert_response_json(market_summaries, 'marketSummaryResponse')
        assert_market_summaries_result(
            market_summaries['marketSummaryResponse']['result']
        )

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_get_trending(self, client: AsyncClient) -> None:
        """Test get_trending method."""
        trending = await client.get_trending()
        assert_response_json(trending, 'finance')
        assert_trending_result(trending['finance']['result'][0])

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_get_currencies(self, client: AsyncClient) -> None:
        """Test get_currencies method."""
        currencies = await client.get_currencies()
        assert_response_json(currencies, 'currencies')
        assert_currencies_result(currencies['currencies']['result'])
