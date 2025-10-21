import asyncio
import json
import logging
import pathlib
from datetime import datetime
from typing import Any

from logging_config import setup_logging

from yafin import AsyncClient
from yafin.const import ALL_MODULES_CSV
from yafin.utils import get_types_with_frequency

logger = logging.getLogger(__name__)

ROOT_PATH = pathlib.Path(__file__).resolve().parent.parent
FIXTURE_PATH = ROOT_PATH.joinpath('tests').joinpath('unit').joinpath('fixtures')
TICKER = 'META'
PERIOD1 = datetime(2020, 1, 1).timestamp()
PERIOD2 = datetime.now().timestamp()


def get_fixture_path(file_name: str) -> str:
    """Get the path to a fixture file."""
    return str(FIXTURE_PATH.joinpath(f'{file_name}.json'))


def write_json(data: dict[str, Any], file_path: str) -> None:
    """Write data to a JSON file."""
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=2)


async def process_mock(
    instance: Any,
    method_name: str,
    kwargs: dict[str, Any] | None = None,
    file_name: str | None = None,
) -> None:
    """Do all steps necessary for storing the mock as a JSON file."""
    method = getattr(instance, method_name)
    data = await method(**kwargs) if kwargs else await method()
    data_path = (
        get_fixture_path(file_name) if file_name else get_fixture_path(method_name)
    )
    write_json(data, data_path)
    logger.debug(f'{method_name.capitalize()} data fetched and stored {data_path}.')


async def main() -> None:  # noqa: D103
    setup_logging()

    params = dict(ticker=TICKER, period1=PERIOD1, period2=PERIOD2)
    params_path = get_fixture_path('params')
    write_json(params, params_path)
    logger.debug(f'Params and stored {params_path}.')

    async with AsyncClient() as client:
        await process_mock(
            instance=client,
            method_name='get_chart',
            kwargs=dict(ticker=TICKER, period_range='1y', interval='1d'),
            file_name='chart',
        )
        await process_mock(
            instance=client,
            method_name='get_quote',
            kwargs=dict(tickers='META'),
            file_name='quotes',
        )
        await process_mock(
            instance=client,
            method_name='get_quote_summary',
            kwargs=dict(ticker=TICKER, modules=ALL_MODULES_CSV),
            file_name='qs_all_modules',
        )
        await process_mock(
            instance=client,
            method_name='get_quote_summary',
            kwargs=dict(ticker=TICKER, modules='quoteType'),
            file_name='qs_quote_type',
        )
        await process_mock(
            instance=client,
            method_name='get_quote_summary',
            kwargs=dict(ticker=TICKER, modules='assetProfile'),
            file_name='qs_asset_profile',
        )
        await process_mock(
            instance=client,
            method_name='get_quote_summary',
            kwargs=dict(ticker=TICKER, modules='summaryProfile'),
            file_name='qs_summary_profile',
        )
        await process_mock(
            instance=client,
            method_name='get_quote_summary',
            kwargs=dict(ticker=TICKER, modules='summaryDetail'),
            file_name='qs_summary_detail',
        )
        await process_mock(
            instance=client,
            method_name='get_quote_summary',
            kwargs=dict(ticker=TICKER, modules='incomeStatementHistory'),
            file_name='qs_income_statement_history',
        )
        await process_mock(
            instance=client,
            method_name='get_quote_summary',
            kwargs=dict(ticker=TICKER, modules='incomeStatementHistoryQuarterly'),
            file_name='qs_income_statement_history_quarterly',
        )
        await process_mock(
            instance=client,
            method_name='get_quote_summary',
            kwargs=dict(ticker=TICKER, modules='balanceSheetHistory'),
            file_name='qs_balance_sheet_history',
        )
        await process_mock(
            instance=client,
            method_name='get_quote_summary',
            kwargs=dict(ticker=TICKER, modules='balanceSheetHistoryQuarterly'),
            file_name='qs_balance_sheet_history_quarterly',
        )
        await process_mock(
            instance=client,
            method_name='get_quote_summary',
            kwargs=dict(ticker=TICKER, modules='cashflowStatementHistory'),
            file_name='qs_cashflow_statement_history',
        )
        await process_mock(
            instance=client,
            method_name='get_quote_summary',
            kwargs=dict(ticker=TICKER, modules='cashflowStatementHistoryQuarterly'),
            file_name='qs_cashflow_statement_history_quarterly',
        )
        await process_mock(
            instance=client,
            method_name='get_quote_summary',
            kwargs=dict(ticker=TICKER, modules='esgScores'),
            file_name='qs_esg_scores',
        )
        await process_mock(
            instance=client,
            method_name='get_quote_summary',
            kwargs=dict(ticker=TICKER, modules='price'),
            file_name='qs_price',
        )
        await process_mock(
            instance=client,
            method_name='get_quote_summary',
            kwargs=dict(ticker=TICKER, modules='defaultKeyStatistics'),
            file_name='qs_default_key_statistics',
        )
        await process_mock(
            instance=client,
            method_name='get_quote_summary',
            kwargs=dict(ticker=TICKER, modules='financialData'),
            file_name='qs_financial_data',
        )
        await process_mock(
            instance=client,
            method_name='get_quote_summary',
            kwargs=dict(ticker=TICKER, modules='calendarEvents'),
            file_name='qs_calendar_events',
        )
        await process_mock(
            instance=client,
            method_name='get_quote_summary',
            kwargs=dict(ticker=TICKER, modules='secFilings'),
            file_name='qs_sec_filings',
        )
        await process_mock(
            instance=client,
            method_name='get_quote_summary',
            kwargs=dict(ticker=TICKER, modules='upgradeDowngradeHistory'),
            file_name='qs_upgrade_downgrade_history',
        )
        await process_mock(
            instance=client,
            method_name='get_quote_summary',
            kwargs=dict(ticker=TICKER, modules='institutionOwnership'),
            file_name='qs_institution_ownership',
        )
        await process_mock(
            instance=client,
            method_name='get_quote_summary',
            kwargs=dict(ticker=TICKER, modules='fundOwnership'),
            file_name='qs_fund_ownership',
        )
        await process_mock(
            instance=client,
            method_name='get_quote_summary',
            kwargs=dict(ticker=TICKER, modules='majorDirectHolders'),
            file_name='qs_major_direct_holders',
        )
        await process_mock(
            instance=client,
            method_name='get_quote_summary',
            kwargs=dict(ticker=TICKER, modules='majorHoldersBreakdown'),
            file_name='qs_major_holders_breakdown',
        )
        await process_mock(
            instance=client,
            method_name='get_quote_summary',
            kwargs=dict(ticker=TICKER, modules='insiderTransactions'),
            file_name='qs_insider_transactions',
        )
        await process_mock(
            instance=client,
            method_name='get_quote_summary',
            kwargs=dict(ticker=TICKER, modules='insiderHolders'),
            file_name='qs_insider_holders',
        )
        await process_mock(
            instance=client,
            method_name='get_quote_summary',
            kwargs=dict(ticker=TICKER, modules='netSharePurchaseActivity'),
            file_name='qs_net_share_purchase_activity',
        )
        await process_mock(
            instance=client,
            method_name='get_quote_summary',
            kwargs=dict(ticker=TICKER, modules='earnings'),
            file_name='qs_earnings',
        )
        await process_mock(
            instance=client,
            method_name='get_quote_summary',
            kwargs=dict(ticker=TICKER, modules='earningsHistory'),
            file_name='qs_earnings_history',
        )
        await process_mock(
            instance=client,
            method_name='get_quote_summary',
            kwargs=dict(ticker=TICKER, modules='earningsTrend'),
            file_name='qs_earnings_trend',
        )
        await process_mock(
            instance=client,
            method_name='get_quote_summary',
            kwargs=dict(ticker=TICKER, modules='industryTrend'),
            file_name='qs_industry_trend',
        )
        await process_mock(
            instance=client,
            method_name='get_quote_summary',
            kwargs=dict(ticker=TICKER, modules='indexTrend'),
            file_name='qs_index_trend',
        )
        await process_mock(
            instance=client,
            method_name='get_quote_summary',
            kwargs=dict(ticker=TICKER, modules='sectorTrend'),
            file_name='qs_sector_trend',
        )
        await process_mock(
            instance=client,
            method_name='get_quote_summary',
            kwargs=dict(ticker=TICKER, modules='recommendationTrend'),
            file_name='qs_recommendation_trend',
        )
        await process_mock(
            instance=client,
            method_name='get_quote_summary',
            kwargs=dict(ticker=TICKER, modules='pageViews'),
            file_name='qs_page_views',
        )
        await process_mock(
            instance=client,
            method_name='get_timeseries',
            kwargs=dict(
                ticker=TICKER,
                types=get_types_with_frequency(
                    frequency='annual', typ='income_statement'
                ),
                period1=PERIOD1,
                period2=PERIOD2,
            ),
            file_name='ts_income_statement',
        )
        await process_mock(
            instance=client,
            method_name='get_timeseries',
            kwargs=dict(
                ticker=TICKER,
                types=get_types_with_frequency(frequency='annual', typ='balance_sheet'),
                period1=PERIOD1,
                period2=PERIOD2,
            ),
            file_name='ts_balance_sheet',
        )
        await process_mock(
            instance=client,
            method_name='get_timeseries',
            kwargs=dict(
                ticker=TICKER,
                types=get_types_with_frequency(frequency='annual', typ='cash_flow'),
                period1=PERIOD1,
                period2=PERIOD2,
            ),
            file_name='ts_cash_flow',
        )
        await process_mock(
            instance=client,
            method_name='get_options',
            kwargs=dict(ticker=TICKER),
            file_name='options',
        )
        await process_mock(
            instance=client,
            method_name='get_search',
            kwargs=dict(tickers='META'),
            file_name='search',
        )
        await process_mock(
            instance=client,
            method_name='get_recommendations',
            kwargs=dict(ticker=TICKER),
            file_name='recommendations',
        )
        await process_mock(
            instance=client,
            method_name='get_insights',
            kwargs=dict(ticker=TICKER),
            file_name='insights',
        )
        await process_mock(
            instance=client,
            method_name='get_market_summaries',
            file_name='market_summaries',
        )
        await process_mock(
            instance=client, method_name='get_trending', file_name='trending'
        )
        await process_mock(
            instance=client, method_name='get_currencies', file_name='currencies'
        )


if __name__ == '__main__':
    asyncio.run(main())
