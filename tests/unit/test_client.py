from datetime import datetime, timedelta
from typing import Any, AsyncGenerator, Type

import pytest
import pytest_asyncio
from curl_cffi.requests.exceptions import HTTPError
from pytest_mock import MockerFixture
from typeguard import TypeCheckError

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
    _assert_ratings_response_json,
    _assert_recommendations_response_json,
    _assert_search_response_json,
    _assert_timeseries_response_json,
    _assert_trending_response_json,
)
from tests._utils import _get_json_fixture, _mock_200_response, _mock_404_response
from yafin import AsyncClient
from yafin.const import (
    ANNUAL_INCOME_STATEMENT_TYPES,
    CALENDAR_EVENT_MODULES,
    QUOTE_SUMMARY_MODULES,
)


class TestUnitClient:
    """Unit tests for yafin.client module."""

    @pytest.mark.asyncio
    async def test_session(self) -> None:
        """Test session attribute."""
        client = AsyncClient()
        assert client._session is None

        client._get_session()
        assert client._session

        await client.close()
        assert client._session is None

        async with AsyncClient() as client:
            assert client._session

        assert client._session is None

    @pytest_asyncio.fixture
    async def client(self) -> AsyncGenerator[AsyncClient, None]:
        """Fresh new instance of AsyncClient for each tests."""
        async with AsyncClient() as client:
            yield client

    @pytest.fixture(scope='session')
    def end_date(self, period2: int | float | None) -> int | float | None:
        """Fresh new instance of end_date for each tests."""
        if period2 is None:
            return None

        return period2 + 1000

    @pytest.fixture(scope='session')
    def start_date(self, end_date: int | float | None) -> int | float | None:
        """Fresh new instance of start_date for each tests."""
        if end_date is None:
            return None

        end_type = type(end_date)
        end_date_dt = datetime.fromtimestamp(end_date / 1000)
        start_dt = end_date_dt - timedelta(days=149)
        return end_type(start_dt.timestamp() * 1000)

    @pytest.fixture(scope='session')
    def quote_json_mock(self, tickers: str) -> dict[str, Any]:
        """Mock get_quote response json with data."""
        file_name = '_'.join(tickers.lower().split(',')) + '.json'
        return _get_json_fixture(file_name, folder_name='quote')

    @pytest.fixture(scope='session')
    def quote_type_json_mock(self, tickers: str) -> dict[str, Any]:
        """Mock get_quote_type response json with data."""
        file_name = '_'.join(tickers.lower().split(',')) + '.json'
        return _get_json_fixture(file_name, folder_name='quote_type')

    @pytest.fixture(scope='session')
    def search_json_mock(self, tickers: str) -> dict[str, Any]:
        """Mock search response json with data."""
        file_name = '_'.join(tickers.lower().split(',')) + '.json'
        return _get_json_fixture(file_name, folder_name='search')

    @pytest.fixture(scope='session')
    def recommendations_json_mock(self, tickers: str) -> dict[str, Any]:
        """Mock recommendations response json with data."""
        file_name = '_'.join(tickers.lower().split(',')) + '.json'
        return _get_json_fixture(file_name, folder_name='recommendations')

    @pytest.fixture(scope='session')
    def insights_json_mock(self, tickers: str) -> dict[str, Any]:
        """Mock insights response json with data."""
        file_name = '_'.join(tickers.lower().split(',')) + '.json'
        return _get_json_fixture(file_name, folder_name='insights')

    @pytest.mark.asyncio
    async def test_get_async_request(
        self,
        client: AsyncClient,
        mocker: MockerFixture,
        chart_json_mock: dict[str, Any],
        ticker: str,
    ) -> None:
        """Test _get_async_request method."""
        _mock_200_response(mocker, response_json=chart_json_mock)
        url = f'https://query2.finance.yahoo.com/v8/finance/chart/{ticker}'
        params = {
            'formatted': 'false',
            'region': 'US',
            'lang': 'en-US',
            'corsDomain': 'finance.yahoo.com',
            'range': '1y',
            'interval': '1d',
            'events': 'div,split',
        }
        response = await client._get_async_request(url, params)
        assert response

    @pytest.mark.asyncio
    async def test_get_async_request_http_err(
        self,
        client: AsyncClient,
        mocker: MockerFixture,
    ) -> None:
        """Test _get_async_request method."""
        _mock_404_response(
            mocker,
            {
                'quoteSummary': {
                    'result': None,
                    'error': {
                        'code': 'Not Found',
                        'description': 'Quote not found for symbol: XXXXXXXX',
                    },
                }
            },
        )
        url = 'https://query2.finance.yahoo.com/v8/finance/chart/xxxxxxxx'
        params = {
            'formatted': 'false',
            'region': 'US',
            'lang': 'en-US',
            'corsDomain': 'finance.yahoo.com',
            'range': '1y',
            'interval': '1d',
            'events': 'div,split',
        }
        with pytest.raises(HTTPError):
            await client._get_async_request(url, params)

    @pytest.mark.parametrize(
        'kwargs, err_cls',
        [
            (
                dict(url=1, params={'region': 'US'}),
                TypeCheckError,
            ),
            (
                dict(url='https://query2.finance.yahoo.com/', params=1),
                TypeCheckError,
            ),
        ],
    )
    @pytest.mark.asyncio
    async def test_get_async_request_invalid_args(
        self, client: AsyncClient, kwargs: dict[str, Any], err_cls: Type[Exception]
    ) -> None:
        """Test _get_async_request method with invalid arguments."""
        with pytest.raises(err_cls):
            await client._get_async_request(**kwargs)

    @pytest.mark.asyncio
    async def test_get_crumb(self, client: AsyncClient, mocker: MockerFixture) -> None:
        """Test _get_crumb method."""
        _mock_200_response(mocker, text='test_crumb')

        assert client._crumb is None

        await client._get_crumb()
        assert client._crumb == 'test_crumb'

        await client.close()
        assert client._crumb is None

    @pytest.mark.parametrize(
        'kwargs',
        [
            dict(interval='1d'),
            dict(interval='1d', period_range='1y'),
            dict(interval='1d', period_range='1y', events='div,split,earn,capitalGain'),
            dict(
                interval='1d',
                period_range='1y',
                events=' div , split , earn , capitalGain ',
            ),
        ],
    )
    @pytest.mark.asyncio
    async def test_get_chart(
        self,
        client: AsyncClient,
        kwargs: dict[str, str],
        mocker: MockerFixture,
        chart_json_mock: dict[str, Any],
        ticker: str,
        period1: int | float | None,
        period2: int | float | None,
    ) -> None:
        """Test get_chart method."""
        _mock_200_response(mocker, response_json=chart_json_mock)
        chart = await client.get_chart(
            ticker=ticker, **kwargs, period1=period1, period2=period2
        )
        _assert_chart_response_json(chart, ticker)

    @pytest.mark.parametrize(
        'kwargs, err_cls',
        [
            (
                dict(
                    ticker=1,
                    period_range='xxx',
                    interval='1d',
                    events='div,split,earn,capitalGain',
                ),
                TypeCheckError,
            ),
            (
                dict(
                    ticker='META',
                    period_range='xxx',
                    interval='1d',
                    events='div,split,earn,capitalGain',
                ),
                ValueError,
            ),
            (
                dict(
                    ticker='META',
                    period_range=1,
                    interval='1d',
                    events='div,split,earn,capitalGain',
                ),
                TypeCheckError,
            ),
            (
                dict(
                    ticker='META',
                    period_range='1y',
                    interval='xxx',
                    events='div,split,earn,capitalGain',
                ),
                ValueError,
            ),
            (
                dict(
                    ticker='META',
                    period_range='1y',
                    interval=1,
                    events='div,split,earn,capitalGain',
                ),
                TypeCheckError,
            ),
            (
                dict(ticker='META', period_range='1y', interval='1d', events='xxx'),
                ValueError,
            ),
            (
                dict(ticker='META', period_range='1y', interval='1d', events=1),
                TypeCheckError,
            ),
        ],
    )
    @pytest.mark.asyncio
    async def test_get_chart_invalid_args(
        self, client: AsyncClient, kwargs: dict[str, Any], err_cls: Type[Exception]
    ) -> None:
        """Test get_chart method with invalid arguments."""
        with pytest.raises(err_cls):
            await client.get_chart(**kwargs)

    @pytest.mark.asyncio
    async def test_get_quote(
        self,
        client: AsyncClient,
        mocker: MockerFixture,
        quote_json_mock: dict[str, Any],
        tickers: str,
    ) -> None:
        """Test get_quote method."""
        _mock_200_response(mocker, response_json=quote_json_mock, text='test_crumb')
        quotes = await client.get_quote(tickers)
        _assert_quote_response_json(quotes, tickers)

    @pytest.mark.asyncio
    async def test_get_quote_invalid_args(
        self, client: AsyncClient, mocker: MockerFixture
    ) -> None:
        """Test get_quote method with invalid arguments."""
        _mock_200_response(mocker, text='test_crumb')
        with pytest.raises(TypeCheckError):
            await client.get_quote(tickers=1)

    @pytest.mark.asyncio
    async def test_get_quote_type(
        self,
        client: AsyncClient,
        mocker: MockerFixture,
        quote_type_json_mock: dict[str, Any],
        tickers: str,
    ) -> None:
        """Test get_quote_type method."""
        _mock_200_response(mocker, response_json=quote_type_json_mock)
        quote_types = await client.get_quote_type(tickers)
        _assert_quote_type_response_json(quote_types, tickers)

    @pytest.mark.asyncio
    async def test_get_quote_type_invalid_args(self, client: AsyncClient) -> None:
        """Test get_quote_type method with invalid arguments."""
        with pytest.raises(TypeCheckError):
            await client.get_quote_type(tickers=1)

    @pytest.mark.asyncio
    async def test_get_quote_summary(
        self,
        client: AsyncClient,
        mocker: MockerFixture,
        quote_summary_all_modules_json_mock: dict[str, Any],
        ticker: str,
    ) -> None:
        """Test get_quote_summary method."""
        _mock_200_response(
            mocker, response_json=quote_summary_all_modules_json_mock, text='test_crumb'
        )
        modules = QUOTE_SUMMARY_MODULES
        quote_summary = await client.get_quote_summary(ticker, modules)
        _assert_quote_summary_response_json(quote_summary, modules)

    @pytest.mark.parametrize(
        'kwargs, err_cls',
        [
            (dict(ticker=1, modules=QUOTE_SUMMARY_MODULES), TypeCheckError),
            (dict(ticker='META', modules='xxx'), ValueError),
            (dict(ticker='META', modules='assetProfil'), ValueError),
            (dict(ticker='META', modules=1), TypeCheckError),
        ],
    )
    @pytest.mark.asyncio
    async def test_get_quote_summary_invalid_args(
        self,
        client: AsyncClient,
        mocker: MockerFixture,
        kwargs: dict[str, Any],
        err_cls: Type[Exception],
    ) -> None:
        """Test get_quote_summary method with invalid arguments."""
        _mock_200_response(mocker, text='test_crumb')
        with pytest.raises(err_cls):
            await client.get_quote_summary(**kwargs)

    @pytest.mark.asyncio
    async def test_get_timeseries(
        self,
        client: AsyncClient,
        mocker: MockerFixture,
        timeseries_income_statement_json_mock: dict[str, Any],
        period1: int | float | None,
        period2: int | float | None,
        ticker: str,
    ) -> None:
        """Test get_timeseries method."""
        types = ANNUAL_INCOME_STATEMENT_TYPES
        _mock_200_response(mocker, response_json=timeseries_income_statement_json_mock)
        timeseries = await client.get_timeseries(
            ticker, types, period1=period1, period2=period2
        )
        _assert_timeseries_response_json(timeseries, types, ticker)

    @pytest.mark.parametrize(
        'kwargs, err_cls',
        [
            (dict(ticker=1, types=ANNUAL_INCOME_STATEMENT_TYPES), TypeCheckError),
            (dict(ticker='META', types='xxx'), ValueError),
            (dict(ticker='META', types=1), TypeCheckError),
            (
                dict(
                    ticker='META',
                    types=ANNUAL_INCOME_STATEMENT_TYPES,
                    period1='xxx',
                ),
                TypeCheckError,
            ),
            (
                dict(
                    ticker='META',
                    types=ANNUAL_INCOME_STATEMENT_TYPES,
                    period2='xxx',
                ),
                TypeCheckError,
            ),
        ],
    )
    @pytest.mark.asyncio
    async def test_get_timeseries_invalid_args(
        self, client: AsyncClient, kwargs: dict[str, Any], err_cls: Type[Exception]
    ) -> None:
        """Test get_timeseries method with invalid arguments."""
        with pytest.raises(err_cls):
            await client.get_timeseries(**kwargs)

    @pytest.mark.asyncio
    async def test_get_options(
        self,
        client: AsyncClient,
        mocker: MockerFixture,
        options_json_mock: dict[str, Any],
        ticker: str,
    ) -> None:
        """Test get_options method."""
        _mock_200_response(mocker, response_json=options_json_mock, text='test_crumb')
        options = await client.get_options(ticker)
        _assert_options_response_json(options, ticker)

    @pytest.mark.asyncio
    async def test_get_options_invalid_args(
        self, client: AsyncClient, mocker: MockerFixture
    ) -> None:
        """Test get_options method with invalid arguments."""
        _mock_200_response(mocker, text='test_crumb')
        with pytest.raises(TypeCheckError):
            await client.get_options(ticker=1)

    @pytest.mark.asyncio
    async def test_get_search(
        self,
        client: AsyncClient,
        mocker: MockerFixture,
        search_json_mock: dict[str, Any],
        tickers: str,
    ) -> None:
        """Test get_search method."""
        _mock_200_response(mocker, response_json=search_json_mock)
        search = await client.get_search(tickers)
        _assert_search_response_json(search)

    @pytest.mark.asyncio
    async def test_get_search_invalid_args(self, client: AsyncClient) -> None:
        """Test get_search method with invalid arguments."""
        with pytest.raises(TypeCheckError):
            await client.get_search(tickers=1)

    @pytest.mark.asyncio
    async def test_get_recommendations(
        self,
        client: AsyncClient,
        recommendations_json_mock: dict[str, Any],
        mocker: MockerFixture,
        tickers: str,
    ) -> None:
        """Test get_recommendations method."""
        _mock_200_response(mocker, response_json=recommendations_json_mock)
        recommendations = await client.get_recommendations(tickers)
        _assert_recommendations_response_json(recommendations, tickers)

    @pytest.mark.asyncio
    async def test_get_recommendations_invalid_args(self, client: AsyncClient) -> None:
        """Test get_recommendations method with invalid arguments."""
        with pytest.raises(TypeCheckError):
            await client.get_recommendations(tickers=1)

    @pytest.mark.asyncio
    async def test_get_insights(
        self,
        client: AsyncClient,
        mocker: MockerFixture,
        insights_json_mock: dict[str, Any],
        tickers: str,
    ) -> None:
        """Test get_insights method."""
        _mock_200_response(mocker, response_json=insights_json_mock)
        insights = await client.get_insights(tickers)
        _assert_insights_response_json(insights, tickers)

    @pytest.mark.asyncio
    async def test_get_insights_invalid_args(self, client: AsyncClient) -> None:
        """Test get_insights method with invalid arguments."""
        with pytest.raises(TypeCheckError):
            await client.get_insights(tickers=1)

    @pytest.mark.asyncio
    async def test_get_ratings(
        self,
        client: AsyncClient,
        mocker: MockerFixture,
        ratings_json_mock: dict[str, Any],
        ticker: str,
    ) -> None:
        """Test get_ratings method."""
        _mock_200_response(mocker, response_json=ratings_json_mock)
        ratings = await client.get_ratings(ticker)
        _assert_ratings_response_json(ratings)

    @pytest.mark.asyncio
    async def test_get_ratings_invalid_args(self, client: AsyncClient) -> None:
        """Test get_ratings method with invalid arguments."""
        with pytest.raises(TypeCheckError):
            await client.get_ratings(ticker=1)

    @pytest.mark.asyncio
    async def test_get_market_summaries(
        self,
        client: AsyncClient,
        mocker: MockerFixture,
        market_summaries_json_mock: dict[str, Any],
    ) -> None:
        """Test get_market_summaries method."""
        _mock_200_response(mocker, response_json=market_summaries_json_mock)
        market_summaries = await client.get_market_summaries()
        _assert_market_summary_response_json(market_summaries)

    @pytest.mark.asyncio
    async def test_get_trending(
        self,
        client: AsyncClient,
        mocker: MockerFixture,
        trending_json_mock: dict[str, Any],
    ) -> None:
        """Test get_trending method."""
        _mock_200_response(mocker, response_json=trending_json_mock)
        trending = await client.get_trending()
        _assert_trending_response_json(trending)

    @pytest.mark.asyncio
    async def test_get_currencies(
        self,
        client: AsyncClient,
        mocker: MockerFixture,
        currencies_json_mock: dict[str, Any],
    ) -> None:
        """Test get_currencies method."""
        _mock_200_response(mocker, response_json=currencies_json_mock)
        currencies = await client.get_currencies()
        _assert_currencies_response_json(currencies)

    @pytest.mark.parametrize(
        'kwargs',
        [
            dict(),
            dict(modules=CALENDAR_EVENT_MODULES),
        ],
    )
    @pytest.mark.asyncio
    async def test_get_calendar_events(
        self,
        client: AsyncClient,
        kwargs: dict[str, str],
        mocker: MockerFixture,
        client_calendar_events_json_mock: dict[str, Any],
        start_date: int | float | None,
        end_date: int | float | None,
    ) -> None:
        """Test get_calendar_events method."""
        _mock_200_response(mocker, response_json=client_calendar_events_json_mock)
        calendar_events = await client.get_calendar_events(
            **kwargs, start_date=start_date, end_date=end_date
        )
        _assert_calendar_events_response_json(calendar_events)

    @pytest.mark.parametrize(
        'kwargs, err_cls',
        [
            (dict(modules='xxx'), ValueError),
            (dict(start_date='xxx'), TypeCheckError),
            (dict(end_date='xxx'), TypeCheckError),
        ],
    )
    @pytest.mark.asyncio
    async def test_get_calendar_events_invalid_args(
        self, client: AsyncClient, kwargs: dict[str, Any], err_cls: Type[Exception]
    ) -> None:
        """Test get_calendar_events method with invalid arguments."""
        with pytest.raises(err_cls):
            await client.get_calendar_events(**kwargs)
