import asyncio
import logging
from types import TracebackType
from typing import Any, Self

from .client import (
    AsyncClient,
    Client,
    _SingletonAsyncClientManager,
    _SingletonClientManager,
)
from .symbol import AsyncSymbol, Symbol
from .types import (
    AssetProfile,
    CalendarEvents,
    ChartResult,
    DefaultKeyStatistics,
    Earnings,
    EarningsHistoryItem,
    EarningsTrendItem,
    FinancialData,
    FundOwnershipItem,
    IndexTrend,
    IndustryTrend,
    InsiderHolderItem,
    InsiderTransactionItem,
    InsightsFinanceResult,
    InstitutionOwnershipItem,
    MajorDirectHolders,
    MajorHoldersBreakdown,
    NetSharePurchaseActivity,
    OptionChainResult,
    PageViews,
    Price,
    QuoteResult,
    QuoteSummaryResult,
    QuoteTypeResult,
    RatingsResult,
    RecommendationsFinanceResult,
    RecommendationTrendItem,
    SearchResult,
    SecFilings,
    SectorTrend,
    SummaryDetail,
    SummaryProfile,
    TimeseriesResult,
    UpgradeDowngradeHistoryItem,
)
from .utils import _async_log_func, _log_func

logger = logging.getLogger(__name__)


class SymbolsBase:
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
        self._ticker_list = self.tickers.split(',')

    def _process_kwargs(self, kwargs: dict[str, Any]) -> dict[str, Any]:
        kwargs_copy = kwargs.copy()
        kwargs_copy.pop('self')
        # pop pytest specific memo: typeguard.TypeCheckMemo
        kwargs_copy.pop('memo', None)
        return kwargs_copy


class Symbols(SymbolsBase):
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
        get_chart: Get chart data for the ticker.
        get_quote: Get quote for the ticker.
        get_quote_type: Get quote type for the ticker.
        get_quote_summary_all_modules: Get quote summary for all modules for the ticker.
        get_asset_profile: Get asset profile for the ticker.
        get_summary_profile: Get summary profile for the ticker.
        get_summary_detail: Get summary detail for the ticker.
        get_price: Get price data for the ticker.
        get_default_key_statistics: Get default key statistics for the ticker.
        get_financial_data: Get financial data for the ticker.
        get_calendar_events: Get calendar events for the ticker.
        get_sec_filings: Get sec filings for the ticker.
        get_upgrade_downgrade_history: Get upgrade downgrade history for the ticker.
        get_institution_ownership: Get institution ownership for the ticker.
        get_fund_ownership: Get fund ownership for the ticker.
        get_major_direct_holders: Get major direct holders for the ticker.
        get_major_holders_breakdown: Get major holders breakdown for the ticker.
        get_insider_transactions: Get insider transactions for the ticker.
        get_insider_holders: Get insider holders for the ticker.
        get_net_share_purchase_activity: Get net share purchase activity for the ticker.
        get_earnings: Get earnings for the ticker.
        get_earnings_history: Get earnings history for the ticker.
        get_earnings_trend: Get earnings trend for the ticker.
        get_industry_trend: Get industry trend for the ticker.
        get_index_trend: Get index trend for the ticker.
        get_sector_trend: Get sector trend for the ticker.
        get_recommendation_trend: Get recommendation trend for the ticker.
        get_page_views: Get page views for the ticker.
        get_income_statement: Get income statement for the ticker.
        get_balance_sheet: Get balance sheet for the ticker.
        get_cash_flow: Get cash flow statement for the ticker.
        get_options: Get options data for the ticker.
        get_search: Get search results for the ticker.
        get_recommendations: Get analyst recommendations for the ticker.
        get_insights: Get insights for the ticker.
        get_ratings: Get ratings for the ticker.
    """

    def __init__(self, tickers: str) -> None:
        """Create Symbols instance.

        Args:
            tickers: Comma-separated ticker symbols.
        """
        super().__init__(tickers)
        self._client: Client | None = None
        self._symbols: list[Symbol] | None = None

    def _get_symbols(self) -> None:
        if self._symbols is None:
            self._symbols = [Symbol(ticker) for ticker in self._ticker_list]

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

        if self._symbols is not None:
            for s in self._symbols:
                s.close()
            self._symbols = None

    def __enter__(self) -> Self:
        """When entering context manager, get the client."""
        self._get_client()
        self._get_symbols()
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None = None,
        exc_val: BaseException | None = None,
        exc_tb: TracebackType | None = None,
    ) -> None:
        """When closing context manager, release the client."""
        self.close()

    @_log_func
    def get_chart(
        self,
        interval: str,
        period_range: str | None = None,
        period1: int | float | None = None,
        period2: int | float | None = None,
        include_pre_post: bool | None = None,
        include_div: bool = True,
        include_split: bool = True,
        include_earn: bool = True,
        include_capital_gain: bool = True,
    ) -> list[ChartResult]:
        """Get chart data for tickers in series requests.

        Args:
            interval: Data interval.
            period_range: Range of the period.
            period1: Start timestamp in seconds. (optional, default: None)
            period2: End timestamp in seconds. (optional, default: None)
            include_pre_post: Whether to include pre and post market.
            include_div: Whether to include dividends.
            include_split: Whether to include stock splits.
            include_earn: Whether to include earnings.
            include_capital_gain: Whether to include capital gains.

        Returns: List of chart response result jsons.

        Note:
            Even though the the endpoint param is called range, period_range was chosen
            to avoid collision with python built-in method name.
        """
        kwargs = self._process_kwargs(locals())
        self._get_symbols()
        return [s.get_chart(**kwargs) for s in self._symbols]

    @_log_func
    def get_quote(self, include_pre_post: bool | None = None) -> list[QuoteResult]:
        """Get quote for tickers in a single request.

        Args:
            include_pre_post: Whether to include pre and post market.

        Returns: List of quote response result jsons.
        """
        kwargs = self._process_kwargs(locals())
        kwargs['tickers'] = self.tickers
        self._get_client()
        quote_json = self._client.get_quote(**kwargs)
        return quote_json['quoteResponse']['result']

    @_log_func
    def get_quote_type(self) -> list[QuoteTypeResult]:
        """Get quote type for tickers in a single request.

        Returns: List of quote type response result jsons.
        """
        self._get_client()
        quote_type_json = self._client.get_quote_type(self.tickers)
        return quote_type_json['quoteType']['result']

    @_log_func
    def get_quote_summary_all_modules(self) -> list[QuoteSummaryResult]:
        """Get quote summary for all modules for tickers.

        Returns: List of quote summary with all modules response result jsons.
        """
        self._get_symbols()
        return [s.get_quote_summary_all_modules() for s in self._symbols]

    @_log_func
    def get_asset_profile(self) -> list[AssetProfile]:
        """Get asset profile for tickers.

        Returns: List of quote summary with asset profile module response result jsons.
        """
        self._get_symbols()
        return [s.get_asset_profile() for s in self._symbols]

    @_log_func
    def get_summary_profile(self) -> list[SummaryProfile]:
        """Get summary profile for tickers.

        Returns:
            List of quote summary with summary profile module response result jsons.
        """
        self._get_symbols()
        return [s.get_summary_profile() for s in self._symbols]

    @_log_func
    def get_summary_detail(self) -> list[SummaryDetail]:
        """Get summary detail for tickers.

        Returns: List of quote summary with summary detail module response result jsons.
        """
        self._get_symbols()
        return [s.get_summary_detail() for s in self._symbols]

    @_log_func
    def get_price(self) -> list[Price]:
        """Get price data for tickers.

        Returns: List of quote summary with price data module response result jsons.
        """
        self._get_symbols()
        return [s.get_price() for s in self._symbols]

    @_log_func
    def get_default_key_statistics(self) -> list[DefaultKeyStatistics]:
        """Get default key statistics for tickers.

        Returns:
            List of quote summary with default key statistics module response result
            jsons.
        """
        self._get_symbols()
        return [s.get_default_key_statistics() for s in self._symbols]

    @_log_func
    def get_financial_data(self) -> list[FinancialData]:
        """Get financial data for tickers.

        Returns: List of quote summary with financial data module response result jsons.
        """
        self._get_symbols()
        return [s.get_financial_data() for s in self._symbols]

    @_log_func
    def get_calendar_events(self) -> list[CalendarEvents]:
        """Get calendar events for tickers.

        Returns:
            List of quote summary with calendar events module response result jsons.
        """
        self._get_symbols()
        return [s.get_calendar_events() for s in self._symbols]

    @_log_func
    def get_sec_filings(self) -> list[SecFilings]:
        """Get sec filings for tickers.

        Returns: List of quote summary with sec filings module response result jsons.
        """
        self._get_symbols()
        return [s.get_sec_filings() for s in self._symbols]

    @_log_func
    def get_upgrade_downgrade_history(self) -> list[list[UpgradeDowngradeHistoryItem]]:
        """Get upgrade downgrade history for tickers.

        Returns:
            List of quote summary with upgrade downgrade history module response results
            jsons.
        """
        self._get_symbols()
        return [s.get_upgrade_downgrade_history() for s in self._symbols]

    @_log_func
    def get_institution_ownership(self) -> list[list[InstitutionOwnershipItem]]:
        """Get institution ownership for tickers.

        Returns:
            List of quote summary with institution ownership module response results
            jsons.
        """
        self._get_symbols()
        return [s.get_institution_ownership() for s in self._symbols]

    @_log_func
    def get_fund_ownership(self) -> list[list[FundOwnershipItem]]:
        """Get fund ownership for tickers.

        Returns:
            List of quote summary with fund ownership module response results jsons.
        """
        self._get_symbols()
        return [s.get_fund_ownership() for s in self._symbols]

    @_log_func
    def get_major_direct_holders(self) -> list[MajorDirectHolders]:
        """Get major direct holders for tickers.

        Returns: List of quote summary with direct holders module response result jsons.
        """
        self._get_symbols()
        return [s.get_major_direct_holders() for s in self._symbols]

    @_log_func
    def get_major_holders_breakdown(self) -> list[MajorHoldersBreakdown]:
        """Get major holders breakdown for tickers.

        Returns:
            List of quote summary with holders breakdown module response result jsons.
        """
        self._get_symbols()
        return [s.get_major_holders_breakdown() for s in self._symbols]

    @_log_func
    def get_insider_transactions(self) -> list[list[InsiderTransactionItem]]:
        """Get insider transactions for tickers.

        Returns:
            List of quote summary with insider transactions module response results
            jsons.
        """
        self._get_symbols()
        return [s.get_insider_transactions() for s in self._symbols]

    @_log_func
    def get_insider_holders(self) -> list[list[InsiderHolderItem]]:
        """Get insider holders for tickers.

        Returns:
            List of quote summary with insider holders module response results jsons.
        """
        self._get_symbols()
        return [s.get_insider_holders() for s in self._symbols]

    @_log_func
    def get_net_share_purchase_activity(self) -> list[NetSharePurchaseActivity]:
        """Get net share purchase activity for tickers.

        Returns:
            List of quote summary with net share purchase activity module response
            result jsons.
        """
        self._get_symbols()
        return [s.get_net_share_purchase_activity() for s in self._symbols]

    @_log_func
    def get_earnings(self) -> list[Earnings]:
        """Get earnings for tickers.

        Returns: List of quote summary with earnings module response result jsons.
        """
        self._get_symbols()
        return [s.get_earnings() for s in self._symbols]

    @_log_func
    def get_earnings_history(self) -> list[list[EarningsHistoryItem]]:
        """Get earnings history for tickers.

        Returns:
            List of quote summary with earnings history module response results jsons.
        """
        self._get_symbols()
        return [s.get_earnings_history() for s in self._symbols]

    @_log_func
    def get_earnings_trend(self) -> list[list[EarningsTrendItem]]:
        """Get earnings trend for tickers.

        Returns:
            List of quote summary with earnings trend module response results jsons.
        """
        self._get_symbols()
        return [s.get_earnings_trend() for s in self._symbols]

    @_log_func
    def get_industry_trend(self) -> list[IndustryTrend]:
        """Get industry trend for tickers.

        Returns: List of quote summary with industry trend module response result jsons.
        """
        self._get_symbols()
        return [s.get_industry_trend() for s in self._symbols]

    @_log_func
    def get_index_trend(self) -> list[IndexTrend]:
        """Get index trend for the ticker.

        Returns: List of quote summary with index trend module response result jsons.
        """
        self._get_symbols()
        return [s.get_index_trend() for s in self._symbols]

    @_log_func
    def get_sector_trend(self) -> list[SectorTrend]:
        """Get sector trend for tickers.

        Returns: List of quote summary with sector trend module response result jsons.
        """
        self._get_symbols()
        return [s.get_sector_trend() for s in self._symbols]

    @_log_func
    def get_recommendation_trend(self) -> list[list[RecommendationTrendItem]]:
        """Get recommendation trend for tickers.

        Returns:
            List of quote summary with recommendation trend module response results
            jsons.
        """
        self._get_symbols()
        return [s.get_recommendation_trend() for s in self._symbols]

    @_log_func
    def get_page_views(self) -> list[PageViews]:
        """Get page views for tickers.

        Returns: List of quote summary with page views module response result jsons.
        """
        self._get_symbols()
        return [s.get_page_views() for s in self._symbols]

    @_log_func
    def get_income_statement(
        self,
        frequency: str,
        period1: int | float | None = None,
        period2: int | float | None = None,
    ) -> list[list[TimeseriesResult]]:
        """Get income statement for tickers.

        Args:
            frequency: annual, quarterly or trailing.
            period1:
                Start timestamp in seconds. (optional, default: 1st Jan 2020 timestamp)
            period2: End timestamp in seconds. (optional, default: now timestamp)

        Returns: List of income statement response results jsons.
        """
        kwargs = self._process_kwargs(locals())
        self._get_symbols()
        return [s.get_income_statement(**kwargs) for s in self._symbols]

    @_log_func
    def get_balance_sheet(
        self,
        frequency: str,
        period1: int | float | None = None,
        period2: int | float | None = None,
    ) -> list[list[TimeseriesResult]]:
        """Get balance sheet for tickers.

        Args:
            frequency: annual, quarterly or trailing.
            period1:
                Start timestamp in seconds. (optional, default: 1st Jan 2020 timestamp)
            period2: End timestamp in seconds. (optional, default: now timestamp)

        Returns: List of balance sheet response results jsons.
        """
        kwargs = self._process_kwargs(locals())
        self._get_symbols()
        return [s.get_balance_sheet(**kwargs) for s in self._symbols]

    @_log_func
    def get_cash_flow(
        self,
        frequency: str,
        period1: int | float | None = None,
        period2: int | float | None = None,
    ) -> list[list[TimeseriesResult]]:
        """Get cash flow statement for tickers.

        Args:
            frequency: annual, quarterly or trailing.
            period1:
                Start timestamp in seconds. (optional, default: 1st Jan 2020 timestamp)
            period2: End timestamp in seconds. (optional, default: now timestamp)

        Returns: List of cash flow response results jsons.
        """
        kwargs = self._process_kwargs(locals())
        self._get_symbols()
        return [s.get_cash_flow(**kwargs) for s in self._symbols]

    @_log_func
    def get_options(self) -> list[OptionChainResult]:
        """Get options data for tickers.

        Returns: List of options response result jsons.
        """
        self._get_symbols()
        return [s.get_options() for s in self._symbols]

    @_log_func
    def get_search(self) -> SearchResult:
        """Get search results for tickers in a single request.

        Returns: Search response result json.
        """
        self._get_client()
        return self._client.get_search(self.tickers)

    @_log_func
    def get_insights(self) -> list[InsightsFinanceResult]:
        """Get insights for tickers in a single request.

        Returns: List of insights response result jsons.
        """
        self._get_client()
        insights_json = self._client.get_insights(self.tickers)
        return insights_json['finance']['result']

    @_log_func
    def get_recommendations(self) -> list[RecommendationsFinanceResult]:
        """Get analyst recommendations for tickers in a single request.

        Returns: List of recommendations response result jsons.
        """
        self._get_client()
        recommendations_json = self._client.get_recommendations(self.tickers)
        return recommendations_json['finance']['result']

    @_log_func
    def get_ratings(self) -> list[RatingsResult]:
        """Get ratings for tickers.

        Returns: List of ratings response result jsons.
        """
        self._get_symbols()
        return [s.get_ratings() for s in self._symbols]


class AsyncSymbols(SymbolsBase):
    """Asynchronous Symbols class for specified tickers.

    Warning: HTTP resources closing
        Uses http resources, so do not forget to close them after use to avoid resource
            leakage or use context manager.

    Attributes:
        ticker: Ticker symbol.
        _client:
            Client instance, that is used for all http requests.
                (Is lazily initialized.)

    Methods:
        get_chart: Get chart data for the ticker.
        get_quote: Get quote for the ticker.
        get_quote_type: Get quote type for the ticker.
        get_quote_summary_all_modules: Get quote summary for all modules for the ticker.
        get_asset_profile: Get asset profile for the ticker.
        get_summary_profile: Get summary profile for the ticker.
        get_summary_detail: Get summary detail for the ticker.
        get_price: Get price data for the ticker.
        get_default_key_statistics: Get default key statistics for the ticker.
        get_financial_data: Get financial data for the ticker.
        get_calendar_events: Get calendar events for the ticker.
        get_sec_filings: Get sec filings for the ticker.
        get_upgrade_downgrade_history: Get upgrade downgrade history for the ticker.
        get_institution_ownership: Get institution ownership for the ticker.
        get_fund_ownership: Get fund ownership for the ticker.
        get_major_direct_holders: Get major direct holders for the ticker.
        get_major_holders_breakdown: Get major holders breakdown for the ticker.
        get_insider_transactions: Get insider transactions for the ticker.
        get_insider_holders: Get insider holders for the ticker.
        get_net_share_purchase_activity: Get net share purchase activity for the ticker.
        get_earnings: Get earnings for the ticker.
        get_earnings_history: Get earnings history for the ticker.
        get_earnings_trend: Get earnings trend for the ticker.
        get_industry_trend: Get industry trend for the ticker.
        get_index_trend: Get index trend for the ticker.
        get_sector_trend: Get sector trend for the ticker.
        get_recommendation_trend: Get recommendation trend for the ticker.
        get_page_views: Get page views for the ticker.
        get_income_statement: Get income statement for the ticker.
        get_balance_sheet: Get balance sheet for the ticker.
        get_cash_flow: Get cash flow statement for the ticker.
        get_options: Get options data for the ticker.
        get_search: Get search results for the ticker.
        get_recommendations: Get analyst recommendations for the ticker.
        get_insights: Get insights for the ticker.
        get_ratings: Get ratings for the ticker.
    """

    def __init__(self, tickers: str) -> None:
        """Create Symbols instance.

        Args:
            tickers: Comma-separated ticker symbols.
        """
        super().__init__(tickers)
        self._client: AsyncClient | None = None
        self._symbols: list[AsyncSymbol] | None = None

    async def _get_symbols(self) -> None:
        if self._symbols is None:
            self._symbols = [AsyncSymbol(ticker) for ticker in self._ticker_list]

    async def _get_client(self) -> None:
        if self._client is None:
            self._client = await _SingletonAsyncClientManager._get_client()

    async def close(self) -> None:
        """Release the client if open for current symbol.

        Note:
            Only if no other symbols are using the client singleton, is the client
                closed.
        """
        if self._client is not None:
            await _SingletonAsyncClientManager._release_client()
            self._client = None

        if self._symbols is not None:
            for s in self._symbols:
                await s.close()
            self._symbols = None

    async def __aenter__(self) -> Self:
        """When entering context manager, get the client."""
        await self._get_client()
        await self._get_symbols()
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None = None,
        exc_val: BaseException | None = None,
        exc_tb: TracebackType | None = None,
    ) -> None:
        """When closing context manager, release the client."""
        await self.close()

    @_async_log_func
    async def get_chart(
        self,
        interval: str,
        period_range: str | None = None,
        period1: int | float | None = None,
        period2: int | float | None = None,
        include_pre_post: bool | None = None,
        include_div: bool = True,
        include_split: bool = True,
        include_earn: bool = True,
        include_capital_gain: bool = True,
    ) -> list[ChartResult]:
        """Get chart data for tickers in series requests.

        Args:
            interval: Data interval.
            period_range: Range of the period.
            period1: Start timestamp in seconds. (optional, default: None)
            period2: End timestamp in seconds. (optional, default: None)
            include_pre_post: Whether to include pre and post market.
            include_div: Whether to include dividends.
            include_split: Whether to include stock splits.
            include_earn: Whether to include earnings.
            include_capital_gain: Whether to include capital gains.

        Returns: List of chart response result jsons.

        Note:
            Even though the the endpoint param is called range, period_range was chosen
            to avoid collision with python built-in method name.
        """
        kwargs = self._process_kwargs(locals())
        await self._get_symbols()
        return await asyncio.gather(*[s.get_chart(**kwargs) for s in self._symbols])

    @_async_log_func
    async def get_quote(
        self, include_pre_post: bool | None = None
    ) -> list[QuoteResult]:
        """Get quote for tickers in a single request.

        Args:
            include_pre_post: Whether to include pre and post market.

        Returns: List of quote response result jsons.
        """
        kwargs = self._process_kwargs(locals())
        kwargs['tickers'] = self.tickers
        await self._get_client()
        quote_json = await self._client.get_quote(**kwargs)
        return quote_json['quoteResponse']['result']

    @_async_log_func
    async def get_quote_type(self) -> list[QuoteTypeResult]:
        """Get quote type for tickers in a single request.

        Returns: List of quote type response result jsons.
        """
        await self._get_client()
        quote_type_json = await self._client.get_quote_type(self.tickers)
        return quote_type_json['quoteType']['result']

    @_async_log_func
    async def get_quote_summary_all_modules(self) -> list[QuoteSummaryResult]:
        """Get quote summary for all modules for tickers.

        Returns: List of quote summary with all modules response result jsons.
        """
        await self._get_symbols()
        return await asyncio.gather(
            *[s.get_quote_summary_all_modules() for s in self._symbols]
        )

    @_async_log_func
    async def get_asset_profile(self) -> list[AssetProfile]:
        """Get asset profile for tickers.

        Returns: List of quote summary with asset profile module response result jsons.
        """
        await self._get_symbols()
        return await asyncio.gather(*[s.get_asset_profile() for s in self._symbols])

    @_async_log_func
    async def get_summary_profile(self) -> list[SummaryProfile]:
        """Get summary profile for tickers.

        Returns:
            List of quote summary with summary profile module response result jsons.
        """
        await self._get_symbols()
        return await asyncio.gather(*[s.get_summary_profile() for s in self._symbols])

    @_async_log_func
    async def get_summary_detail(self) -> list[SummaryDetail]:
        """Get summary detail for tickers.

        Returns: List of quote summary with summary detail module response result jsons.
        """
        await self._get_symbols()
        return await asyncio.gather(*[s.get_summary_detail() for s in self._symbols])

    @_async_log_func
    async def get_price(self) -> list[Price]:
        """Get price data for tickers.

        Returns: List of quote summary with price data module response result jsons.
        """
        await self._get_symbols()
        return await asyncio.gather(*[s.get_price() for s in self._symbols])

    @_async_log_func
    async def get_default_key_statistics(self) -> list[DefaultKeyStatistics]:
        """Get default key statistics for tickers.

        Returns:
            List of quote summary with default key statistics module response result
            jsons.
        """
        await self._get_symbols()
        return await asyncio.gather(
            *[s.get_default_key_statistics() for s in self._symbols]
        )

    @_async_log_func
    async def get_financial_data(self) -> list[FinancialData]:
        """Get financial data for tickers.

        Returns: List of quote summary with financial data module response result jsons.
        """
        await self._get_symbols()
        return await asyncio.gather(*[s.get_financial_data() for s in self._symbols])

    @_async_log_func
    async def get_calendar_events(self) -> list[CalendarEvents]:
        """Get calendar events for tickers.

        Returns:
            List of quote summary with calendar events module response result jsons.
        """
        await self._get_symbols()
        return await asyncio.gather(*[s.get_calendar_events() for s in self._symbols])

    @_async_log_func
    async def get_sec_filings(self) -> list[SecFilings]:
        """Get sec filings for tickers.

        Returns: List of quote summary with sec filings module response result jsons.
        """
        await self._get_symbols()
        return await asyncio.gather(*[s.get_sec_filings() for s in self._symbols])

    @_async_log_func
    async def get_upgrade_downgrade_history(
        self,
    ) -> list[list[UpgradeDowngradeHistoryItem]]:
        """Get upgrade downgrade history for tickers.

        Returns:
            List of quote summary with upgrade downgrade history module response results
            jsons.
        """
        await self._get_symbols()
        return await asyncio.gather(
            *[s.get_upgrade_downgrade_history() for s in self._symbols]
        )

    @_async_log_func
    async def get_institution_ownership(self) -> list[list[InstitutionOwnershipItem]]:
        """Get institution ownership for tickers.

        Returns:
            List of quote summary with institution ownership module response results
            jsons.
        """
        await self._get_symbols()
        return await asyncio.gather(
            *[s.get_institution_ownership() for s in self._symbols]
        )

    @_async_log_func
    async def get_fund_ownership(self) -> list[list[FundOwnershipItem]]:
        """Get fund ownership for tickers.

        Returns:
            List of quote summary with fund ownership module response results jsons.
        """
        await self._get_symbols()
        return await asyncio.gather(*[s.get_fund_ownership() for s in self._symbols])

    @_async_log_func
    async def get_major_direct_holders(self) -> list[MajorDirectHolders]:
        """Get major direct holders for tickers.

        Returns: List of quote summary with direct holders module response result jsons.
        """
        await self._get_symbols()
        return await asyncio.gather(
            *[s.get_major_direct_holders() for s in self._symbols]
        )

    @_async_log_func
    async def get_major_holders_breakdown(self) -> list[MajorHoldersBreakdown]:
        """Get major holders breakdown for tickers.

        Returns:
            List of quote summary with holders breakdown module response result jsons.
        """
        await self._get_symbols()
        return await asyncio.gather(
            *[s.get_major_holders_breakdown() for s in self._symbols]
        )

    @_async_log_func
    async def get_insider_transactions(self) -> list[list[InsiderTransactionItem]]:
        """Get insider transactions for tickers.

        Returns:
            List of quote summary with insider transactions module response results
            jsons.
        """
        await self._get_symbols()
        return await asyncio.gather(
            *[s.get_insider_transactions() for s in self._symbols]
        )

    @_async_log_func
    async def get_insider_holders(self) -> list[list[InsiderHolderItem]]:
        """Get insider holders for tickers.

        Returns:
            List of quote summary with insider holders module response results jsons.
        """
        await self._get_symbols()
        return await asyncio.gather(*[s.get_insider_holders() for s in self._symbols])

    @_async_log_func
    async def get_net_share_purchase_activity(self) -> list[NetSharePurchaseActivity]:
        """Get net share purchase activity for tickers.

        Returns:
            List of quote summary with net share purchase activity module response
            result jsons.
        """
        await self._get_symbols()
        return await asyncio.gather(
            *[s.get_net_share_purchase_activity() for s in self._symbols]
        )

    @_async_log_func
    async def get_earnings(self) -> list[Earnings]:
        """Get earnings for tickers.

        Returns: List of quote summary with earnings module response result jsons.
        """
        await self._get_symbols()
        return await asyncio.gather(*[s.get_earnings() for s in self._symbols])

    @_async_log_func
    async def get_earnings_history(self) -> list[list[EarningsHistoryItem]]:
        """Get earnings history for tickers.

        Returns:
            List of quote summary with earnings history module response results jsons.
        """
        await self._get_symbols()
        return await asyncio.gather(*[s.get_earnings_history() for s in self._symbols])

    @_async_log_func
    async def get_earnings_trend(self) -> list[list[EarningsTrendItem]]:
        """Get earnings trend for tickers.

        Returns:
            List of quote summary with earnings trend module response results jsons.
        """
        await self._get_symbols()
        return await asyncio.gather(*[s.get_earnings_trend() for s in self._symbols])

    @_async_log_func
    async def get_industry_trend(self) -> list[IndustryTrend]:
        """Get industry trend for tickers.

        Returns: List of quote summary with industry trend module response result jsons.
        """
        await self._get_symbols()
        return await asyncio.gather(*[s.get_industry_trend() for s in self._symbols])

    @_async_log_func
    async def get_index_trend(self) -> list[IndexTrend]:
        """Get index trend for the ticker.

        Returns: List of quote summary with index trend module response result jsons.
        """
        await self._get_symbols()
        return await asyncio.gather(*[s.get_index_trend() for s in self._symbols])

    @_async_log_func
    async def get_sector_trend(self) -> list[SectorTrend]:
        """Get sector trend for tickers.

        Returns: List of quote summary with sector trend module response result jsons.
        """
        await self._get_symbols()
        return await asyncio.gather(*[s.get_sector_trend() for s in self._symbols])

    @_async_log_func
    async def get_recommendation_trend(self) -> list[list[RecommendationTrendItem]]:
        """Get recommendation trend for tickers.

        Returns:
            List of quote summary with recommendation trend module response results
            jsons.
        """
        await self._get_symbols()
        return await asyncio.gather(
            *[s.get_recommendation_trend() for s in self._symbols]
        )

    @_async_log_func
    async def get_page_views(self) -> list[PageViews]:
        """Get page views for tickers.

        Returns: List of quote summary with page views module response result jsons.
        """
        await self._get_symbols()
        return await asyncio.gather(*[s.get_page_views() for s in self._symbols])

    @_async_log_func
    async def get_income_statement(
        self,
        frequency: str,
        period1: int | float | None = None,
        period2: int | float | None = None,
    ) -> list[list[TimeseriesResult]]:
        """Get income statement for tickers.

        Args:
            frequency: annual, quarterly or trailing.
            period1:
                Start timestamp in seconds. (optional, default: 1st Jan 2020 timestamp)
            period2: End timestamp in seconds. (optional, default: now timestamp)

        Returns: List of income statement response results jsons.
        """
        kwargs = self._process_kwargs(locals())
        await self._get_symbols()
        return await asyncio.gather(
            *[s.get_income_statement(**kwargs) for s in self._symbols]
        )

    @_async_log_func
    async def get_balance_sheet(
        self,
        frequency: str,
        period1: int | float | None = None,
        period2: int | float | None = None,
    ) -> list[list[TimeseriesResult]]:
        """Get balance sheet for tickers.

        Args:
            frequency: annual, quarterly or trailing.
            period1:
                Start timestamp in seconds. (optional, default: 1st Jan 2020 timestamp)
            period2: End timestamp in seconds. (optional, default: now timestamp)

        Returns: List of balance sheet response results jsons.
        """
        kwargs = self._process_kwargs(locals())
        await self._get_symbols()
        return await asyncio.gather(
            *[s.get_balance_sheet(**kwargs) for s in self._symbols]
        )

    @_async_log_func
    async def get_cash_flow(
        self,
        frequency: str,
        period1: int | float | None = None,
        period2: int | float | None = None,
    ) -> list[list[TimeseriesResult]]:
        """Get cash flow statement for tickers.

        Args:
            frequency: annual, quarterly or trailing.
            period1:
                Start timestamp in seconds. (optional, default: 1st Jan 2020 timestamp)
            period2: End timestamp in seconds. (optional, default: now timestamp)

        Returns: List of cash flow response results jsons.
        """
        kwargs = self._process_kwargs(locals())
        await self._get_symbols()
        return await asyncio.gather(*[s.get_cash_flow(**kwargs) for s in self._symbols])

    @_async_log_func
    async def get_options(self) -> list[OptionChainResult]:
        """Get options data for tickers.

        Returns: List of options response result jsons.
        """
        await self._get_symbols()
        return await asyncio.gather(*[s.get_options() for s in self._symbols])

    @_async_log_func
    async def get_search(self) -> SearchResult:
        """Get search results for tickers in a single request.

        Returns: Search response result json.
        """
        await self._get_client()
        return await self._client.get_search(self.tickers)

    @_async_log_func
    async def get_insights(self) -> list[InsightsFinanceResult]:
        """Get insights for tickers in a single request.

        Returns: List of insights response result jsons.
        """
        await self._get_client()
        insights_json = await self._client.get_insights(self.tickers)
        return insights_json['finance']['result']

    @_async_log_func
    async def get_recommendations(self) -> list[RecommendationsFinanceResult]:
        """Get analyst recommendations for tickers in a single request.

        Returns: List of recommendations response result jsons.
        """
        await self._get_client()
        recommendations_json = await self._client.get_recommendations(self.tickers)
        return recommendations_json['finance']['result']

    @_async_log_func
    async def get_ratings(self) -> list[RatingsResult]:
        """Get ratings for tickers.

        Returns: List of ratings response result jsons.
        """
        await self._get_symbols()
        return await asyncio.gather(*[s.get_ratings() for s in self._symbols])
