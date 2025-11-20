import logging
from types import TracebackType
from typing import Self, Type

from .client import Client, _SingletonClientManager
from .types import (
    InsightsFinanceResult,
    QuoteResult,
    QuoteTypeResult,
    RecommendationsFinanceResult,
    SearchResponseJson,
)
from .utils import _log_func

logger = logging.getLogger(__name__)


class SymbolBase:
    """Base for synchronous and asynchronous Symbol classes for a specific ticker.

    Attributes:
        ticker: Ticker symbol.
    """

    def __init__(self, tickers: str) -> None:
        """Create new Symbols instance.

        Args:
            tickers: Comma-separated ticker symbols.
        """
        self.tickers = tickers
        # self._ticker_list = self.ticker.split(',')
        # self._symbols = [Symbol(ticker) for ticker in self._ticker_list]


class Symbols(SymbolBase):
    """Symbols class for specified tickers.

    Warning: HTTP resources closing
        Uses http resources, so do not forget to close them after use to avoid resource
            leakage or use context manager.

    Attributes:
        ticker: Ticker symbol.
        _client:
            Client instance, that is used for all http requests.
                (Is lazily initialized.)

    Methods:
        get_quote: Get quote for the ticker.
        get_quote_type: Get quote type for the ticker.
        get_search: Get search results for the ticker.
        get_recommendations: Get analyst recommendations for the ticker.
        get_insights: Get insights for the ticker.
    """

    def __init__(self, tickers: str) -> None:
        """Create Symbols instance.

        Args:
            tickers: Comma-separated ticker symbols.
        """
        super().__init__(tickers)
        self._client: Client | None = None

    def _get_client(self) -> None:
        if self._client is None:
            self._client = _SingletonClientManager._get_client()

    def close(self) -> None:
        """Release the client if open for current symbol.

        Note:
            Only if no other symbols are using the client singleton, is the client
                closed.
        """
        if self._client is not None:
            _SingletonClientManager._release_client()
            self._client = None

    def __enter__(self) -> Self:
        """When entering context manager, get the client."""
        self._get_client()
        return self

    def __exit__(
        self,
        exc_type: Type[BaseException] | None = None,
        exc_val: BaseException | None = None,
        exc_tb: TracebackType | None = None,
    ) -> None:
        """When closing context manager, release the client."""
        self.close()

    @_log_func
    def get_quote(self) -> list[QuoteResult]:
        """Get quote for tickers.

        Returns: Quote response result json.
        """
        self._get_client()
        quote_json = self._client.get_quote(self.tickers)
        return quote_json['quoteResponse']['result']

    @_log_func
    def get_quote_type(self) -> list[QuoteTypeResult]:
        """Get quote type for tickers.

        Returns: Quote type response result json.
        """
        self._get_client()
        quote_type_json = self._client.get_quote_type(self.tickers)
        return quote_type_json['quoteType']['result']

    @_log_func
    def get_search(self) -> SearchResponseJson:
        """Get search results for tickers.

        Returns: Search response result json.
        """
        self._get_client()
        return self._client.get_search(self.tickers)

    @_log_func
    def get_insights(self) -> list[InsightsFinanceResult]:
        """Get insights for tickers.

        Returns: Insights response result json.
        """
        self._get_client()
        insights_json = self._client.get_insights(self.tickers)
        return insights_json['finance']['result']

    @_log_func
    def get_recommendations(self) -> list[RecommendationsFinanceResult]:
        """Get analyst recommendations for tickers.

        Returns: Recommendations response result json.
        """
        self._get_client()
        recommendations_json = self._client.get_recommendations(self.tickers)
        return recommendations_json['finance']['result']
