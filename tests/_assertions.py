from typing import Any, Callable

from typeguard import check_type

from tests._const import _MODULE_MAP, _PARSE_TICKER_FUNCS_MAP, _RESULT_KEY_MAP
from yafin.types import (
    CalendarEventsFinanceResult,
    CalendarEventsResponseJson,
    ChartResponseJson,
    ChartResult,
    CurrenciesResponseJson,
    CurrenciesResult,
    InsightsFinanceResult,
    InsightsResponseJson,
    MarketSummaryResponseJson,
    MarketSummaryResponseResult,
    OptionChainResult,
    OptionsResponseJson,
    QuoteResponseJson,
    QuoteResult,
    QuoteSummaryResponseJson,
    QuoteSummaryResult,
    QuoteTypeResponseJson,
    QuoteTypeResult,
    RatingsResult,
    RecommendationsFinanceResult,
    RecommendationsResponseJson,
    SearchResult,
    TimeseriesResponseJson,
    TimeseriesResult,
    TrendingFinanceResult,
    TrendingResponseJson,
)


def _assert_result(
    result: dict[str, Any],
    typ: type[Any],
    expected_ticker: str | None = None,
) -> None:
    assert result
    assert check_type(result, typ)

    if expected_ticker:
        # get function for ticker assertion
        parse_ticker_funcs: list[Callable[..., str]] = _PARSE_TICKER_FUNCS_MAP[typ]

        for func in parse_ticker_funcs:
            assert func(result) == expected_ticker


def _assert_chart_result(chart_result: dict[str, Any], expected_ticker: str) -> None:
    _assert_result(chart_result, ChartResult, expected_ticker)


def _assert_quotes_result(quote_result: dict[str, Any], expected_ticker: str) -> None:
    _assert_result(quote_result, QuoteResult, expected_ticker)


def _assert_quote_types_result(
    quote_types_result: dict[str, Any], expected_ticker: str
) -> None:
    _assert_result(quote_types_result, QuoteTypeResult, expected_ticker)


def _assert_recommendations_result(
    recommendation_result: dict[str, Any], expected_ticker: str
) -> None:
    _assert_result(recommendation_result, RecommendationsFinanceResult, expected_ticker)


def _assert_insights_result(
    insights_result: dict[str, Any], expected_ticker: str
) -> None:
    _assert_result(insights_result, InsightsFinanceResult, expected_ticker)


def _assert_quote_summary_result(
    quote_summary_result: dict[str, Any], modules: str
) -> None:
    _assert_result(quote_summary_result, QuoteSummaryResult)
    assert sorted(quote_summary_result.keys()) == sorted(modules.split(','))


def _assert_quote_summary_single_module_result(
    quote_summary_single_module_result: dict[str, Any], module: str
) -> None:
    _assert_result(quote_summary_single_module_result, _MODULE_MAP[module])
    # assert list(quote_summary_single_module_result.keys()) == [module]


def _assert_timeseries_result(
    timeseries_results: list[dict[str, Any]],
    expected_ticker: str,
    expected_types: str,
) -> None:
    assert timeseries_results
    # assert check_type(timeseries_results, list[TimeseriesResult])

    for result in timeseries_results:
        assert result['meta']['symbol'][0] == expected_ticker
        assert check_type(result, TimeseriesResult)

    timeseries_result_types = [
        result['meta']['type'][0] for result in timeseries_results
    ]
    assert sorted(timeseries_result_types) == sorted(expected_types.split(','))


def _assert_options_result(
    options_result: dict[str, Any], expected_ticker: str
) -> None:
    _assert_result(options_result, OptionChainResult, expected_ticker)


def _assert_trending_result(trending_result: dict[str, Any]) -> None:
    _assert_result(trending_result, TrendingFinanceResult)


def _assert_calendar_events_result(calendar_events_result: dict[str, Any]) -> None:
    _assert_result(calendar_events_result, CalendarEventsFinanceResult)


def _assert_ratings_result(
    ratings_result: dict[str, Any], expected_ticker: str
) -> None:
    _assert_result(ratings_result, RatingsResult, expected_ticker)


def _assert_search_result(search_result: dict[str, Any]) -> None:
    _assert_result(search_result, SearchResult)


def _assert_result_list(
    result_list: list[dict[str, Any]],
    typ: type[Any],
    tickers: str,
    assert_result_func: Callable[..., Any],
    *args: Any,
    **kwargs: Any,
) -> None:
    tickers_list = tickers.split(',')
    assert len(result_list) == len(tickers_list)

    parse_ticker_funcs: list[Callable[..., str]] | None = _PARSE_TICKER_FUNCS_MAP.get(
        typ
    )

    if parse_ticker_funcs is not None:
        # get function for sorting result_list by ticker
        parse_ticker_func = parse_ticker_funcs[0]

        for expected_ticker, result in zip(
            sorted(tickers_list),
            sorted(result_list, key=parse_ticker_func),
        ):
            assert_result_func(result, expected_ticker, *args, **kwargs)

    else:
        for result in result_list:
            assert_result_func(result, *args, **kwargs)


def _assert_chart_result_list(
    chart_result_list: list[dict[str, Any]], tickers: str
) -> None:
    _assert_result_list(chart_result_list, ChartResult, tickers, _assert_chart_result)


def _assert_quotes_result_list(
    quote_result_list: list[dict[str, Any]], tickers: str
) -> None:
    _assert_result_list(quote_result_list, QuoteResult, tickers, _assert_quotes_result)


def _assert_quote_types_result_list(
    quote_types_result_list: list[dict[str, Any]], tickers: str
) -> None:
    _assert_result_list(
        quote_types_result_list, QuoteTypeResult, tickers, _assert_quote_types_result
    )


def _assert_recommendations_result_list(
    recommendation_result_list: list[dict[str, Any]], tickers: str
) -> None:
    _assert_result_list(
        recommendation_result_list,
        RecommendationsFinanceResult,
        tickers,
        _assert_recommendations_result,
    )


def _assert_quote_summary_result_list(
    quote_summary_result_list: list[dict[str, Any]], tickers: str, modules: str
) -> None:
    _assert_result_list(
        quote_summary_result_list,
        QuoteSummaryResult,
        tickers,
        _assert_quote_summary_result,
        modules,
    )


def _assert_quote_summary_single_module_result_list(
    quote_summary_single_module_result_list: list[dict[str, Any]],
    tickers: str,
    module: str,
) -> None:
    tickers_list = tickers.split(',')
    assert len(quote_summary_single_module_result_list) == len(tickers_list)

    for result in quote_summary_single_module_result_list:
        _assert_quote_summary_single_module_result(result, module)


def _assert_timeseries_result_list(
    timeseries_results_list: list[list[dict[str, Any]]],
    tickers: str,
    expected_types: str,
) -> None:
    tickers_list = tickers.split(',')
    assert len(timeseries_results_list) == len(tickers_list)

    for expected_ticker, result in zip(
        sorted(tickers_list),
        sorted(
            timeseries_results_list, key=lambda result: result[0]['meta']['symbol'][0]
        ),
    ):
        _assert_timeseries_result(result, expected_ticker, expected_types)


def _assert_options_result_list(
    options_result_list: list[dict[str, Any]], tickers: str
) -> None:
    _assert_result_list(
        options_result_list, OptionChainResult, tickers, _assert_options_result
    )


def _assert_ratings_result_list(
    ratings_result_list: list[dict[str, Any]], tickers: str
) -> None:
    _assert_result_list(
        ratings_result_list, RatingsResult, tickers, _assert_ratings_result
    )


def _assert_insights_result_list(
    insights_result_list: list[dict[str, Any]], tickers: str
) -> None:
    _assert_result_list(
        insights_result_list, InsightsFinanceResult, tickers, _assert_insights_result
    )


def _assert_market_summary_result_list(
    market_summary_result_list: list[dict[str, Any]],
) -> None:
    assert market_summary_result_list

    for market_summary in market_summary_result_list:
        assert check_type(market_summary, MarketSummaryResponseResult)


def _assert_currencies_result_list(
    currencies_result_list: list[dict[str, Any]],
) -> None:
    assert currencies_result_list
    for currency in currencies_result_list:
        assert check_type(currency, CurrenciesResult)


def _assert_response_json(response_json: dict[str, Any], typ: type[Any]) -> None:
    assert response_json
    assert check_type(response_json, typ)
    key = _RESULT_KEY_MAP[typ]
    assert response_json[key]['error'] is None


def _assert_chart_response_json(chart: dict[str, Any], ticker: str) -> None:
    _assert_response_json(chart, ChartResponseJson)
    _assert_chart_result(chart['chart']['result'][0], ticker)


def _assert_quote_response_json(quotes: dict[str, Any], tickers: str) -> None:
    _assert_response_json(quotes, QuoteResponseJson)
    _assert_quotes_result_list(quotes['quoteResponse']['result'], tickers)


def _assert_quote_type_response_json(quote_types: dict[str, Any], tickers: str) -> None:
    _assert_response_json(quote_types, QuoteTypeResponseJson)
    _assert_quote_types_result_list(quote_types['quoteType']['result'], tickers)


def _assert_quote_summary_response_json(
    quote_summary: dict[str, Any], modules: str
) -> None:
    _assert_response_json(quote_summary, QuoteSummaryResponseJson)
    _assert_quote_summary_result(quote_summary['quoteSummary']['result'][0], modules)


def _assert_timeseries_response_json(
    timeseries: dict[str, Any], types: str, ticker: str
) -> None:
    _assert_response_json(timeseries, TimeseriesResponseJson)
    _assert_timeseries_result(timeseries['timeseries']['result'], ticker, types)


def _assert_options_response_json(options: dict[str, Any], ticker: str) -> None:
    _assert_response_json(options, OptionsResponseJson)
    _assert_options_result(options['optionChain']['result'][0], ticker)


def _assert_recommendations_response_json(
    recommendations: dict[str, Any], tickers: str
) -> None:
    _assert_response_json(recommendations, RecommendationsResponseJson)
    _assert_recommendations_result_list(recommendations['finance']['result'], tickers)


def _assert_insights_response_json(insights: dict[str, Any], tickers: str) -> None:
    _assert_response_json(insights, InsightsResponseJson)
    _assert_insights_result_list(insights['finance']['result'], tickers)


def _assert_market_summary_response_json(market_summaries: dict[str, Any]) -> None:
    _assert_response_json(market_summaries, MarketSummaryResponseJson)
    _assert_market_summary_result_list(
        market_summaries['marketSummaryResponse']['result']
    )


def _assert_trending_response_json(trending: dict[str, Any]) -> None:
    _assert_response_json(trending, TrendingResponseJson)
    _assert_trending_result(trending['finance']['result'][0])


def _assert_currencies_response_json(currencies: dict[str, Any]) -> None:
    _assert_response_json(currencies, CurrenciesResponseJson)
    _assert_currencies_result_list(currencies['currencies']['result'])


def _assert_calendar_events_response_json(calendar_events: dict[str, Any]) -> None:
    _assert_response_json(calendar_events, CalendarEventsResponseJson)
    _assert_calendar_events_result(calendar_events['finance']['result'])
