import logging
from collections.abc import Callable
from functools import wraps
from typing import Any, NoReturn, Type
from urllib.parse import urlencode

from .const import _TYPES, FREQUENCIES
from .exceptions import TrailingBalanceSheetError

logger = logging.getLogger(__name__)

def _error(msg: str, err_cls: Type[Exception] = Exception) -> NoReturn:
    """Log error message and raise exception.

    Args:
        msg: error message (hint), that will be logged and raised.
        err_cls: class of the raised error, default Exception.
    """
    logger.error(msg)
    raise err_cls(msg)


def _encode_url(url: str, params: dict[str, str] | None = None) -> str:
    """Print URL with parameters.

    Args:
        url: base url, where query param will be added.
        params: http request query parameters.

    Returns: url with params
    """
    if params is None:
        return url

    params_copy = params.copy()

    if 'crumb' in params:
        params_copy['crumb'] = 'REDACTED'

    return f'{url}?{urlencode(params_copy)}'


def get_types_with_frequency(frequency: str, typ: str) -> str:
    """Enrich types with frequency.

    Args:
        frequency:
            frequency used for timeseries endpoint, e.g.: annual, quarterly or trailing.
        typ:
            type of types, e.g.: income_statement, balance_sheet or cash_flow,
            which is used for fetching all types for given financial.
            e.g. for income_statement: NetIncome,EBIT,EBITDA,GrossProfit, ...

    Returns:
        types enriched with frequency e.g. for income_statement:
            trailingNetIncome,trailingEBIT,trailingEBITDA,trailingGrossProfit, ...

    Raises:
        ValueError: If frequency or typ are not in list of valid values.
        TrailingBalanceSheetError:
            If attempting to request balance sheet with trailing
                frequency.
    """
    if typ not in _TYPES.keys():
        _error(msg=f'Invalid {typ=}. Valid values: {_TYPES.keys()}', err_cls=ValueError)

    if frequency not in FREQUENCIES:
        _error(
            msg=f'Invalid {frequency=}. Valid values: {FREQUENCIES}', err_cls=ValueError
        )

    if typ == 'balance_sheet' and frequency == 'trailing':
        _error(
            msg=f'{frequency=} not allowed for balance sheet.',
            err_cls=TrailingBalanceSheetError,
        )

    types = _TYPES[typ]
    types_with_frequency = [f'{frequency}{t}' for t in types]
    return ','.join(types_with_frequency)


def _get_func_name_and_args(
    func: Callable[..., Any], args: tuple[Any, ...]
) -> tuple[str, tuple[Any, ...]]:
    """Helper function, that takes function and its' arguments.
    It then checks, whether the first argument is a class instance.
    If so, then it returns class_name.method_name and arguments exclusing the first one.
    If not, then it returns function_name and arguments in unchaged form.

    Args:
        func: python function
        args: arguments to the function

    Returns: function name and arguments
    """
    # check if first argument is class instance (self)
    if args and hasattr(args[0], func.__name__):
        func_name = f'{args[0].__class__.__name__}.{func.__name__}'
        return func_name, args[1:]

    return func.__name__, args


def _log_args(func: Callable[..., Any]) -> Callable[..., Any]:
    """Decorator for logging functions."""

    @wraps(func)
    async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
        func_name, _ = _get_func_name_and_args(func, args)

        logger.debug(f'{func_name} was called.')
        result = await func(*args, **kwargs)
        logger.debug(f'{func_name} finished.')

        return result

    return async_wrapper
