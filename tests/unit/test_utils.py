from typing import Any

import pandas as pd
import pytest
from curl_cffi.requests.exceptions import HTTPError

from tests.assertions import assert_contains_keys, assert_keys_are_not_none
from yafin.const import TYPES
from yafin.utils import (
    _get_func_name_and_args,
    encode_url,
    error,
    get_types_with_frequency,
    process_chart_like_yfinance,
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

    # @pytest.mark.parametrize(
    #     'arg, expected',
    #     [
    #         ('xxx', 'xxx'),
    #         (111, '111'),
    #         (['xxx'], "['xxx']"),
    #         ('x' * (CHAR_LIMIT + 1), 'x' * CHAR_LIMIT + '...'),
    #         (int('1' * (CHAR_LIMIT + 1)), '1' * CHAR_LIMIT + '...'),
    #         (['x' * (CHAR_LIMIT)], "['" + 'x' * (CHAR_LIMIT - 2) + '...'),
    #     ],
    # )
    # def test_shorten_arg(self, arg: Any, expected: str) -> None:
    #     """Test shorten_arg function."""
    #     assert shorten_arg(arg) == expected

    # def test_shorten_args(self) -> None:
    #     """Test shorten_args function."""
    #     pass

    # def test_shorten_kwargs(self) -> None:
    #     """Test shorten_kwargs function."""
    #     pass
