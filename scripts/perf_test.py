import asyncio
import statistics
from collections.abc import Callable
from datetime import timedelta
from functools import wraps
from time import perf_counter
from typing import Any

import pandas as pd
from curl_cffi import requests
from yfinance import Ticker

from yafin import AsyncSymbol
from yafin.utils import _get_func_name_and_args

NRUNS = 1


def log_performance(n: int = 1) -> Callable[..., Any]:
    """Decorator for logging functions and its' performance."""

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            func_name, _ = _get_func_name_and_args(func, args)
            run_times = []

            print(f'{func_name} running {n} time(s) started.')
            total_start_time = perf_counter()

            for idx in range(1, n + 1):
                print(f'  {func_name} run no.{idx} started.')
                run_start_time = perf_counter()

                result = func(*args, **kwargs)

                run_elapsed_time = perf_counter() - run_start_time
                run_times.append(run_elapsed_time)
                run_elapsed_time_td = timedelta(seconds=run_elapsed_time)
                print(
                    f'  {func_name} run no.{idx} finished with '
                    f'elapsed_time={run_elapsed_time_td}.'
                )

            total_elapsed_time = perf_counter() - total_start_time
            total_elapsed_time_td = timedelta(seconds=total_elapsed_time)
            avg_elapsed_time_td = timedelta(seconds=statistics.mean(run_times))
            print(
                f'{func_name} running {n} time(s) finished with '
                f'total={total_elapsed_time_td} and average={avg_elapsed_time_td}.'
            )

            return result

        return wrapper

    return decorator


def process_chart_like_yfinance(chart: dict[str, Any]) -> pd.DataFrame:
    """Process chart response json into pandas dataframe, exact as yfinance."""
    dividends = chart['events'].get('dividends')
    dividends_df = pd.DataFrame(
        dividends.values() if dividends else {'date': [], 'amount': []}
    ).rename(columns={'amount': 'dividends'})

    splits = chart['events'].get('splits')
    splits_df = pd.DataFrame(
        splits.values()
        if splits
        else {'date': [], 'numerator': [], 'denominator': [], 'splitRatio': []}
    )
    splits_df['splits'] = splits_df['numerator'] / splits_df['denominator']

    chart_df = (
        pd.DataFrame({'date': chart['timestamp'], **chart['indicators']['quote'][0]})
        .set_index('date')
        .join(dividends_df.set_index('date').loc[:, 'dividends'])
        .join(splits_df.set_index('date').loc[:, 'splits'])
        .fillna(value={'dividends': 0, 'splits': 0})
    )
    chart_df.index = pd.to_datetime(chart_df.index, unit='s')
    chart_df.columns = chart_df.columns.str.capitalize()
    chart_df = chart_df.rename(columns={'Splits': 'Stock Splits'})
    return chart_df.loc[
        :,
        ['Open', 'High', 'Low', 'Close', 'Volume', 'Dividends', 'Stock Splits'],
    ]

def test_process_chart_like_yfinance(self) -> None:
    """Test process_chart_like_yfinance function."""
    timestamps = [1759843800, 1759930200, 1760016600, 1760103000, 1760371117]
    opens = [
        717.719970703125,
        713.4500122070312,
        718.280029296875,
        730.9199829101562,
        713.010009765625,
    ]
    closes = [
        713.0800170898438,
        717.8400268554688,
        733.510009765625,
        705.2999877929688,
        712.2550048828125,
    ]
    lows = [
        705.75,
        707.8099975585938,
        712.4400024414062,
        704.510009765625,
        707.6412963867188,
    ]
    highs = [
        718.5,
        719.6500244140625,
        733.510009765625,
        735.27001953125,
        719.9400024414062,
    ]
    volumes = [12062900, 10790600, 12717200, 16887300, 5193768]
    adj_closes = [
        713.0800170898438,
        717.8400268554688,
        733.510009765625,
        705.2999877929688,
        712.2550048828125,
    ]
    simplifed_chart = {
        'meta': {
            'currency': 'USD',
            'symbol': 'META',
        },
        'timestamp': timestamps,
        'events': {
            'dividends': {'1760103000': {'amount': 0.525, 'date': 1760103000}},
            'splits': {
                '1759930200': {
                    'date': 1759930200,
                    'numerator': 4.0,
                    'denominator': 1.0,
                    'splitRatio': '4:1',
                },
            },
        },
        'indicators': {
            'quote': [
                {
                    'open': opens,
                    'close': closes,
                    'low': lows,
                    'high': highs,
                    'volume': volumes,
                }
            ],
            'adjclose': [{'adjclose': adj_closes}],
        },
    }
    simplifed_chart_df = process_chart_like_yfinance(simplifed_chart)
    expected_df = pd.DataFrame(
        {
            'Open': opens,
            'High': highs,
            'Low': lows,
            'Close': closes,
            'Volume': volumes,
            'Dividends': [0.0, 0.0, 0.0, 0.525, 0.0],
            'Stock Splits': [0.0, 4.0, 0.0, 0.0, 0.0],
        },
        index=pd.DatetimeIndex(
            data=pd.to_datetime(timestamps, unit='s'), name='date'
        ),
    )
    assert simplifed_chart_df.equals(expected_df)

@log_performance(NRUNS)
def main_yfinance() -> None:  # noqa: D103
    # async session does not work, throws
    #   yfinance.exceptions.YFDataException: Yahoo API requires curl_cffi session
    #   not <class 'curl_cffi.requests.session.AsyncSession'>.
    #   Solution: stop setting session, let YF handle.
    # session = requests.AsyncSession(impersonate="chrome")

    with requests.Session(impersonate='chrome') as session:
        meta = Ticker('META', session=session)
        history_df = meta.history(period='1y', interval='1d')

    print(history_df)
    print(history_df.info())

    session.close()


@log_performance(NRUNS)
async def main() -> None:  # noqa: D103
    async with AsyncSymbol('META') as symbol:
        chart = await symbol.get_chart(period_range='1y', interval='1d')
        chart_df = process_chart_like_yfinance(chart)

    print(chart_df)
    print(chart_df.info())


if __name__ == '__main__':
    main_yfinance()
    asyncio.run(main())
