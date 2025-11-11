import json
import pathlib
from typing import Any

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


def _mock_200_response(
    mocker: MockerFixture,
    response_json: dict[str, Any] | None = None,
    text: str | None = None,
) -> None:
    """Mock response with status code 200."""
    mock_response = mocker.Mock(spec=Response)
    mock_response.status_code = 200
    mock_response.raise_for_status = mocker.Mock()

    if response_json:
        mock_response.json.return_value = response_json

    if text:
        mock_response.text = text

    mocker.patch(
        'yafin.client.AsyncSession.request',
        new=mocker.AsyncMock(return_value=mock_response),
    )


def _mock_404_response(mocker: MockerFixture, response_json: dict[str, Any]) -> None:
    """Mock response with status code 404."""
    mock_response = mocker.Mock(spec=Response)
    mock_response.status_code = 404
    mock_response.json.return_value = response_json
    mock_response.raise_for_status.side_effect = HTTPError(
        '404 Client Error: Not Found for url'
    )
    mocker.patch(
        'yafin.client.AsyncSession.request',
        new=mocker.AsyncMock(return_value=mock_response),
    )
