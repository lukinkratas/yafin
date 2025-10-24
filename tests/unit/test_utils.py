from typing import Any, Type

import pytest
from curl_cffi.requests.exceptions import HTTPError

from tests.assertions import assert_contains_keys, assert_keys_are_not_none
from yafin.const import (
    _TYPES,
    ANNUAL_BALANCE_SHEET_TYPES_CSV,
    ANNUAL_CASH_FLOW_TYPES_CSV,
    ANNUAL_INCOME_STATEMENT_TYPES_CSV,
    QUARTERLY_BALANCE_SHEET_TYPES_CSV,
    QUARTERLY_CASH_FLOW_TYPES_CSV,
    QUARTERLY_INCOME_STATEMENT_TYPES_CSV,
    TRAILING_CASH_FLOW_TYPES_CSV,
    TRAILING_INCOME_STATEMENT_TYPES_CSV,
)
from yafin.exceptions import TrailingBalanceSheetError
from yafin.utils import (
    _encode_url,
    _error,
    _get_func_name_and_args,
    get_types_with_frequency,
)


class TestUnitUtils:
    """Unit tests for yafin.utils module."""

    @pytest.mark.parametrize(
        'kwargs, err_cls',
        [
            (dict(msg='Error'), Exception),
            (dict(msg='Error', err_cls=HTTPError), HTTPError),
            (dict(msg='Error', err_cls=ValueError), ValueError),
            (
                dict(msg='Error', err_cls=TrailingBalanceSheetError),
                TrailingBalanceSheetError,
            ),
        ],
    )
    def test_error(self, kwargs: dict[str, Any], err_cls: Type[Exception]) -> None:
        """Test error function."""
        with pytest.raises(err_cls):
            _error(**kwargs)

    def test_encode_url(self) -> None:
        """Test compile_url function."""
        url = r'https://query2.finance.yahoo.com'
        params = {
            'ticker': 'META',
            'region': 'US',
        }
        compiled_url = _encode_url(url, params)
        assert compiled_url == r'https://query2.finance.yahoo.com?ticker=META&region=US'

    @pytest.mark.parametrize(
        'kwargs, expected',
        [
            (
                dict(frequency='annual', typ='income_statement'),
                ANNUAL_INCOME_STATEMENT_TYPES_CSV,
            ),
            (
                dict(frequency='quarterly', typ='income_statement'),
                QUARTERLY_INCOME_STATEMENT_TYPES_CSV,
            ),
            (
                dict(frequency='trailing', typ='income_statement'),
                TRAILING_INCOME_STATEMENT_TYPES_CSV,
            ),
            (
                dict(frequency='annual', typ='balance_sheet'),
                ANNUAL_BALANCE_SHEET_TYPES_CSV,
            ),
            (
                dict(frequency='quarterly', typ='balance_sheet'),
                QUARTERLY_BALANCE_SHEET_TYPES_CSV,
            ),
            (dict(frequency='annual', typ='cash_flow'), ANNUAL_CASH_FLOW_TYPES_CSV),
            (
                dict(frequency='quarterly', typ='cash_flow'),
                QUARTERLY_CASH_FLOW_TYPES_CSV,
            ),
            (dict(frequency='trailing', typ='cash_flow'), TRAILING_CASH_FLOW_TYPES_CSV),
        ],
    )
    def test_get_types_with_frequency(
        self, kwargs: dict[str, Any], expected: str
    ) -> None:
        """Test get_types_with_frequency function."""
        types = get_types_with_frequency(**kwargs)
        types_list = types.split(',')
        expected_types_list = [
            f'{kwargs["frequency"]}{t}' for t in _TYPES[kwargs['typ']]
        ]
        assert sorted(types_list) == sorted(expected_types_list)

    @pytest.mark.parametrize(
        'kwargs, err_cls',
        [
            (
                dict(frequency='trailing', typ='balance_sheet'),
                TrailingBalanceSheetError,
            ),
            (dict(frequency='xxx', typ='income_statement'), ValueError),
            (dict(frequency='annual', typ='xxx'), ValueError),
        ],
    )
    def test_get_types_with_frequency_invalid_args(
        self, kwargs: dict[str, Any], err_cls: Type[Exception]
    ) -> None:
        """Test get_types_with_frequency function with invalid arguments."""
        with pytest.raises(err_cls):
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
