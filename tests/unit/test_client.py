from datetime import datetime, timedelta
from typing import Any, AsyncGenerator, Generator

import pytest
import pytest_asyncio
from curl_cffi.requests.exceptions import HTTPError
from pytest_mock import MockerFixture

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
from tests._utils import _get_json_fixture, _mock_response
from yafin import AsyncClient, Client
from yafin.client import _SingletonAsyncClientManager, _SingletonClientManager
from yafin.const import (
    ANNUAL_INCOME_STATEMENT_TYPES,
    CALENDAR_EVENT_MODULES,
    QUOTE_SUMMARY_MODULES,
)


@pytest.fixture
def end_date(period2: int | float | None) -> int | float | None:
    """Fresh new instance of end_date for each tests."""
    if period2 is None:
        return None

    return period2 * 1000


@pytest.fixture
def start_date(end_date: int | float | None) -> int | float | None:
    """Fresh new instance of start_date for each tests."""
    if end_date is None:
        return None

    end_type = type(end_date)
    end_date_dt = datetime.fromtimestamp(end_date / 1000)
    start_dt = end_date_dt - timedelta(days=149)
    return end_type(start_dt.timestamp() * 1000)


@pytest.fixture
def quote_json_mock(tickers_name: str) -> dict[str, Any]:
    """Quote response json mock."""
    return _get_json_fixture(file_name=f'{tickers_name}.json', folder_name='quote')


@pytest.fixture
def quote_type_json_mock(tickers_name: str) -> dict[str, Any]:
    """Quote_type response json mock."""
    return _get_json_fixture(file_name=f'{tickers_name}.json', folder_name='quote_type')


@pytest.fixture
def search_json_mock(tickers_name: str) -> dict[str, Any]:
    """Search response json mock."""
    return _get_json_fixture(file_name=f'{tickers_name}.json', folder_name='search')


@pytest.fixture
def recommendations_json_mock(tickers_name: str) -> dict[str, Any]:
    """Recommendations response json mock."""
    return _get_json_fixture(
        file_name=f'{tickers_name}.json', folder_name='recommendations'
    )


@pytest.fixture
def insights_json_mock(tickers_name: str) -> dict[str, Any]:
    """Insights response json mock."""
    return _get_json_fixture(file_name=f'{tickers_name}.json', folder_name='insights')


@pytest.fixture
def calendar_events_json_mock() -> dict[str, Any]:
    """Currencies response json mock."""
    return _get_json_fixture(file_name='calendar_events.json')


@pytest.fixture(
    params=[
        dict(),
        dict(events='div,split,earn,capitalGain'),
        dict(events=' div , split , earn , capitalGain '),
    ]
)
def chart_kwargs(request: pytest.FixtureRequest) -> dict[str, Any]:
    """Fresh new instance of kwargs for chart for each test."""
    return request.param


@pytest.fixture(
    params=[
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
                period_range='1y',
                interval='xxx',
                events='div,split,earn,capitalGain',
            ),
            ValueError,
        ),
        (
            dict(ticker='META', period_range='1y', interval='1d', events='xxx'),
            ValueError,
        ),
    ],
    scope='session',
)
def invalid_chart_kwargs_err_tuple(
    request: pytest.FixtureRequest,
) -> tuple[dict[str, Any], type[Exception]]:
    """Fresh new instance of invalid kwargs, err tuple for chart for each test."""
    return request.param


@pytest.fixture(
    params=[
        (dict(ticker='META', types='xxx'), ValueError),
    ]
)
def invalid_timeseries_kwargs_err_tuple(
    request: pytest.FixtureRequest,
) -> tuple[dict[str, Any], type[Exception]]:
    """Fresh new instance of invalid kwargs, err tuple for timeseries for each test."""
    return request.param


@pytest.fixture(
    params=[
        dict(),
        dict(modules=CALENDAR_EVENT_MODULES),
    ]
)
def calendar_events_kwargs(
    request: pytest.FixtureRequest,
) -> tuple[dict[str, Any], type[Exception]]:
    """Fresh new instance of kwargs for calendar events for each test."""
    return request.param


@pytest.fixture(
    params=[
        (dict(ticker='META', modules='xxx'), ValueError),
        (dict(ticker='META', modules='assetProfil'), ValueError),
    ]
)
def invalid_quote_summary_kwargs_err_tuple(
    request: pytest.FixtureRequest,
) -> tuple[dict[str, Any], type[Exception]]:
    """Fresh new instance of invalid kwargs, err tuple for quote summary for each
    test.
    """
    return request.param


class TestUnitClient:
    """Unit tests for yafin.Client."""

    def test_session(self) -> None:
        """Test session attribute."""
        client = Client()
        assert client._session is None

        client._get_session()
        assert client._session

        client.close()
        assert client._session is None

        with Client() as client:
            assert client._session

        assert client._session is None

    @pytest.fixture
    def client(self) -> Generator[Client, None, None]:
        """Fresh new instance of Client for each tests."""
        with Client() as client:
            yield client

    def test_get_request(
        self,
        client: Client,
        mocker: MockerFixture,
        chart_json_mock: dict[str, Any],
        ticker: str,
        interval: str,
        period_range: str | None,
    ) -> None:
        """Test _get_request method."""
        _mock_response(
            mocker,
            patched_method='yafin.client.Session.get',
            response_jsons=[chart_json_mock],
        )
        params = (
            client._DEFAULT_PARAMS
            | client._CHART_PARAMS
            | {
                'range': period_range,
                'interval': interval,
            }
        )
        response = client._get_request(client._CHART_URL.format(ticker=ticker), params)
        assert response

    def test_get_request_http_err(
        self,
        client: Client,
        mocker: MockerFixture,
        interval: str,
        period_range: str | None,
    ) -> None:
        """Test _get_request method."""
        _mock_response(
            mocker,
            patched_method='yafin.client.Session.get',
            status_code=404,
            response_jsons=[
                {
                    'quoteSummary': {
                        'result': None,
                        'error': {
                            'code': 'Not Found',
                            'description': 'Quote not found for symbol: XXXXXXXX',
                        },
                    }
                }
            ],
        )
        params = (
            client._DEFAULT_PARAMS
            | client._CHART_PARAMS
            | {
                'range': period_range,
                'interval': interval,
                'events': 'div,split',
            }
        )
        with pytest.raises(HTTPError):
            client._get_request(client._CHART_URL.format(ticker='xxxxxxxx'), params)

    def test_get_crumb(self, client: Client, mocker: MockerFixture) -> None:
        """Test _get_crumb method."""
        _mock_response(
            mocker, patched_method='yafin.client.Session.get', text='test_crumb'
        )

        assert client._crumb is None

        client._get_crumb()
        assert client._crumb == 'test_crumb'

        client.close()
        assert client._crumb is None

    def test_get_chart(
        self,
        client: Client,
        chart_kwargs: dict[str, str],
        mocker: MockerFixture,
        chart_json_mock: dict[str, Any],
        ticker: str,
        interval: str,
        period_range: str | None,
        period1: int | float | None,
        period2: int | float | None,
    ) -> None:
        """Test get_chart method."""
        _mock_response(
            mocker,
            patched_method='yafin.client.Session.get',
            response_jsons=[chart_json_mock],
        )
        chart = client.get_chart(
            ticker=ticker,
            interval=interval,
            period_range=period_range,
            period1=period1,
            period2=period2,
            **chart_kwargs,
        )
        _assert_chart_response_json(chart, ticker)

    def test_get_chart_invalid_args(
        self,
        client: Client,
        invalid_chart_kwargs_err_tuple: tuple[dict[str, Any], type[Exception]],
    ) -> None:
        """Test get_chart method with invalid arguments."""
        kwargs, err_cls = invalid_chart_kwargs_err_tuple
        with pytest.raises(err_cls):
            client.get_chart(**kwargs)

    def test_get_quote(
        self,
        client: Client,
        mocker: MockerFixture,
        quote_json_mock: dict[str, Any],
        tickers: str,
    ) -> None:
        """Test get_quote method."""
        _mock_response(
            mocker,
            patched_method='yafin.client.Session.get',
            response_jsons=[quote_json_mock],
            text='test_crumb',
        )
        quotes = client.get_quote(tickers)
        _assert_quote_response_json(quotes, tickers)

    def test_get_quote_type(
        self,
        client: Client,
        mocker: MockerFixture,
        quote_type_json_mock: dict[str, Any],
        tickers: str,
    ) -> None:
        """Test get_quote_type method."""
        _mock_response(
            mocker,
            patched_method='yafin.client.Session.get',
            response_jsons=[quote_type_json_mock],
        )
        quote_types = client.get_quote_type(tickers)
        _assert_quote_type_response_json(quote_types, tickers)

    def test_get_quote_summary(
        self,
        client: Client,
        mocker: MockerFixture,
        quote_summary_all_modules_json_mock: dict[str, Any],
        ticker: str,
    ) -> None:
        """Test get_quote_summary method."""
        _mock_response(
            mocker,
            patched_method='yafin.client.Session.get',
            response_jsons=[quote_summary_all_modules_json_mock],
            text='test_crumb',
        )
        modules = QUOTE_SUMMARY_MODULES
        quote_summary = client.get_quote_summary(ticker, modules)
        _assert_quote_summary_response_json(quote_summary, modules)

    def test_get_quote_summary_invalid_args(
        self,
        client: Client,
        mocker: MockerFixture,
        invalid_quote_summary_kwargs_err_tuple: tuple[dict[str, Any], type[Exception]],
    ) -> None:
        """Test get_quote_summary method with invalid arguments."""
        _mock_response(
            mocker, patched_method='yafin.client.Session.get', text='test_crumb'
        )
        kwargs, err_cls = invalid_quote_summary_kwargs_err_tuple
        with pytest.raises(err_cls):
            client.get_quote_summary(**kwargs)

    def test_get_timeseries(
        self,
        client: Client,
        mocker: MockerFixture,
        timeseries_income_statement_json_mock: dict[str, Any],
        period1: int | float | None,
        period2: int | float | None,
        ticker: str,
    ) -> None:
        """Test get_timeseries method."""
        types = ANNUAL_INCOME_STATEMENT_TYPES
        _mock_response(
            mocker,
            patched_method='yafin.client.Session.get',
            response_jsons=[timeseries_income_statement_json_mock],
        )
        timeseries = client.get_timeseries(
            ticker, types, period1=period1, period2=period2
        )
        _assert_timeseries_response_json(timeseries, types, ticker)

    def test_get_timeseries_invalid_args(self, client: Client) -> None:
        """Test get_timeseries method with invalid arguments."""
        with pytest.raises(ValueError):
            client.get_timeseries(ticker='META', types='xxx')

    def test_get_options(
        self,
        client: Client,
        mocker: MockerFixture,
        options_json_mock: dict[str, Any],
        ticker: str,
    ) -> None:
        """Test get_options method."""
        _mock_response(
            mocker,
            patched_method='yafin.client.Session.get',
            response_jsons=[options_json_mock],
            text='test_crumb',
        )
        options = client.get_options(ticker)
        _assert_options_response_json(options, ticker)

    def test_get_search(
        self,
        client: Client,
        mocker: MockerFixture,
        search_json_mock: dict[str, Any],
        tickers: str,
    ) -> None:
        """Test get_search method."""
        _mock_response(
            mocker,
            patched_method='yafin.client.Session.get',
            response_jsons=[search_json_mock],
        )
        search = client.get_search(tickers)
        _assert_search_result(search)

    def test_get_recommendations(
        self,
        client: Client,
        recommendations_json_mock: dict[str, Any],
        mocker: MockerFixture,
        tickers: str,
    ) -> None:
        """Test get_recommendations method."""
        _mock_response(
            mocker,
            patched_method='yafin.client.Session.get',
            response_jsons=[recommendations_json_mock],
        )
        recommendations = client.get_recommendations(tickers)
        _assert_recommendations_response_json(recommendations, tickers)

    def test_get_insights(
        self,
        client: Client,
        mocker: MockerFixture,
        insights_json_mock: dict[str, Any],
        tickers: str,
    ) -> None:
        """Test get_insights method."""
        _mock_response(
            mocker,
            patched_method='yafin.client.Session.get',
            response_jsons=[insights_json_mock],
        )
        insights = client.get_insights(tickers)
        _assert_insights_response_json(insights, tickers)

    def test_get_ratings(
        self,
        client: Client,
        mocker: MockerFixture,
        ratings_json_mock: dict[str, Any],
        ticker: str,
    ) -> None:
        """Test get_ratings method."""
        _mock_response(
            mocker,
            patched_method='yafin.client.Session.get',
            response_jsons=[ratings_json_mock],
        )
        ratings = client.get_ratings(ticker)
        _assert_ratings_result(ratings, ticker)

    def test_get_market_summaries(
        self,
        client: Client,
        mocker: MockerFixture,
        market_summaries_json_mock: dict[str, Any],
    ) -> None:
        """Test get_market_summaries method."""
        _mock_response(
            mocker,
            patched_method='yafin.client.Session.get',
            response_jsons=[market_summaries_json_mock],
        )
        market_summaries = client.get_market_summaries()
        _assert_market_summary_response_json(market_summaries)

    def test_get_trending(
        self,
        client: Client,
        mocker: MockerFixture,
        trending_json_mock: dict[str, Any],
    ) -> None:
        """Test get_trending method."""
        _mock_response(
            mocker,
            patched_method='yafin.client.Session.get',
            response_jsons=[trending_json_mock],
        )
        trending = client.get_trending()
        _assert_trending_response_json(trending)

    def test_get_currencies(
        self,
        client: Client,
        mocker: MockerFixture,
        currencies_json_mock: dict[str, Any],
    ) -> None:
        """Test get_currencies method."""
        _mock_response(
            mocker,
            patched_method='yafin.client.Session.get',
            response_jsons=[currencies_json_mock],
        )
        currencies = client.get_currencies()
        _assert_currencies_response_json(currencies)

    def test_get_calendar_events(
        self,
        client: Client,
        calendar_events_kwargs: dict[str, str],
        mocker: MockerFixture,
        calendar_events_json_mock: dict[str, Any],
        start_date: int | float | None,
        end_date: int | float | None,
    ) -> None:
        """Test get_calendar_events method."""
        _mock_response(
            mocker,
            patched_method='yafin.client.Session.get',
            response_jsons=[calendar_events_json_mock],
        )
        calendar_events = client.get_calendar_events(
            **calendar_events_kwargs, start_date=start_date, end_date=end_date
        )
        _assert_calendar_events_response_json(calendar_events)

    def test_get_calendar_events_invalid_args(self, client: Client) -> None:
        """Test get_calendar_events method with invalid arguments."""
        with pytest.raises(ValueError):
            client.get_calendar_events(modules='xxx')


class TestUnitAsyncClient:
    """Unit tests for yafin.AsyncClient."""

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
    async def async_client(self) -> AsyncGenerator[AsyncClient, None]:
        """Fresh new instance of AsyncClient for each tests."""
        async with AsyncClient() as async_client:
            yield async_client

    @pytest.mark.asyncio
    async def test_get_request(
        self,
        async_client: AsyncClient,
        mocker: MockerFixture,
        chart_json_mock: dict[str, Any],
        ticker: str,
    ) -> None:
        """Test _get_request method."""
        _mock_response(
            mocker,
            patched_method='yafin.client.AsyncSession.get',
            response_jsons=[chart_json_mock],
            async_mock=True,
        )
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
        response = await async_client._get_request(url, params)
        assert response

    @pytest.mark.asyncio
    async def test_get_request_http_err(
        self, async_client: AsyncClient, mocker: MockerFixture
    ) -> None:
        """Test _get_request method."""
        _mock_response(
            mocker,
            patched_method='yafin.client.AsyncSession.get',
            status_code=404,
            response_jsons=[
                {
                    'quoteSummary': {
                        'result': None,
                        'error': {
                            'code': 'Not Found',
                            'description': 'Quote not found for symbol: XXXXXXXX',
                        },
                    }
                }
            ],
            async_mock=True,
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
            await async_client._get_request(url, params)

    @pytest.mark.asyncio
    async def test_get_crumb(
        self, async_client: AsyncClient, mocker: MockerFixture
    ) -> None:
        """Test _get_crumb method."""
        _mock_response(
            mocker,
            patched_method='yafin.client.AsyncSession.get',
            text='test_crumb',
            async_mock=True,
        )

        assert async_client._crumb is None

        await async_client._get_crumb()
        assert async_client._crumb == 'test_crumb'

        await async_client.close()
        assert async_client._crumb is None

    @pytest.mark.asyncio
    async def test_get_chart(
        self,
        async_client: AsyncClient,
        chart_kwargs: dict[str, str],
        mocker: MockerFixture,
        chart_json_mock: dict[str, Any],
        ticker: str,
        interval: str,
        period_range: str | None,
        period1: int | float | None,
        period2: int | float | None,
    ) -> None:
        """Test get_chart method."""
        _mock_response(
            mocker,
            patched_method='yafin.client.AsyncSession.get',
            response_jsons=[chart_json_mock],
            async_mock=True,
        )
        chart = await async_client.get_chart(
            ticker=ticker,
            interval=interval,
            period_range=period_range,
            period1=period1,
            period2=period2,
            **chart_kwargs,
        )
        _assert_chart_response_json(chart, ticker)

    @pytest.mark.asyncio
    async def test_get_chart_invalid_args(
        self,
        async_client: AsyncClient,
        invalid_chart_kwargs_err_tuple: tuple[dict[str, Any], type[Exception]],
    ) -> None:
        """Test get_chart method with invalid arguments."""
        kwargs, err_cls = invalid_chart_kwargs_err_tuple
        with pytest.raises(err_cls):
            await async_client.get_chart(**kwargs)

    @pytest.mark.asyncio
    async def test_get_quote(
        self,
        async_client: AsyncClient,
        mocker: MockerFixture,
        quote_json_mock: dict[str, Any],
        tickers: str,
    ) -> None:
        """Test get_quote method."""
        _mock_response(
            mocker,
            patched_method='yafin.client.AsyncSession.get',
            response_jsons=[quote_json_mock],
            text='test_crumb',
            async_mock=True,
        )
        quotes = await async_client.get_quote(tickers)
        _assert_quote_response_json(quotes, tickers)

    @pytest.mark.asyncio
    async def test_get_quote_type(
        self,
        async_client: AsyncClient,
        mocker: MockerFixture,
        quote_type_json_mock: dict[str, Any],
        tickers: str,
    ) -> None:
        """Test get_quote_type method."""
        _mock_response(
            mocker,
            patched_method='yafin.client.AsyncSession.get',
            response_jsons=[quote_type_json_mock],
            async_mock=True,
        )
        quote_types = await async_client.get_quote_type(tickers)
        _assert_quote_type_response_json(quote_types, tickers)

    @pytest.mark.asyncio
    async def test_get_quote_summary(
        self,
        async_client: AsyncClient,
        mocker: MockerFixture,
        quote_summary_all_modules_json_mock: dict[str, Any],
        ticker: str,
    ) -> None:
        """Test get_quote_summary method."""
        _mock_response(
            mocker,
            patched_method='yafin.client.AsyncSession.get',
            response_jsons=[quote_summary_all_modules_json_mock],
            text='test_crumb',
            async_mock=True,
        )
        modules = QUOTE_SUMMARY_MODULES
        quote_summary = await async_client.get_quote_summary(ticker, modules)
        _assert_quote_summary_response_json(quote_summary, modules)

    @pytest.mark.asyncio
    async def test_get_quote_summary_invalid_args(
        self,
        async_client: AsyncClient,
        mocker: MockerFixture,
        invalid_quote_summary_kwargs_err_tuple: tuple[dict[str, Any], type[Exception]],
    ) -> None:
        """Test get_quote_summary method with invalid arguments."""
        _mock_response(
            mocker,
            patched_method='yafin.client.AsyncSession.get',
            text='test_crumb',
            async_mock=True,
        )
        kwargs, err_cls = invalid_quote_summary_kwargs_err_tuple
        with pytest.raises(err_cls):
            await async_client.get_quote_summary(**kwargs)

    @pytest.mark.asyncio
    async def test_get_timeseries(
        self,
        async_client: AsyncClient,
        mocker: MockerFixture,
        timeseries_income_statement_json_mock: dict[str, Any],
        period1: int | float | None,
        period2: int | float | None,
        ticker: str,
    ) -> None:
        """Test get_timeseries method."""
        types = ANNUAL_INCOME_STATEMENT_TYPES
        _mock_response(
            mocker,
            patched_method='yafin.client.AsyncSession.get',
            response_jsons=[timeseries_income_statement_json_mock],
            async_mock=True,
        )
        timeseries = await async_client.get_timeseries(
            ticker, types, period1=period1, period2=period2
        )
        _assert_timeseries_response_json(timeseries, types, ticker)

    @pytest.mark.asyncio
    async def test_get_timeseries_invalid_args(self, async_client: AsyncClient) -> None:
        """Test get_timeseries method with invalid arguments."""
        with pytest.raises(ValueError):
            await async_client.get_timeseries(ticker='META', types='xxx')

    @pytest.mark.asyncio
    async def test_get_options(
        self,
        async_client: AsyncClient,
        mocker: MockerFixture,
        options_json_mock: dict[str, Any],
        ticker: str,
    ) -> None:
        """Test get_options method."""
        _mock_response(
            mocker,
            patched_method='yafin.client.AsyncSession.get',
            response_jsons=[options_json_mock],
            text='test_crumb',
            async_mock=True,
        )
        options = await async_client.get_options(ticker)
        _assert_options_response_json(options, ticker)

    @pytest.mark.asyncio
    async def test_get_search(
        self,
        async_client: AsyncClient,
        mocker: MockerFixture,
        search_json_mock: dict[str, Any],
        tickers: str,
    ) -> None:
        """Test get_search method."""
        _mock_response(
            mocker,
            patched_method='yafin.client.AsyncSession.get',
            response_jsons=[search_json_mock],
            async_mock=True,
        )
        search = await async_client.get_search(tickers)
        _assert_search_result(search)

    @pytest.mark.asyncio
    async def test_get_recommendations(
        self,
        async_client: AsyncClient,
        recommendations_json_mock: dict[str, Any],
        mocker: MockerFixture,
        tickers: str,
    ) -> None:
        """Test get_recommendations method."""
        _mock_response(
            mocker,
            patched_method='yafin.client.AsyncSession.get',
            response_jsons=[recommendations_json_mock],
            async_mock=True,
        )
        recommendations = await async_client.get_recommendations(tickers)
        _assert_recommendations_response_json(recommendations, tickers)

    @pytest.mark.asyncio
    async def test_get_insights(
        self,
        async_client: AsyncClient,
        mocker: MockerFixture,
        insights_json_mock: dict[str, Any],
        tickers: str,
    ) -> None:
        """Test get_insights method."""
        _mock_response(
            mocker,
            patched_method='yafin.client.AsyncSession.get',
            response_jsons=[insights_json_mock],
            async_mock=True,
        )
        insights = await async_client.get_insights(tickers)
        _assert_insights_response_json(insights, tickers)

    @pytest.mark.asyncio
    async def test_get_ratings(
        self,
        async_client: AsyncClient,
        mocker: MockerFixture,
        ratings_json_mock: dict[str, Any],
        ticker: str,
    ) -> None:
        """Test get_ratings method."""
        _mock_response(
            mocker,
            patched_method='yafin.client.AsyncSession.get',
            response_jsons=[ratings_json_mock],
            async_mock=True,
        )
        ratings = await async_client.get_ratings(ticker)
        _assert_ratings_result(ratings, ticker)

    @pytest.mark.asyncio
    async def test_get_market_summaries(
        self,
        async_client: AsyncClient,
        mocker: MockerFixture,
        market_summaries_json_mock: dict[str, Any],
    ) -> None:
        """Test get_market_summaries method."""
        _mock_response(
            mocker,
            patched_method='yafin.client.AsyncSession.get',
            response_jsons=[market_summaries_json_mock],
            async_mock=True,
        )
        market_summaries = await async_client.get_market_summaries()
        _assert_market_summary_response_json(market_summaries)

    @pytest.mark.asyncio
    async def test_get_trending(
        self,
        async_client: AsyncClient,
        mocker: MockerFixture,
        trending_json_mock: dict[str, Any],
    ) -> None:
        """Test get_trending method."""
        _mock_response(
            mocker,
            patched_method='yafin.client.AsyncSession.get',
            response_jsons=[trending_json_mock],
            async_mock=True,
        )
        trending = await async_client.get_trending()
        _assert_trending_response_json(trending)

    @pytest.mark.asyncio
    async def test_get_currencies(
        self,
        async_client: AsyncClient,
        mocker: MockerFixture,
        currencies_json_mock: dict[str, Any],
    ) -> None:
        """Test get_currencies method."""
        _mock_response(
            mocker,
            patched_method='yafin.client.AsyncSession.get',
            response_jsons=[currencies_json_mock],
            async_mock=True,
        )
        currencies = await async_client.get_currencies()
        _assert_currencies_response_json(currencies)

    @pytest.mark.asyncio
    async def test_get_calendar_events(
        self,
        async_client: AsyncClient,
        calendar_events_kwargs: dict[str, str],
        mocker: MockerFixture,
        calendar_events_json_mock: dict[str, Any],
        start_date: int | float | None,
        end_date: int | float | None,
    ) -> None:
        """Test get_calendar_events method."""
        _mock_response(
            mocker,
            patched_method='yafin.client.AsyncSession.get',
            response_jsons=[calendar_events_json_mock],
            async_mock=True,
        )
        calendar_events = await async_client.get_calendar_events(
            **calendar_events_kwargs, start_date=start_date, end_date=end_date
        )
        _assert_calendar_events_response_json(calendar_events)

    @pytest.mark.asyncio
    async def test_get_calendar_events_invalid_args(
        self, async_client: AsyncClient
    ) -> None:
        """Test get_calendar_events method with invalid arguments."""
        with pytest.raises(ValueError):
            await async_client.get_calendar_events(modules='xxx')


class TestUnitClientManager:
    """Unit tests for yafin._ClientManager module."""

    @pytest.fixture
    def client_manager(self) -> _SingletonClientManager:
        """Fresh new instance of _ClientManager for each tests."""
        return _SingletonClientManager()

    def test_client(self, client_manager: _SingletonClientManager) -> None:
        """Test client attribute."""
        assert client_manager._refcount == 0
        assert client_manager._client is None

        client_manager._get_client()
        assert client_manager._refcount == 1
        assert client_manager._client is not None

        client_manager._release_client()
        assert client_manager._refcount == 0
        assert client_manager._client is None

    def test_client_singleton(self, client_manager: _SingletonClientManager) -> None:
        """Test client attribute singleton pattern."""
        client1 = client_manager._get_client()
        client2 = client_manager._get_client()

        assert client_manager._refcount == 2
        assert client_manager._client is not None
        assert client1 is client2

        client_manager._release_client()
        assert client_manager._refcount == 1
        assert client_manager._client is not None

        client_manager._release_client()
        assert client_manager._refcount == 0
        assert client_manager._client is None


class TestUnitAsyncClientManager:
    """Unit tests for yafin._AsyncClientManager module."""

    @pytest_asyncio.fixture
    async def async_client_manager(self) -> _SingletonAsyncClientManager:
        """Fresh new instance of _ClientManager for each tests."""
        return _SingletonAsyncClientManager()

    @pytest.mark.asyncio
    async def test_client(
        self, async_client_manager: _SingletonAsyncClientManager
    ) -> None:
        """Test client attribute."""
        assert async_client_manager._refcount == 0
        assert async_client_manager._client is None

        async_client_manager._get_client()
        assert async_client_manager._refcount == 1
        assert async_client_manager._client is not None

        await async_client_manager._release_client()
        assert async_client_manager._refcount == 0
        assert async_client_manager._client is None

    @pytest.mark.asyncio
    async def test_client_singleton(
        self, async_client_manager: _SingletonAsyncClientManager
    ) -> None:
        """Test client attribute singleton pattern."""
        client1 = async_client_manager._get_client()
        client2 = async_client_manager._get_client()

        assert async_client_manager._refcount == 2
        assert async_client_manager._client is not None
        assert client1 is client2

        await async_client_manager._release_client()
        assert async_client_manager._refcount == 1
        assert async_client_manager._client is not None

        await async_client_manager._release_client()
        assert async_client_manager._refcount == 0
        assert async_client_manager._client is None
