import logging
from types import TracebackType
from typing import Any, Self, Type

from typeguard import typechecked

from .client import AsyncClient
from .const import ALL_MODULES_CSV
from .utils import _log_args, get_types_with_frequency

logger = logging.getLogger(__name__)

type Result = dict[str, Any]
type ResultList = list[Result]


class _ClientManager:
    """Manages a client singleton for all symbols."""

    _client: AsyncClient | None = None
    _refcount = 0

    @classmethod
    def get_client(cls) -> AsyncClient:
        """Create client singleton if not exists."""
        if cls._client is None:
            cls._client = AsyncClient()

        cls._refcount += 1

        return cls._client

    @classmethod
    async def release_client(cls) -> None:
        """Decrease refcount and close client singleton if no symbols left."""
        cls._refcount -= 1

        if cls._refcount <= 0 and cls._client:
            await cls._client.close()
            cls._client = None


class AsyncSymbol(object):
    """Symbol class for a specific ticker.

    Warning: HTTP resources closing
        Uses http resources, so do not forget to close them after use to avoid resource
            leakage or use context manager.

    Attributes:
        ticker: Ticker symbol.
        _client:
            client instance, that is used for all http requests.
                (Is lazily initialized.)
    """

    @typechecked
    def __init__(self, ticker: str) -> None:
        """Create new AsyncSymbol instance.

        Args:
            ticker: Ticker symbol.
        """
        self.ticker = ticker
        self._client: AsyncClient | None = None

    def _get_client(self) -> None:
        if self._client is None:
            self._client = _ClientManager.get_client()

    async def close(self) -> None:
        """Release the client if open for current symbol.

        Note:
            Only if no other symbols are using the client singleton, is the client
                closed.
        """
        if self._client:
            await _ClientManager.release_client()
            self._client = None

    async def __aenter__(self) -> Self:
        """When entering context manager, get the client."""
        self._get_client()
        return self

    async def __aexit__(
        self,
        exc_type: Type[BaseException] | None = None,
        exc_val: BaseException | None = None,
        exc_tb: TracebackType | None = None,
    ) -> None:
        """When closing context manager, release the client."""
        await self.close()

    @_log_args
    @typechecked
    async def get_chart(
        self,
        period_range: str,
        interval: str,
        include_div: bool = True,
        include_split: bool = True,
        include_earn: bool = True,
        include_capital_gain: bool = True,
    ) -> Result:
        """Get chart data for the ticker.

        Args:
            period_range: Range of the period.
            interval: Data interval.
            include_div: Whether to include dividends.
            include_split: Whether to include stock splits.
            include_earn: Whether to include earnings.
            include_capital_gain: Whether to include capital gains.

        Returns: Chart response result json.
        """
        events_list = []

        if include_div:
            events_list.append('div')

        if include_split:
            events_list.append('split')

        if include_earn:
            events_list.append('earn')

        if include_capital_gain:
            events_list.append('capitalGain')

        events = ','.join(events_list) if events_list else None

        self._get_client()
        chart_json = await self._client.get_chart(
            self.ticker, period_range, interval, events
        )
        return chart_json['chart']['result'][0]

    @_log_args
    async def get_quote(self) -> Result:
        """Get quote for the ticker.

        Returns: Quote response result json.
        """
        self._get_client()
        quote_json = await self._client.get_quote(self.ticker)
        # client.get_quote can be quiried with multiple tickers, e.g.: 'META,AAPL'
        # from Stonk class we are only querying one ticker
        return quote_json['quoteResponse']['result'][0]

    @_log_args
    async def get_quote_summary_all_modules(self) -> Result:
        """Get quote summary for all modules for the ticker.

        Returns: Quote summary with all modules response result json.
        """
        self._get_client()
        quote_summary_json = await self._client.get_quote_summary(
            self.ticker, ALL_MODULES_CSV
        )
        return quote_summary_json['quoteSummary']['result'][0]

    @_log_args
    @typechecked
    async def _get_quote_summary_single_module(self, module: str) -> Result:
        self._get_client()
        quote_summary_json = await self._client.get_quote_summary(self.ticker, module)
        return quote_summary_json['quoteSummary']['result'][0][module]

    @_log_args
    async def get_quote_type(self) -> Result:
        """Get quote type for the ticker.

        Returns: Quote summary with quote type module response result json.
        """
        return await self._get_quote_summary_single_module('quoteType')

    @_log_args
    async def get_asset_profile(self) -> Result:
        """Get asset profile for the ticker.

        Returns: Quote summary with asset profile module response result json.
        """
        return await self._get_quote_summary_single_module('assetProfile')

    @_log_args
    async def get_summary_profile(self) -> Result:
        """Get summary profile for the ticker.

        Returns: Quote summary with summary profile module response result json.
        """
        return await self._get_quote_summary_single_module('summaryProfile')

    @_log_args
    async def get_summary_detail(self) -> Result:
        """Get summary detail for the ticker.

        Returns: Quote summary with summary detail module response result json.
        """
        return await self._get_quote_summary_single_module('summaryDetail')

    @_log_args
    async def get_income_statement_history(self) -> ResultList:
        """Get income statement history for the ticker.

        Returns:
            Quote summary with income statement history module response results
                json.
        """
        result = await self._get_quote_summary_single_module('incomeStatementHistory')
        return result['incomeStatementHistory']

    @_log_args
    async def get_income_statement_history_quarterly(self) -> ResultList:
        """Get income statement history quarterly for the ticker.

        Returns:
            Quote summary with income statement history quarterly module response
                results json.
        """
        result = await self._get_quote_summary_single_module(
            'incomeStatementHistoryQuarterly'
        )
        return result['incomeStatementHistory']

    @_log_args
    async def get_balance_sheet_history(self) -> ResultList:
        """Get balance sheet history for the ticker.

        Returns: Quote summary with balance sheet history module response results json.
        """
        result = await self._get_quote_summary_single_module('balanceSheetHistory')
        return result['balanceSheetStatements']

    @_log_args
    async def get_balance_sheet_history_quarterly(self) -> ResultList:
        """Get balance sheet history quarterly for the ticker.

        Returns:
            Quote summary with balance sheet history quarterly module response
                results json.
        """
        result = await self._get_quote_summary_single_module(
            'balanceSheetHistoryQuarterly'
        )
        return result['balanceSheetStatements']

    @_log_args
    async def get_cashflow_statement_history(self) -> ResultList:
        """Get cashflow statement history for the ticker.

        Returns:
            Quote summary with cashflow statement history module response results
                json.
        """
        result = await self._get_quote_summary_single_module('cashflowStatementHistory')
        return result['cashflowStatements']

    @_log_args
    async def get_cashflow_statement_history_quarterly(self) -> ResultList:
        """Get cashflow statement history quarterly for the ticker.

        Returns:
            Quote summary with cashflow statement history quarterly module response
                results json.
        """
        result = await self._get_quote_summary_single_module(
            'cashflowStatementHistoryQuarterly'
        )
        return result['cashflowStatements']

    @_log_args
    async def get_esg_scores(self) -> Result:
        """Get esg scores for the ticker.

        Returns: Quote summary with esg scores module response result json.
        """
        return await self._get_quote_summary_single_module('esgScores')

    @_log_args
    async def get_price(self) -> Result:
        """Get price data for the ticker.

        Returns: Quote summary with price data module response result json.
        """
        return await self._get_quote_summary_single_module('price')

    @_log_args
    async def get_default_key_statistics(self) -> Result:
        """Get default key statistics for the ticker.

        Returns: Quote summary with default key statistics module response result json.
        """
        return await self._get_quote_summary_single_module('defaultKeyStatistics')

    @_log_args
    async def get_financial_data(self) -> Result:
        """Get financial data for the ticker.

        Returns: Quote summary with financial data module response result json.
        """
        return await self._get_quote_summary_single_module('financialData')

    @_log_args
    async def get_calendar_events(self) -> Result:
        """Get calendar events for the ticker.

        Returns: Quote summary with calendar events module response result json.
        """
        return await self._get_quote_summary_single_module('calendarEvents')

    @_log_args
    async def get_sec_filings(self) -> Result:
        """Get sec filings for the ticker.

        Returns: Quote summary with sec filings module response result json.
        """
        return await self._get_quote_summary_single_module('secFilings')

    @_log_args
    async def get_upgrade_downgrade_history(self) -> ResultList:
        """Get upgrade downgrade history for the ticker.

        Returns:
            Quote summary with upgrade downgrade history module response results
                json.
        """
        result = await self._get_quote_summary_single_module('upgradeDowngradeHistory')
        return result['history']

    @_log_args
    async def get_institution_ownership(self) -> ResultList:
        """Get institution ownership for the ticker.

        Returns: Quote summary with institution ownership module response results json.
        """
        result = await self._get_quote_summary_single_module('institutionOwnership')
        return result['ownershipList']

    @_log_args
    async def get_fund_ownership(self) -> ResultList:
        """Get fund ownership for the ticker.

        Returns: Quote summary with fund ownership module response results json.
        """
        result = await self._get_quote_summary_single_module('fundOwnership')
        return result['ownershipList']

    @_log_args
    async def get_major_direct_holders(self) -> Result:
        """Get major direct holders for the ticker.

        Returns: Quote summary with direct holders module response result json.
        """
        return await self._get_quote_summary_single_module('majorDirectHolders')

    @_log_args
    async def get_major_holders_breakdown(self) -> Result:
        """Get major holders breakdown for the ticker.

        Returns: Quote summary with holders breakdown module response result json.
        """
        return await self._get_quote_summary_single_module('majorHoldersBreakdown')

    @_log_args
    async def get_insider_transactions(self) -> ResultList:
        """Get insider transactions for the ticker.

        Returns: Quote summary with insider transactions module response results json.
        """
        result = await self._get_quote_summary_single_module('insiderTransactions')
        return result['transactions']

    @_log_args
    async def get_insider_holders(self) -> ResultList:
        """Get insider holders for the ticker.

        Returns: Quote summary with insider holders module response results json.
        """
        result = await self._get_quote_summary_single_module('insiderHolders')
        return result['holders']

    @_log_args
    async def get_net_share_purchase_activity(self) -> Result:
        """Get net share purchase activity for the ticker.

        Returns:
            Quote summary with net share purchase activity module response result
                json.
        """
        return await self._get_quote_summary_single_module('netSharePurchaseActivity')

    @_log_args
    async def get_earnings(self) -> Result:
        """Get earnings for the ticker.

        Returns: Quote summary with earnings module response result json.
        """
        return await self._get_quote_summary_single_module('earnings')

    @_log_args
    async def get_earnings_history(self) -> ResultList:
        """Get earnings history for the ticker.

        Returns: Quote summary with earnings history module response results json.
        """
        result = await self._get_quote_summary_single_module('earningsHistory')
        return result['history']

    @_log_args
    async def get_earnings_trend(self) -> ResultList:
        """Get earnings trend for the ticker.

        Returns: Quote summary with earnings trend module response results json.
        """
        result = await self._get_quote_summary_single_module('earningsTrend')
        return result['trend']

    @_log_args
    async def get_industry_trend(self) -> Result:
        """Get industry trend for the ticker.

        Returns: Quote summary with industry trend module response result json.
        """
        return await self._get_quote_summary_single_module('industryTrend')

    @_log_args
    async def get_index_trend(self) -> Result:
        """Get index trend for the ticker.

        Returns: Quote summary with index trend module response result json.
        """
        return await self._get_quote_summary_single_module('indexTrend')

    @_log_args
    async def get_sector_trend(self) -> Result:
        """Get sector trend for the ticker.

        Returns: Quote summary with sector trend module response result json.
        """
        return await self._get_quote_summary_single_module('sectorTrend')

    @_log_args
    async def get_recommendation_trend(self) -> ResultList:
        """Get recommendation trend for the ticker.

        Returns: Quote summary with recommendation trend module response results json.
        """
        result = await self._get_quote_summary_single_module('recommendationTrend')
        return result['trend']

    @_log_args
    async def get_page_views(self) -> Result:
        """Get page views for the ticker.

        Returns: Quote summary with page views module response result json.
        """
        return await self._get_quote_summary_single_module('pageViews')

    @_log_args
    @typechecked
    async def _get_financials(
        self,
        frequency: str,
        typ: str,
        period1: int | float | None = None,
        period2: int | float | None = None,
    ) -> ResultList:
        self._get_client()
        types = get_types_with_frequency(frequency, typ)
        timeseries_json = await self._client.get_timeseries(
            self.ticker, types, period1, period2
        )
        return timeseries_json['timeseries']['result']

    @_log_args
    @typechecked
    async def get_income_statement(
        self,
        frequency: str,
        period1: int | float | None = None,
        period2: int | float | None = None,
    ) -> ResultList:
        """Get income statement for the ticker.

        Args:
            frequency: annual, quarterly or trailing.
            period1: Start timestamp.
            period2: End timestamp.

        Returns: Income statement response results json.
        """
        return await self._get_financials(
            frequency, 'income_statement', period1, period2
        )

    @_log_args
    @typechecked
    async def get_balance_sheet(
        self,
        frequency: str,
        period1: int | float | None = None,
        period2: int | float | None = None,
    ) -> ResultList:
        """Get balance sheet for the ticker.

        Args:
            frequency: annual, quarterly or trailing.
            period1: Start timestamp.
            period2: End timestamp.

        Returns: Balance sheet response results json.
        """
        return await self._get_financials(frequency, 'balance_sheet', period1, period2)

    @_log_args
    @typechecked
    async def get_cash_flow(
        self,
        frequency: str,
        period1: int | float | None = None,
        period2: int | float | None = None,
    ) -> ResultList:
        """Get cash flow statement for the ticker.

        Args:
            frequency: annual, quarterly or trailing.
            period1: Start timestamp.
            period2: End timestamp.

        Returns: Cash flow response results json.
        """
        return await self._get_financials(frequency, 'cash_flow', period1, period2)

    @_log_args
    async def get_options(self) -> Result:
        """Get options data for the ticker.

        Returns: Options response result json.
        """
        self._get_client()
        options_json = await self._client.get_options(self.ticker)
        return options_json['optionChain']['result'][0]

    @_log_args
    async def get_search(self) -> Result:
        """Get search results for the ticker.

        Returns: Search response result json.
        """
        self._get_client()
        return await self._client.get_search(self.ticker)

    @_log_args
    async def get_recommendations(self) -> Result:
        """Get analyst recommendations for the ticker.

        Returns: Recommendations response result json.
        """
        self._get_client()
        recommendations_json = await self._client.get_recommendations(self.ticker)
        return recommendations_json['finance']['result'][0]

    @_log_args
    async def get_insights(self) -> Result:
        """Get insights for the ticker.

        Returns: Insights response result json.
        """
        self._get_client()
        insights_json = await self._client.get_insights(self.ticker)
        return insights_json['finance']['result']
