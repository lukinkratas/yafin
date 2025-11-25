from typing import Any

import pytest
from curl_cffi.requests.exceptions import HTTPError

from yafin.const import (
    _TYPES,
    ANNUAL_BALANCE_SHEET_TYPES_SET,
    ANNUAL_CASH_FLOW_TYPES_SET,
    ANNUAL_INCOME_STATEMENT_TYPES_SET,
    CALENDAR_EVENT_MODULES_SET,
    EVENTS_SET,
    INTERVALS,
    OTHER_TYPES_SET,
    PERIOD_RANGES,
    QUARTERLY_BALANCE_SHEET_TYPES_SET,
    QUARTERLY_CASH_FLOW_TYPES_SET,
    QUARTERLY_INCOME_STATEMENT_TYPES_SET,
    QUOTE_SUMMARY_MODULES_SET,
    TRAILING_CASH_FLOW_TYPES_SET,
    TRAILING_INCOME_STATEMENT_TYPES_SET,
)
from yafin.exceptions import TrailingBalanceSheetError
from yafin.utils import (
    _check_calendar_event_modules,
    _check_events,
    _check_frequency,
    _check_interval,
    _check_period_range,
    _check_quote_summary_modules,
    _check_typ,
    _check_types,
    _encode_url,
    _error,
    get_types_with_frequency,
)


class TestUnitUtils:
    """Unit tests for yafin.utils module."""

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
    def test_error(self, kwargs: dict[str, Any], err_cls: type[Exception]) -> None:
        """Test error function."""
        with pytest.raises(err_cls):
            _error(**kwargs)

    @pytest.mark.parametrize('interval', INTERVALS)
    def test_check_interval(self, interval: str) -> None:
        """Test _check_interval function with."""
        _check_interval(interval)

    def test_check_interval_invalid_args(self) -> None:
        """Test _check_interval function with invalid arguments."""
        with pytest.raises(ValueError):
            _check_interval('xxx')

    @pytest.mark.parametrize('period_range', PERIOD_RANGES)
    def test_check_period_range(self, period_range: str) -> None:
        """Test _check_period_range function."""
        _check_period_range(period_range)

    def test_check_period_range_invalid_args(self) -> None:
        """Test _check_period_range function with invalid arguments."""
        with pytest.raises(ValueError):
            _check_period_range('xxx')

    def test_check_events(self) -> None:
        """Test _check_events function."""
        _check_events(EVENTS_SET)

    def test_check_events_invalid_args(self) -> None:
        """Test _check_events function with invalid arguments."""
        with pytest.raises(ValueError):
            _check_events({'xxx'})

    def test_check_quote_summary_modules(self) -> None:
        """Test _check_quote_summary_modules function."""
        _check_quote_summary_modules(QUOTE_SUMMARY_MODULES_SET)

    def test_check_quote_summary_modules_invalid_args(self) -> None:
        """Test _check_quote_summary_modules function with invalid arguments."""
        with pytest.raises(ValueError):
            _check_quote_summary_modules({'xxx'})

    def test_check_calendar_event_modules(self) -> None:
        """Test _check_calendar_event_modules function."""
        _check_calendar_event_modules(CALENDAR_EVENT_MODULES_SET)

    def test_check_calendar_event_modules_invalid_args(self) -> None:
        """Test _check_calendar_event_modules function with invalid arguments."""
        with pytest.raises(ValueError):
            _check_calendar_event_modules({'xxx'})

    @pytest.mark.parametrize(
        'types',
        [
            ANNUAL_INCOME_STATEMENT_TYPES_SET,
            QUARTERLY_INCOME_STATEMENT_TYPES_SET,
            TRAILING_INCOME_STATEMENT_TYPES_SET,
            ANNUAL_BALANCE_SHEET_TYPES_SET,
            QUARTERLY_BALANCE_SHEET_TYPES_SET,
            ANNUAL_CASH_FLOW_TYPES_SET,
            QUARTERLY_CASH_FLOW_TYPES_SET,
            TRAILING_CASH_FLOW_TYPES_SET,
            OTHER_TYPES_SET,
        ],
    )
    def test_check_types(self, types: set[str]) -> None:
        """Test _check_types function."""
        _check_types(types)

    def test_check_types_invalid_args(self) -> None:
        """Test _check_types function with invalid arguments."""
        with pytest.raises(ValueError):
            _check_types({'xxx'})

    @pytest.mark.parametrize('typ', _TYPES.keys())
    def test_check_typ(self, typ: str) -> None:
        """Test _check_typ function."""
        _check_typ(typ)

    def test_check_typ_invalid_args(self) -> None:
        """Test _check_typ function with invalid arguments."""
        with pytest.raises(ValueError):
            _check_typ('xxx')

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
            dict(frequency=None, typ='other'),
        ],
    )
    def test_check_frequency(self, kwargs: dict[str, Any]) -> None:
        """Test _check_frequency function."""
        _check_frequency(**kwargs)

    @pytest.mark.parametrize(
        'kwargs, err_cls',
        [
            (
                dict(frequency='trailing', typ='balance_sheet'),
                TrailingBalanceSheetError,
            ),
            (dict(frequency='xxx', typ='income_statement'), ValueError),
            (dict(frequency='annual', typ='other'), ValueError),
        ],
    )
    def test_check_frequency_invalid_args(
        self, kwargs: dict[str, Any], err_cls: type[Exception]
    ) -> None:
        """Test _check_frequency function with invalid arguments."""
        with pytest.raises(err_cls):
            _check_frequency(**kwargs)

    @pytest.mark.parametrize(
        'kwargs, expected_set',
        [
            (
                dict(frequency='annual', typ='income_statement'),
                ANNUAL_INCOME_STATEMENT_TYPES_SET,
            ),
            (
                dict(frequency='quarterly', typ='income_statement'),
                QUARTERLY_INCOME_STATEMENT_TYPES_SET,
            ),
            (
                dict(frequency='trailing', typ='income_statement'),
                TRAILING_INCOME_STATEMENT_TYPES_SET,
            ),
            (
                dict(frequency='annual', typ='balance_sheet'),
                ANNUAL_BALANCE_SHEET_TYPES_SET,
            ),
            (
                dict(frequency='quarterly', typ='balance_sheet'),
                QUARTERLY_BALANCE_SHEET_TYPES_SET,
            ),
            (dict(frequency='annual', typ='cash_flow'), ANNUAL_CASH_FLOW_TYPES_SET),
            (
                dict(frequency='quarterly', typ='cash_flow'),
                QUARTERLY_CASH_FLOW_TYPES_SET,
            ),
            (dict(frequency='trailing', typ='cash_flow'), TRAILING_CASH_FLOW_TYPES_SET),
            (dict(frequency=None, typ='other'), OTHER_TYPES_SET),
        ],
    )
    def test_get_types_with_frequency(
        self, kwargs: dict[str, Any], expected_set: set[str]
    ) -> None:
        """Test get_types_with_frequency function."""
        types = get_types_with_frequency(**kwargs)
        types_list = types.split(',')
        # have to compare sorted iterables, bcs of the order.
        assert sorted(types_list) == sorted(expected_set)

    @pytest.mark.parametrize(
        'kwargs, err_cls',
        [
            (dict(frequency='xxx', typ='income_statement'), ValueError),
            (dict(frequency='annual', typ='xxx'), ValueError),
            (
                dict(frequency='trailing', typ='balance_sheet'),
                TrailingBalanceSheetError,
            ),
        ],
    )
    def test_get_types_with_frequency_invalid_args(
        self, kwargs: dict[str, Any], err_cls: type[Exception]
    ) -> None:
        """Test get_types_with_frequency function with invalid arguments."""
        with pytest.raises(err_cls):
            get_types_with_frequency(**kwargs)
