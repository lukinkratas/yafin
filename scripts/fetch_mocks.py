import asyncio
import json
import logging
import pathlib
from datetime import datetime
from typing import Any

from tests._utils import _get_fixture_path, _process_chart_like_yfinance
from yafin import AsyncClient
from yafin.const import (
    ANNUAL_BALANCE_SHEET_TYPES,
    ANNUAL_CASH_FLOW_TYPES,
    ANNUAL_INCOME_STATEMENT_TYPES,
    CALENDAR_EVENT_MODULES,
    OTHER_TYPES,
    QUOTE_SUMMARY_MODULES,
)
from yafin.utils import _alog_func

from .logging_config import configure_logging

logger = logging.getLogger(__name__)

TICKERS = 'META,AAPL'
TICKERS_NAME = TICKERS.replace(',', '_').lower()
PERIOD1 = datetime(2020, 1, 1).timestamp()
PERIOD2 = datetime.now().timestamp()
INTERVAL = '1d'
PERIOD_RANGE = '1y'


def write_json(data: dict[str, Any], file_path: pathlib.Path) -> None:
    """Write data to a JSON file."""
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=2)


@_alog_func
async def process_mock(
    instance: Any,
    method_name: str,
    kwargs: dict[str, Any] | None = None,
    file_name: str | None = None,
    folder_name: str | None = None,
) -> dict[str, Any]:
    """Do all steps necessary for storing the mock as a JSON file."""
    method = getattr(instance, method_name)
    data = await method(**kwargs) if kwargs else await method()
    data_path = (
        _get_fixture_path(file_name, folder_name)
        if file_name
        else _get_fixture_path(method_name, folder_name)
    )
    write_json(data, data_path)
    logger.debug(f'{method_name} data fetched and stored {data_path}.')
    return data


async def main() -> None:  # noqa: D103
    configure_logging()

    params = dict(
        tickers=TICKERS,
        interval=INTERVAL,
        period_range=PERIOD_RANGE,
        period1=PERIOD1,
        period2=PERIOD2,
    )
    params_path = _get_fixture_path('params.json')
    write_json(params, params_path)
    logger.debug(f'Params and stored {params_path}.')

    async with AsyncClient() as client:
        await process_mock(
            instance=client,
            method_name='get_quote',
            kwargs=dict(tickers=TICKERS),
            file_name=f'{TICKERS_NAME}.json',
            folder_name='quote',
        )
        await process_mock(
            instance=client,
            method_name='get_quote_type',
            kwargs=dict(tickers=TICKERS),
            file_name=f'{TICKERS_NAME}.json',
            folder_name='quote_type',
        )
        await process_mock(
            instance=client,
            method_name='get_search',
            kwargs=dict(tickers=TICKERS),
            file_name=f'{TICKERS_NAME}.json',
            folder_name='search',
        )
        await process_mock(
            instance=client,
            method_name='get_recommendations',
            kwargs=dict(tickers=TICKERS),
            file_name=f'{TICKERS_NAME}.json',
            folder_name='recommendations',
        )
        await process_mock(
            instance=client,
            method_name='get_insights',
            kwargs=dict(tickers=TICKERS),
            file_name=f'{TICKERS_NAME}.json',
            folder_name='insights',
        )

        for ticker in TICKERS.split(','):
            chart = await process_mock(
                instance=client,
                method_name='get_chart',
                kwargs=dict(
                    ticker=ticker, interval=INTERVAL, period_range=PERIOD_RANGE
                ),
                file_name=f'{ticker.lower()}_{INTERVAL}_{PERIOD_RANGE}.json',
                folder_name='chart',
            )

            chart_df = _process_chart_like_yfinance(chart['chart']['result'][0])
            chart_path = _get_fixture_path(f'{ticker.lower()}.csv', 'performance')
            chart_df.to_csv(chart_path)

            await process_mock(
                instance=client,
                method_name='get_quote',
                kwargs=dict(tickers=ticker),
                file_name=f'{ticker.lower()}.json',
                folder_name='quote',
            )
            await process_mock(
                instance=client,
                method_name='get_quote_type',
                kwargs=dict(tickers=ticker),
                file_name=f'{ticker.lower()}.json',
                folder_name='quote_type',
            )
            await process_mock(
                instance=client,
                method_name='get_quote_summary',
                kwargs=dict(ticker=ticker, modules=QUOTE_SUMMARY_MODULES),
                file_name=f'all_modules_{ticker.lower()}.json',
                folder_name='quote_summary',
            )
            await process_mock(
                instance=client,
                method_name='get_quote_summary',
                kwargs=dict(ticker=ticker, modules='assetProfile'),
                file_name=f'asset_profile_{ticker.lower()}.json',
                folder_name='quote_summary',
            )
            await process_mock(
                instance=client,
                method_name='get_quote_summary',
                kwargs=dict(ticker=ticker, modules='summaryProfile'),
                file_name=f'summary_profile_{ticker.lower()}.json',
                folder_name='quote_summary',
            )
            await process_mock(
                instance=client,
                method_name='get_quote_summary',
                kwargs=dict(ticker=ticker, modules='summaryDetail'),
                file_name=f'summary_detail_{ticker.lower()}.json',
                folder_name='quote_summary',
            )
            await process_mock(
                instance=client,
                method_name='get_quote_summary',
                kwargs=dict(ticker=ticker, modules='price'),
                file_name=f'price_{ticker.lower()}.json',
                folder_name='quote_summary',
            )
            await process_mock(
                instance=client,
                method_name='get_quote_summary',
                kwargs=dict(ticker=ticker, modules='defaultKeyStatistics'),
                file_name=f'default_key_statistics_{ticker.lower()}.json',
                folder_name='quote_summary',
            )
            await process_mock(
                instance=client,
                method_name='get_quote_summary',
                kwargs=dict(ticker=ticker, modules='financialData'),
                file_name=f'financial_data_{ticker.lower()}.json',
                folder_name='quote_summary',
            )
            await process_mock(
                instance=client,
                method_name='get_quote_summary',
                kwargs=dict(ticker=ticker, modules='calendarEvents'),
                file_name=f'calendar_events_{ticker.lower()}.json',
                folder_name='quote_summary',
            )
            await process_mock(
                instance=client,
                method_name='get_quote_summary',
                kwargs=dict(ticker=ticker, modules='secFilings'),
                file_name=f'sec_filings_{ticker.lower()}.json',
                folder_name='quote_summary',
            )
            await process_mock(
                instance=client,
                method_name='get_quote_summary',
                kwargs=dict(ticker=ticker, modules='upgradeDowngradeHistory'),
                file_name=f'upgrade_downgrade_history_{ticker.lower()}.json',
                folder_name='quote_summary',
            )
            await process_mock(
                instance=client,
                method_name='get_quote_summary',
                kwargs=dict(ticker=ticker, modules='institutionOwnership'),
                file_name=f'institution_ownership_{ticker.lower()}.json',
                folder_name='quote_summary',
            )
            await process_mock(
                instance=client,
                method_name='get_quote_summary',
                kwargs=dict(ticker=ticker, modules='fundOwnership'),
                file_name=f'fund_ownership_{ticker.lower()}.json',
                folder_name='quote_summary',
            )
            await process_mock(
                instance=client,
                method_name='get_quote_summary',
                kwargs=dict(ticker=ticker, modules='majorDirectHolders'),
                file_name=f'major_direct_holders_{ticker.lower()}.json',
                folder_name='quote_summary',
            )
            await process_mock(
                instance=client,
                method_name='get_quote_summary',
                kwargs=dict(ticker=ticker, modules='majorHoldersBreakdown'),
                file_name=f'major_holders_breakdown_{ticker.lower()}.json',
                folder_name='quote_summary',
            )
            await process_mock(
                instance=client,
                method_name='get_quote_summary',
                kwargs=dict(ticker=ticker, modules='insiderTransactions'),
                file_name=f'insider_transactions_{ticker.lower()}.json',
                folder_name='quote_summary',
            )
            await process_mock(
                instance=client,
                method_name='get_quote_summary',
                kwargs=dict(ticker=ticker, modules='insiderHolders'),
                file_name=f'insider_holders_{ticker.lower()}.json',
                folder_name='quote_summary',
            )
            await process_mock(
                instance=client,
                method_name='get_quote_summary',
                kwargs=dict(ticker=ticker, modules='netSharePurchaseActivity'),
                file_name=f'net_share_purchase_activity_{ticker.lower()}.json',
                folder_name='quote_summary',
            )
            await process_mock(
                instance=client,
                method_name='get_quote_summary',
                kwargs=dict(ticker=ticker, modules='earnings'),
                file_name=f'earnings_{ticker.lower()}.json',
                folder_name='quote_summary',
            )
            await process_mock(
                instance=client,
                method_name='get_quote_summary',
                kwargs=dict(ticker=ticker, modules='earningsHistory'),
                file_name=f'earnings_history_{ticker.lower()}.json',
                folder_name='quote_summary',
            )
            await process_mock(
                instance=client,
                method_name='get_quote_summary',
                kwargs=dict(ticker=ticker, modules='earningsTrend'),
                file_name=f'earnings_trend_{ticker.lower()}.json',
                folder_name='quote_summary',
            )
            await process_mock(
                instance=client,
                method_name='get_quote_summary',
                kwargs=dict(ticker=ticker, modules='industryTrend'),
                file_name=f'industry_trend_{ticker.lower()}.json',
                folder_name='quote_summary',
            )
            await process_mock(
                instance=client,
                method_name='get_quote_summary',
                kwargs=dict(ticker=ticker, modules='indexTrend'),
                file_name=f'index_trend_{ticker.lower()}.json',
                folder_name='quote_summary',
            )
            await process_mock(
                instance=client,
                method_name='get_quote_summary',
                kwargs=dict(ticker=ticker, modules='sectorTrend'),
                file_name=f'sector_trend_{ticker.lower()}.json',
                folder_name='quote_summary',
            )
            await process_mock(
                instance=client,
                method_name='get_quote_summary',
                kwargs=dict(ticker=ticker, modules='recommendationTrend'),
                file_name=f'recommendation_trend_{ticker.lower()}.json',
                folder_name='quote_summary',
            )
            await process_mock(
                instance=client,
                method_name='get_quote_summary',
                kwargs=dict(ticker=ticker, modules='pageViews'),
                file_name=f'page_views_{ticker.lower()}.json',
                folder_name='quote_summary',
            )
            await process_mock(
                instance=client,
                method_name='get_timeseries',
                kwargs=dict(
                    ticker=ticker,
                    types=ANNUAL_INCOME_STATEMENT_TYPES,
                    period1=PERIOD1,
                    period2=PERIOD2,
                ),
                file_name=f'income_statement_{ticker.lower()}.json',
                folder_name='timeseries',
            )
            await process_mock(
                instance=client,
                method_name='get_timeseries',
                kwargs=dict(
                    ticker=ticker,
                    types=ANNUAL_BALANCE_SHEET_TYPES,
                    period1=PERIOD1,
                    period2=PERIOD2,
                ),
                file_name=f'balance_sheet_{ticker.lower()}.json',
                folder_name='timeseries',
            )
            await process_mock(
                instance=client,
                method_name='get_timeseries',
                kwargs=dict(
                    ticker=ticker,
                    types=ANNUAL_CASH_FLOW_TYPES,
                    period1=PERIOD1,
                    period2=PERIOD2,
                ),
                file_name=f'cash_flow_{ticker.lower()}.json',
                folder_name='timeseries',
            )
            await process_mock(
                instance=client,
                method_name='get_timeseries',
                kwargs=dict(
                    ticker=ticker,
                    types=OTHER_TYPES,
                    period1=PERIOD1,
                    period2=PERIOD2,
                ),
                file_name=f'other_{ticker.lower()}.json',
                folder_name='timeseries',
            )
            await process_mock(
                instance=client,
                method_name='get_options',
                kwargs=dict(ticker=ticker),
                file_name=f'{ticker.lower()}.json',
                folder_name='options',
            )
            await process_mock(
                instance=client,
                method_name='get_search',
                kwargs=dict(tickers=ticker),
                file_name=f'{ticker.lower()}.json',
                folder_name='search',
            )
            await process_mock(
                instance=client,
                method_name='get_recommendations',
                kwargs=dict(tickers=ticker),
                file_name=f'{ticker.lower()}.json',
                folder_name='recommendations',
            )
            await process_mock(
                instance=client,
                method_name='get_insights',
                kwargs=dict(tickers=ticker),
                file_name=f'{ticker.lower()}.json',
                folder_name='insights',
            )
            await process_mock(
                instance=client,
                method_name='get_ratings',
                kwargs=dict(ticker=ticker),
                file_name=f'{ticker.lower()}.json',
                folder_name='ratings',
            )
            await process_mock(
                instance=client,
                method_name='get_market_summaries',
                file_name='market_summaries.json',
            )
            await process_mock(
                instance=client, method_name='get_trending', file_name='trending.json'
            )
            await process_mock(
                instance=client,
                method_name='get_currencies',
                file_name='currencies.json',
            )
            await process_mock(
                instance=client,
                method_name='get_calendar_events',
                kwargs=dict(modules=CALENDAR_EVENT_MODULES),
                file_name='calendar_events.json',
            )


if __name__ == '__main__':
    asyncio.run(main())
