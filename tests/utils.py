from typing import Any

from curl_cffi.requests import Response
from curl_cffi.requests.exceptions import HTTPError
from pytest_mock import MockerFixture


def mock_200_response(mocker: MockerFixture, response_json: dict[str, Any]) -> None:
    """Mock response with status code 200."""
    mock_response = mocker.Mock(spec=Response)
    mock_response.status_code = 200
    mock_response.json.return_value = response_json
    mock_response.raise_for_status = mocker.Mock()
    mocker.patch(
        'yafin.client.AsyncSession.get',
        new=mocker.AsyncMock(return_value=mock_response),
    )


def mock_404_response(mocker: MockerFixture, response_json: dict[str, Any]) -> None:
    """Mock response with status code 404."""
    mock_response = mocker.Mock(spec=Response)
    mock_response.status_code = 404
    mock_response.json.return_value = response_json
    mock_response.raise_for_status.side_effect = HTTPError(
        '404 Client Error: Not Found for url'
    )
    mocker.patch(
        'yafin.client.AsyncSession.get',
        new=mocker.AsyncMock(return_value=mock_response),
    )
