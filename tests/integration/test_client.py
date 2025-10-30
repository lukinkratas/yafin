from typing import AsyncGenerator

import pytest
import pytest_asyncio

from tests._assertions import (
    _assert_analysis_result,
    _assert_annual_income_stmt_result,
    _assert_chart_result,
    _assert_client_calendar_events_result,
    _assert_currencies_results,
    _assert_insights,
    _assert_market_summary_results,
    _assert_options_result,
    _assert_quote_summary_all_modules_result,
    _assert_quote_types,
    _assert_quotes,
    _assert_ratings_result,
    _assert_recommendations,
    _assert_response_json,
    _assert_search_result,
    _assert_trending_result,
)
from yafin import AsyncClient
from yafin.const import ALL_MODULES, ANNUAL_INCOME_STATEMENT_TYPES


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
        _assert_response_json(chart, 'chart')
        _assert_chart_result(chart['chart']['result'][0], ticker)

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_get_quote(self, client: AsyncClient) -> None:
        """Test get_quote method."""
        tickers = 'META,AAPL,MSFT,AMZN,GOOGL,NVDA'
        quotes = await client.get_quote(tickers)
        _assert_response_json(quotes, 'quoteResponse')
        _assert_quotes(quotes, tickers)

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_get_quote_type(self, client: AsyncClient) -> None:
        """Test get_quote_type method."""
        tickers = 'META,AAPL,MSFT,AMZN,GOOGL,NVDA'
        quote_types = await client.get_quote_type(tickers)
        _assert_response_json(quote_types, 'quoteType')
        _assert_quote_types(quote_types, tickers)

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_get_quote_summary(self, client: AsyncClient) -> None:
        """Test get_quote_summary method."""
        ticker = 'META'
        modules = ALL_MODULES
        quote_summary = await client.get_quote_summary(ticker, modules)
        _assert_response_json(quote_summary, 'quoteSummary')
        _assert_quote_summary_all_modules_result(
            quote_summary['quoteSummary']['result'][0]
        )

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_get_timeseries(self, client: AsyncClient) -> None:
        """Test get_timeseries method."""
        timeseries = await client.get_timeseries(
            ticker='META', types=ANNUAL_INCOME_STATEMENT_TYPES
        )
        _assert_response_json(timeseries, 'timeseries')
        _assert_annual_income_stmt_result(timeseries['timeseries']['result'][0])

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_get_options(self, client: AsyncClient) -> None:
        """Test get_options method."""
        ticker = 'META'
        options = await client.get_options(ticker)
        _assert_response_json(options, 'optionChain')
        _assert_options_result(options['optionChain']['result'][0], ticker)

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_get_search(self, client: AsyncClient) -> None:
        """Test get_search method."""
        search = await client.get_search(tickers='META')
        _assert_search_result(search)

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_get_recommendations(self, client: AsyncClient) -> None:
        """Test get_recommendations method."""
        tickers = 'META,AAPL,MSFT,AMZN,GOOGL,NVDA'
        recommendations = await client.get_recommendations(tickers)
        _assert_response_json(recommendations, 'finance')
        _assert_recommendations(recommendations, tickers)

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_get_insights(self, client: AsyncClient) -> None:
        """Test get_insights method."""
        tickers = 'META,AAPL,MSFT,AMZN,GOOGL,NVDA'
        insights = await client.get_insights(tickers)
        _assert_response_json(insights, 'finance')
        _assert_insights(insights, tickers)

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_get_ratings(self, client: AsyncClient) -> None:
        """Test get_ratings method."""
        ticker = 'META'
        ratings = await client.get_ratings(ticker)
        _assert_ratings_result(ratings)

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_get_analysis(self, client: AsyncClient) -> None:
        """Test get_analysis method."""
        ticker = 'META'
        analysis = await client.get_analysis(ticker)
        _assert_analysis_result(analysis, ticker)

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_get_market_summaries(self, client: AsyncClient) -> None:
        """Test get_market_summaries method."""
        market_summaries = await client.get_market_summaries()
        _assert_response_json(market_summaries, 'marketSummaryResponse')
        _assert_market_summary_results(
            market_summaries['marketSummaryResponse']['result']
        )

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_get_trending(self, client: AsyncClient) -> None:
        """Test get_trending method."""
        trending = await client.get_trending()
        _assert_response_json(trending, 'finance')
        _assert_trending_result(trending['finance']['result'][0])

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_get_currencies(self, client: AsyncClient) -> None:
        """Test get_currencies method."""
        currencies = await client.get_currencies()
        _assert_response_json(currencies, 'currencies')
        _assert_currencies_results(currencies['currencies']['result'])

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_get_calendar_events(self, client: AsyncClient) -> None:
        """Test get_calendar_events method."""
        calendar_events = await client.get_calendar_events()
        _assert_response_json(calendar_events, 'finance')
        _assert_client_calendar_events_result(calendar_events['finance']['result'])
