import asyncio
import logging
from datetime import datetime, timedelta
from functools import lru_cache
from time import sleep
from types import TracebackType
from typing import Any, Self

from async_lru import alru_cache
from curl_cffi import AsyncSession, Response, Session
from curl_cffi.requests.exceptions import HTTPError, Timeout

from .const import EVENTS
from .types import (
    CalendarEventsResponseJson,
    ChartResponseJson,
    CurrenciesResponseJson,
    InsightsResponseJson,
    MarketSummaryResponseJson,
    OptionsResponseJson,
    QuoteResponseJson,
    QuoteSummaryResponseJson,
    QuoteTypeResponseJson,
    RatingsResult,
    RecommendationsResponseJson,
    SearchResult,
    TimeseriesResponseJson,
    TrendingResponseJson,
)
from .utils import (
    _async_log_func,
    _check_calendar_event_modules,
    _check_events,
    _check_interval,
    _check_period_range,
    _check_quote_summary_modules,
    _check_types,
    _encode_url,
    _log_func,
)

logger = logging.getLogger(__name__)


class ClientBase:
    """Base for synchronous and asynchronous Client classes for Yahoo Finance API.

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
    _CRUMB_URL = f'{_BASE_URL}/v1/test/getcrumb'
    _CHART_URL = f'{_BASE_URL}/v8/finance/chart/{{ticker}}'
    _QUOTE_URL = f'{_BASE_URL}/v7/finance/quote'
    _QUOTE_TYPE_URL = f'{_BASE_URL}/v1/finance/quoteType/'
    _QUOTE_SUMMARY_URL = f'{_BASE_URL}/v10/finance/quoteSummary/{{ticker}}'
    _TIMESERIES_URL = (
        f'{_BASE_URL}/ws/fundamentals-timeseries/v1/finance/timeseries/{{ticker}}'
    )
    _OPTIONS_URL = f'{_BASE_URL}/v7/finance/options/{{ticker}}'
    _SEARCH_URL = f'{_BASE_URL}/v1/finance/search'
    _RECOMMENDATIONS_URL = f'{_BASE_URL}/v6/finance/recommendationsbysymbol/{{tickers}}'
    _INSIGHTS_URL = f'{_BASE_URL}/ws/insights/v3/finance/insights'
    _RATINGS_URL = f'{_BASE_URL}/v2/ratings/top/{{ticker}}'
    _MARKET_SUMMARIES_URL = f'{_BASE_URL}/v6/finance/quote/marketSummary'
    _TRENDING_URL = f'{_BASE_URL}/v1/finance/trending/US'
    _CURRENCIES_URL = f'{_BASE_URL}/v1/finance/currencies'
    _CALENDAR_EVENTS_URL = f'{_BASE_URL}/ws/screeners/v1/finance/calendar-events'
    _DEFAULT_PARAMS = {
        'region': 'US',
        'lang': 'en-US',
        'formatted': False,
        'corsDomain': 'finance.yahoo.com',
    }
    _CHART_PARAMS = {
        'source': 'cosaic',
        'includeAdjustedClose': True,
        'userYfid': True,
    }
    _QUOTE_TYPE_PARAMS = {
        'enablePrivateCompany': True,
    }
    _QUOTE_SUMMARY_PARAMS = {
        'enablePrivateCompany': True,
        'enableQSPExpandedEarnings': True,
        'overnightPrice': True,
    }
    _TIMESERIES_PARAMS = {
        'merge': False,
        'padTimeSeries': True,
    }
    _OPTIONS_PARAMS = {
        'date': -1,
        'straddle': False,
    }
    _INSIGHTS_PARAMS = {
        'disableRelatedReports': True,
        'getAllResearchReports': True,
        'reportsCount': 4,
        'ssl': True,
    }
    _RATINGS_PARAMS = {'exclude_noncurrent': True}
    _CALENDAR_EVENTS_PARAMS = {
        'countPerDay': 25,
        'economicEventsHighImportanceOnly': True,
        'economicEventsRegionFilter': '',
    }

    def __init__(self, timeout: float = 5.0, max_retries: int = 5) -> None:
        self.timeout = timeout
        self.max_retries = max_retries
        self._crumb: str | None = None


class Client(ClientBase):
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

    Methods:
        get_chart: Get chart data for the ticker.
        get_quote: Get quote for tickers.
        get_quote_type: Get quote type for tickers.
        get_quote_summary: Get quote summary for the ticker.
        get_timeseries: Get timeseries for the ticker.
        get_options: Get options for the ticker.
        get_search: Get search results for tickers.
        get_recommendations: Get analyst recommendations for tickers.
        get_insights: Get insights for tickers.
        get_ratings: Get ratings for the ticker.
        get_market_summaries: Get market summaries.
        get_trending: Get trending tickers.
        get_currencies: Get currency exchange rates.
        get_calendar_event: Get calendar events.
    """

    def __init__(self, timeout: float = 5.0, max_retries: int = 5) -> None:
        """Create new Client instance.

        Args:
            timeout: timeout (in secs) for each http request.
            max_retries: number of retries in case of failed request.
        """
        super().__init__(timeout, max_retries)
        self._session: Session[Any] | None = None

    def _get_session(self) -> None:
        if self._session is None:
            self._session = Session(impersonate='chrome', timeout=self.timeout)

    @_log_func
    def close(self) -> None:
        """Close the session if open and reset crumb."""
        if self._session is not None:
            self._session.close()
            self._session = None

        if self._crumb is not None:
            self._crumb = None

    def __enter__(self) -> Self:
        """When entering context manager, create the session."""
        self._get_session()
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None = None,
        exc_val: BaseException | None = None,
        exc_tb: TracebackType | None = None,
    ) -> None:
        """When closing context manager, close the session."""
        self.close()

    @_log_func
    def _get_request(
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
                response = self._session.get(**kwargs)
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
                sleep(wait_time)

        # # gives RET503 ruff err
        # # _error(msg=f'All {self.max_retries} requests failed.', err_cls=HTTPError)
        msg = f'All {self.max_retries} requests failed.'
        logger.error(msg)
        raise HTTPError(msg)

    @_log_func
    @lru_cache(maxsize=128)
    def _get_crumb(self) -> None:
        if self._crumb is None:
            response = self._get_request(self._CRUMB_URL)
            self._crumb = response.text

    @lru_cache(maxsize=128)
    @_log_func
    def get_chart(
        self,
        ticker: str,
        interval: str,
        period_range: str | None = None,
        period1: int | float | None = None,
        period2: int | float | None = None,
        include_pre_post: bool | None = None,
        events: str | None = EVENTS,
    ) -> ChartResponseJson:
        """Get chart data for the ticker.

        Args:
            ticker: Ticker symbol.
            interval: Data interval.
            period_range: Range of the period.
            period1: Start timestamp in seconds. (optional, default: None)
            period2: End timestamp in seconds. (optional, default: None)
            include_pre_post: Whether to include pre and post market.
            events: Comma-separated events to include.

        Returns: Chart response json including result and error.

        Raises:
            ValueError: If any of period_range, interval or parsed_events are not in
                list of valid values.

        Note:
            Even though the the endpoint param is called range, period_range was chosen
            to avoid collision with python built-in method name.
        """
        logger.debug(
            f'Getting finance/chart for {ticker=}, '
            f'{period_range=}, {interval=}, {events=}, {period1=}, {period2=}.'
        )

        params = self._DEFAULT_PARAMS | self._CHART_PARAMS

        _check_interval(interval)
        params['interval'] = interval

        if period_range is not None:
            _check_period_range(period_range)
            params['range'] = period_range

        if period1 is not None:
            params['period1'] = int(period1)

        if period2 is not None:
            params['period2'] = int(period2)

        if include_pre_post is not None:
            params['includePrePost'] = include_pre_post

        if events is not None:
            parsed_events = {e.strip() for e in events.split(',')}
            _check_events(parsed_events)
            # join parsed events, bcs they can be stripped
            params['events'] = ','.join(parsed_events)

        response = self._get_request(self._CHART_URL.format(ticker=ticker), params)
        return response.json()

    @_log_func
    @lru_cache(maxsize=128)
    def get_quote(
        self, tickers: str, include_pre_post: bool | None = None
    ) -> QuoteResponseJson:
        """Get quote for tickers.

        Args:
            tickers: Comma-separated ticker symbols.
            include_pre_post: Whether to include pre and post market.

        Returns: Quote response json including result and error.
        """
        logger.debug(f'Getting finance/quote for {tickers=}.')

        self._get_crumb()
        params = self._DEFAULT_PARAMS | {'symbols': tickers, 'crumb': self._crumb}

        if include_pre_post is not None:
            params['includePrePost'] = include_pre_post

        response = self._get_request(self._QUOTE_URL, params)
        return response.json()

    @_log_func
    @lru_cache(maxsize=128)
    def get_quote_type(self, tickers: str) -> QuoteTypeResponseJson:
        """Get quote type for tickers.

        Args:
            tickers: Comma-separated ticker symbols.

        Returns: Quote type response json including result and error.
        """
        logger.debug(f'Getting finance/quoteType for {tickers=}.')

        params = self._DEFAULT_PARAMS | self._QUOTE_TYPE_PARAMS | {'symbol': tickers}
        response = self._get_request(self._QUOTE_TYPE_URL, params)
        return response.json()

    @_log_func
    @lru_cache(maxsize=128)
    def get_quote_summary(self, ticker: str, modules: str) -> QuoteSummaryResponseJson:
        """Get quote summary for the ticker.

        Args:
            ticker: Ticker symbol.
            modules: Comma-separated modules to include.

        Returns: Quote summary response json including result and error.

        Raises: ValueError: If modules are not in list of valid values.
        """
        logger.debug(f'Getting finance/quoteSummary for {ticker=}.')

        parsed_modules = {m.strip() for m in modules.split(',')}
        _check_quote_summary_modules(parsed_modules)

        self._get_crumb()
        params = (
            self._DEFAULT_PARAMS
            | self._QUOTE_SUMMARY_PARAMS
            | {
                'crumb': self._crumb,
                # join parsed modules, bcs they can be stripped
                'modules': ','.join(parsed_modules),
            }
        )

        response = self._get_request(
            self._QUOTE_SUMMARY_URL.format(ticker=ticker), params
        )
        return response.json()

    @_log_func
    def get_timeseries(
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
            period1:
                Start timestamp in seconds. (optional, default: 1st Jan 2020 timestamp)
            period2: End timestamp in seconds. (optional, default: now timestamp)

        Returns: Timeseries response json including result and error.

        Raises: ValueError: If types are not in list of valid values.
        """
        logger.debug(
            f'Getting finance/timeseries for {ticker=}, '
            f'{types=}, {period1=}, {period2=}.'
        )

        parsed_types = {t.strip() for t in types.split(',')}
        _check_types(parsed_types)

        params = (
            self._DEFAULT_PARAMS
            | self._TIMESERIES_PARAMS
            | {
                # join parsed types, bcs they can be stripped
                'type': ','.join(parsed_types)
            }
        )

        if period1 is None:
            period1 = datetime(2020, 1, 1).astimezone().timestamp()

        params['period1'] = int(period1)

        if period2 is None:
            period2 = datetime.now().astimezone().timestamp()

        params['period2'] = int(period2)

        response = self._get_request(self._TIMESERIES_URL.format(ticker=ticker), params)
        return response.json()

    @_log_func
    @lru_cache(maxsize=128)
    def get_options(self, ticker: str) -> OptionsResponseJson:
        """Get options for the ticker.

        Args:
            ticker: Ticker symbol.

        Returns: Options response json including result and error.
        """
        logger.debug(f'Getting finance/options for {ticker=}.')

        self._get_crumb()
        params = self._DEFAULT_PARAMS | self._OPTIONS_PARAMS | {'crumb': self._crumb}
        response = self._get_request(self._OPTIONS_URL.format(ticker=ticker), params)
        return response.json()

    @_log_func
    @lru_cache(maxsize=128)
    def get_search(self, tickers: str) -> SearchResult:
        """Get search results for tickers.

        Args:
            tickers: Comma-separated ticker symbols.

        Returns: Search result json.
        """
        logger.debug(f'Getting finance/search for {tickers=}.')

        params = self._DEFAULT_PARAMS | {'q': tickers}
        response = self._get_request(self._SEARCH_URL, params)
        return response.json()

    @_log_func
    @lru_cache(maxsize=128)
    def get_recommendations(self, tickers: str) -> RecommendationsResponseJson:
        """Get analyst recommendations for tickers.

        Args:
            tickers: Comma-separated ticker symbols.

        Returns: Recommendations response json including result and error.
        """
        logger.debug(f'Getting finance/recommendations for {tickers=}.')

        params = self._DEFAULT_PARAMS
        response = self._get_request(
            self._RECOMMENDATIONS_URL.format(tickers=tickers), params
        )
        return response.json()

    @_log_func
    @lru_cache(maxsize=128)
    def get_insights(self, tickers: str) -> InsightsResponseJson:
        """Get insights for tickers.

        Args:
            tickers: Comma-separated ticker symbols.

        Returns: Insights response json including result and error.
        """
        logger.debug(f'Getting finance/insights for {tickers=}.')

        params = self._DEFAULT_PARAMS | self._INSIGHTS_PARAMS | {'symbols': tickers}
        response = self._get_request(self._INSIGHTS_URL, params)
        return response.json()

    @_log_func
    @lru_cache(maxsize=128)
    def get_ratings(self, ticker: str) -> RatingsResult:
        """Get ratings for the ticker.

        Args:
            ticker: Ticker symbol.

        Returns: Ratings result json.
        """
        logger.debug(f'Getting ratings for {ticker=}.')

        params = self._DEFAULT_PARAMS | self._RATINGS_PARAMS
        response = self._get_request(self._RATINGS_URL.format(ticker=ticker), params)
        return response.json()

    @_log_func
    @lru_cache(maxsize=128)
    def get_market_summaries(self) -> MarketSummaryResponseJson:
        """Get market summaries.

        Returns: Market summaries response json including result and error.
        """
        logger.debug('Getting finance/quote/marketSummary.')

        params = self._DEFAULT_PARAMS
        response = self._get_request(self._MARKET_SUMMARIES_URL, params)
        return response.json()

    @_log_func
    @lru_cache(maxsize=128)
    def get_trending(self) -> TrendingResponseJson:
        """Get trending tickers.

        Returns: Trending tickers response json including result and error.
        """
        logger.debug('Getting finance/trending.')

        params = self._DEFAULT_PARAMS
        response = self._get_request(self._TRENDING_URL, params)
        return response.json()

    @_log_func
    @lru_cache(maxsize=128)
    def get_currencies(self) -> CurrenciesResponseJson:
        """Get currency exchange rates.

        Returns: Currency exchange rates response json including result and error.
        """
        logger.debug('Getting finance/currencies.')

        params = self._DEFAULT_PARAMS
        response = self._get_request(self._CURRENCIES_URL, params)
        return response.json()

    @_log_func
    def get_calendar_events(
        self,
        modules: str | None = None,
        start_date: int | float | None = None,
        end_date: int | float | None = None,
    ) -> CalendarEventsResponseJson:
        """Get calendar events.

        Args:
            modules: Comma-separated modules to include.
            start_date:
                Start timestamp in miliseconds.
                (optional, default: (period2 - 149days) timestamp)
            end_date: End timestamp in miliseconds. (optional, default: now timestamp)

        Returns: Calendar events response json including result and error.

        Note: Query range cannot be greater than 150 days.
        """
        logger.debug('Getting finance/calendar-events.')

        params = self._DEFAULT_PARAMS | self._CALENDAR_EVENTS_PARAMS

        if modules:
            parsed_modules = {m.strip() for m in modules.split(',')}
            _check_calendar_event_modules(parsed_modules)
            # join parsed modules, bcs they can be stripped
            params['modules'] = ','.join(parsed_modules)

        if end_date is None:
            end_date = datetime.now().astimezone().timestamp() * 1000

        params['endDate'] = int(end_date)

        if start_date is None:
            end_date_dt = datetime.fromtimestamp(end_date / 1000)
            start_dt = end_date_dt - timedelta(days=149)
            start_date = start_dt.timestamp() * 1000

        params['startDate'] = int(start_date)

        response = self._get_request(self._CALENDAR_EVENTS_URL, params)
        return response.json()


class AsyncClient(ClientBase):
    """Asynchronous Client for Yahoo Finance API.

    Warning: HTTP resources closing
        Uses http resources, so do not forget to close them after use to avoid resource
            leakage or use context manager.

    Attributes:
        timeout: timeout (in secs) for each http request.
        max_retries: number of retries in case of failed request.
        _session:
            session instance, that is used for all http requests.
                (Is lazily initialized.)

    Methods:
        get_chart: Get chart data for the ticker.
        get_quote: Get quote for tickers.
        get_quote_type: Get quote type for tickers.
        get_quote_summary: Get quote summary for the ticker.
        get_timeseries: Get timeseries for the ticker.
        get_options: Get options for the ticker.
        get_search: Get search results for tickers.
        get_recommendations: Get analyst recommendations for tickers.
        get_insights: Get insights for tickers.
        get_ratings: Get ratings for the ticker.
        get_market_summaries: Get market summaries.
        get_trending: Get trending tickers.
        get_currencies: Get currency exchange rates.
        get_calendar_event: Get calendar events.
    """

    def __init__(self, timeout: float = 5.0, max_retries: int = 5) -> None:
        """Create new AsynClient instance.

        Args:
            timeout: timeout (in secs) for each http request.
            max_retries: number of retries in case of failed request.
        """
        super().__init__(timeout, max_retries)
        self._session: AsyncSession[Any] | None = None

    def _get_session(self) -> None:
        if self._session is None:
            self._session = AsyncSession(impersonate='chrome', timeout=self.timeout)

    @_async_log_func
    async def close(self) -> None:
        """Close the session if open and reset crumb."""
        if self._session is not None:
            await self._session.close()
            self._session = None

        if self._crumb is not None:
            self._crumb = None

    async def __aenter__(self) -> Self:
        """When entering context manager, create the session."""
        self._get_session()
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None = None,
        exc_val: BaseException | None = None,
        exc_tb: TracebackType | None = None,
    ) -> None:
        """When closing context manager, close the session."""
        await self.close()

    @_async_log_func
    async def _get_request(
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
                response = await self._session.get(**kwargs)
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

    @_async_log_func
    @alru_cache(maxsize=128)
    async def _get_crumb(self) -> None:
        if self._crumb is None:
            response = await self._get_request(self._CRUMB_URL)
            self._crumb = response.text

    @_async_log_func
    @alru_cache(maxsize=128)
    async def get_chart(
        self,
        ticker: str,
        interval: str,
        period_range: str | None = None,
        period1: int | float | None = None,
        period2: int | float | None = None,
        include_pre_post: bool | None = None,
        events: str | None = EVENTS,
    ) -> ChartResponseJson:
        """Get chart data for the ticker.

        Args:
            ticker: Ticker symbol.
            interval: Data interval.
            period_range: Range of the period.
            period1: Start timestamp in seconds. (optional, default: None)
            period2: End timestamp in seconds. (optional, default: None)
            include_pre_post: Whether to include pre and post market.
            events: Comma-separated events to include.

        Returns: Chart response json including result and error.

        Raises:
            ValueError: If any of period_range, interval or parsed_events are not in
                list of valid values.

        Note:
            Even though the the endpoint param is called range, period_range was chosen
            to avoid collision with python built-in method name.
        """
        logger.debug(
            f'Getting finance/chart for {ticker=}, '
            f'{period_range=}, {interval=}, {events=}, {period1=}, {period2=}.'
        )

        params = self._DEFAULT_PARAMS | self._CHART_PARAMS

        _check_interval(interval)
        params['interval'] = interval

        if period_range is not None:
            _check_period_range(period_range)
            params['range'] = period_range

        if period1 is not None:
            params['period1'] = int(period1)

        if period2 is not None:
            params['period2'] = int(period2)

        if include_pre_post is not None:
            params['includePrePost'] = include_pre_post

        if events is not None:
            parsed_events = {e.strip() for e in events.split(',')}
            _check_events(parsed_events)
            # join parsed events, bcs they can be stripped
            params['events'] = ','.join(parsed_events)

        response = await self._get_request(
            self._CHART_URL.format(ticker=ticker), params
        )
        return response.json()

    @_async_log_func
    @alru_cache(maxsize=128)
    async def get_quote(
        self, tickers: str, include_pre_post: bool | None = None
    ) -> QuoteResponseJson:
        """Get quote for tickers.

        Args:
            tickers: Comma-separated ticker symbols.
            include_pre_post: Whether to include pre and post market.

        Returns: Quote response json including result and error.
        """
        logger.debug(f'Getting finance/quote for {tickers=}.')

        await self._get_crumb()
        params = self._DEFAULT_PARAMS | {'symbols': tickers, 'crumb': self._crumb}

        if include_pre_post is not None:
            params['includePrePost'] = include_pre_post

        response = await self._get_request(self._QUOTE_URL, params)
        return response.json()

    @_async_log_func
    @alru_cache(maxsize=128)
    async def get_quote_type(self, tickers: str) -> QuoteTypeResponseJson:
        """Get quote type for tickers.

        Args:
            tickers: Comma-separated ticker symbols.

        Returns: Quote type response json including result and error.
        """
        logger.debug(f'Getting finance/quoteType for {tickers=}.')

        params = self._DEFAULT_PARAMS | self._QUOTE_TYPE_PARAMS | {'symbol': tickers}
        response = await self._get_request(self._QUOTE_TYPE_URL, params)
        return response.json()

    @_async_log_func
    @alru_cache(maxsize=128)
    async def get_quote_summary(
        self, ticker: str, modules: str
    ) -> QuoteSummaryResponseJson:
        """Get quote summary for the ticker.

        Args:
            ticker: Ticker symbol.
            modules: Comma-separated modules to include.

        Returns: Quote summary response json including result and error.

        Raises: ValueError: If modules are not in list of valid values.
        """
        logger.debug(f'Getting finance/quoteSummary for {ticker=}.')

        parsed_modules = {m.strip() for m in modules.split(',')}
        _check_quote_summary_modules(parsed_modules)

        await self._get_crumb()
        params = (
            self._DEFAULT_PARAMS
            | self._QUOTE_SUMMARY_PARAMS
            | {
                'crumb': self._crumb,
                # join parsed modules, bcs they can be stripped
                'modules': ','.join(parsed_modules),
            }
        )

        response = await self._get_request(
            self._QUOTE_SUMMARY_URL.format(ticker=ticker), params
        )
        return response.json()

    @_async_log_func
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
            period1:
                Start timestamp in seconds. (optional, default: 1st Jan 2020 timestamp)
            period2: End timestamp in seconds. (optional, default: now timestamp)

        Returns: Timeseries response json including result and error.

        Raises: ValueError: If types are not in list of valid values.
        """
        logger.debug(
            f'Getting finance/timeseries for {ticker=}, '
            f'{types=}, {period1=}, {period2=}.'
        )

        parsed_types = {t.strip() for t in types.split(',')}
        _check_types(parsed_types)

        params = (
            self._DEFAULT_PARAMS
            | self._TIMESERIES_PARAMS
            | {
                # join parsed types, bcs they can be stripped
                'type': ','.join(parsed_types)
            }
        )

        if period1 is None:
            period1 = datetime(2020, 1, 1).astimezone().timestamp()

        params['period1'] = int(period1)

        if period2 is None:
            period2 = datetime.now().astimezone().timestamp()

        params['period2'] = int(period2)

        response = await self._get_request(
            self._TIMESERIES_URL.format(ticker=ticker), params
        )
        return response.json()

    @_async_log_func
    @alru_cache(maxsize=128)
    async def get_options(self, ticker: str) -> OptionsResponseJson:
        """Get options for the ticker.

        Args:
            ticker: Ticker symbol.

        Returns: Options response json including result and error.
        """
        logger.debug(f'Getting finance/options for {ticker=}.')

        await self._get_crumb()
        params = self._DEFAULT_PARAMS | self._OPTIONS_PARAMS | {'crumb': self._crumb}
        response = await self._get_request(
            self._OPTIONS_URL.format(ticker=ticker), params
        )
        return response.json()

    @_async_log_func
    @alru_cache(maxsize=128)
    async def get_search(self, tickers: str) -> SearchResult:
        """Get search results for tickers.

        Args:
            tickers: Comma-separated ticker symbols.

        Returns: Search result json.
        """
        logger.debug(f'Getting finance/search for {tickers=}.')

        params = self._DEFAULT_PARAMS | {'q': tickers}
        response = await self._get_request(self._SEARCH_URL, params)
        return response.json()

    @_async_log_func
    @alru_cache(maxsize=128)
    async def get_recommendations(self, tickers: str) -> RecommendationsResponseJson:
        """Get analyst recommendations for tickers.

        Args:
            tickers: Comma-separated ticker symbols.

        Returns: Recommendations response json including result and error.
        """
        logger.debug(f'Getting finance/recommendations for {tickers=}.')

        params = self._DEFAULT_PARAMS
        response = await self._get_request(
            self._RECOMMENDATIONS_URL.format(tickers=tickers), params
        )
        return response.json()

    @_async_log_func
    @alru_cache(maxsize=128)
    async def get_insights(self, tickers: str) -> InsightsResponseJson:
        """Get insights for tickers.

        Args:
            tickers: Comma-separated ticker symbols.

        Returns: Insights response json including result and error.
        """
        logger.debug(f'Getting finance/insights for {tickers=}.')

        params = self._DEFAULT_PARAMS | self._INSIGHTS_PARAMS | {'symbols': tickers}
        response = await self._get_request(self._INSIGHTS_URL, params)
        return response.json()

    @_async_log_func
    @alru_cache(maxsize=128)
    async def get_ratings(self, ticker: str) -> RatingsResult:
        """Get ratings for the ticker.

        Args:
            ticker: Ticker symbol.

        Returns: Ratings result json.
        """
        logger.debug(f'Getting ratings for {ticker=}.')

        params = self._DEFAULT_PARAMS | self._RATINGS_PARAMS
        response = await self._get_request(
            self._RATINGS_URL.format(ticker=ticker), params
        )
        return response.json()

    @_async_log_func
    @alru_cache(maxsize=128)
    async def get_market_summaries(self) -> MarketSummaryResponseJson:
        """Get market summaries.

        Returns: Market summaries response json including result and error.
        """
        logger.debug('Getting finance/quote/marketSummary.')

        params = self._DEFAULT_PARAMS
        response = await self._get_request(self._MARKET_SUMMARIES_URL, params)
        return response.json()

    @_async_log_func
    @alru_cache(maxsize=128)
    async def get_trending(self) -> TrendingResponseJson:
        """Get trending tickers.

        Returns: Trending tickers response json including result and error.
        """
        logger.debug('Getting finance/trending.')

        params = self._DEFAULT_PARAMS
        response = await self._get_request(self._TRENDING_URL, params)
        return response.json()

    @_async_log_func
    @alru_cache(maxsize=128)
    async def get_currencies(self) -> CurrenciesResponseJson:
        """Get currency exchange rates.

        Returns: Currency exchange rates response json including result and error.
        """
        logger.debug('Getting finance/currencies.')

        params = self._DEFAULT_PARAMS
        response = await self._get_request(self._CURRENCIES_URL, params)
        return response.json()

    @_async_log_func
    async def get_calendar_events(
        self,
        modules: str | None = None,
        start_date: int | float | None = None,
        end_date: int | float | None = None,
    ) -> CalendarEventsResponseJson:
        """Get calendar events.

        Args:
            modules: Comma-separated modules to include.
            start_date:
                Start timestamp in miliseconds.
                (optional, default: (period2 - 149days) timestamp)
            end_date: End timestamp in miliseconds. (optional, default: now timestamp)

        Returns: Calendar events response json including result and error.

        Note: Query range cannot be greater than 150 days.
        """
        logger.debug('Getting finance/calendar-events.')

        params = self._DEFAULT_PARAMS | self._CALENDAR_EVENTS_PARAMS

        if modules:
            parsed_modules = {m.strip() for m in modules.split(',')}
            _check_calendar_event_modules(parsed_modules)
            # join parsed modules, bcs they can be stripped
            params['modules'] = ','.join(parsed_modules)

        if end_date is None:
            end_date = datetime.now().astimezone().timestamp() * 1000

        params['endDate'] = int(end_date)

        if start_date is None:
            end_date_dt = datetime.fromtimestamp(end_date / 1000)
            start_dt = end_date_dt - timedelta(days=149)
            start_date = start_dt.timestamp() * 1000

        params['startDate'] = int(start_date)

        response = await self._get_request(self._CALENDAR_EVENTS_URL, params)
        return response.json()


class _SingletonClientManager:
    """Manages a Client singleton."""

    _refcount = 0
    _client: Client | None = None

    @classmethod
    def _get_client(cls) -> Client:
        """Create Client singleton if not exists."""
        if cls._client is None:
            cls._client = Client()

        cls._refcount += 1

        return cls._client

    @classmethod
    def _release_client(cls) -> None:
        """Decrease refcount and close client singleton if no symbols left."""
        cls._refcount -= 1

        if cls._refcount <= 0 and cls._client is not None:
            cls._client.close()
            cls._client = None


class _SingletonAsyncClientManager:
    """Manages a AsyncClient singleton."""

    _refcount = 0
    _client: AsyncClient | None = None
    _lock = asyncio.Lock()

    @classmethod
    async def _get_client(cls) -> AsyncClient:
        """Create client singleton if not exists."""
        async with cls._lock:
            if cls._client is None:
                cls._client = AsyncClient()

            cls._refcount += 1

            return cls._client

    @classmethod
    async def _release_client(cls) -> None:
        """Decrease refcount and close client singleton if no symbols left."""
        async with cls._lock:
            cls._refcount -= 1

            if cls._refcount <= 0 and cls._client is not None:
                await cls._client.close()
                cls._client = None
