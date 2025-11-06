from typing import Type, TypeVar

from typeguard import check_type

from yafin.types import (
    AnalysisResponseJson,
    AssetProfile,
    BalanceSheetItem,
    CalendarEvents,
    CalendarEventsFinanceResult,
    CalendarEventsResponseJson,
    CashflowItem,
    ChartResponseJson,
    ChartResult,
    CurrenciesResponseJson,
    CurrenciesResult,
    DefaultKeyStatistics,
    Earnings,
    EarningsHistoryItem,
    EarningsTrendItem,
    FinancialData,
    FundOwnershipItem,
    IncomeStatementItem,
    IndexTrend,
    IndustryTrend,
    InsiderHolderItem,
    InsiderTransactionItem,
    InsightsFinanceResult,
    InsightsResponseJson,
    InstitutionOwnershipItem,
    MajorDirectHolders,
    MajorHoldersBreakdown,
    MarketSummaryResponseJson,
    MarketSummaryResponseResult,
    NetSharePurchaseActivity,
    OptionChainResult,
    OptionsResponseJson,
    PageViews,
    Price,
    QuoteResponseJson,
    QuoteResult,
    QuoteSummaryModuleReturnValue,
    QuoteSummaryResponseJson,
    QuoteSummaryResult,
    QuoteTypeItem,
    QuoteTypeResponseJson,
    QuoteTypeResult,
    RatingsResponseJson,
    RecommendationsFinanceResult,
    RecommendationsResponseJson,
    RecommendationTrendItem,
    ResponseJson,
    SearchResponseJson,
    SecFilings,
    SectorTrend,
    SummaryDetail,
    SummaryProfile,
    TimeseriesResponseJson,
    TimeseriesResult,
    TrendingFinanceResult,
    TrendingResponseJson,
    UpgradeDowngradeHistoryItem,
)

T = TypeVar('T', bound=ResponseJson)


def _assert_response_json(response_json: ResponseJson, typ: Type[T]) -> None:
    key_map = {
        ChartResponseJson: 'chart',
        QuoteResponseJson: 'quoteResponse',
        QuoteTypeResponseJson: 'quoteType',
        QuoteSummaryResponseJson: 'quoteSummary',
        TimeseriesResponseJson: 'timeseries',
        OptionsResponseJson: 'optionChain',
        RecommendationsResponseJson: 'finance',
        InsightsResponseJson: 'finance',
        MarketSummaryResponseJson: 'marketSummaryResponse',
        TrendingResponseJson: 'finance',
        CurrenciesResponseJson: 'currencies',
        CalendarEventsResponseJson: 'finance',
    }
    assert response_json
    assert check_type(response_json, typ)
    key = key_map[typ]
    assert response_json[key]['error'] is None  # type: ignore[literal-required]


def _assert_chart_result(chart_result: ChartResult, ticker: str) -> None:
    assert chart_result
    assert check_type(chart_result, ChartResult)
    assert chart_result['meta']['symbol'] == ticker


def _assert_chart_response_json(chart: ChartResponseJson, ticker: str) -> None:
    _assert_response_json(chart, ChartResponseJson)
    _assert_chart_result(chart['chart']['result'][0], ticker)


def _assert_quote_result(quote_result: QuoteResult, ticker: str) -> None:
    assert quote_result
    assert check_type(quote_result, QuoteResult)
    assert quote_result['symbol'] == ticker


def _assert_quote_response_json(quotes: QuoteResponseJson, tickers: str) -> None:
    _assert_response_json(quotes, QuoteResponseJson)
    tickers_list = tickers.split(',')
    quotes_list = quotes['quoteResponse']['result']
    assert len(quotes_list) == len(tickers_list)
    for ticker, quote in zip(
        sorted(tickers_list), sorted(quotes_list, key=lambda result: result['symbol'])
    ):
        _assert_quote_result(quote, ticker)


def _assert_quote_type_result(quote_type_result: QuoteTypeResult, ticker: str) -> None:
    assert quote_type_result
    assert check_type(quote_type_result, QuoteTypeResult)
    assert quote_type_result['symbol'] == ticker


def _assert_quote_type_response_json(
    quote_types: QuoteTypeResponseJson, tickers: str
) -> None:
    _assert_response_json(quote_types, QuoteTypeResponseJson)
    tickers_list = tickers.split(',')
    quote_types_list = quote_types['quoteType']['result']
    assert len(quote_types_list) == len(tickers_list)
    for ticker, quote in zip(
        sorted(tickers_list),
        sorted(quote_types_list, key=lambda result: result['symbol']),
    ):
        _assert_quote_type_result(quote, ticker)


def _assert_quote_summary_single_module_result(
    quote_summary_single_module_result: QuoteSummaryModuleReturnValue,
    module: str,
) -> None:
    type_map = {
        'assetProfile': AssetProfile,
        'recommendationTrend': list[RecommendationTrendItem],
        'incomeStatementHistory': list[IncomeStatementItem],
        'incomeStatementHistoryQuarterly': list[IncomeStatementItem],
        'balanceSheetHistory': list[BalanceSheetItem],
        'balanceSheetHistoryQuarterly': list[BalanceSheetItem],
        'cashflowStatementHistory': list[CashflowItem],
        'cashflowStatementHistoryQuarterly': list[CashflowItem],
        'indexTrend': IndexTrend,
        'defaultKeyStatistics': DefaultKeyStatistics,
        'industryTrend': IndustryTrend,
        'quoteType': QuoteTypeItem,
        'fundOwnership': list[FundOwnershipItem],
        'summaryDetail': SummaryDetail,
        'insiderHolders': list[InsiderHolderItem],
        'calendarEvents': CalendarEvents,
        'upgradeDowngradeHistory': list[UpgradeDowngradeHistoryItem],
        'price': Price,
        'earningsTrend': list[EarningsTrendItem],
        'secFilings': SecFilings,
        'institutionOwnership': list[InstitutionOwnershipItem],
        'majorHoldersBreakdown': MajorHoldersBreakdown,
        'earningsHistory': list[EarningsHistoryItem],
        'majorDirectHolders': MajorDirectHolders,
        'summaryProfile': SummaryProfile,
        'netSharePurchaseActivity': NetSharePurchaseActivity,
        'insiderTransactions': list[InsiderTransactionItem],
        'sectorTrend': SectorTrend,
        'earnings': Earnings,
        'pageViews': PageViews,
        'financialData': FinancialData,
    }
    assert quote_summary_single_module_result
    assert check_type(quote_summary_single_module_result, type_map[module])


def _assert_quote_summary_result(
    quote_summary_result: QuoteSummaryResult, modules: str
) -> None:
    assert quote_summary_result
    assert check_type(quote_summary_result, QuoteSummaryResult)
    assert sorted(quote_summary_result.keys()) == sorted(modules.split(','))


def _assert_quote_summary_response_json(
    quote_summary: QuoteSummaryResponseJson, modules: str
) -> None:
    _assert_response_json(quote_summary, QuoteSummaryResponseJson)
    _assert_quote_summary_result(quote_summary['quoteSummary']['result'][0], modules)


def _assert_timeseries_result(
    timeseries_results: list[TimeseriesResult], types: str, ticker: str
) -> None:
    assert timeseries_results
    assert check_type(timeseries_results, list[TimeseriesResult])
    timeseries_result_types = [
        result['meta']['type'][0] for result in timeseries_results
    ]
    assert sorted(timeseries_result_types) == sorted(types.split(','))
    timeseries_result_symbols = [
        result['meta']['symbol'][0] == ticker for result in timeseries_results
    ]
    assert all(timeseries_result_symbols)


def _assert_timeseries_response_json(
    timeseries: TimeseriesResponseJson, types: str, ticker: str
) -> None:
    _assert_response_json(timeseries, TimeseriesResponseJson)
    _assert_timeseries_result(timeseries['timeseries']['result'], types, ticker)


def _assert_options_result(options_result: OptionChainResult, ticker: str) -> None:
    assert options_result
    assert check_type(options_result, OptionChainResult)
    assert options_result['underlyingSymbol'] == ticker
    assert options_result['quote']['symbol'] == ticker


def _assert_options_response_json(options: OptionsResponseJson, ticker: str) -> None:
    _assert_response_json(options, OptionsResponseJson)
    _assert_options_result(options['optionChain']['result'][0], ticker)


def _assert_search_response_json(search: SearchResponseJson) -> None:
    assert search
    assert check_type(search, SearchResponseJson)


def _assert_recommendation_result(
    recommendation_result: RecommendationsFinanceResult, ticker: str
) -> None:
    assert recommendation_result
    assert check_type(recommendation_result, RecommendationsFinanceResult)
    assert recommendation_result['symbol'] == ticker


def _assert_recommendations_response_json(
    recommendations: RecommendationsResponseJson, tickers: str
) -> None:
    _assert_response_json(recommendations, RecommendationsResponseJson)
    tickers_list = tickers.split(',')
    recommendations_list = recommendations['finance']['result']
    assert len(recommendations_list) == len(tickers_list)
    for ticker, insight in zip(
        sorted(tickers_list),
        sorted(recommendations_list, key=lambda result: result['symbol']),
    ):
        _assert_recommendation_result(insight, ticker)


def _assert_insight_result(insights_result: InsightsFinanceResult, ticker: str) -> None:
    assert insights_result
    assert check_type(insights_result, InsightsFinanceResult)
    assert insights_result['symbol'] == ticker


def _assert_insights_response_json(
    insights: InsightsResponseJson, tickers: str
) -> None:
    _assert_response_json(insights, InsightsResponseJson)
    tickers_list = tickers.split(',')
    insights_list = insights['finance']['result']
    assert len(insights_list) == len(tickers_list)
    for ticker, insight in zip(
        sorted(tickers_list), sorted(insights_list, key=lambda result: result['symbol'])
    ):
        _assert_insight_result(insight, ticker)


def _assert_ratings_response_json(ratings: RatingsResponseJson) -> None:
    assert ratings
    assert check_type(ratings, RatingsResponseJson)


def _assert_analysis_response_json(analysis: AnalysisResponseJson, ticker: str) -> None:
    assert analysis
    assert check_type(analysis, AnalysisResponseJson)
    assert analysis['symbol'] == ticker


def _assert_market_summary_results(
    market_summary_results: list[MarketSummaryResponseResult],
) -> None:
    assert market_summary_results
    for market_summary in market_summary_results:
        assert check_type(market_summary, MarketSummaryResponseResult)


def _assert_market_summary_response_json(
    market_summaries: MarketSummaryResponseJson,
) -> None:
    _assert_response_json(market_summaries, MarketSummaryResponseJson)
    _assert_market_summary_results(market_summaries['marketSummaryResponse']['result'])


def _assert_trending_result(trending_result: TrendingFinanceResult) -> None:
    assert trending_result
    assert check_type(trending_result, TrendingFinanceResult)


def _assert_trending_response_json(trending: TrendingResponseJson) -> None:
    _assert_response_json(trending, TrendingResponseJson)
    _assert_trending_result(trending['finance']['result'][0])


def _assert_currencies_results(currencies_results: list[CurrenciesResult]) -> None:
    assert currencies_results
    for currency in currencies_results:
        assert check_type(currency, CurrenciesResult)


def _assert_currencies_response_json(currencies: CurrenciesResponseJson) -> None:
    _assert_response_json(currencies, CurrenciesResponseJson)
    _assert_currencies_results(currencies['currencies']['result'])


def _assert_calendar_events_result(
    calendar_events_result: CalendarEventsFinanceResult,
) -> None:
    assert calendar_events_result
    assert check_type(calendar_events_result, CalendarEventsFinanceResult)


def _assert_calendar_events_response_json(
    calendar_events: CalendarEventsResponseJson,
) -> None:
    _assert_response_json(calendar_events, CalendarEventsResponseJson)
    _assert_calendar_events_result(calendar_events['finance']['result'])
