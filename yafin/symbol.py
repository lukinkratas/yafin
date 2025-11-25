import logging
from types import TracebackType
from typing import Any, Self

from .client import (
    AsyncClient,
    Client,
    _SingletonAsyncClientManager,
    _SingletonClientManager,
)
from .const import QUOTE_SUMMARY_MODULES
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
    QuoteSummaryModuleResult,
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
from .utils import _async_log_func, _log_func, get_types_with_frequency

logger = logging.getLogger(__name__)


class SymbolBase:
    """Base for synchronous and asynchronous Symbol classes for a specific ticker.

    Attributes:
        ticker: Ticker symbol.
    """

    def __init__(self, ticker: str) -> None:
        """Create new Symbol instance.

        Args:
            ticker: Ticker symbol.
        """
        self.ticker = ticker


class Symbol(SymbolBase):
    """Symbol class for a specific ticker.

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

    def __init__(self, ticker: str) -> None:
        """Create new Symbol instance.

        Args:
            ticker: Ticker symbol.
        """
        super().__init__(ticker)
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
    ) -> ChartResult:
        """Get chart data for the ticker.

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

        Returns: Chart response result json.

        Note:
            Even though the the endpoint param is called range, period_range was chosen
            to avoid collision with python built-in method name.
        """
        kwargs: dict[str, Any] = {'ticker': self.ticker, 'interval': interval}

        if period_range is not None:
            kwargs['period_range'] = period_range

        if period1 is not None:
            kwargs['period1'] = period1

        if period2 is not None:
            kwargs['period2'] = period2

        if include_pre_post is not None:
            kwargs['include_pre_post'] = include_pre_post

        events_list = []

        if include_div:
            events_list.append('div')

        if include_split:
            events_list.append('split')

        if include_earn:
            events_list.append('earn')

        if include_capital_gain:
            events_list.append('capitalGain')

        if events_list:
            kwargs['events'] = ','.join(events_list)

        self._get_client()
        chart_json = self._client.get_chart(**kwargs)
        return chart_json['chart']['result'][0]

    @_log_func
    def get_quote(self, include_pre_post: bool | None = None) -> QuoteResult:
        """Get quote for the ticker.

        Args:
            include_pre_post: Whether to include pre and post market.

        Returns: Quote response result json.
        """
        kwargs: dict[str, Any] = {'tickers': self.ticker}

        if include_pre_post is not None:
            kwargs['include_pre_post'] = include_pre_post

        self._get_client()
        quote_json = self._client.get_quote(**kwargs)
        return quote_json['quoteResponse']['result'][0]

    @_log_func
    def get_quote_type(self) -> QuoteTypeResult:
        """Get quote type for the ticker.

        Returns: Quote type response result json.
        """
        self._get_client()
        quote_type_json = self._client.get_quote_type(self.ticker)
        return quote_type_json['quoteType']['result'][0]

    @_log_func
    def get_quote_summary_all_modules(self) -> QuoteSummaryResult:
        """Get quote summary for all modules for the ticker.

        Returns: Quote summary with all modules response result json.
        """
        self._get_client()
        quote_summary_json = self._client.get_quote_summary(
            self.ticker, QUOTE_SUMMARY_MODULES
        )
        return quote_summary_json['quoteSummary']['result'][0]

    @_log_func
    def _get_quote_summary_single_module(self, module: str) -> QuoteSummaryModuleResult:
        self._get_client()
        quote_summary_json = self._client.get_quote_summary(self.ticker, module)
        return quote_summary_json['quoteSummary']['result'][0][module]

    @_log_func
    def get_asset_profile(self) -> AssetProfile:
        """Get asset profile for the ticker.

        Returns: Quote summary with asset profile module response result json.
        """
        return self._get_quote_summary_single_module('assetProfile')

    @_log_func
    def get_summary_profile(self) -> SummaryProfile:
        """Get summary profile for the ticker.

        Returns: Quote summary with summary profile module response result json.
        """
        return self._get_quote_summary_single_module('summaryProfile')

    @_log_func
    def get_summary_detail(self) -> SummaryDetail:
        """Get summary detail for the ticker.

        Returns: Quote summary with summary detail module response result json.
        """
        return self._get_quote_summary_single_module('summaryDetail')

    @_log_func
    def get_price(self) -> Price:
        """Get price data for the ticker.

        Returns: Quote summary with price data module response result json.
        """
        return self._get_quote_summary_single_module('price')

    @_log_func
    def get_default_key_statistics(self) -> DefaultKeyStatistics:
        """Get default key statistics for the ticker.

        Returns: Quote summary with default key statistics module response result json.
        """
        return self._get_quote_summary_single_module('defaultKeyStatistics')

    @_log_func
    def get_financial_data(self) -> FinancialData:
        """Get financial data for the ticker.

        Returns: Quote summary with financial data module response result json.
        """
        return self._get_quote_summary_single_module('financialData')

    @_log_func
    def get_calendar_events(self) -> CalendarEvents:
        """Get calendar events for the ticker.

        Returns: Quote summary with calendar events module response result json.
        """
        return self._get_quote_summary_single_module('calendarEvents')

    @_log_func
    def get_sec_filings(self) -> SecFilings:
        """Get sec filings for the ticker.

        Returns: Quote summary with sec filings module response result json.
        """
        return self._get_quote_summary_single_module('secFilings')

    @_log_func
    def get_upgrade_downgrade_history(self) -> list[UpgradeDowngradeHistoryItem]:
        """Get upgrade downgrade history for the ticker.

        Returns:
            Quote summary with upgrade downgrade history module response results
                json.
        """
        result = self._get_quote_summary_single_module('upgradeDowngradeHistory')
        return result['history']

    @_log_func
    def get_institution_ownership(self) -> list[InstitutionOwnershipItem]:
        """Get institution ownership for the ticker.

        Returns: Quote summary with institution ownership module response results json.
        """
        result = self._get_quote_summary_single_module('institutionOwnership')
        return result['ownershipList']

    @_log_func
    def get_fund_ownership(self) -> list[FundOwnershipItem]:
        """Get fund ownership for the ticker.

        Returns: Quote summary with fund ownership module response results json.
        """
        result = self._get_quote_summary_single_module('fundOwnership')
        return result['ownershipList']

    @_log_func
    def get_major_direct_holders(self) -> MajorDirectHolders:
        """Get major direct holders for the ticker.

        Returns: Quote summary with direct holders module response result json.
        """
        return self._get_quote_summary_single_module('majorDirectHolders')

    @_log_func
    def get_major_holders_breakdown(self) -> MajorHoldersBreakdown:
        """Get major holders breakdown for the ticker.

        Returns: Quote summary with holders breakdown module response result json.
        """
        return self._get_quote_summary_single_module('majorHoldersBreakdown')

    @_log_func
    def get_insider_transactions(self) -> list[InsiderTransactionItem]:
        """Get insider transactions for the ticker.

        Returns: Quote summary with insider transactions module response results json.
        """
        result = self._get_quote_summary_single_module('insiderTransactions')
        return result['transactions']

    @_log_func
    def get_insider_holders(self) -> list[InsiderHolderItem]:
        """Get insider holders for the ticker.

        Returns: Quote summary with insider holders module response results json.
        """
        result = self._get_quote_summary_single_module('insiderHolders')
        return result['holders']

    @_log_func
    def get_net_share_purchase_activity(self) -> NetSharePurchaseActivity:
        """Get net share purchase activity for the ticker.

        Returns:
            Quote summary with net share purchase activity module response result
                json.
        """
        return self._get_quote_summary_single_module('netSharePurchaseActivity')

    @_log_func
    def get_earnings(self) -> Earnings:
        """Get earnings for the ticker.

        Returns: Quote summary with earnings module response result json.
        """
        return self._get_quote_summary_single_module('earnings')

    @_log_func
    def get_earnings_history(self) -> list[EarningsHistoryItem]:
        """Get earnings history for the ticker.

        Returns: Quote summary with earnings history module response results json.
        """
        result = self._get_quote_summary_single_module('earningsHistory')
        return result['history']

    @_log_func
    def get_earnings_trend(self) -> list[EarningsTrendItem]:
        """Get earnings trend for the ticker.

        Returns: Quote summary with earnings trend module response results json.
        """
        result = self._get_quote_summary_single_module('earningsTrend')
        return result['trend']

    @_log_func
    def get_industry_trend(self) -> IndustryTrend:
        """Get industry trend for the ticker.

        Returns: Quote summary with industry trend module response result json.
        """
        return self._get_quote_summary_single_module('industryTrend')

    @_log_func
    def get_index_trend(self) -> IndexTrend:
        """Get index trend for the ticker.

        Returns: Quote summary with index trend module response result json.
        """
        return self._get_quote_summary_single_module('indexTrend')

    @_log_func
    def get_sector_trend(self) -> SectorTrend:
        """Get sector trend for the ticker.

        Returns: Quote summary with sector trend module response result json.
        """
        return self._get_quote_summary_single_module('sectorTrend')

    @_log_func
    def get_recommendation_trend(self) -> list[RecommendationTrendItem]:
        """Get recommendation trend for the ticker.

        Returns: Quote summary with recommendation trend module response results json.
        """
        result = self._get_quote_summary_single_module('recommendationTrend')
        return result['trend']

    @_log_func
    def get_page_views(self) -> PageViews:
        """Get page views for the ticker.

        Returns: Quote summary with page views module response result json.
        """
        return self._get_quote_summary_single_module('pageViews')

    @_log_func
    def _get_financials(
        self,
        frequency: str,
        typ: str,
        period1: int | float | None = None,
        period2: int | float | None = None,
    ) -> list[TimeseriesResult]:
        self._get_client()
        types = get_types_with_frequency(typ, frequency)
        timeseries_json = self._client.get_timeseries(
            self.ticker, types, period1, period2
        )
        return timeseries_json['timeseries']['result']

    @_log_func
    def get_income_statement(
        self,
        frequency: str,
        period1: int | float | None = None,
        period2: int | float | None = None,
    ) -> list[TimeseriesResult]:
        """Get income statement for the ticker.

        Args:
            frequency: annual, quarterly or trailing.
            period1:
                Start timestamp in seconds. (optional, default: 1st Jan 2020 timestamp)
            period2: End timestamp in seconds. (optional, default: now timestamp)

        Returns: Income statement response results json.
        """
        return self._get_financials(frequency, 'income_statement', period1, period2)

    @_log_func
    def get_balance_sheet(
        self,
        frequency: str,
        period1: int | float | None = None,
        period2: int | float | None = None,
    ) -> list[TimeseriesResult]:
        """Get balance sheet for the ticker.

        Args:
            frequency: annual, quarterly or trailing.
            period1:
                Start timestamp in seconds. (optional, default: 1st Jan 2020 timestamp)
            period2: End timestamp in seconds. (optional, default: now timestamp)

        Returns: Balance sheet response results json.
        """
        return self._get_financials(frequency, 'balance_sheet', period1, period2)

    @_log_func
    def get_cash_flow(
        self,
        frequency: str,
        period1: int | float | None = None,
        period2: int | float | None = None,
    ) -> list[TimeseriesResult]:
        """Get cash flow statement for the ticker.

        Args:
            frequency: annual, quarterly or trailing.
            period1:
                Start timestamp in seconds. (optional, default: 1st Jan 2020 timestamp)
            period2: End timestamp in seconds. (optional, default: now timestamp)

        Returns: Cash flow response results json.
        """
        return self._get_financials(frequency, 'cash_flow', period1, period2)

    @_log_func
    def get_options(self) -> OptionChainResult:
        """Get options data for the ticker.

        Returns: Options response result json.
        """
        self._get_client()
        options_json = self._client.get_options(self.ticker)
        return options_json['optionChain']['result'][0]

    @_log_func
    def get_search(self) -> SearchResult:
        """Get search results for the ticker.

        Returns: Search result json.
        """
        self._get_client()
        return self._client.get_search(self.ticker)

    @_log_func
    def get_recommendations(self) -> RecommendationsFinanceResult:
        """Get analyst recommendations for the ticker.

        Returns: Recommendations response result json.
        """
        self._get_client()
        recommendations_json = self._client.get_recommendations(self.ticker)
        return recommendations_json['finance']['result'][0]

    @_log_func
    def get_insights(self) -> InsightsFinanceResult:
        """Get insights for the ticker.

        Returns: Insights response result json.
        """
        self._get_client()
        insights_json = self._client.get_insights(self.ticker)
        return insights_json['finance']['result'][0]

    @_log_func
    def get_ratings(self) -> RatingsResult:
        """Get ratings for the ticker.

        Returns: Ratings result json.
        """
        self._get_client()
        return self._client.get_ratings(self.ticker)


class AsyncSymbol(SymbolBase):
    """Asynchronous Symbol class for a specific ticker.

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

    def __init__(self, ticker: str) -> None:
        """Create new AsyncSymbol instance.

        Args:
            ticker: Ticker symbol.
        """
        super().__init__(ticker)
        self._client: AsyncClient | None = None

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

    async def __aenter__(self) -> Self:
        """When entering context manager, get the client."""
        await self._get_client()
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
    ) -> ChartResult:
        """Get chart data for the ticker.

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

        Returns: Chart response result json.

        Note:
            Even though the the endpoint param is called range, period_range was chosen
            to avoid collision with python built-in method name.
        """
        kwargs: dict[str, Any] = {'ticker': self.ticker, 'interval': interval}

        if period_range is not None:
            kwargs['period_range'] = period_range

        if period1 is not None:
            kwargs['period1'] = period1

        if period2 is not None:
            kwargs['period2'] = period2

        if include_pre_post is not None:
            kwargs['include_pre_post'] = include_pre_post

        events_list = []

        if include_div:
            events_list.append('div')

        if include_split:
            events_list.append('split')

        if include_earn:
            events_list.append('earn')

        if include_capital_gain:
            events_list.append('capitalGain')

        if events_list:
            kwargs['events'] = ','.join(events_list)

        await self._get_client()
        chart_json = await self._client.get_chart(**kwargs)
        return chart_json['chart']['result'][0]

    @_async_log_func
    async def get_quote(self, include_pre_post: bool | None = None) -> QuoteResult:
        """Get quote for the ticker.

        Args:
            include_pre_post: Whether to include pre and post market.

        Returns: Quote response result json.
        """
        kwargs: dict[str, Any] = {'tickers': self.ticker}

        if include_pre_post is not None:
            kwargs['include_pre_post'] = include_pre_post

        await self._get_client()
        quote_json = await self._client.get_quote(**kwargs)
        return quote_json['quoteResponse']['result'][0]

    @_async_log_func
    async def get_quote_type(self) -> QuoteTypeResult:
        """Get quote type for the ticker.

        Returns: Quote type response result json.
        """
        await self._get_client()
        quote_type_json = await self._client.get_quote_type(self.ticker)
        return quote_type_json['quoteType']['result'][0]

    @_async_log_func
    async def get_quote_summary_all_modules(self) -> QuoteSummaryResult:
        """Get quote summary for all modules for the ticker.

        Returns: Quote summary with all modules response result json.
        """
        await self._get_client()
        quote_summary_json = await self._client.get_quote_summary(
            self.ticker, QUOTE_SUMMARY_MODULES
        )
        return quote_summary_json['quoteSummary']['result'][0]

    @_async_log_func
    async def _get_quote_summary_single_module(
        self, module: str
    ) -> QuoteSummaryModuleResult:
        await self._get_client()
        quote_summary_json = await self._client.get_quote_summary(self.ticker, module)
        return quote_summary_json['quoteSummary']['result'][0][module]

    @_async_log_func
    async def get_asset_profile(self) -> AssetProfile:
        """Get asset profile for the ticker.

        Returns: Quote summary with asset profile module response result json.
        """
        return await self._get_quote_summary_single_module('assetProfile')

    @_async_log_func
    async def get_summary_profile(self) -> SummaryProfile:
        """Get summary profile for the ticker.

        Returns: Quote summary with summary profile module response result json.
        """
        return await self._get_quote_summary_single_module('summaryProfile')

    @_async_log_func
    async def get_summary_detail(self) -> SummaryDetail:
        """Get summary detail for the ticker.

        Returns: Quote summary with summary detail module response result json.
        """
        return await self._get_quote_summary_single_module('summaryDetail')

    @_async_log_func
    async def get_price(self) -> Price:
        """Get price data for the ticker.

        Returns: Quote summary with price data module response result json.
        """
        return await self._get_quote_summary_single_module('price')

    @_async_log_func
    async def get_default_key_statistics(self) -> DefaultKeyStatistics:
        """Get default key statistics for the ticker.

        Returns: Quote summary with default key statistics module response result json.
        """
        return await self._get_quote_summary_single_module('defaultKeyStatistics')

    @_async_log_func
    async def get_financial_data(self) -> FinancialData:
        """Get financial data for the ticker.

        Returns: Quote summary with financial data module response result json.
        """
        return await self._get_quote_summary_single_module('financialData')

    @_async_log_func
    async def get_calendar_events(self) -> CalendarEvents:
        """Get calendar events for the ticker.

        Returns: Quote summary with calendar events module response result json.
        """
        return await self._get_quote_summary_single_module('calendarEvents')

    @_async_log_func
    async def get_sec_filings(self) -> SecFilings:
        """Get sec filings for the ticker.

        Returns: Quote summary with sec filings module response result json.
        """
        return await self._get_quote_summary_single_module('secFilings')

    @_async_log_func
    async def get_upgrade_downgrade_history(self) -> list[UpgradeDowngradeHistoryItem]:
        """Get upgrade downgrade history for the ticker.

        Returns:
            Quote summary with upgrade downgrade history module response results
                json.
        """
        result = await self._get_quote_summary_single_module('upgradeDowngradeHistory')
        return result['history']

    @_async_log_func
    async def get_institution_ownership(self) -> list[InstitutionOwnershipItem]:
        """Get institution ownership for the ticker.

        Returns: Quote summary with institution ownership module response results json.
        """
        result = await self._get_quote_summary_single_module('institutionOwnership')
        return result['ownershipList']

    @_async_log_func
    async def get_fund_ownership(self) -> list[FundOwnershipItem]:
        """Get fund ownership for the ticker.

        Returns: Quote summary with fund ownership module response results json.
        """
        result = await self._get_quote_summary_single_module('fundOwnership')
        return result['ownershipList']

    @_async_log_func
    async def get_major_direct_holders(self) -> MajorDirectHolders:
        """Get major direct holders for the ticker.

        Returns: Quote summary with direct holders module response result json.
        """
        return await self._get_quote_summary_single_module('majorDirectHolders')

    @_async_log_func
    async def get_major_holders_breakdown(self) -> MajorHoldersBreakdown:
        """Get major holders breakdown for the ticker.

        Returns: Quote summary with holders breakdown module response result json.
        """
        return await self._get_quote_summary_single_module('majorHoldersBreakdown')

    @_async_log_func
    async def get_insider_transactions(self) -> list[InsiderTransactionItem]:
        """Get insider transactions for the ticker.

        Returns: Quote summary with insider transactions module response results json.
        """
        result = await self._get_quote_summary_single_module('insiderTransactions')
        return result['transactions']

    @_async_log_func
    async def get_insider_holders(self) -> list[InsiderHolderItem]:
        """Get insider holders for the ticker.

        Returns: Quote summary with insider holders module response results json.
        """
        result = await self._get_quote_summary_single_module('insiderHolders')
        return result['holders']

    @_async_log_func
    async def get_net_share_purchase_activity(self) -> NetSharePurchaseActivity:
        """Get net share purchase activity for the ticker.

        Returns:
            Quote summary with net share purchase activity module response result
                json.
        """
        return await self._get_quote_summary_single_module('netSharePurchaseActivity')

    @_async_log_func
    async def get_earnings(self) -> Earnings:
        """Get earnings for the ticker.

        Returns: Quote summary with earnings module response result json.
        """
        return await self._get_quote_summary_single_module('earnings')

    @_async_log_func
    async def get_earnings_history(self) -> list[EarningsHistoryItem]:
        """Get earnings history for the ticker.

        Returns: Quote summary with earnings history module response results json.
        """
        result = await self._get_quote_summary_single_module('earningsHistory')
        return result['history']

    @_async_log_func
    async def get_earnings_trend(self) -> list[EarningsTrendItem]:
        """Get earnings trend for the ticker.

        Returns: Quote summary with earnings trend module response results json.
        """
        result = await self._get_quote_summary_single_module('earningsTrend')
        return result['trend']

    @_async_log_func
    async def get_industry_trend(self) -> IndustryTrend:
        """Get industry trend for the ticker.

        Returns: Quote summary with industry trend module response result json.
        """
        return await self._get_quote_summary_single_module('industryTrend')

    @_async_log_func
    async def get_index_trend(self) -> IndexTrend:
        """Get index trend for the ticker.

        Returns: Quote summary with index trend module response result json.
        """
        return await self._get_quote_summary_single_module('indexTrend')

    @_async_log_func
    async def get_sector_trend(self) -> SectorTrend:
        """Get sector trend for the ticker.

        Returns: Quote summary with sector trend module response result json.
        """
        return await self._get_quote_summary_single_module('sectorTrend')

    @_async_log_func
    async def get_recommendation_trend(self) -> list[RecommendationTrendItem]:
        """Get recommendation trend for the ticker.

        Returns: Quote summary with recommendation trend module response results json.
        """
        result = await self._get_quote_summary_single_module('recommendationTrend')
        return result['trend']

    @_async_log_func
    async def get_page_views(self) -> PageViews:
        """Get page views for the ticker.

        Returns: Quote summary with page views module response result json.
        """
        return await self._get_quote_summary_single_module('pageViews')

    @_async_log_func
    async def _get_financials(
        self,
        frequency: str,
        typ: str,
        period1: int | float | None = None,
        period2: int | float | None = None,
    ) -> list[TimeseriesResult]:
        await self._get_client()
        types = get_types_with_frequency(typ, frequency)
        timeseries_json = await self._client.get_timeseries(
            self.ticker, types, period1, period2
        )
        return timeseries_json['timeseries']['result']

    @_async_log_func
    async def get_income_statement(
        self,
        frequency: str,
        period1: int | float | None = None,
        period2: int | float | None = None,
    ) -> list[TimeseriesResult]:
        """Get income statement for the ticker.

        Args:
            frequency: annual, quarterly or trailing.
            period1:
                Start timestamp in seconds. (optional, default: 1st Jan 2020 timestamp)
            period2: End timestamp in seconds. (optional, default: now timestamp)

        Returns: Income statement response results json.
        """
        return await self._get_financials(
            frequency, 'income_statement', period1, period2
        )

    @_async_log_func
    async def get_balance_sheet(
        self,
        frequency: str,
        period1: int | float | None = None,
        period2: int | float | None = None,
    ) -> list[TimeseriesResult]:
        """Get balance sheet for the ticker.

        Args:
            frequency: annual, quarterly or trailing.
            period1:
                Start timestamp in seconds. (optional, default: 1st Jan 2020 timestamp)
            period2: End timestamp in seconds. (optional, default: now timestamp)

        Returns: Balance sheet response results json.
        """
        return await self._get_financials(frequency, 'balance_sheet', period1, period2)

    @_async_log_func
    async def get_cash_flow(
        self,
        frequency: str,
        period1: int | float | None = None,
        period2: int | float | None = None,
    ) -> list[TimeseriesResult]:
        """Get cash flow statement for the ticker.

        Args:
            frequency: annual, quarterly or trailing.
            period1:
                Start timestamp in seconds. (optional, default: 1st Jan 2020 timestamp)
            period2: End timestamp in seconds. (optional, default: now timestamp)

        Returns: Cash flow response results json.
        """
        return await self._get_financials(frequency, 'cash_flow', period1, period2)

    @_async_log_func
    async def get_options(self) -> OptionChainResult:
        """Get options data for the ticker.

        Returns: Options response result json.
        """
        await self._get_client()
        options_json = await self._client.get_options(self.ticker)
        return options_json['optionChain']['result'][0]

    @_async_log_func
    async def get_search(self) -> SearchResult:
        """Get search results for the ticker.

        Returns: Search result json.
        """
        await self._get_client()
        return await self._client.get_search(self.ticker)

    @_async_log_func
    async def get_recommendations(self) -> RecommendationsFinanceResult:
        """Get analyst recommendations for the ticker.

        Returns: Recommendations response result json.
        """
        await self._get_client()
        recommendations_json = await self._client.get_recommendations(self.ticker)
        return recommendations_json['finance']['result'][0]

    @_async_log_func
    async def get_insights(self) -> InsightsFinanceResult:
        """Get insights for the ticker.

        Returns: Insights response result json.
        """
        await self._get_client()
        insights_json = await self._client.get_insights(self.ticker)
        return insights_json['finance']['result'][0]

    @_async_log_func
    async def get_ratings(self) -> RatingsResult:
        """Get ratings for the ticker.

        Returns: Ratings result json.
        """
        await self._get_client()
        return await self._client.get_ratings(self.ticker)
