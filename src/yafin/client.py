import logging
from datetime import datetime
from types import TracebackType
from typing import Any, Self, Type

from curl_cffi.requests import AsyncSession, Response
from curl_cffi.requests.exceptions import HTTPError
from typeguard import typechecked

from .const import ALL_MODULES, ALL_TYPES, EVENTS, INTERVALS, RANGES
from .utils import encode_url, error, log_args

logger = logging.getLogger(__name__)

type ResponseJson = dict[str, Any]


class AsyncClient(object):
    """Client for Yahoo Finance API.

    Warning: HTTP resources closing
        Uses http resources, so do not forget to close them after use to avoid resource
            leakage or use context manager.

    Attributes:
        timeout: timeout (in secs) for each http request.
        _open_session:
            session instance, that is used for all http requests.
                (Is lazily initialized.)
    """

    _BASE_URL = r'https://query2.finance.yahoo.com'
    _DEFAULT_PARAMS = {
        'formatted': 'false',
        'region': 'US',
        'lang': 'en-US',
        'corsDomain': 'finance.yahoo.com',
    }

    @typechecked
    def __init__(self, timeout: int = 5) -> None:
        """Create new AsynClient instance.

        Args:
            timeout: timeout (in secs) for each http request.
        """
        self.timeout = timeout
        self._open_session: AsyncSession[Any] | None = None
        self._crumb: str | None = None

    @property
    def session(self) -> AsyncSession[Any]:
        """Session attribute for http requests."""
        return self._get_session()

    def _get_session(self) -> AsyncSession[Any]:
        if self._open_session is None:
            self._open_session = AsyncSession(
                impersonate='chrome', timeout=self.timeout
            )

        return self._open_session

    @log_args
    async def close(self) -> None:
        """Close the session if open and reset crumb."""
        if self._open_session:
            await self._open_session.close()
            self._open_session = None

        self._crumb = None

    async def __aenter__(self) -> Self:
        """When entering context manager, create the session."""
        self._get_session()
        return self

    async def __aexit__(
        self,
        exc_type: Type[BaseException] | None = None,
        exc_val: BaseException | None = None,
        exc_tb: TracebackType | None = None,
    ) -> None:
        """When closing context manager, close the session."""
        await self.close()

    @log_args
    @typechecked
    async def _get_async_request(
        self, url: str, params: dict[str, Any] | None = None
    ) -> Response:
        logger.debug(encode_url(url, params))

        try:
            response = await self.session.get(url, params=params)
            response.raise_for_status()

        except HTTPError as e:
            logger.error(f'HTTP error: {e}')
            raise e

        return response

    @log_args
    async def _get_crumb(self) -> str | None:
        if not self._crumb:
            url = f'{self._BASE_URL}/v1/test/getcrumb'
            response = await self._get_async_request(url=url)
            self._crumb = response.text

        return self._crumb

    @log_args
    @typechecked
    async def get_chart(
        self,
        ticker: str,
        period_range: str,
        interval: str,
        events: str | None = 'div,split',
    ) -> ResponseJson:
        """Get chart data for the ticker.

        Args:
            ticker: Ticker symbol.
            period_range: Range of the period.
            interval: Data interval.
            events: Events to include.

        Returns: Chart response json including result and error.

        Raises:
            ValueError: If any of period_range, interval or parsed_events are not in
                list of valid values.
        """
        logger.debug(
            f'Getting finance/chart for ticker {ticker}, {period_range=}, {interval=}, {events=}.'  # noqa E501
        )

        if period_range not in RANGES:
            error(
                msg=f'Invalid {period_range=}. Valid values: {RANGES}',
                err_cls=ValueError,
            )

        if interval not in INTERVALS:
            error(
                msg=f'Invalid {interval=}. Valid values: {INTERVALS}',
                err_cls=ValueError,
            )

        if events:
            parsed_events = {e.strip() for e in events.split(',')}

            if not parsed_events <= EVENTS:
                error(
                    msg=(
                        f'Invalid events={parsed_events - EVENTS}. '
                        f'Valid values: {EVENTS}'
                    ),
                    err_cls=ValueError,
                )

        url = f'{self._BASE_URL}/v8/finance/chart/{ticker}'
        params = self._DEFAULT_PARAMS | {'range': period_range, 'interval': interval}

        if events:
            params['events'] = ','.join(parsed_events)

        response = await self._get_async_request(url, params)
        return response.json()

    @log_args
    @typechecked
    async def get_quote(self, tickers: str) -> ResponseJson:
        """Get quote for the ticker(s).

        Args:
            tickers: Comma-separated ticker symbols.

        Returns: Quote response json including result and error.
        """
        logger.debug(f'Getting finance/quote for ticker {tickers}.')

        url = f'{self._BASE_URL}/v7/finance/quote'
        params = self._DEFAULT_PARAMS | {
            'symbols': tickers,
            'crumb': await self._get_crumb(),
        }
        response = await self._get_async_request(url, params)
        return response.json()

    @log_args
    @typechecked
    async def get_quote_summary(self, ticker: str, modules: str) -> ResponseJson:
        """Get quote summary for the ticker.

        Args:
            ticker: Ticker symbol.
            modules: Comma-separated modules to include.

        Returns: Quote summary response json including result and error.
        """
        logger.debug(f'Getting finance/quoteSummary for ticker {ticker}.')

        parsed_modules = {m.strip() for m in modules.split(',')}

        if not parsed_modules <= ALL_MODULES:
            error(
                msg=(
                    f'Invalid modules={parsed_modules - ALL_MODULES}. '
                    f'Valid values: {ALL_MODULES}'
                ),
                err_cls=ValueError,
            )

        url = f'{self._BASE_URL}/v10/finance/quoteSummary/{ticker}'
        params = self._DEFAULT_PARAMS | {
            'modules': ','.join(parsed_modules),
            'crumb': await self._get_crumb(),
        }
        response = await self._get_async_request(url, params)
        return response.json()

    @log_args
    @typechecked
    async def get_timeseries(
        self,
        ticker: str,
        types: str,
        period1: int | float | None = None,
        period2: int | float | None = None,
    ) -> ResponseJson:
        """Get timeseries for the ticker.

        Args:
            ticker: Ticker symbol.
            types: Timeseries types (incl. frequency) to include.
            period1: Start timestamp (optional).
            period2: End timestamp (optional).

        Returns: Timeseries response json including result and error.

        Raises:
            ValueError: If types are not in list of valid values.
        """
        logger.debug(
            f'Getting finance/timeseries for ticker {ticker}, {types=}, {period1=}, {period2=}.'  # noqa E501
        )

        parsed_types = {t.strip() for t in types.split(',')}

        if not parsed_types <= ALL_TYPES:
            error(
                msg=(
                    f'Invalid types={parsed_types - ALL_TYPES}. '
                    f'Valid values: {ALL_TYPES}'
                ),
                err_cls=ValueError,
            )

        if not period1:
            period1 = datetime(2020, 1, 1).timestamp()

        if not period2:
            period2 = datetime.now().timestamp()

        url = f'{self._BASE_URL}/ws/fundamentals-timeseries/v1/finance/timeseries/{ticker}'  # noqa E501
        params = self._DEFAULT_PARAMS | {
            'type': ','.join(parsed_types),
            'period1': int(period1),
            'period2': int(period2),
        }

        response = await self._get_async_request(url, params)
        return response.json()

    @log_args
    @typechecked
    async def get_options(self, ticker: str) -> ResponseJson:
        """Get options for the ticker.

        Args:
            ticker: Ticker symbol.

        Returns: Options response json including result and error.
        """
        logger.debug(f'Getting finance/options for ticker {ticker}.')

        url = f'{self._BASE_URL}/v7/finance/options/{ticker}'
        params = self._DEFAULT_PARAMS | {'crumb': await self._get_crumb()}
        response = await self._get_async_request(url, params)
        return response.json()

    @log_args
    @typechecked
    async def get_search(self, tickers: str) -> ResponseJson:
        """Get search results for the ticker.

        Args:
            tickers: Comma-separated ticker symbols.

        Returns: Search response json including result and error.
        """
        logger.debug(f'Getting finance/search for ticker {tickers}.')

        url = f'{self._BASE_URL}/v1/finance/search'
        params = self._DEFAULT_PARAMS | {'q': tickers}
        response = await self._get_async_request(url, params)
        return response.json()

    @log_args
    @typechecked
    async def get_recommendations(self, ticker: str) -> ResponseJson:
        """Get analyst recommendations for the ticker.

        Args:
            ticker: Ticker symbol.

        Returns: Recommendations response json including result and error.
        """
        logger.debug(f'Getting finance/recommendations for ticker {ticker}.')

        url = f'{self._BASE_URL}/v6/finance/recommendationsbysymbol/{ticker}'
        params = self._DEFAULT_PARAMS
        response = await self._get_async_request(url, params)
        return response.json()

    @log_args
    @typechecked
    async def get_insights(self, ticker: str) -> ResponseJson:
        """Get insights for the ticker.

        Args:
            ticker: Ticker symbol.

        Returns: Insights response json including result and error.
        """
        logger.debug(f'Getting finance/insights for ticker {ticker}.')

        url = f'{self._BASE_URL}/ws/insights/v2/finance/insights'
        params = self._DEFAULT_PARAMS | {'symbol': ticker}
        response = await self._get_async_request(url, params)
        return response.json()

    @log_args
    async def get_market_summaries(self) -> ResponseJson:
        """Get market summaries.

        Returns: Market summaries response json including result and error.
        """
        logger.debug('Getting finance/quote/marketSummary.')

        url = f'{self._BASE_URL}/v6/finance/quote/marketSummary'
        params = self._DEFAULT_PARAMS
        response = await self._get_async_request(url, params)
        return response.json()

    @log_args
    async def get_trending(self) -> ResponseJson:
        """Get trending tickers.

        Returns: Trending tickers response json including result and error.
        """
        logger.debug('Getting finance/trending.')

        url = f'{self._BASE_URL}/v1/finance/trending/US'
        params = self._DEFAULT_PARAMS
        response = await self._get_async_request(url, params)
        return response.json()

    @log_args
    async def get_currencies(self) -> ResponseJson:
        """Get currency exchange rates.

        Returns: Currency exchange rates response json including result and error.
        """
        logger.debug('Getting finance/currencies.')

        url = f'{self._BASE_URL}/v1/finance/currencies'
        params = self._DEFAULT_PARAMS
        response = await self._get_async_request(url, params)
        return response.json()
