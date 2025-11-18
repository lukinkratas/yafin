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


def _mock_response(
    mocker: MockerFixture,
    patched_method: str,
    status_code: int = 200,
    response_json: dict[str, Any] | None = None,
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

    if response_json is not None:
        mock_response.json.return_value = response_json

    if text is not None:
        mock_response.text = text

    if url is not None:
        mock_response.url = url

    mock_class = mocker.AsyncMock if async_mock else mocker.Mock
    mocker.patch(patched_method, new=mock_class(return_value=mock_response))
