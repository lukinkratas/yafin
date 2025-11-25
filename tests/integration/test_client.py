from typing import AsyncGenerator, Generator

import pytest
import pytest_asyncio

from tests._assertions import (
    _assert_calendar_events_response_json,
    _assert_chart_response_json,
    _assert_currencies_response_json,
    _assert_insights_response_json,
    _assert_market_summary_response_json,
    _assert_options_response_json,
    _assert_quote_response_json,
    _assert_quote_summary_response_json,
    _assert_quote_type_response_json,
    _assert_ratings_result,
    _assert_recommendations_response_json,
    _assert_search_result,
    _assert_timeseries_response_json,
    _assert_trending_response_json,
)
from yafin import AsyncClient, Client
from yafin.const import (
    ANNUAL_INCOME_STATEMENT_TYPES,
    CALENDAR_EVENT_MODULES,
    QUOTE_SUMMARY_MODULES,
)


class TestIntegrationClient:
    """Integration tests for yafin.Client."""

    @pytest.fixture
    def client(self) -> Generator[Client, None, None]:
        """Fixture for Client."""
        with Client() as client:
            yield client

    @pytest.mark.integration
    def test_get_chart(
        self, client: Client, ticker: str, interval: str, period_range: str
    ) -> None:
        """Test get_chart method."""
        chart = client.get_chart(ticker, interval, period_range)
        _assert_chart_response_json(chart, ticker)

    @pytest.mark.integration
    def test_get_quote(self, client: Client, tickers: str) -> None:
        """Test get_quote method."""
        quotes = client.get_quote(tickers)
        _assert_quote_response_json(quotes, tickers)

    @pytest.mark.integration
    def test_get_quote_type(self, client: Client, tickers: str) -> None:
        """Test get_quote_type method."""
        quote_types = client.get_quote_type(tickers)
        _assert_quote_type_response_json(quote_types, tickers)

    @pytest.mark.integration
    def test_get_quote_summary(self, client: Client, ticker: str) -> None:
        """Test get_quote_summary method."""
        modules = QUOTE_SUMMARY_MODULES
        quote_summary = client.get_quote_summary(ticker, modules)
        _assert_quote_summary_response_json(quote_summary, modules)

    @pytest.mark.integration
    def test_get_timeseries(self, client: Client, ticker: str) -> None:
        """Test get_timeseries method."""
        types = ANNUAL_INCOME_STATEMENT_TYPES
        timeseries = client.get_timeseries(ticker, types)
        _assert_timeseries_response_json(timeseries, types, ticker)

    @pytest.mark.integration
    def test_get_options(self, client: Client, ticker: str) -> None:
        """Test get_options method."""
        options = client.get_options(ticker)
        _assert_options_response_json(options, ticker)

    @pytest.mark.integration
    def test_get_search(self, client: Client, tickers: str) -> None:
        """Test get_search method."""
        search = client.get_search(tickers)
        _assert_search_result(search)

    @pytest.mark.integration
    def test_get_recommendations(self, client: Client, tickers: str) -> None:
        """Test get_recommendations method."""
        recommendations = client.get_recommendations(tickers)
        _assert_recommendations_response_json(recommendations, tickers)

    @pytest.mark.integration
    def test_get_insights(self, client: Client, tickers: str) -> None:
        """Test get_insights method."""
        insights = client.get_insights(tickers)
        _assert_insights_response_json(insights, tickers)

    @pytest.mark.integration
    def test_get_ratings(self, client: Client, ticker: str) -> None:
        """Test get_ratings method."""
        ratings = client.get_ratings(ticker)
        _assert_ratings_result(ratings, ticker)

    @pytest.mark.integration
    def test_get_market_summaries(self, client: Client) -> None:
        """Test get_market_summaries method."""
        market_summaries = client.get_market_summaries()
        _assert_market_summary_response_json(market_summaries)

    @pytest.mark.integration
    def test_get_trending(self, client: Client) -> None:
        """Test get_trending method."""
        trending = client.get_trending()
        _assert_trending_response_json(trending)

    @pytest.mark.integration
    def test_get_currencies(self, client: Client) -> None:
        """Test get_currencies method."""
        currencies = client.get_currencies()
        _assert_currencies_response_json(currencies)

    @pytest.mark.integration
    def test_get_calendar_events(self, client: Client) -> None:
        """Test get_calendar_events method."""
        modules = CALENDAR_EVENT_MODULES
        calendar_events = client.get_calendar_events(modules)
        _assert_calendar_events_response_json(calendar_events)


class TestIntegrationAsyncClient:
    """Integration tests for yafin.AsyncClient."""

    @pytest_asyncio.fixture
    async def async_client(self) -> AsyncGenerator[AsyncClient, None]:
        """Fixture for AsyncClient."""
        async with AsyncClient() as async_client:
            yield async_client

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_get_chart(
        self, async_client: AsyncClient, ticker: str, interval: str, period_range: str
    ) -> None:
        """Test get_chart method."""
        chart = await async_client.get_chart(ticker, interval, period_range)
        _assert_chart_response_json(chart, ticker)

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_get_quote(self, async_client: AsyncClient, tickers: str) -> None:
        """Test get_quote method."""
        quotes = await async_client.get_quote(tickers)
        _assert_quote_response_json(quotes, tickers)

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_get_quote_type(
        self, async_client: AsyncClient, tickers: str
    ) -> None:
        """Test get_quote_type method."""
        quote_types = await async_client.get_quote_type(tickers)
        _assert_quote_type_response_json(quote_types, tickers)

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_get_quote_summary(
        self, async_client: AsyncClient, ticker: str
    ) -> None:
        """Test get_quote_summary method."""
        modules = QUOTE_SUMMARY_MODULES
        quote_summary = await async_client.get_quote_summary(ticker, modules)
        _assert_quote_summary_response_json(quote_summary, modules)

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_get_timeseries(self, async_client: AsyncClient, ticker: str) -> None:
        """Test get_timeseries method."""
        types = ANNUAL_INCOME_STATEMENT_TYPES
        timeseries = await async_client.get_timeseries(ticker, types)
        _assert_timeseries_response_json(timeseries, types, ticker)

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_get_options(self, async_client: AsyncClient, ticker: str) -> None:
        """Test get_options method."""
        options = await async_client.get_options(ticker)
        _assert_options_response_json(options, ticker)

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_get_search(self, async_client: AsyncClient, tickers: str) -> None:
        """Test get_search method."""
        search = await async_client.get_search(tickers)
        _assert_search_result(search)

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_get_recommendations(
        self, async_client: AsyncClient, tickers: str
    ) -> None:
        """Test get_recommendations method."""
        recommendations = await async_client.get_recommendations(tickers)
        _assert_recommendations_response_json(recommendations, tickers)

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_get_insights(self, async_client: AsyncClient, tickers: str) -> None:
        """Test get_insights method."""
        insights = await async_client.get_insights(tickers)
        _assert_insights_response_json(insights, tickers)

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_get_ratings(self, async_client: AsyncClient, ticker: str) -> None:
        """Test get_ratings method."""
        ratings = await async_client.get_ratings(ticker)
        _assert_ratings_result(ratings, ticker)

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_get_market_summaries(self, async_client: AsyncClient) -> None:
        """Test get_market_summaries method."""
        market_summaries = await async_client.get_market_summaries()
        _assert_market_summary_response_json(market_summaries)

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_get_trending(self, async_client: AsyncClient) -> None:
        """Test get_trending method."""
        trending = await async_client.get_trending()
        _assert_trending_response_json(trending)

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_get_currencies(self, async_client: AsyncClient) -> None:
        """Test get_currencies method."""
        currencies = await async_client.get_currencies()
        _assert_currencies_response_json(currencies)

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_get_calendar_events(self, async_client: AsyncClient) -> None:
        """Test get_calendar_events method."""
        modules = CALENDAR_EVENT_MODULES
        calendar_events = await async_client.get_calendar_events(modules)
        _assert_calendar_events_response_json(calendar_events)
