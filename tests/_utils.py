import json
import pathlib
from typing import Any
from zoneinfo import ZoneInfo

import pandas as pd
from curl_cffi.requests import Response
from curl_cffi.requests.exceptions import HTTPError
from pytest_mock import MockerFixture

FIXTURE_PATH = pathlib.Path(__file__).resolve().parent.joinpath('fixtures')


def _get_fixture_path(file_name: str, folder_name: str | None = None) -> pathlib.Path:
    """Get the path to a fixture file."""
    folder = FIXTURE_PATH.joinpath(folder_name) if folder_name else FIXTURE_PATH
    return folder.joinpath(file_name)


def _get_json_fixture(file_name: str, folder_name: str | None = None) -> dict[str, Any]:
    json_path = _get_fixture_path(file_name, folder_name)
    return json.loads(json_path.read_text())


def _mock_response(
    mocker: MockerFixture,
    patched_method: str,
    status_code: int = 200,
    response_jsons: list[dict[str, Any]] | None = None,
    text: str | None = None,
    url: str | None = None,
    async_mock: bool = False,
) -> None:
    """Mock response with status code 200."""
    mock_response = mocker.Mock(spec=Response)
    mock_response.status_code = status_code
    mock_response.raise_for_status = mocker.Mock()

    if status_code == 404:
        mock_response.raise_for_status.side_effect = HTTPError(
            '404 Client Error: Not Found for url'
        )

    if response_jsons is not None and len(response_jsons) == 1:
        mock_response.json.return_value = response_jsons[0]

    elif response_jsons is not None and len(response_jsons) > 1:
        mock_response.json.side_effect = [rj for rj in response_jsons]

    if text is not None:
        mock_response.text = text

    if url is not None:
        mock_response.url = url

    mock_class = mocker.AsyncMock if async_mock else mocker.Mock
    mocker.patch(patched_method, new=mock_class(return_value=mock_response))


def _process_chart_like_yfinance(chart_result: dict[str, Any]) -> pd.DataFrame:
    """Process chart response json into pandas dataframe, exact as yfinance."""
    tz_info = ZoneInfo(chart_result['meta']['exchangeTimezoneName'])
    timestamps = chart_result['timestamp']
    ohlcvs = chart_result['indicators']['quote'][0]
    # adjcloses = chart['indicators']['adjclose'][0]['adjclose']

    chart_df = pd.DataFrame({**ohlcvs}, index=timestamps).rename(
        columns={
            'open': 'Open',
            'volume': 'Volume',
            'close': 'Close',
            'low': 'Low',
            'high': 'High',
        }
    )

    chart_df['Date'] = pd.to_datetime(chart_df.index.to_list(), unit='s', utc=True)
    chart_df['Date'] = chart_df['Date'].dt.tz_convert(tz_info)

    dividends = chart_result['events'].get('dividends')
    dividends_df = (
        pd.DataFrame(
            dividends.values() if dividends is not None else {'date': [], 'amount': []}
        )
        .set_index('date')
        .rename(columns={'amount': 'Dividends'})
    )
    chart_df = chart_df.join(dividends_df).fillna(value={'Dividends': 0})

    splits = chart_result['events'].get('splits')
    splits_df = (
        pd.DataFrame(
            splits.values() if splits is not None else {'date': [], 'numerator': []}
        )
        .set_index('date')
        .rename(columns={'numerator': 'Stock Splits'})
    )
    chart_df = chart_df.join(splits_df['Stock Splits']).fillna(
        value={'Stock Splits': 0}
    )

    return chart_df.set_index('Date').loc[
        :,
        ['Open', 'High', 'Low', 'Close', 'Volume', 'Dividends', 'Stock Splits'],
    ]
