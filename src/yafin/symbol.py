import logging
from types import TracebackType
from typing import Any, Type

from typeguard import typechecked

from .client import AsyncClient
from .const import ALL_MODULES_CSV
from .utils import get_types_with_frequency, log_args

logger = logging.getLogger(__name__)


class _ClientManager:
    """Internal singleton-like shared client manager for AsyncClient."""

    _open_client: AsyncClient | None = None
    _refcount = 0

    @classmethod
    def get_client(cls) -> AsyncClient:
        """Create shared client if not exists."""
        if cls._open_client is None:
            cls._open_client = AsyncClient()

        cls._refcount += 1

        return cls._open_client

    @classmethod
    async def release_client(cls) -> None:
        """Decrease refcount and close share client if no symbols left."""
        cls._refcount -= 1

        if cls._refcount <= 0 and cls._open_client:
            await cls._open_client.close()
            cls._open_client = None


class AsyncSymbol(object):
    """Symbol class for a specific ticker."""

    @typechecked
    def __init__(self, ticker: str) -> None:
        self.ticker = ticker
        self._open_client: AsyncClient | None = None

    @property
    def client(self) -> AsyncClient:
        """Client attribute for API requests."""
        return self._get_client()

    def _get_client(self) -> AsyncClient:
        """Create client if not exists."""
        if self._open_client is None:
            self._open_client = _ClientManager.get_client()

        return self._open_client

    async def close(self) -> None:
        """Close the client if open."""
        if self._open_client:
            await _ClientManager.release_client()
            self._open_client = None

    async def __aenter__(self) -> 'AsyncSymbol':
        """When entering context manager, create the client."""
        self._get_client()
        return self

    async def __aexit__(
        self,
        exc_type: Type[BaseException] | None = None,
        exc_val: BaseException | None = None,
        exc_tb: TracebackType | None = None,
    ) -> None:
        """When closing context manager, close the client."""
        await self.close()

    @log_args
    @typechecked
    async def get_chart(
        self,
        period_range: str,
        interval: str,
        include_div: bool = True,
        include_split: bool = True,
    ) -> dict[str, Any]:
        """Get chart data for the ticker.

        Args:
            period_range: Range of the period
            interval: Data interval
            include_div: Whether to include dividends
            include_split: Whether to include stock splits

        Returns: Chart data as a dictionary.
        """
        events_list = []

        if include_div:
            events_list.append('div')

        if include_split:
            events_list.append('split')

        events = ','.join(events_list) if events_list else None

        chart_json = await self.client.get_chart(
            self.ticker, period_range, interval, events
        )
        return chart_json['chart']['result'][0]

    @log_args
    async def get_quote(self) -> dict[str, Any]:
        """Get quote for the ticker."""
        quote_json = await self.client.get_quote(self.ticker)
        # client.get_quote can be quiried with multiple tickers, e.g.: 'META,AAPL'
        # from Stonk class we are only querying one ticker
        return quote_json['quoteResponse']['result'][0]

    @log_args
    async def get_quote_summary_all_modules(self) -> dict[str, Any]:
        """Get quote summary for all modules for the ticker."""
        quote_summary_json = await self.client.get_quote_summary(
            self.ticker, ALL_MODULES_CSV
        )
        return quote_summary_json['quoteSummary']['result'][0]

    @log_args
    async def _get_quote_summary_single_module(self, module: str) -> dict[str, Any]:
        quote_summary_json = await self.client.get_quote_summary(self.ticker, module)
        return quote_summary_json['quoteSummary']['result'][0][module]

    @log_args
    async def get_quote_type(self) -> dict[str, Any]:
        """Get quote type for the ticker."""
        return await self._get_quote_summary_single_module('quoteType')

    @log_args
    async def get_asset_profile(self) -> dict[str, Any]:
        """Get asset profile for the ticker."""
        return await self._get_quote_summary_single_module('assetProfile')

    @log_args
    async def get_summary_profile(self) -> dict[str, Any]:
        """Get summary profile for the ticker."""
        return await self._get_quote_summary_single_module('summaryProfile')

    @log_args
    async def get_summary_detail(self) -> dict[str, Any]:
        """Get summary detail for the ticker."""
        return await self._get_quote_summary_single_module('summaryDetail')

    @log_args
    async def get_income_statement_history(self) -> list[dict[str, Any]]:
        """Get income statement history for the ticker."""
        result = await self._get_quote_summary_single_module('incomeStatementHistory')
        return result['incomeStatementHistory']

    @log_args
    async def get_income_statement_history_quarterly(self) -> list[dict[str, Any]]:
        """Get income statement history quarterly for the ticker."""
        result = await self._get_quote_summary_single_module(
            'incomeStatementHistoryQuarterly'
        )
        return result['incomeStatementHistory']

    @log_args
    async def get_balance_sheet_history(self) -> list[dict[str, Any]]:
        """Get balance sheet history for the ticker."""
        result = await self._get_quote_summary_single_module('balanceSheetHistory')
        return result['balanceSheetStatements']

    @log_args
    async def get_balance_sheet_history_quarterly(self) -> list[dict[str, Any]]:
        """Get balance sheet history quarterly for the ticker."""
        result = await self._get_quote_summary_single_module(
            'balanceSheetHistoryQuarterly'
        )
        return result['balanceSheetStatements']

    @log_args
    async def get_cashflow_statement_history(self) -> list[dict[str, Any]]:
        """Get cashflow statement history for the ticker."""
        result = await self._get_quote_summary_single_module('cashflowStatementHistory')
        return result['cashflowStatements']

    @log_args
    async def get_cashflow_statement_history_quarterly(self) -> list[dict[str, Any]]:
        """Get cashflow statement history quarterly for the ticker."""
        result = await self._get_quote_summary_single_module(
            'cashflowStatementHistoryQuarterly'
        )
        return result['cashflowStatements']

    @log_args
    async def get_esg_scores(self) -> dict[str, Any]:
        """Get esg scores for the ticker."""
        return await self._get_quote_summary_single_module('esgScores')

    @log_args
    async def get_price(self) -> dict[str, Any]:
        """Get price data for the ticker."""
        return await self._get_quote_summary_single_module('price')

    @log_args
    async def get_default_key_statistics(self) -> dict[str, Any]:
        """Get default key statistics for the ticker."""
        return await self._get_quote_summary_single_module('defaultKeyStatistics')

    @log_args
    async def get_financial_data(self) -> dict[str, Any]:
        """Get financial data for the ticker."""
        return await self._get_quote_summary_single_module('financialData')

    @log_args
    async def get_calendar_events(self) -> dict[str, Any]:
        """Get calendar events for the ticker."""
        return await self._get_quote_summary_single_module('calendarEvents')

    @log_args
    async def get_sec_filings(self) -> dict[str, Any]:
        """Get sec filings for the ticker."""
        return await self._get_quote_summary_single_module('secFilings')

    @log_args
    async def get_upgrade_downgrade_history(self) -> list[dict[str, Any]]:
        """Get upgrade downgrade history for the ticker."""
        result = await self._get_quote_summary_single_module('upgradeDowngradeHistory')
        return result['history']

    @log_args
    async def get_institution_ownership(self) -> list[dict[str, Any]]:
        """Get institution ownership for the ticker."""
        result = await self._get_quote_summary_single_module('institutionOwnership')
        return result['ownershipList']

    @log_args
    async def get_fund_ownership(self) -> list[dict[str, Any]]:
        """Get fund ownership for the ticker."""
        result = await self._get_quote_summary_single_module('fundOwnership')
        return result['ownershipList']

    @log_args
    async def get_major_direct_holders(self) -> dict[str, Any]:
        """Get major direct holders for the ticker."""
        return await self._get_quote_summary_single_module('majorDirectHolders')

    @log_args
    async def get_major_holders_breakdown(self) -> dict[str, Any]:
        """Get major holders breakdown for the ticker."""
        return await self._get_quote_summary_single_module('majorHoldersBreakdown')

    @log_args
    async def get_insider_transactions(self) -> list[dict[str, Any]]:
        """Get insider transactions for the ticker."""
        result = await self._get_quote_summary_single_module('insiderTransactions')
        return result['transactions']

    @log_args
    async def get_insider_holders(self) -> list[dict[str, Any]]:
        """Get insider holders for the ticker."""
        result = await self._get_quote_summary_single_module('insiderHolders')
        return result['holders']

    @log_args
    async def get_net_share_purchase_activity(self) -> dict[str, Any]:
        """Get net share purchase activity for the ticker."""
        return await self._get_quote_summary_single_module('netSharePurchaseActivity')

    @log_args
    async def get_earnings(self) -> dict[str, Any]:
        """Get earnings for the ticker."""
        return await self._get_quote_summary_single_module('earnings')

    @log_args
    async def get_earnings_history(self) -> list[dict[str, Any]]:
        """Get earnings history for the ticker."""
        result = await self._get_quote_summary_single_module('earningsHistory')
        return result['history']

    @log_args
    async def get_earnings_trend(self) -> list[dict[str, Any]]:
        """Get earnings trend for the ticker."""
        result = await self._get_quote_summary_single_module('earningsTrend')
        return result['trend']

    @log_args
    async def get_industry_trend(self) -> dict[str, Any]:
        """Get industry trend for the ticker."""
        return await self._get_quote_summary_single_module('industryTrend')

    @log_args
    async def get_index_trend(self) -> dict[str, Any]:
        """Get index trend for the ticker."""
        return await self._get_quote_summary_single_module('indexTrend')

    @log_args
    async def get_sector_trend(self) -> dict[str, Any]:
        """Get sector trend for the ticker."""
        return await self._get_quote_summary_single_module('sectorTrend')

    @log_args
    async def get_recommendation_trend(self) -> list[dict[str, Any]]:
        """Get recommendation trend for the ticker."""
        result = await self._get_quote_summary_single_module('recommendationTrend')
        return result['trend']

    @log_args
    async def get_page_views(self) -> dict[str, Any]:
        """Get page views for the ticker."""
        return await self._get_quote_summary_single_module('pageViews')

    @log_args
    async def _get_financials(
        self,
        frequency: str,
        typ: str,
        period1: int | float | None = None,
        period2: int | float | None = None,
    ) -> list[dict[str, Any]]:
        types = get_types_with_frequency(frequency, typ)
        timeseries_json = await self.client.get_timeseries(
            self.ticker, types, period1, period2
        )
        return timeseries_json['timeseries']['result']

    @log_args
    @typechecked
    async def get_income_statement(
        self,
        frequency: str,
        period1: int | float | None = None,
        period2: int | float | None = None,
    ) -> list[dict[str, Any]]:
        """Get income statement financials for the ticker.

        Args:
            frequency: annual, quarterly or trailing.
            period1: Start timestamp (optional).
            period2: End timestamp (optional).

        Returns: Income statement financials as a dictionary.
        """
        return await self._get_financials(
            frequency, 'income_statement', period1, period2
        )

    @log_args
    @typechecked
    async def get_balance_sheet(
        self,
        frequency: str,
        period1: int | float | None = None,
        period2: int | float | None = None,
    ) -> list[dict[str, Any]]:
        """Get balance sheet financials for the ticker.

        Args:
            frequency: annual, quarterly or trailing.
            period1: Start timestamp (optional).
            period2: End timestamp (optional).

        Returns: Balance sheet financials as a dictionary.
        """
        return await self._get_financials(frequency, 'balance_sheet', period1, period2)

    @log_args
    @typechecked
    async def get_cash_flow(
        self,
        frequency: str,
        period1: int | float | None = None,
        period2: int | float | None = None,
    ) -> list[dict[str, Any]]:
        """Get cash flow financials for the ticker.

        Args:
            frequency: annual, quarterly or trailing.
            period1: Start timestamp (optional).
            period2: End timestamp (optional).

        Returns: Cash flow financials as a dictionary.
        """
        return await self._get_financials(frequency, 'cash_flow', period1, period2)

    @log_args
    async def get_options(self) -> dict[str, Any]:
        """Get options data for the ticker."""
        options_json = await self.client.get_options(self.ticker)
        return options_json['optionChain']['result'][0]

    @log_args
    async def get_search(self) -> dict[str, Any]:
        """Get search results for the ticker."""
        return await self.client.get_search(self.ticker)

    @log_args
    async def get_recommendations(self) -> dict[str, Any]:
        """Get analyst recommendations for the ticker."""
        recommendations_json = await self.client.get_recommendations(self.ticker)
        return recommendations_json['finance']['result'][0]

    @log_args
    async def get_insights(self) -> dict[str, Any]:
        """Get news insights for the ticker."""
        insights_json = await self.client.get_insights(self.ticker)
        return insights_json['finance']['result']
