from datetime import datetime
from typing import Any, AsyncGenerator, Type

import pytest
import pytest_asyncio
from curl_cffi.requests.exceptions import HTTPError
from pytest_mock import MockerFixture
from typeguard import TypeCheckError

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
from tests.utils import mock_200_response, mock_404_response
from yafin import AsyncClient
from yafin.const import ALL_MODULES_CSV
from yafin.utils import get_types_with_frequency


class TestUnitClient:
    """Unit tests for yafin.client module."""

    @pytest.mark.asyncio
    async def test_session(self) -> None:
        """Test session attribute."""
        client = AsyncClient()
        assert client._open_session is None

        client._get_session()
        assert client._open_session
        assert client.session

        await client.close()
        assert client._open_session is None

        async with AsyncClient() as client:
            assert client._open_session
            assert client.session

        assert client._open_session is None

    @pytest_asyncio.fixture
    async def client(self) -> AsyncGenerator[AsyncClient, None]:
        """Fixture for AsyncClient."""
        async with AsyncClient() as client:
            yield client

    @pytest.mark.asyncio
    async def test_get_async_request(
        self,
        client: AsyncClient,
        mocker: MockerFixture,
        chart_json_mock: dict[str, Any],
    ) -> None:
        """Test _get_async_request method."""
        mock_200_response(mocker, chart_json_mock)
        url = 'https://query2.finance.yahoo.com/v8/finance/chart/META'
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
        mock_404_response(
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
    async def test_get_crumb(self) -> None:
        """Test _get_crumb method."""
        client = AsyncClient()
        assert client._crumb is None

        await client._get_crumb()
        assert client._crumb

        await client.close()
        assert client._crumb is None

    @pytest.mark.parametrize(
        'kwargs',
        [
            dict(ticker='META', period_range='1y', interval='1d'),
            dict(ticker='META', period_range='1y', interval='1d', events='div,split'),
            dict(
                ticker='META', period_range='1y', interval='1d', events=' div , split '
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
    ) -> None:
        """Test get_chart method."""
        mock_200_response(mocker, chart_json_mock)
        chart = await client.get_chart(**kwargs)
        assert_response_json(chart, 'chart')
        assert_chart_result(chart['chart']['result'][0], kwargs['ticker'])

    @pytest.mark.parametrize(
        'kwargs, err_cls',
        [
            (
                dict(ticker=1, period_range='xxx', interval='1d', events='div,split'),
                TypeCheckError,
            ),
            (
                dict(
                    ticker='META', period_range='xxx', interval='1d', events='div,split'
                ),
                ValueError,
            ),
            (
                dict(ticker='META', period_range=1, interval='1d', events='div,split'),
                TypeCheckError,
            ),
            (
                dict(
                    ticker='META', period_range='1y', interval='xxx', events='div,split'
                ),
                ValueError,
            ),
            (
                dict(ticker='META', period_range='1y', interval=1, events='div,split'),
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
    ) -> None:
        """Test get_quote method."""
        mock_200_response(mocker, quote_json_mock)
        tickers = 'META'
        quotes = await client.get_quote(tickers)
        assert_response_json(quotes, 'quoteResponse')
        assert_quotes(quotes, tickers)

    @pytest.mark.asyncio
    async def test_get_quote_invalid_args(self, client: AsyncClient) -> None:
        """Test get_quote method with invalid arguments."""
        with pytest.raises(TypeCheckError):
            await client.get_quote(tickers=1)

    @pytest.mark.asyncio
    async def test_get_quote_summary(
        self,
        client: AsyncClient,
        mocker: MockerFixture,
        quote_summary_all_modules_json_mock: dict[str, Any],
    ) -> None:
        """Test get_quote_summary method."""
        mock_200_response(mocker, quote_summary_all_modules_json_mock)
        ticker = 'META'
        modules = ALL_MODULES_CSV
        quote_summary = await client.get_quote_summary(ticker, modules)
        assert_response_json(quote_summary, 'quoteSummary')
        assert_quote_summary_all_modules_result(
            quote_summary['quoteSummary']['result'][0]
        )

    @pytest.mark.parametrize(
        'kwargs, err_cls',
        [
            (dict(ticker=1, modules=ALL_MODULES_CSV), TypeCheckError),
            (dict(ticker='META', modules='xxx'), ValueError),
            (dict(ticker='META', modules='assetProfil'), ValueError),
            (dict(ticker='META', modules=1), TypeCheckError),
        ],
    )
    @pytest.mark.asyncio
    async def test_get_quote_summary_invalid_args(
        self, client: AsyncClient, kwargs: dict[str, Any], err_cls: Type[Exception]
    ) -> None:
        """Test get_quote_summary method with invalid arguments."""
        with pytest.raises(err_cls):
            await client.get_quote_summary(**kwargs)

    @pytest.mark.parametrize(
        'kwargs',
        [
            dict(
                ticker='META',
                types=get_types_with_frequency(
                    frequency='annual', typ='income_statement'
                ),
            ),
            dict(
                ticker='META',
                types=get_types_with_frequency(
                    frequency='annual', typ='income_statement'
                ),
                period1=datetime(2020, 1, 1).timestamp(),
                period2=datetime.now().timestamp(),
            ),
            dict(
                ticker='META',
                types=get_types_with_frequency(
                    frequency='annual', typ='income_statement'
                ),
                period1=1577833200.0,
                period2=1760857217.66133,
            ),
            dict(
                ticker='META',
                types=get_types_with_frequency(
                    frequency='annual', typ='income_statement'
                ),
                period1=1577833200,
                period2=1760857217,
            ),
            dict(
                ticker='META',
                types=get_types_with_frequency(
                    frequency='annual', typ='income_statement'
                ),
                period1=datetime(2020, 1, 1).timestamp(),
            ),
            dict(
                ticker='META',
                types=get_types_with_frequency(
                    frequency='annual', typ='income_statement'
                ),
                period1=1577833200.0,
            ),
            dict(
                ticker='META',
                types=get_types_with_frequency(
                    frequency='annual', typ='income_statement'
                ),
                period1=1577833200,
            ),
            dict(
                ticker='META',
                types=get_types_with_frequency(
                    frequency='annual', typ='income_statement'
                ),
                period2=datetime.now().timestamp(),
            ),
            dict(
                ticker='META',
                types=get_types_with_frequency(
                    frequency='annual', typ='income_statement'
                ),
                period2=1760857217.66133,
            ),
            dict(
                ticker='META',
                types=get_types_with_frequency(
                    frequency='annual', typ='income_statement'
                ),
                period2=1760857217,
            ),
        ],
    )
    @pytest.mark.asyncio
    async def test_get_timeseries(
        self,
        client: AsyncClient,
        kwargs: dict[str, Any],
        mocker: MockerFixture,
        timeseries_income_statement_json_mock: dict[str, Any],
    ) -> None:
        """Test get_timeseries method."""
        mock_200_response(mocker, timeseries_income_statement_json_mock)
        timeseries = await client.get_timeseries(**kwargs)
        assert_response_json(timeseries, 'timeseries')
        assert_annual_income_stmt_result(timeseries['timeseries']['result'])

    @pytest.mark.parametrize(
        'kwargs, err_cls',
        [
            (
                dict(
                    ticker=1,
                    types=get_types_with_frequency(
                        frequency='annual', typ='income_statement'
                    ),
                ),
                TypeCheckError,
            ),
            (dict(ticker='META', types='xxx'), ValueError),
            (dict(ticker='META', types=1), TypeCheckError),
            (
                dict(
                    ticker='META',
                    types=get_types_with_frequency(
                        frequency='annual', typ='income_statement'
                    ),
                    period1='xxx',
                ),
                TypeCheckError,
            ),
            (
                dict(
                    ticker='META',
                    types=get_types_with_frequency(
                        frequency='annual', typ='income_statement'
                    ),
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
    ) -> None:
        """Test get_options method."""
        mock_200_response(mocker, options_json_mock)
        ticker = 'META'
        options = await client.get_options(ticker)
        assert_response_json(options, 'optionChain')
        assert_options_result(options['optionChain']['result'][0], ticker)

    @pytest.mark.asyncio
    async def test_get_options_invalid_args(self, client: AsyncClient) -> None:
        """Test get_options method with invalid arguments."""
        with pytest.raises(TypeCheckError):
            await client.get_options(ticker=1)

    @pytest.mark.asyncio
    async def test_get_search(
        self,
        client: AsyncClient,
        mocker: MockerFixture,
        search_json_mock: dict[str, Any],
    ) -> None:
        """Test get_search method."""
        mock_200_response(mocker, search_json_mock)
        search = await client.get_search(tickers='META')
        assert_search(search)

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
    ) -> None:
        """Test get_recommendations method."""
        mock_200_response(mocker, recommendations_json_mock)
        ticker = 'META'
        recommendations = await client.get_recommendations(ticker)
        assert_response_json(recommendations, 'finance')
        assert_recommendations_result(recommendations['finance']['result'][0], ticker)

    @pytest.mark.asyncio
    async def test_get_recommendations_invalid_args(self, client: AsyncClient) -> None:
        """Test get_recommendations method with invalid arguments."""
        with pytest.raises(TypeCheckError):
            await client.get_recommendations(ticker=1)

    @pytest.mark.asyncio
    async def test_get_insights(
        self,
        client: AsyncClient,
        mocker: MockerFixture,
        insights_json_mock: dict[str, Any],
    ) -> None:
        """Test get_insights method."""
        mock_200_response(mocker, insights_json_mock)
        ticker = 'META'
        insights = await client.get_insights(ticker)
        assert_response_json(insights, 'finance')
        assert_insights_result(insights['finance']['result'], ticker)

    @pytest.mark.asyncio
    async def test_get_insights_invalid_args(self, client: AsyncClient) -> None:
        """Test get_insights method with invalid arguments."""
        with pytest.raises(TypeCheckError):
            await client.get_insights(ticker=1)

    @pytest.mark.asyncio
    async def test_get_market_summaries(
        self,
        client: AsyncClient,
        mocker: MockerFixture,
        market_summaries_json_mock: dict[str, Any],
    ) -> None:
        """Test get_market_summaries method."""
        mock_200_response(mocker, market_summaries_json_mock)
        market_summaries = await client.get_market_summaries()
        assert_response_json(market_summaries, 'marketSummaryResponse')
        assert_market_summaries_result(
            market_summaries['marketSummaryResponse']['result']
        )

    @pytest.mark.asyncio
    async def test_get_trending(
        self,
        client: AsyncClient,
        mocker: MockerFixture,
        trending_json_mock: dict[str, Any],
    ) -> None:
        """Test get_trending method."""
        mock_200_response(mocker, trending_json_mock)
        trending = await client.get_trending()
        assert_response_json(trending, 'finance')
        assert_trending_result(trending['finance']['result'][0])

    @pytest.mark.asyncio
    async def test_get_currencies(
        self,
        client: AsyncClient,
        mocker: MockerFixture,
        currencies_json_mock: dict[str, Any],
    ) -> None:
        """Test get_currencies method."""
        mock_200_response(mocker, currencies_json_mock)
        currencies = await client.get_currencies()
        assert_response_json(currencies, 'currencies')
        assert_currencies_result(currencies['currencies']['result'])
