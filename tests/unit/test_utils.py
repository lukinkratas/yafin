from typing import Any

import pytest
from curl_cffi.requests.exceptions import HTTPError

from tests.assertions import assert_contains_keys, assert_keys_are_not_none
from yafin.const import TYPES
from yafin.utils import (
    _get_func_name_and_args,
    encode_url,
    error,
    get_types_with_frequency,
)


class TestUnitUtils:
    """Unit tests for yafin.utils module."""

    def test_error(self) -> None:
        """Test error function."""
        with pytest.raises(Exception):
            error('Error')

    def test_error_http(self) -> None:
        """Test error function with HTTP error."""
        with pytest.raises(HTTPError):
            error('Error', HTTPError)

    def test_encode_url(self) -> None:
        """Test compile_url function."""
        url = r'https://query2.finance.yahoo.com'
        params = {
            'ticker': 'META',
            'region': 'US',
        }
        compiled_url = encode_url(url, params)
        assert compiled_url == r'https://query2.finance.yahoo.com?ticker=META&region=US'

    @pytest.mark.parametrize(
        'kwargs',
        [
            dict(frequency='annual', typ='income_statement'),
            dict(frequency='quarterly', typ='income_statement'),
            dict(frequency='trailing', typ='income_statement'),
            dict(frequency='annual', typ='balance_sheet'),
            dict(frequency='quarterly', typ='balance_sheet'),
            dict(frequency='annual', typ='cash_flow'),
            dict(frequency='quarterly', typ='cash_flow'),
            dict(frequency='trailing', typ='cash_flow'),
        ],
    )
    def test_get_types_with_frequency(self, kwargs: dict[str, Any]) -> None:
        """Test get_types_with_frequency function."""
        types = get_types_with_frequency(**kwargs)
        types_list = types.split(',')
        expected_types_list = [
            f'{kwargs["frequency"]}{t}' for t in TYPES[kwargs['typ']]
        ]
        assert sorted(types_list) == sorted(expected_types_list)

    @pytest.mark.parametrize(
        'kwargs',
        [
            dict(frequency='trailing', typ='balance_sheet'),
            dict(frequency='xxx', typ='income_statement'),
            dict(frequency='annual', typ='xxx'),
        ],
    )
    def test_get_types_with_frequency_invalid_args(
        self, kwargs: dict[str, Any]
    ) -> None:
        """Test get_types_with_frequency function with invalid arguments."""
        with pytest.raises(Exception):
            get_types_with_frequency(**kwargs)

    def test_get_func_name_and_args(self) -> None:
        """Test _get_func_name_and_args function."""
        func = print
        args = ('a', 'b', 'c')
        func_name, args_copy = _get_func_name_and_args(func, args)
        assert func_name == 'print'
        assert args_copy == ('a', 'b', 'c')

    def test_assert_contains_keys(self) -> None:
        """Test assert_contains_keys function."""
        assert_contains_keys({'a': 1, 'b': 2}, ['a', 'b'])
        assert_contains_keys({'a': 1, 'b': 2}, ['a'])
        with pytest.raises(AssertionError):
            assert_contains_keys({'a': 1}, ['a', 'b'])

    @pytest.mark.parametrize(
        'kwargs',
        [
            dict(data={'a': 0, 'b': 2}, keys=['a', 'b']),
            dict(data={'a': {}, 'b': 2}, keys=['a', 'b']),
            dict(data={'a': [], 'b': 2}, keys=['a', 'b']),
            dict(data={'a': (), 'b': 2}, keys=['a', 'b']),
            dict(data={'a': '', 'b': 2}, keys=['a', 'b']),
            dict(data={'a': None, 'b': 2}, keys=['a', 'b']),
        ],
    )
    def test_assert_keys_are_not_none(self, kwargs: dict[str, Any]) -> None:
        """Test assert_keys_are_not_none function."""
        with pytest.raises(AssertionError):
            assert_keys_are_not_none(**kwargs)
