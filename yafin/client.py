import asyncio
import logging
from datetime import datetime, timedelta
from types import TracebackType
from typing import Any, Self, Type
from zoneinfo import ZoneInfo

from curl_cffi import AsyncSession, Response
from curl_cffi.requests.exceptions import HTTPError, Timeout

from .const import (
    _ALL_TYPES_SET,
    CALENDAR_EVENT_MODULES_SET,
    EVENTS,
    INTERVALS,
    QUOTE_SUMMARY_MODULES_SET,
    RANGES,
)
from .types import (
    AnalysisResponseJson,
    CalendarEventsResponseJson,
    ChartResponseJson,
    CurrenciesResponseJson,
    InsightsResponseJson,
    MarketSummaryResponseJson,
    OptionsResponseJson,
    QuoteResponseJson,
    QuoteSummaryResponseJson,
    QuoteTypeResponseJson,
    RatingsResponseJson,
    RecommendationsResponseJson,
    SearchResponseJson,
    TimeseriesResponseJson,
    TrendingResponseJson,
)
from .utils import _encode_url, _error, _log_args

logger = logging.getLogger(__name__)


class AsyncClient(object):
    """Client for Yahoo Finance API.

    Warning: HTTP resources closing
        Uses http resources, so do not forget to close them after use to avoid resource
            leakage or use context manager.

    Attributes:
        timeout: timeout (in secs) for each http request.
        max_retries: number of retries in case of failed request.
        _session:
            session instance, that is used for all http requests.
                (Is lazily initialized.)
    """

    _BASE_URL = r'https://query2.finance.yahoo.com'
    _DEFAULT_PARAMS = {
        'region': 'US',
        'lang': 'en-US',
        'formatted': False,
        'corsDomain': 'finance.yahoo.com',
    }

    def __init__(self, timeout: float = 5.0, max_retries: int = 5) -> None:
        """Create new AsynClient instance.

        Args:
            timeout: timeout (in secs) for each http request.
            max_retries: number of retries in case of failed request.
        """
        self.timeout = timeout
        self.max_retries = max_retries
        self._session: AsyncSession[Any] | None = None
        self._crumb: str | None = None

    def _get_session(self) -> None:
        if self._session is None:
            self._session = AsyncSession(impersonate='chrome', timeout=self.timeout)

    @_log_args
    async def close(self) -> None:
        """Close the session if open and reset crumb."""
        if self._session:
            await self._session.close()
            self._session = None

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

    @_log_args
    async def _get_async_request(
        self,
        url: str,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> Response:
        logger.debug(_encode_url(url, params))

        kwargs: dict[str, Any] = {'url': url}

        if params is not None:
            kwargs['params'] = params

        if headers is not None:
            kwargs['headers'] = headers

        for attempt in range(1, self.max_retries + 1):
            try:
                logger.debug(f'Request no. {attempt}/{self.max_retries} - started.')
                self._get_session()
                response = await self._session.request(method='GET', **kwargs)
                response.raise_for_status()
                logger.debug(f'Request no. {attempt}/{self.max_retries} - succeeded.')
                return response

            except (HTTPError, Timeout) as e:
                logger.warning(f'Request no. {attempt}/{self.max_retries} - failed.')

                if (
                    response.status_code >= 400
                    and response.status_code <= 499
                    and response.status_code != 429
                ):
                    raise e

                wait_time = min(2**attempt, 60)  # Exponential backoff with cap
                await asyncio.sleep(wait_time)

        # # gives RET503 ruff err
        # # _error(msg=f'All {self.max_retries} requests failed.', err_cls=HTTPError)
        msg = f'All {self.max_retries} requests failed.'
        logger.error(msg)
        raise HTTPError(msg)

    @_log_args
    async def _get_crumb(self) -> str | None:
        if not self._crumb:
            url = f'{self._BASE_URL}/v1/test/getcrumb'
            response = await self._get_async_request(url)
            self._crumb = response.text

        return self._crumb

    @_log_args
    async def get_chart(
        self,
        ticker: str,
        period_range: str,
        interval: str,
        events: str | None = 'div,split,earn,capitalGain',
    ) -> ChartResponseJson:
        """Get chart data for the ticker.

        Args:
            ticker: Ticker symbol.
            period_range: Range of the period.
            interval: Data interval.
            events: Comma-separated events to include.

        Returns: Chart response json including result and error.

        Raises:
            ValueError: If any of period_range, interval or parsed_events are not in
                list of valid values.
        """
        logger.debug(
            f'Getting finance/chart for {ticker=}, '
            f'{period_range=}, {interval=}, {events=}.'
        )

        if period_range not in RANGES:
            _error(
                msg=f'Invalid {period_range=}. Valid values: {RANGES}',
                err_cls=ValueError,
            )

        if interval not in INTERVALS:
            _error(
                msg=f'Invalid {interval=}. Valid values: {INTERVALS}',
                err_cls=ValueError,
            )

        if events:
            parsed_events = {e.strip() for e in events.split(',')}

            if not parsed_events <= EVENTS:
                _error(
                    msg=(
                        f'Invalid events={parsed_events - EVENTS}. '
                        f'Valid values: {EVENTS}'
                    ),
                    err_cls=ValueError,
                )

        url = f'{self._BASE_URL}/v8/finance/chart/{ticker}'
        params = self._DEFAULT_PARAMS | {
            'range': period_range,
            'interval': interval,
            'includePrePost': True,
            'source': 'cosaic',
            'includeAdjustedClose': True,
            'userYfid': True,
        }

        if events:
            params['events'] = ','.join(parsed_events)

        response = await self._get_async_request(url, params)
        return response.json()

    @_log_args
    async def get_quote(self, tickers: str) -> QuoteResponseJson:
        """Get quote for tickers.

        Args:
            tickers: Comma-separated ticker symbols.

        Returns: Quote response json including result and error.
        """
        logger.debug(f'Getting finance/quote for {tickers=}.')

        url = f'{self._BASE_URL}/v7/finance/quote'
        params = self._DEFAULT_PARAMS | {
            'symbols': tickers,
            'includePrePost': True,
            'crumb': await self._get_crumb(),
        }
        response = await self._get_async_request(url, params)
        return response.json()

    @_log_args
    async def get_quote_type(self, tickers: str) -> QuoteTypeResponseJson:
        """Get quote type for tickers.

        Args:
            tickers: Comma-separated ticker symbols.

        Returns: Quote type response json including result and error.
        """
        logger.debug(f'Getting finance/quoteType for {tickers=}.')

        url = f'{self._BASE_URL}/v1/finance/quoteType/'
        params = self._DEFAULT_PARAMS | {
            'symbol': tickers,
            'enablePrivateCompany': True,
        }
        response = await self._get_async_request(url, params)
        return response.json()

    @_log_args
    async def get_quote_summary(
        self, ticker: str, modules: str
    ) -> QuoteSummaryResponseJson:
        """Get quote summary for the ticker.

        Args:
            ticker: Ticker symbol.
            modules: Comma-separated modules to include.

        Returns: Quote summary response json including result and error.
        """
        logger.debug(f'Getting finance/quoteSummary for {ticker=}.')

        parsed_modules = {m.strip() for m in modules.split(',')}

        if not parsed_modules <= QUOTE_SUMMARY_MODULES_SET:
            _error(
                msg=(
                    f'Invalid modules={parsed_modules - QUOTE_SUMMARY_MODULES_SET}. '
                    f'Valid values: {QUOTE_SUMMARY_MODULES_SET}'
                ),
                err_cls=ValueError,
            )

        url = f'{self._BASE_URL}/v10/finance/quoteSummary/{ticker}'
        params = self._DEFAULT_PARAMS | {
            'modules': ','.join(parsed_modules),
            'enablePrivateCompany': True,
            'enableQSPExpandedEarnings': True,
            'overnightPrice': True,
            'crumb': await self._get_crumb(),
        }
        response = await self._get_async_request(url, params)
        return response.json()

    @_log_args
    async def get_timeseries(
        self,
        ticker: str,
        types: str,
        period1: int | float | None = None,
        period2: int | float | None = None,
    ) -> TimeseriesResponseJson:
        """Get timeseries for the ticker.

        Args:
            ticker: Ticker symbol.
            types: Comma-separated types (incl. frequency) to include.
            period1: Start timestamp in seconds.
            period2: End timestamp in seconds.

        Returns: Timeseries response json including result and error.

        Raises:
            ValueError: If types are not in list of valid values.
        """
        logger.debug(
            f'Getting finance/timeseries for {ticker=}, '
            f'{types=}, {period1=}, {period2=}.'
        )

        parsed_types = {t.strip() for t in types.split(',')}

        if not parsed_types <= _ALL_TYPES_SET:
            _error(
                msg=(
                    f'Invalid types={parsed_types - _ALL_TYPES_SET}. '
                    f'Valid values: {_ALL_TYPES_SET}'
                ),
                err_cls=ValueError,
            )

        if period1 is None:
            period1 = datetime(2020, 1, 1, tzinfo=ZoneInfo('UTC')).timestamp()

        if period2 is None:
            period2 = datetime.now(tz=ZoneInfo('UTC')).timestamp()

        url = (
            f'{self._BASE_URL}/ws/fundamentals-timeseries/'
            f'v1/finance/timeseries/{ticker}'
        )
        params = self._DEFAULT_PARAMS | {
            'merge': False,
            'padTimeSeries': True,
            'period1': int(period1),
            'period2': int(period2),
            'type': ','.join(parsed_types),
        }

        response = await self._get_async_request(url, params)
        return response.json()

    @_log_args
    async def get_options(self, ticker: str) -> OptionsResponseJson:
        """Get options for the ticker.

        Args:
            ticker: Ticker symbol.

        Returns: Options response json including result and error.
        """
        logger.debug(f'Getting finance/options for {ticker=}.')

        url = f'{self._BASE_URL}/v7/finance/options/{ticker}'
        params = self._DEFAULT_PARAMS | {
            'date': -1,
            'straddle': False,
            'crumb': await self._get_crumb(),
        }
        response = await self._get_async_request(url, params)
        return response.json()

    @_log_args
    async def get_search(self, tickers: str) -> SearchResponseJson:
        """Get search results for tickers.

        Args:
            tickers: Comma-separated ticker symbols.

        Returns: Search response json.
        """
        logger.debug(f'Getting finance/search for {tickers=}.')

        url = f'{self._BASE_URL}/v1/finance/search'
        params = self._DEFAULT_PARAMS | {'q': tickers}
        response = await self._get_async_request(url, params)
        return response.json()

    @_log_args
    async def get_recommendations(self, tickers: str) -> RecommendationsResponseJson:
        """Get analyst recommendations for tickers.

        Args:
            tickers: Comma-separated ticker symbols.

        Returns: Recommendations response json including result and error.
        """
        logger.debug(f'Getting finance/recommendations for {tickers=}.')

        url = f'{self._BASE_URL}/v6/finance/recommendationsbysymbol/{tickers}'
        params = self._DEFAULT_PARAMS
        response = await self._get_async_request(url, params)
        return response.json()

    @_log_args
    async def get_insights(self, tickers: str) -> InsightsResponseJson:
        """Get insights for tickers.

        Args:
            tickers: Comma-separated ticker symbols.

        Returns: Insights response json including result and error.
        """
        logger.debug(f'Getting finance/insights for {tickers=}.')

        url = f'{self._BASE_URL}/ws/insights/v3/finance/insights'
        params = self._DEFAULT_PARAMS | {
            'symbols': tickers,
            'disableRelatedReports': True,
            'getAllResearchReports': True,
            'reportsCount': 4,
            'ssl': True,
        }
        response = await self._get_async_request(url, params)
        return response.json()

    @_log_args
    async def get_ratings(self, ticker: str) -> RatingsResponseJson:
        """Get ratings for the ticker.

        Args:
            ticker: Ticker symbol.

        Returns: Ratings response json.
        """
        logger.debug(f'Getting ratings for {ticker=}.')

        url = f'{self._BASE_URL}/v2/ratings/top/{ticker}'
        params = self._DEFAULT_PARAMS | {'exclude_noncurrent': True}
        response = await self._get_async_request(url, params)
        return response.json()

    @_log_args
    async def get_analysis(self, ticker: str) -> AnalysisResponseJson:
        """Get analysis for the ticker.

        Args:
            ticker: Ticker symbol.

        Returns: Analysis response json.
        """
        logger.debug(f'Getting analysis for {ticker=}.')

        url = 'https://finance.yahoo.com/xhr/ticker-analysis'
        params = self._DEFAULT_PARAMS | {'debug': False, 'symbol': ticker}
        headers = {'Accept': 'application/json'}
        response = await self._get_async_request(url, params, headers)
        return response.json()

    @_log_args
    async def get_market_summaries(self) -> MarketSummaryResponseJson:
        """Get market summaries.

        Returns: Market summaries response json including result and error.
        """
        logger.debug('Getting finance/quote/marketSummary.')

        url = f'{self._BASE_URL}/v6/finance/quote/marketSummary'
        params = self._DEFAULT_PARAMS
        response = await self._get_async_request(url, params)
        return response.json()

    @_log_args
    async def get_trending(self) -> TrendingResponseJson:
        """Get trending tickers.

        Returns: Trending tickers response json including result and error.
        """
        logger.debug('Getting finance/trending.')

        url = f'{self._BASE_URL}/v1/finance/trending/US'
        params = self._DEFAULT_PARAMS
        response = await self._get_async_request(url, params)
        return response.json()

    @_log_args
    async def get_currencies(self) -> CurrenciesResponseJson:
        """Get currency exchange rates.

        Returns: Currency exchange rates response json including result and error.
        """
        logger.debug('Getting finance/currencies.')

        url = f'{self._BASE_URL}/v1/finance/currencies'
        params = self._DEFAULT_PARAMS
        response = await self._get_async_request(url, params)
        return response.json()

    @_log_args
    async def get_calendar_events(
        self,
        modules: str | None = None,
        period1: int | float | None = None,
        period2: int | float | None = None,
    ) -> CalendarEventsResponseJson:
        """Get calendar events.

        Args:
            modules: Comma-separated modules to include.
            period1: Start timestamp in miliseconds.
            period2: End timestamp in miliseconds.

        Returns: Calendar events response json including result and error.

        Note: Query range cannot be greater than 150 days.
        """
        logger.debug('Getting finance/calendar-events.')

        if period2 is None:
            period2 = datetime.now(tz=ZoneInfo('UTC')).timestamp() * 1000

        if period1 is None:
            dt = datetime.fromtimestamp(period2 / 1000) - timedelta(days=149)
            period1 = dt.timestamp() * 1000

        url = f'{self._BASE_URL}/ws/screeners/v1/finance/calendar-events'
        params = self._DEFAULT_PARAMS | {
            'countPerDay': 25,
            'economicEventsHighImportanceOnly': True,
            'economicEventsRegionFilter': '',
            'startDate': int(period1),
            'endDate': int(period2),
        }

        if modules:
            parsed_modules = {m.strip() for m in modules.split(',')}

            if not parsed_modules <= CALENDAR_EVENT_MODULES_SET:
                _error(
                    msg=(
                        f'Invalid modules={parsed_modules - CALENDAR_EVENT_MODULES_SET}'
                        f'. Valid values: {CALENDAR_EVENT_MODULES_SET}'
                    ),
                    err_cls=ValueError,
                )

            params['modules'] = ','.join(parsed_modules)

        response = await self._get_async_request(url, params)
        return response.json()
