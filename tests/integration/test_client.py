from typing import AsyncGenerator

import pytest
import pytest_asyncio

from tests._assertions import (
    _assert_analysis_response_json,
    _assert_calendar_events_response_json,
    _assert_chart_response_json,
    _assert_currencies_response_json,
    _assert_insights_response_json,
    _assert_market_summary_response_json,
    _assert_options_response_json,
    _assert_quote_response_json,
    _assert_quote_summary_response_json,
    _assert_quote_type_response_json,
    _assert_ratings_response_json,
    _assert_recommendations_response_json,
    _assert_search_response_json,
    _assert_timeseries_response_json,
    _assert_trending_response_json,
)
from yafin import AsyncClient
from yafin.const import (
    ANNUAL_INCOME_STATEMENT_TYPES,
    CALENDAR_EVENT_MODULES,
    QUOTE_SUMMARY_MODULES,
)


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
        _assert_chart_response_json(chart, ticker)

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_get_quote(self, client: AsyncClient) -> None:
        """Test get_quote method."""
        tickers = 'META,AAPL,MSFT,AMZN,GOOGL,NVDA'
        quotes = await client.get_quote(tickers)
        _assert_quote_response_json(quotes, tickers)

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_get_quote_type(self, client: AsyncClient) -> None:
        """Test get_quote_type method."""
        tickers = 'META,AAPL,MSFT,AMZN,GOOGL,NVDA'
        quote_types = await client.get_quote_type(tickers)
        _assert_quote_type_response_json(quote_types, tickers)

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_get_quote_summary(self, client: AsyncClient) -> None:
        """Test get_quote_summary method."""
        ticker = 'META'
        modules = QUOTE_SUMMARY_MODULES
        quote_summary = await client.get_quote_summary(ticker, modules)
        _assert_quote_summary_response_json(quote_summary, modules)

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_get_timeseries(self, client: AsyncClient) -> None:
        """Test get_timeseries method."""
        ticker = 'META'
        types = ANNUAL_INCOME_STATEMENT_TYPES
        timeseries = await client.get_timeseries(ticker, types)
        _assert_timeseries_response_json(timeseries, types, ticker)

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_get_options(self, client: AsyncClient) -> None:
        """Test get_options method."""
        ticker = 'META'
        options = await client.get_options(ticker)
        _assert_options_response_json(options, ticker)

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_get_search(self, client: AsyncClient) -> None:
        """Test get_search method."""
        search = await client.get_search(tickers='META')
        _assert_search_response_json(search)

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_get_recommendations(self, client: AsyncClient) -> None:
        """Test get_recommendations method."""
        tickers = 'META,AAPL,MSFT,AMZN,GOOGL,NVDA'
        recommendations = await client.get_recommendations(tickers)
        _assert_recommendations_response_json(recommendations, tickers)

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_get_insights(self, client: AsyncClient) -> None:
        """Test get_insights method."""
        tickers = 'META,AAPL,MSFT,AMZN,GOOGL,NVDA'
        insights = await client.get_insights(tickers)
        _assert_insights_response_json(insights, tickers)

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_get_ratings(self, client: AsyncClient) -> None:
        """Test get_ratings method."""
        ticker = 'META'
        ratings = await client.get_ratings(ticker)
        _assert_ratings_response_json(ratings)

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_get_analysis(self, client: AsyncClient) -> None:
        """Test get_analysis method."""
        ticker = 'META'
        analysis = await client.get_analysis(ticker)
        _assert_analysis_response_json(analysis, ticker)

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_get_market_summaries(self, client: AsyncClient) -> None:
        """Test get_market_summaries method."""
        market_summaries = await client.get_market_summaries()
        _assert_market_summary_response_json(market_summaries)

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_get_trending(self, client: AsyncClient) -> None:
        """Test get_trending method."""
        trending = await client.get_trending()
        _assert_trending_response_json(trending)

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_get_currencies(self, client: AsyncClient) -> None:
        """Test get_currencies method."""
        currencies = await client.get_currencies()
        _assert_currencies_response_json(currencies)

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_get_calendar_events(self, client: AsyncClient) -> None:
        """Test get_calendar_events method."""
        modules = CALENDAR_EVENT_MODULES
        calendar_events = await client.get_calendar_events(modules)
        _assert_calendar_events_response_json(calendar_events)
