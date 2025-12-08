from typing import Any, NotRequired, TypeAlias, TypedDict

Error: TypeAlias = dict[str, Any] | None


class Format(TypedDict):
    raw: NotRequired[int | float]
    fmt: NotRequired[str | float | None]
    longFmt: NotRequired[str]


class ChartResultMeta(TypedDict):
    currency: str
    symbol: str
    exchangeName: str
    fullExchangeName: str
    instrumentType: str
    firstTradeDate: int
    regularMarketTime: int
    hasPrePostMarketData: bool
    gmtoffset: int
    timezone: str
    exchangeTimezoneName: str
    regularMarketPrice: float
    fiftyTwoWeekHigh: float
    fiftyTwoWeekLow: float
    regularMarketDayHigh: float
    regularMarketDayLow: float
    regularMarketVolume: int
    longName: str
    shortName: str
    chartPreviousClose: float
    priceHint: int
    currentTradingPeriod: dict[str, Any]
    dataGranularity: str
    range: str
    validRanges: list[str]


class DividendEvent(TypedDict):
    amount: float
    date: int


class SplitEvent(TypedDict):
    date: int
    numerator: int
    denominator: int
    splitRatio: str


class ChartResultEvents(TypedDict):
    dividends: NotRequired[dict[str, DividendEvent]]
    splits: NotRequired[dict[str, SplitEvent]]


class ChartResultIndicatorsQuote(TypedDict):
    low: list[float]
    close: list[float]
    high: list[float]
    open: list[float]
    volume: list[int]


class ChartResultIndicators(TypedDict):
    quote: list[ChartResultIndicatorsQuote]
    adjclose: list[dict[str, list[float]]]


class ChartResult(TypedDict):
    meta: ChartResultMeta
    timestamp: list[int]
    events: ChartResultEvents
    indicators: ChartResultIndicators


class Chart(TypedDict):
    result: list[ChartResult]
    error: Error


class ChartResponseJson(TypedDict):
    chart: Chart


class QuoteResult(TypedDict):
    language: str
    region: str
    quoteType: str
    typeDisp: str
    quoteSourceName: str
    triggerable: bool
    customPriceAlertConfidence: str
    currency: str
    marketState: str
    shortName: str
    longName: str
    hasPrePostMarketData: bool
    firstTradeDateMilliseconds: int
    priceHint: int
    preMarketChange: NotRequired[float]
    preMarketChangePercent: NotRequired[float]
    preMarketPrice: NotRequired[float]
    postMarketChangePercent: NotRequired[float]
    postMarketPrice: NotRequired[float]
    postMarketChange: NotRequired[float]
    regularMarketChange: float
    regularMarketDayHigh: float
    regularMarketDayRange: str
    regularMarketDayLow: float
    regularMarketVolume: int
    regularMarketPreviousClose: float
    bid: float
    ask: float
    bidSize: int
    askSize: int
    fullExchangeName: str
    financialCurrency: str
    regularMarketOpen: float
    averageDailyVolume3Month: int
    averageDailyVolume10Day: int
    fiftyTwoWeekLowChange: float
    fiftyTwoWeekLowChangePercent: float
    fiftyTwoWeekRange: str
    fiftyTwoWeekHighChange: float
    fiftyTwoWeekHighChangePercent: float
    fiftyTwoWeekLow: float
    fiftyTwoWeekHigh: float
    fiftyTwoWeekChangePercent: float
    dividendDate: NotRequired[int]
    earningsTimestamp: int
    earningsTimestampStart: int
    earningsTimestampEnd: int
    earningsCallTimestampStart: int
    earningsCallTimestampEnd: int
    isEarningsDateEstimate: bool
    trailingAnnualDividendRate: float
    trailingPE: float
    dividendRate: NotRequired[float]
    trailingAnnualDividendYield: float
    dividendYield: NotRequired[float]
    epsTrailingTwelveMonths: float
    epsForward: float
    epsCurrentYear: float
    priceEpsCurrentYear: float
    corporateActions: list[Any]
    preMarketTime: NotRequired[int]
    postMarketTime: NotRequired[int]
    regularMarketTime: int
    exchange: str
    messageBoardId: str
    exchangeTimezoneName: str
    exchangeTimezoneShortName: str
    gmtOffSetMilliseconds: int
    market: str
    esgPopulated: bool
    regularMarketChangePercent: float
    regularMarketPrice: float
    sharesOutstanding: int
    bookValue: float
    fiftyDayAverage: float
    fiftyDayAverageChange: float
    fiftyDayAverageChangePercent: float
    twoHundredDayAverage: float
    twoHundredDayAverageChange: float
    twoHundredDayAverageChangePercent: float
    marketCap: int
    forwardPE: float
    priceToBook: float
    sourceInterval: int
    exchangeDataDelayedBy: int
    ipoExpectedDate: NotRequired[str]
    prevName: NotRequired[str]
    nameChangeDate: NotRequired[str]
    averageAnalystRating: str
    tradeable: bool
    cryptoTradeable: bool
    displayName: NotRequired[str]
    symbol: str


class QuoteResponse(TypedDict):
    result: list[QuoteResult]
    error: Error


class QuoteResponseJson(TypedDict):
    quoteResponse: QuoteResponse


class QuoteTypeResult(TypedDict):
    symbol: str
    quoteType: str
    quartrId: str
    exchange: str
    shortName: str
    longName: str
    messageBoardId: str
    exchangeTimezoneName: str
    exchangeTimezoneShortName: str
    gmtOffSetMilliseconds: str
    market: str
    isEsgPopulated: bool
    hasSelerityEarnings: bool
    selerityIsGaap: bool


class QuoteType(TypedDict):
    result: list[QuoteTypeResult]
    error: Error


class QuoteTypeResponseJson(TypedDict):
    quoteType: QuoteType


class CompanyOfficer(TypedDict):
    maxAge: int
    name: str
    age: int
    title: str
    yearBorn: int
    fiscalYear: int
    totalPay: Format
    exercisedValue: Format
    unexercisedValue: Format


class AssetProfile(TypedDict):
    address1: str
    city: str
    state: str
    zip: str
    country: str
    phone: str
    website: str
    industry: str
    industryKey: str
    industryDisp: str
    sector: str
    sectorKey: str
    sectorDisp: str
    longBusinessSummary: str
    fullTimeEmployees: int
    companyOfficers: list[CompanyOfficer]
    auditRisk: int
    boardRisk: int
    compensationRisk: int
    shareHolderRightsRisk: int
    overallRisk: int
    governanceEpochDate: int
    compensationAsOfEpochDate: int
    executiveTeam: list[Any]
    maxAge: int
    irWebsite: NotRequired[str]


class RecommendationTrendItem(TypedDict):
    period: str
    strongBuy: int
    buy: int
    hold: int
    sell: int
    strongSell: int


class RecommendationTrend(TypedDict):
    trend: list[RecommendationTrendItem]
    maxAge: int


class IncomeStatementItem(TypedDict):
    maxAge: int
    endDate: Format
    totalRevenue: Format
    costOfRevenue: Format
    grossProfit: Format
    researchDevelopment: Format
    sellingGeneralAdministrative: Format
    nonRecurring: Format
    otherOperatingExpenses: Format
    totalOperatingExpenses: Format
    operatingIncome: Format
    totalOtherIncomeExpenseNet: Format
    ebit: Format
    interestExpense: Format
    incomeBeforeTax: Format
    incomeTaxExpense: Format
    minorityInterest: Format
    netIncomeFromContinuingOps: Format
    discontinuedOperations: Format
    extraordinaryItems: Format
    effectOfAccountingCharges: Format
    otherItems: Format
    netIncome: Format
    netIncomeApplicableToCommonShares: Format


class IncomeStatementHistory(TypedDict):
    incomeStatementHistory: list[IncomeStatementItem]
    maxAge: int


class IncomeStatementHistoryQuarterly(TypedDict):
    incomeStatementHistory: list[IncomeStatementItem]
    maxAge: int


class BalanceSheetItem(TypedDict):
    maxAge: int
    endDate: Format


class BalanceSheetHistory(TypedDict):
    balanceSheetStatements: list[BalanceSheetItem]
    maxAge: int


class BalanceSheetHistoryQuarterly(TypedDict):
    balanceSheetStatements: list[BalanceSheetItem]
    maxAge: int


class CashflowItem(TypedDict):
    maxAge: int
    endDate: Format
    netIncome: Format


class CashflowStatementHistory(TypedDict):
    cashflowStatements: list[CashflowItem]
    maxAge: int


class CashflowStatementHistoryQuarterly(TypedDict):
    cashflowStatements: list[CashflowItem]
    maxAge: int


class IndexTrend(TypedDict):
    maxAge: int
    symbol: str
    estimates: list[dict[str, Any]]


class DefaultKeyStatistics(TypedDict):
    maxAge: int
    priceHint: int
    enterpriseValue: int
    forwardPE: float
    profitMargins: float
    floatShares: int
    sharesOutstanding: int
    sharesShort: int
    sharesShortPriorMonth: int
    sharesShortPreviousMonthDate: int
    dateShortInterest: int
    sharesPercentSharesOut: float
    heldPercentInsiders: float
    heldPercentInstitutions: float
    shortRatio: float
    shortPercentOfFloat: float
    beta: float
    impliedSharesOutstanding: int
    category: None
    bookValue: float
    priceToBook: float
    fundFamily: None
    legalType: None
    lastFiscalYearEnd: int
    nextFiscalYearEnd: int
    mostRecentQuarter: int
    earningsQuarterlyGrowth: float
    netIncomeToCommon: int
    trailingEps: float
    forwardEps: float
    lastSplitFactor: str | None
    enterpriseToRevenue: float
    enterpriseToEbitda: float
    SandP52WeekChange: float
    lastDividendValue: float
    lastDividendDate: int
    latestShareClass: None
    leadInvestor: None
    lastSplitDate: NotRequired[int]


DefaultKeyStatistics.__annotations__['52WeekChange'] = float


class IndustryTrend(TypedDict):
    maxAge: int
    symbol: None
    estimates: list[Any]


class QuoteTypeItem(TypedDict):
    exchange: str
    quoteType: str
    symbol: str
    underlyingSymbol: str
    shortName: str
    longName: str
    firstTradeDateEpochUtc: int
    timeZoneFullName: str
    timeZoneShortName: str
    uuid: str
    messageBoardId: str
    gmtOffSetMilliseconds: int
    maxAge: int


class FundOwnershipItem(TypedDict):
    maxAge: int
    reportDate: Format
    organization: str
    pctHeld: Format
    position: Format
    value: Format
    pctChange: Format


class FundOwnership(TypedDict):
    maxAge: int
    ownershipList: list[FundOwnershipItem]


class SummaryDetail(TypedDict):
    maxAge: int
    priceHint: int
    previousClose: float
    open: float
    dayLow: float
    dayHigh: float
    regularMarketPreviousClose: float
    regularMarketOpen: float
    regularMarketDayLow: float
    regularMarketDayHigh: float
    dividendRate: float
    dividendYield: float
    exDividendDate: int
    payoutRatio: float
    beta: float
    trailingPE: float
    forwardPE: float
    volume: int
    regularMarketVolume: int
    averageVolume: int
    averageVolume10days: int
    averageDailyVolume10Day: int
    bid: float
    ask: float
    bidSize: int
    askSize: int
    marketCap: int
    fiftyTwoWeekLow: float
    fiftyTwoWeekHigh: float
    allTimeHigh: float
    allTimeLow: float
    priceToSalesTrailing12Months: float
    fiftyDayAverage: float
    twoHundredDayAverage: float
    trailingAnnualDividendRate: float
    trailingAnnualDividendYield: float
    currency: str
    fromCurrency: None
    toCurrency: None
    lastMarket: None
    coinMarketCapLink: None
    algorithm: None
    tradeable: bool
    fiveYearAvgDividendYield: NotRequired[float]


class InsiderHolderItem(TypedDict):
    maxAge: int
    name: str
    relation: str
    url: str
    transactionDescription: str
    latestTransDate: Format
    positionDirect: NotRequired[Format]
    positionDirectDate: NotRequired[Format]
    positionIndirect: NotRequired[Format]
    positionIndirectDate: NotRequired[Format]


class InsiderHolders(TypedDict):
    holders: list[InsiderHolderItem]
    maxAge: int


class CalendarEventEarnings(TypedDict):
    earningsDate: list[int]
    earningsCallDate: list[int]
    isEarningsDateEstimate: bool
    earningsAverage: float
    earningsLow: float
    earningsHigh: float
    revenueAverage: int
    revenueLow: int
    revenueHigh: int


class CalendarEvents(TypedDict):
    maxAge: int
    earnings: CalendarEventEarnings
    exDividendDate: int
    dividendDate: int


class UpgradeDowngradeHistoryItem(TypedDict):
    epochGradeDate: int
    firm: str
    toGrade: str
    fromGrade: str
    action: str
    priceTargetAction: str
    currentPriceTarget: float
    priorPriceTarget: float


class UpgradeDowngradeHistory(TypedDict):
    history: list[UpgradeDowngradeHistoryItem]
    maxAge: int


class Price(TypedDict):
    maxAge: int
    preMarketSource: NotRequired[str]
    preMarketChangePercent: NotRequired[float]
    preMarketChange: NotRequired[float]
    preMarketTime: NotRequired[int]
    preMarketPrice: NotRequired[float]
    postMarketChangePercent: NotRequired[float]
    postMarketChange: NotRequired[float]
    postMarketTime: NotRequired[int]
    postMarketPrice: NotRequired[float]
    postMarketSource: NotRequired[str]
    regularMarketChangePercent: float
    regularMarketChange: float
    regularMarketTime: int
    priceHint: int
    regularMarketPrice: float
    regularMarketDayHigh: float
    regularMarketDayLow: float
    regularMarketVolume: int
    averageDailyVolume10Day: NotRequired[int]
    averageDailyVolume3Month: NotRequired[int]
    regularMarketPreviousClose: float
    regularMarketSource: str
    regularMarketOpen: float
    overnightMarketSource: NotRequired[str]
    overnightMarketChangePercent: NotRequired[float]
    overnightMarketChange: NotRequired[float]
    overnightMarketTime: NotRequired[int]
    overnightMarketPrice: NotRequired[float]
    exchange: str
    exchangeName: str
    exchangeDataDelayedBy: int
    marketState: str
    quoteType: str
    symbol: str
    underlyingSymbol: None
    shortName: str
    longName: str
    currency: str
    quoteSourceName: str
    currencySymbol: str
    fromCurrency: None
    toCurrency: None
    lastMarket: None
    marketCap: int


class EarningsTrendItem(TypedDict):
    maxAge: int
    period: str
    endDate: str
    growth: Format
    earningsEstimate: dict[str, Any]
    revenueEstimate: dict[str, Any]
    epsTrend: dict[str, Any]
    epsRevisions: dict[str, Any]


class EarningsTrend(TypedDict):
    trend: list[EarningsTrendItem]
    defaultMethodology: str
    maxAge: int


class SecFilingsItem(TypedDict):
    date: str
    epochDate: int
    type: str
    title: str
    edgarUrl: str
    exhibits: list[dict[str, Any]]
    maxAge: int


class SecFilings(TypedDict):
    filings: list[SecFilingsItem]
    maxAge: int


class InstitutionOwnershipItem(TypedDict):
    maxAge: int
    reportDate: Format
    organization: str
    pctHeld: Format
    position: Format
    value: Format
    pctChange: Format


class InstitutionOwnership(TypedDict):
    maxAge: int
    ownershipList: list[InstitutionOwnershipItem]


class MajorHoldersBreakdown(TypedDict):
    maxAge: int
    insidersPercentHeld: float
    institutionsPercentHeld: float
    institutionsFloatPercentHeld: float
    institutionsCount: int


class EarningsHistoryItem(TypedDict):
    maxAge: int
    epsActual: Format
    epsEstimate: Format
    epsDifference: Format
    surprisePercent: Format
    quarter: Format
    currency: str
    period: str


class EarningsHistory(TypedDict):
    history: list[EarningsHistoryItem]
    defaultMethodology: str
    maxAge: int


class MajorDirectHolders(TypedDict):
    holders: list[Any]
    maxAge: int


class SummaryProfile(TypedDict):
    address1: str
    city: str
    state: str
    zip: str
    country: str
    phone: str
    website: str
    industry: str
    industryKey: str
    industryDisp: str
    sector: str
    sectorKey: str
    sectorDisp: str
    longBusinessSummary: str
    fullTimeEmployees: int
    companyOfficers: list[Any]
    executiveTeam: list[Any]
    maxAge: int
    irWebsite: NotRequired[str]


class NetSharePurchaseActivity(TypedDict):
    maxAge: int
    period: str
    buyInfoCount: int
    buyInfoShares: int
    sellInfoCount: int
    netInfoCount: int
    netInfoShares: int
    totalInsiderShares: int
    sellPercentInsiderShares: NotRequired[float]
    sellInfoShares: NotRequired[int]
    netPercentInsiderShares: NotRequired[float]
    buyPercentInsiderShares: NotRequired[float]


class InsiderTransactionItem(TypedDict):
    maxAge: int
    shares: Format
    value: Format
    filerUrl: str
    transactionText: str
    filerName: str
    filerRelation: str
    moneyText: str
    startDate: Format
    ownership: str


class InsiderTransactions(TypedDict):
    transactions: list[InsiderTransactionItem]
    maxAge: int


class SectorTrend(TypedDict):
    maxAge: int
    symbol: None
    estimates: list[Any]


class Earnings(TypedDict):
    maxAge: int
    earningsChart: dict[str, Any]
    financialsChart: dict[str, Any]
    financialCurrency: str
    defaultMethodology: str


class PageViews(TypedDict):
    shortTermTrend: str
    midTermTrend: str
    longTermTrend: str
    maxAge: int


class FinancialData(TypedDict):
    maxAge: int
    currentPrice: float
    targetHighPrice: float
    targetLowPrice: float
    targetMeanPrice: float
    targetMedianPrice: float
    recommendationMean: float
    recommendationKey: str
    numberOfAnalystOpinions: int
    totalCash: int
    totalCashPerShare: float
    ebitda: int
    totalDebt: int
    quickRatio: float
    currentRatio: float
    totalRevenue: int
    debtToEquity: float
    revenuePerShare: float
    returnOnAssets: float
    returnOnEquity: float
    grossProfits: int
    freeCashflow: int
    operatingCashflow: int
    earningsGrowth: float
    revenueGrowth: float
    grossMargins: float
    ebitdaMargins: float
    operatingMargins: float
    profitMargins: float
    financialCurrency: str


class QuoteSummaryResult(TypedDict):
    assetProfile: NotRequired[AssetProfile]
    recommendationTrend: NotRequired[RecommendationTrend]
    incomeStatementHistory: NotRequired[IncomeStatementHistory]
    incomeStatementHistoryQuarterly: NotRequired[IncomeStatementHistoryQuarterly]
    balanceSheetHistory: NotRequired[BalanceSheetHistory]
    balanceSheetHistoryQuarterly: NotRequired[BalanceSheetHistoryQuarterly]
    cashflowStatementHistory: NotRequired[CashflowStatementHistory]
    cashflowStatementHistoryQuarterly: NotRequired[CashflowStatementHistoryQuarterly]
    indexTrend: NotRequired[IndexTrend]
    defaultKeyStatistics: NotRequired[DefaultKeyStatistics]
    industryTrend: NotRequired[IndustryTrend]
    quoteType: NotRequired[QuoteTypeItem]
    fundOwnership: NotRequired[FundOwnership]
    summaryDetail: NotRequired[SummaryDetail]
    insiderHolders: NotRequired[InsiderHolders]
    calendarEvents: NotRequired[CalendarEvents]
    upgradeDowngradeHistory: NotRequired[UpgradeDowngradeHistory]
    price: NotRequired[Price]
    earningsTrend: NotRequired[EarningsTrend]
    secFilings: NotRequired[SecFilings]
    institutionOwnership: NotRequired[InstitutionOwnership]
    majorHoldersBreakdown: NotRequired[MajorHoldersBreakdown]
    earningsHistory: NotRequired[EarningsHistory]
    majorDirectHolders: NotRequired[MajorDirectHolders]
    summaryProfile: NotRequired[SummaryProfile]
    netSharePurchaseActivity: NotRequired[NetSharePurchaseActivity]
    insiderTransactions: NotRequired[InsiderTransactions]
    sectorTrend: NotRequired[SectorTrend]
    earnings: NotRequired[Earnings]
    pageViews: NotRequired[PageViews]
    financialData: NotRequired[FinancialData]


class QuoteSummary(TypedDict):
    result: list[QuoteSummaryResult]
    error: Error


class QuoteSummaryResponseJson(TypedDict):
    quoteSummary: QuoteSummary


class TimeseriesResultMeta(TypedDict):
    symbol: list[str]
    type: list[str]


class TimeseriesResultItem(TypedDict):
    dataId: int
    asOfDate: str
    periodType: str
    currencyCode: str
    reportedValue: Format
    businessSegmentData: NotRequired[list[dict[str, Any]]]
    geographicSegmentData: NotRequired[list[dict[str, Any]]]


class TimeseriesResult(TypedDict):
    meta: TimeseriesResultMeta
    timestamp: NotRequired[list[int]]
    EnterpriseValue: NotRequired[list[TimeseriesResultItem]]
    EnterprisesValueEBITDARatio: NotRequired[list[TimeseriesResultItem]]
    EnterprisesValueRevenueRatio: NotRequired[list[TimeseriesResultItem]]
    ForwardPeRatio: NotRequired[list[TimeseriesResultItem]]
    MarketCap: NotRequired[list[TimeseriesResultItem]]
    PbRatio: NotRequired[list[TimeseriesResultItem]]
    PeRatio: NotRequired[list[TimeseriesResultItem]]
    PegRatio: NotRequired[list[TimeseriesResultItem]]
    PsRatio: NotRequired[list[TimeseriesResultItem]]
    analystRatings: NotRequired[list[TimeseriesResultItem]]
    annualAccountsPayable: NotRequired[list[TimeseriesResultItem]]
    annualAccountsReceivable: NotRequired[list[TimeseriesResultItem]]
    annualAccruedInterestReceivable: NotRequired[list[TimeseriesResultItem]]
    annualAccumulatedDepreciation: NotRequired[list[TimeseriesResultItem]]
    annualAdditionalPaidInCapital: NotRequired[list[TimeseriesResultItem]]
    annualAdjustedGeographySegmentData: NotRequired[list[TimeseriesResultItem]]
    annualAllowanceForDoubtfulAccountsReceivable: NotRequired[
        list[TimeseriesResultItem | None]
    ]
    annualAmortization: NotRequired[list[TimeseriesResultItem]]
    annualAmortizationCashFlow: NotRequired[list[TimeseriesResultItem]]
    annualAmortizationOfIntangibles: NotRequired[list[TimeseriesResultItem]]
    annualAmortizationOfIntangiblesIncomeStatement: NotRequired[
        list[TimeseriesResultItem]
    ]
    annualAmortizationOfSecurities: NotRequired[list[TimeseriesResultItem]]
    annualAssetImpairmentCharge: NotRequired[list[TimeseriesResultItem]]
    annualAssetsHeldForSaleCurrent: NotRequired[list[TimeseriesResultItem]]
    annualAvailableForSaleSecurities: NotRequired[list[TimeseriesResultItem]]
    annualAverageDilutionEarnings: NotRequired[list[TimeseriesResultItem]]
    annualBasicAccountingChange: NotRequired[list[TimeseriesResultItem]]
    annualBasicAverageShares: NotRequired[list[TimeseriesResultItem]]
    annualBasicContinuousOperations: NotRequired[list[TimeseriesResultItem]]
    annualBasicDiscontinuousOperations: NotRequired[list[TimeseriesResultItem]]
    annualBasicEPS: NotRequired[list[TimeseriesResultItem]]
    annualBasicEPSOtherGainsLosses: NotRequired[list[TimeseriesResultItem]]
    annualBasicExtraordinary: NotRequired[list[TimeseriesResultItem]]
    annualBeginningCashPosition: NotRequired[list[TimeseriesResultItem]]
    annualBuildingsAndImprovements: NotRequired[list[TimeseriesResultItem]]
    annualCapitalExpenditure: NotRequired[list[TimeseriesResultItem]]
    annualCapitalExpenditureReported: NotRequired[list[TimeseriesResultItem]]
    annualCapitalLeaseObligations: NotRequired[list[TimeseriesResultItem]]
    annualCapitalStock: NotRequired[list[TimeseriesResultItem]]
    annualCashAndCashEquivalents: NotRequired[list[TimeseriesResultItem]]
    annualCashCashEquivalentsAndFederalFundsSold: NotRequired[
        list[TimeseriesResultItem]
    ]
    annualCashCashEquivalentsAndShortTermInvestments: NotRequired[
        list[TimeseriesResultItem]
    ]
    annualCashDividendsPaid: NotRequired[list[TimeseriesResultItem | None]]
    annualCashEquivalents: NotRequired[list[TimeseriesResultItem]]
    annualCashFinancial: NotRequired[list[TimeseriesResultItem]]
    annualCashFlowFromContinuingFinancingActivities: NotRequired[
        list[TimeseriesResultItem]
    ]
    annualCashFlowFromContinuingInvestingActivities: NotRequired[
        list[TimeseriesResultItem]
    ]
    annualCashFlowFromContinuingOperatingActivities: NotRequired[
        list[TimeseriesResultItem]
    ]
    annualCashFlowFromDiscontinuedOperation: NotRequired[list[TimeseriesResultItem]]
    annualCashFlowsfromusedinOperatingActivitiesDirect: NotRequired[
        list[TimeseriesResultItem]
    ]
    annualCashFromDiscontinuedFinancingActivities: NotRequired[
        list[TimeseriesResultItem]
    ]
    annualCashFromDiscontinuedInvestingActivities: NotRequired[
        list[TimeseriesResultItem]
    ]
    annualCashFromDiscontinuedOperatingActivities: NotRequired[
        list[TimeseriesResultItem]
    ]
    annualChangeInAccountPayable: NotRequired[list[TimeseriesResultItem]]
    annualChangeInAccruedExpense: NotRequired[list[TimeseriesResultItem]]
    annualChangeInDividendPayable: NotRequired[list[TimeseriesResultItem]]
    annualChangeInIncomeTaxPayable: NotRequired[list[TimeseriesResultItem]]
    annualChangeInInterestPayable: NotRequired[list[TimeseriesResultItem]]
    annualChangeInInventory: NotRequired[list[TimeseriesResultItem]]
    annualChangeInOtherCurrentAssets: NotRequired[list[TimeseriesResultItem]]
    annualChangeInOtherCurrentLiabilities: NotRequired[list[TimeseriesResultItem]]
    annualChangeInOtherWorkingCapital: NotRequired[list[TimeseriesResultItem]]
    annualChangeInPayable: NotRequired[list[TimeseriesResultItem]]
    annualChangeInPayablesAndAccruedExpense: NotRequired[list[TimeseriesResultItem]]
    annualChangeInPrepaidAssets: NotRequired[list[TimeseriesResultItem]]
    annualChangeInReceivables: NotRequired[list[TimeseriesResultItem]]
    annualChangeInTaxPayable: NotRequired[list[TimeseriesResultItem]]
    annualChangeInWorkingCapital: NotRequired[list[TimeseriesResultItem]]
    annualChangesInAccountReceivables: NotRequired[list[TimeseriesResultItem]]
    annualChangesInCash: NotRequired[list[TimeseriesResultItem]]
    annualClassesofCashPayments: NotRequired[list[TimeseriesResultItem]]
    annualClassesofCashReceiptsfromOperatingActivities: NotRequired[
        list[TimeseriesResultItem]
    ]
    annualCommercialPaper: NotRequired[list[TimeseriesResultItem]]
    annualCommonStock: NotRequired[list[TimeseriesResultItem]]
    annualCommonStockDividendPaid: NotRequired[list[TimeseriesResultItem | None]]
    annualCommonStockEquity: NotRequired[list[TimeseriesResultItem]]
    annualCommonStockIssuance: NotRequired[list[TimeseriesResultItem | None]]
    annualCommonStockPayments: NotRequired[list[TimeseriesResultItem]]
    annualConstructionInProgress: NotRequired[list[TimeseriesResultItem]]
    annualContinuingAndDiscontinuedBasicEPS: NotRequired[list[TimeseriesResultItem]]
    annualContinuingAndDiscontinuedDilutedEPS: NotRequired[list[TimeseriesResultItem]]
    annualCostOfRevenue: NotRequired[list[TimeseriesResultItem]]
    annualCurrentAccruedExpenses: NotRequired[list[TimeseriesResultItem | None]]
    annualCurrentAssets: NotRequired[list[TimeseriesResultItem]]
    annualCurrentCapitalLeaseObligation: NotRequired[list[TimeseriesResultItem]]
    annualCurrentDebt: NotRequired[list[TimeseriesResultItem]]
    annualCurrentDebtAndCapitalLeaseObligation: NotRequired[list[TimeseriesResultItem]]
    annualCurrentDeferredAssets: NotRequired[list[TimeseriesResultItem]]
    annualCurrentDeferredLiabilities: NotRequired[list[TimeseriesResultItem]]
    annualCurrentDeferredRevenue: NotRequired[list[TimeseriesResultItem]]
    annualCurrentDeferredTaxesAssets: NotRequired[list[TimeseriesResultItem]]
    annualCurrentDeferredTaxesLiabilities: NotRequired[list[TimeseriesResultItem]]
    annualCurrentLiabilities: NotRequired[list[TimeseriesResultItem]]
    annualCurrentNotesPayable: NotRequired[list[TimeseriesResultItem]]
    annualCurrentProvisions: NotRequired[list[TimeseriesResultItem]]
    annualDeferredIncomeTax: NotRequired[list[TimeseriesResultItem]]
    annualDeferredTax: NotRequired[list[TimeseriesResultItem]]
    annualDefinedPensionBenefit: NotRequired[list[TimeseriesResultItem]]
    annualDepletion: NotRequired[list[TimeseriesResultItem]]
    annualDepletionIncomeStatement: NotRequired[list[TimeseriesResultItem]]
    annualDepreciation: NotRequired[list[TimeseriesResultItem]]
    annualDepreciationAmortizationDepletion: NotRequired[list[TimeseriesResultItem]]
    annualDepreciationAmortizationDepletionIncomeStatement: NotRequired[
        list[TimeseriesResultItem]
    ]
    annualDepreciationAndAmortization: NotRequired[list[TimeseriesResultItem]]
    annualDepreciationAndAmortizationInIncomeStatement: NotRequired[
        list[TimeseriesResultItem]
    ]
    annualDepreciationIncomeStatement: NotRequired[list[TimeseriesResultItem]]
    annualDerivativeProductLiabilities: NotRequired[list[TimeseriesResultItem]]
    annualDilutedAccountingChange: NotRequired[list[TimeseriesResultItem]]
    annualDilutedAverageShares: NotRequired[list[TimeseriesResultItem]]
    annualDilutedContinuousOperations: NotRequired[list[TimeseriesResultItem]]
    annualDilutedDiscontinuousOperations: NotRequired[list[TimeseriesResultItem]]
    annualDilutedEPS: NotRequired[list[TimeseriesResultItem]]
    annualDilutedEPSOtherGainsLosses: NotRequired[list[TimeseriesResultItem]]
    annualDilutedExtraordinary: NotRequired[list[TimeseriesResultItem]]
    annualDilutedNIAvailtoComStockholders: NotRequired[list[TimeseriesResultItem]]
    annualDividendPaidCFO: NotRequired[list[TimeseriesResultItem]]
    annualDividendPerShare: NotRequired[list[TimeseriesResultItem]]
    annualDividendReceivedCFO: NotRequired[list[TimeseriesResultItem]]
    annualDividendsPaidDirect: NotRequired[list[TimeseriesResultItem]]
    annualDividendsPayable: NotRequired[list[TimeseriesResultItem]]
    annualDividendsReceivedCFI: NotRequired[list[TimeseriesResultItem]]
    annualDividendsReceivedDirect: NotRequired[list[TimeseriesResultItem]]
    annualDomesticSales: NotRequired[list[TimeseriesResultItem]]
    annualDuefromRelatedPartiesCurrent: NotRequired[list[TimeseriesResultItem]]
    annualDuefromRelatedPartiesNonCurrent: NotRequired[list[TimeseriesResultItem]]
    annualDuetoRelatedPartiesCurrent: NotRequired[list[TimeseriesResultItem]]
    annualDuetoRelatedPartiesNonCurrent: NotRequired[list[TimeseriesResultItem]]
    annualEBIT: NotRequired[list[TimeseriesResultItem]]
    annualEBITDA: NotRequired[list[TimeseriesResultItem]]
    annualEarningsFromEquityInterest: NotRequired[list[TimeseriesResultItem]]
    annualEarningsFromEquityInterestNetOfTax: NotRequired[list[TimeseriesResultItem]]
    annualEarningsLossesFromEquityInvestments: NotRequired[list[TimeseriesResultItem]]
    annualEffectOfExchangeRateChanges: NotRequired[list[TimeseriesResultItem]]
    annualEmployeeBenefits: NotRequired[list[TimeseriesResultItem]]
    annualEndCashPosition: NotRequired[list[TimeseriesResultItem]]
    annualExcessTaxBenefitFromStockBasedCompensation: NotRequired[
        list[TimeseriesResultItem]
    ]
    annualExciseTaxes: NotRequired[list[TimeseriesResultItem]]
    annualFinancialAssets: NotRequired[list[TimeseriesResultItem]]
    annualFinancialAssetsDesignatedasFairValueThroughProfitorLossTotal: NotRequired[
        list[TimeseriesResultItem]
    ]
    annualFinancingCashFlow: NotRequired[list[TimeseriesResultItem]]
    annualFinishedGoods: NotRequired[list[TimeseriesResultItem]]
    annualFixedAssetsRevaluationReserve: NotRequired[list[TimeseriesResultItem]]
    annualForeignCurrencyTranslationAdjustments: NotRequired[list[TimeseriesResultItem]]
    annualForeignSales: NotRequired[list[TimeseriesResultItem]]
    annualFreeCashFlow: NotRequired[list[TimeseriesResultItem]]
    annualGainLossOnInvestmentSecurities: NotRequired[list[TimeseriesResultItem]]
    annualGainLossOnSaleOfBusiness: NotRequired[list[TimeseriesResultItem]]
    annualGainLossOnSaleOfPPE: NotRequired[list[TimeseriesResultItem]]
    annualGainOnSaleOfBusiness: NotRequired[list[TimeseriesResultItem]]
    annualGainOnSaleOfPPE: NotRequired[list[TimeseriesResultItem]]
    annualGainOnSaleOfSecurity: NotRequired[list[TimeseriesResultItem]]
    annualGainsLossesNotAffectingRetainedEarnings: NotRequired[
        list[TimeseriesResultItem]
    ]
    annualGeneralAndAdministrativeExpense: NotRequired[list[TimeseriesResultItem]]
    annualGeneralPartnershipCapital: NotRequired[list[TimeseriesResultItem]]
    annualGoodwill: NotRequired[list[TimeseriesResultItem]]
    annualGoodwillAndOtherIntangibleAssets: NotRequired[list[TimeseriesResultItem]]
    annualGrossAccountsReceivable: NotRequired[list[TimeseriesResultItem | None]]
    annualGrossPPE: NotRequired[list[TimeseriesResultItem]]
    annualGrossProfit: NotRequired[list[TimeseriesResultItem]]
    annualHedgingAssetsCurrent: NotRequired[list[TimeseriesResultItem]]
    annualHeldToMaturitySecurities: NotRequired[list[TimeseriesResultItem]]
    annualImpairmentOfCapitalAssets: NotRequired[list[TimeseriesResultItem]]
    annualIncomeTaxPaidSupplementalData: NotRequired[list[TimeseriesResultItem]]
    annualIncomeTaxPayable: NotRequired[list[TimeseriesResultItem]]
    annualInsuranceAndClaims: NotRequired[list[TimeseriesResultItem]]
    annualInterestExpense: NotRequired[list[TimeseriesResultItem]]
    annualInterestExpenseNonOperating: NotRequired[list[TimeseriesResultItem]]
    annualInterestIncome: NotRequired[list[TimeseriesResultItem]]
    annualInterestIncomeNonOperating: NotRequired[list[TimeseriesResultItem]]
    annualInterestPaidCFF: NotRequired[list[TimeseriesResultItem]]
    annualInterestPaidCFO: NotRequired[list[TimeseriesResultItem]]
    annualInterestPaidDirect: NotRequired[list[TimeseriesResultItem]]
    annualInterestPaidSupplementalData: NotRequired[list[TimeseriesResultItem]]
    annualInterestPayable: NotRequired[list[TimeseriesResultItem]]
    annualInterestReceivedCFI: NotRequired[list[TimeseriesResultItem]]
    annualInterestReceivedCFO: NotRequired[list[TimeseriesResultItem]]
    annualInterestReceivedDirect: NotRequired[list[TimeseriesResultItem]]
    annualInventoriesAdjustmentsAllowances: NotRequired[list[TimeseriesResultItem]]
    annualInventory: NotRequired[list[TimeseriesResultItem]]
    annualInvestedCapital: NotRequired[list[TimeseriesResultItem]]
    annualInvestingCashFlow: NotRequired[list[TimeseriesResultItem]]
    annualInvestmentProperties: NotRequired[list[TimeseriesResultItem]]
    annualInvestmentinFinancialAssets: NotRequired[list[TimeseriesResultItem]]
    annualInvestmentsAndAdvances: NotRequired[list[TimeseriesResultItem]]
    annualInvestmentsInOtherVenturesUnderEquityMethod: NotRequired[
        list[TimeseriesResultItem]
    ]
    annualInvestmentsinAssociatesatCost: NotRequired[list[TimeseriesResultItem]]
    annualInvestmentsinJointVenturesatCost: NotRequired[list[TimeseriesResultItem]]
    annualInvestmentsinSubsidiariesatCost: NotRequired[list[TimeseriesResultItem]]
    annualIssuanceOfCapitalStock: NotRequired[list[TimeseriesResultItem | None]]
    annualIssuanceOfDebt: NotRequired[list[TimeseriesResultItem]]
    annualLandAndImprovements: NotRequired[list[TimeseriesResultItem]]
    annualLeases: NotRequired[list[TimeseriesResultItem]]
    annualLiabilitiesHeldforSaleNonCurrent: NotRequired[list[TimeseriesResultItem]]
    annualLimitedPartnershipCapital: NotRequired[list[TimeseriesResultItem]]
    annualLineOfCredit: NotRequired[list[TimeseriesResultItem]]
    annualLoansReceivable: NotRequired[list[TimeseriesResultItem]]
    annualLongTermCapitalLeaseObligation: NotRequired[list[TimeseriesResultItem]]
    annualLongTermDebt: NotRequired[list[TimeseriesResultItem | None]]
    annualLongTermDebtAndCapitalLeaseObligation: NotRequired[list[TimeseriesResultItem]]
    annualLongTermDebtIssuance: NotRequired[list[TimeseriesResultItem]]
    annualLongTermDebtPayments: NotRequired[list[TimeseriesResultItem]]
    annualLongTermEquityInvestment: NotRequired[list[TimeseriesResultItem]]
    annualLongTermProvisions: NotRequired[list[TimeseriesResultItem]]
    annualLossAdjustmentExpense: NotRequired[list[TimeseriesResultItem]]
    annualMachineryFurnitureEquipment: NotRequired[list[TimeseriesResultItem]]
    annualMinimumPensionLiabilities: NotRequired[list[TimeseriesResultItem]]
    annualMinorityInterest: NotRequired[list[TimeseriesResultItem]]
    annualMinorityInterests: NotRequired[list[TimeseriesResultItem]]
    annualNetBusinessPurchaseAndSale: NotRequired[list[TimeseriesResultItem]]
    annualNetCommonStockIssuance: NotRequired[list[TimeseriesResultItem]]
    annualNetDebt: NotRequired[list[TimeseriesResultItem]]
    annualNetForeignCurrencyExchangeGainLoss: NotRequired[list[TimeseriesResultItem]]
    annualNetIncome: NotRequired[list[TimeseriesResultItem]]
    annualNetIncomeCommonStockholders: NotRequired[list[TimeseriesResultItem]]
    annualNetIncomeContinuousOperations: NotRequired[list[TimeseriesResultItem]]
    annualNetIncomeDiscontinuousOperations: NotRequired[list[TimeseriesResultItem]]
    annualNetIncomeExtraordinary: NotRequired[list[TimeseriesResultItem]]
    annualNetIncomeFromContinuingAndDiscontinuedOperation: NotRequired[
        list[TimeseriesResultItem]
    ]
    annualNetIncomeFromContinuingOperationNetMinorityInterest: NotRequired[
        list[TimeseriesResultItem]
    ]
    annualNetIncomeFromContinuingOperations: NotRequired[list[TimeseriesResultItem]]
    annualNetIncomeFromTaxLossCarryforward: NotRequired[list[TimeseriesResultItem]]
    annualNetIncomeIncludingNoncontrollingInterests: NotRequired[
        list[TimeseriesResultItem]
    ]
    annualNetIntangiblesPurchaseAndSale: NotRequired[list[TimeseriesResultItem]]
    annualNetInterestIncome: NotRequired[list[TimeseriesResultItem]]
    annualNetInvestmentPropertiesPurchaseAndSale: NotRequired[
        list[TimeseriesResultItem]
    ]
    annualNetInvestmentPurchaseAndSale: NotRequired[list[TimeseriesResultItem]]
    annualNetIssuancePaymentsOfDebt: NotRequired[list[TimeseriesResultItem]]
    annualNetLongTermDebtIssuance: NotRequired[list[TimeseriesResultItem]]
    annualNetNonOperatingInterestIncomeExpense: NotRequired[list[TimeseriesResultItem]]
    annualNetOtherFinancingCharges: NotRequired[list[TimeseriesResultItem]]
    annualNetOtherInvestingChanges: NotRequired[list[TimeseriesResultItem]]
    annualNetPPE: NotRequired[list[TimeseriesResultItem]]
    annualNetPPEPurchaseAndSale: NotRequired[list[TimeseriesResultItem]]
    annualNetPolicyholderBenefitsAndClaims: NotRequired[list[TimeseriesResultItem]]
    annualNetPreferredStockIssuance: NotRequired[list[TimeseriesResultItem]]
    annualNetShortTermDebtIssuance: NotRequired[list[TimeseriesResultItem]]
    annualNetTangibleAssets: NotRequired[list[TimeseriesResultItem]]
    annualNonCurrentAccountsReceivable: NotRequired[list[TimeseriesResultItem]]
    annualNonCurrentAccruedExpenses: NotRequired[list[TimeseriesResultItem]]
    annualNonCurrentDeferredAssets: NotRequired[list[TimeseriesResultItem]]
    annualNonCurrentDeferredLiabilities: NotRequired[list[TimeseriesResultItem]]
    annualNonCurrentDeferredRevenue: NotRequired[list[TimeseriesResultItem]]
    annualNonCurrentDeferredTaxesAssets: NotRequired[list[TimeseriesResultItem]]
    annualNonCurrentDeferredTaxesLiabilities: NotRequired[list[TimeseriesResultItem]]
    annualNonCurrentNoteReceivables: NotRequired[list[TimeseriesResultItem]]
    annualNonCurrentPensionAndOtherPostretirementBenefitPlans: NotRequired[
        list[TimeseriesResultItem]
    ]
    annualNonCurrentPrepaidAssets: NotRequired[list[TimeseriesResultItem]]
    annualNormalizedBasicEPS: NotRequired[list[TimeseriesResultItem]]
    annualNormalizedDilutedEPS: NotRequired[list[TimeseriesResultItem]]
    annualNormalizedEBITDA: NotRequired[list[TimeseriesResultItem]]
    annualNormalizedIncome: NotRequired[list[TimeseriesResultItem]]
    annualNotesReceivable: NotRequired[list[TimeseriesResultItem]]
    annualOccupancyAndEquipment: NotRequired[list[TimeseriesResultItem]]
    annualOperatingCashFlow: NotRequired[list[TimeseriesResultItem]]
    annualOperatingExpense: NotRequired[list[TimeseriesResultItem]]
    annualOperatingGainsLosses: NotRequired[list[TimeseriesResultItem]]
    annualOperatingIncome: NotRequired[list[TimeseriesResultItem]]
    annualOperatingRevenue: NotRequired[list[TimeseriesResultItem]]
    annualOrdinarySharesNumber: NotRequired[list[TimeseriesResultItem]]
    annualOtherCapitalStock: NotRequired[list[TimeseriesResultItem]]
    annualOtherCashAdjustmentInsideChangeinCash: NotRequired[list[TimeseriesResultItem]]
    annualOtherCashAdjustmentOutsideChangeinCash: NotRequired[
        list[TimeseriesResultItem]
    ]
    annualOtherCashPaymentsfromOperatingActivities: NotRequired[
        list[TimeseriesResultItem]
    ]
    annualOtherCashReceiptsfromOperatingActivities: NotRequired[
        list[TimeseriesResultItem]
    ]
    annualOtherCurrentAssets: NotRequired[list[TimeseriesResultItem]]
    annualOtherCurrentBorrowings: NotRequired[list[TimeseriesResultItem]]
    annualOtherCurrentLiabilities: NotRequired[list[TimeseriesResultItem]]
    annualOtherEquityAdjustments: NotRequired[list[TimeseriesResultItem]]
    annualOtherEquityInterest: NotRequired[list[TimeseriesResultItem]]
    annualOtherGandA: NotRequired[list[TimeseriesResultItem]]
    annualOtherIncomeExpense: NotRequired[list[TimeseriesResultItem]]
    annualOtherIntangibleAssets: NotRequired[list[TimeseriesResultItem]]
    annualOtherInventories: NotRequired[list[TimeseriesResultItem]]
    annualOtherInvestments: NotRequired[list[TimeseriesResultItem]]
    annualOtherNonCashItems: NotRequired[list[TimeseriesResultItem]]
    annualOtherNonCurrentAssets: NotRequired[list[TimeseriesResultItem]]
    annualOtherNonCurrentLiabilities: NotRequired[list[TimeseriesResultItem]]
    annualOtherNonInterestExpense: NotRequired[list[TimeseriesResultItem]]
    annualOtherNonOperatingIncomeExpenses: NotRequired[list[TimeseriesResultItem]]
    annualOtherOperatingExpenses: NotRequired[list[TimeseriesResultItem]]
    annualOtherPayable: NotRequired[list[TimeseriesResultItem]]
    annualOtherProperties: NotRequired[list[TimeseriesResultItem]]
    annualOtherReceivables: NotRequired[list[TimeseriesResultItem]]
    annualOtherShortTermInvestments: NotRequired[list[TimeseriesResultItem]]
    annualOtherSpecialCharges: NotRequired[list[TimeseriesResultItem]]
    annualOtherTaxes: NotRequired[list[TimeseriesResultItem]]
    annualOtherunderPreferredStockDividend: NotRequired[
        list[TimeseriesResultItem | None]
    ]
    annualPayables: NotRequired[list[TimeseriesResultItem]]
    annualPayablesAndAccruedExpenses: NotRequired[list[TimeseriesResultItem]]
    annualPaymentsonBehalfofEmployees: NotRequired[list[TimeseriesResultItem]]
    annualPaymentstoSuppliersforGoodsandServices: NotRequired[
        list[TimeseriesResultItem]
    ]
    annualPensionAndEmployeeBenefitExpense: NotRequired[list[TimeseriesResultItem]]
    annualPensionandOtherPostRetirementBenefitPlansCurrent: NotRequired[
        list[TimeseriesResultItem]
    ]
    annualPolicyholderBenefitsCeded: NotRequired[list[TimeseriesResultItem]]
    annualPolicyholderBenefitsGross: NotRequired[list[TimeseriesResultItem]]
    annualPreferredSecuritiesOutsideStockEquity: NotRequired[list[TimeseriesResultItem]]
    annualPreferredSharesNumber: NotRequired[list[TimeseriesResultItem]]
    annualPreferredStock: NotRequired[list[TimeseriesResultItem]]
    annualPreferredStockDividendPaid: NotRequired[list[TimeseriesResultItem]]
    annualPreferredStockDividends: NotRequired[list[TimeseriesResultItem]]
    annualPreferredStockEquity: NotRequired[list[TimeseriesResultItem]]
    annualPreferredStockIssuance: NotRequired[list[TimeseriesResultItem]]
    annualPreferredStockPayments: NotRequired[list[TimeseriesResultItem]]
    annualPrepaidAssets: NotRequired[list[TimeseriesResultItem]]
    annualPretaxIncome: NotRequired[list[TimeseriesResultItem]]
    annualProceedsFromStockOptionExercised: NotRequired[list[TimeseriesResultItem]]
    annualProfessionalExpenseAndContractServicesExpense: NotRequired[
        list[TimeseriesResultItem]
    ]
    annualProperties: NotRequired[list[TimeseriesResultItem]]
    annualProvisionForDoubtfulAccounts: NotRequired[list[TimeseriesResultItem]]
    annualProvisionandWriteOffofAssets: NotRequired[list[TimeseriesResultItem]]
    annualPurchaseOfBusiness: NotRequired[list[TimeseriesResultItem]]
    annualPurchaseOfIntangibles: NotRequired[list[TimeseriesResultItem]]
    annualPurchaseOfInvestment: NotRequired[list[TimeseriesResultItem]]
    annualPurchaseOfInvestmentProperties: NotRequired[list[TimeseriesResultItem]]
    annualPurchaseOfPPE: NotRequired[list[TimeseriesResultItem]]
    annualRawMaterials: NotRequired[list[TimeseriesResultItem]]
    annualReceiptsfromCustomers: NotRequired[list[TimeseriesResultItem]]
    annualReceiptsfromGovernmentGrants: NotRequired[list[TimeseriesResultItem]]
    annualReceivables: NotRequired[list[TimeseriesResultItem]]
    annualReceivablesAdjustmentsAllowances: NotRequired[list[TimeseriesResultItem]]
    annualReconciledCostOfRevenue: NotRequired[list[TimeseriesResultItem]]
    annualReconciledDepreciation: NotRequired[list[TimeseriesResultItem]]
    annualRentAndLandingFees: NotRequired[list[TimeseriesResultItem]]
    annualRentExpenseSupplemental: NotRequired[list[TimeseriesResultItem]]
    annualRepaymentOfDebt: NotRequired[list[TimeseriesResultItem]]
    annualReportedNormalizedBasicEPS: NotRequired[list[TimeseriesResultItem]]
    annualReportedNormalizedDilutedEPS: NotRequired[list[TimeseriesResultItem]]
    annualRepurchaseOfCapitalStock: NotRequired[list[TimeseriesResultItem]]
    annualResearchAndDevelopment: NotRequired[list[TimeseriesResultItem]]
    annualRestrictedCash: NotRequired[list[TimeseriesResultItem]]
    annualRestrictedCommonStock: NotRequired[list[TimeseriesResultItem]]
    annualRestructuringAndMergernAcquisition: NotRequired[list[TimeseriesResultItem]]
    annualRetainedEarnings: NotRequired[list[TimeseriesResultItem]]
    annualSalariesAndWages: NotRequired[list[TimeseriesResultItem]]
    annualSaleOfBusiness: NotRequired[list[TimeseriesResultItem]]
    annualSaleOfIntangibles: NotRequired[list[TimeseriesResultItem]]
    annualSaleOfInvestment: NotRequired[list[TimeseriesResultItem]]
    annualSaleOfInvestmentProperties: NotRequired[list[TimeseriesResultItem]]
    annualSaleOfPPE: NotRequired[list[TimeseriesResultItem]]
    annualSecuritiesAmortization: NotRequired[list[TimeseriesResultItem]]
    annualSellingAndMarketingExpense: NotRequired[list[TimeseriesResultItem]]
    annualSellingGeneralAndAdministration: NotRequired[list[TimeseriesResultItem]]
    annualShareIssued: NotRequired[list[TimeseriesResultItem]]
    annualShortTermDebtIssuance: NotRequired[list[TimeseriesResultItem]]
    annualShortTermDebtPayments: NotRequired[list[TimeseriesResultItem]]
    annualSpecialIncomeCharges: NotRequired[list[TimeseriesResultItem]]
    annualStockBasedCompensation: NotRequired[list[TimeseriesResultItem]]
    annualStockholdersEquity: NotRequired[list[TimeseriesResultItem]]
    annualTangibleBookValue: NotRequired[list[TimeseriesResultItem]]
    annualTaxEffectOfUnusualItems: NotRequired[list[TimeseriesResultItem]]
    annualTaxLossCarryforwardBasicEPS: NotRequired[list[TimeseriesResultItem]]
    annualTaxLossCarryforwardDilutedEPS: NotRequired[list[TimeseriesResultItem]]
    annualTaxProvision: NotRequired[list[TimeseriesResultItem]]
    annualTaxRateForCalcs: NotRequired[list[TimeseriesResultItem]]
    annualTaxesReceivable: NotRequired[list[TimeseriesResultItem]]
    annualTaxesRefundPaid: NotRequired[list[TimeseriesResultItem]]
    annualTaxesRefundPaidDirect: NotRequired[list[TimeseriesResultItem]]
    annualTotalAssets: NotRequired[list[TimeseriesResultItem]]
    annualTotalCapitalization: NotRequired[list[TimeseriesResultItem]]
    annualTotalDebt: NotRequired[list[TimeseriesResultItem]]
    annualTotalEquityGrossMinorityInterest: NotRequired[list[TimeseriesResultItem]]
    annualTotalExpenses: NotRequired[list[TimeseriesResultItem]]
    annualTotalLiabilitiesNetMinorityInterest: NotRequired[list[TimeseriesResultItem]]
    annualTotalNonCurrentAssets: NotRequired[list[TimeseriesResultItem]]
    annualTotalNonCurrentLiabilitiesNetMinorityInterest: NotRequired[
        list[TimeseriesResultItem]
    ]
    annualTotalOperatingIncomeAsReported: NotRequired[list[TimeseriesResultItem]]
    annualTotalOtherFinanceCost: NotRequired[list[TimeseriesResultItem]]
    annualTotalPartnershipCapital: NotRequired[list[TimeseriesResultItem]]
    annualTotalRevenue: NotRequired[list[TimeseriesResultItem]]
    annualTotalTaxPayable: NotRequired[list[TimeseriesResultItem]]
    annualTotalUnusualItems: NotRequired[list[TimeseriesResultItem]]
    annualTotalUnusualItemsExcludingGoodwill: NotRequired[list[TimeseriesResultItem]]
    annualTradeandOtherPayablesNonCurrent: NotRequired[list[TimeseriesResultItem]]
    annualTradingSecurities: NotRequired[list[TimeseriesResultItem]]
    annualTreasurySharesNumber: NotRequired[list[TimeseriesResultItem | None]]
    annualTreasuryStock: NotRequired[list[TimeseriesResultItem]]
    annualUnrealizedGainLoss: NotRequired[list[TimeseriesResultItem]]
    annualUnrealizedGainLossOnInvestmentSecurities: NotRequired[
        list[TimeseriesResultItem]
    ]
    annualWorkInProcess: NotRequired[list[TimeseriesResultItem]]
    annualWorkingCapital: NotRequired[list[TimeseriesResultItem]]
    annualWriteOff: NotRequired[list[TimeseriesResultItem]]
    conferenceEvents: NotRequired[list[TimeseriesResultItem]]
    conferencePresentation: NotRequired[list[TimeseriesResultItem]]
    corporateAnalystMeeting: NotRequired[list[TimeseriesResultItem]]
    corporateConferenceCallEvents: NotRequired[list[TimeseriesResultItem]]
    earningsConferenceCallEvents: NotRequired[list[TimeseriesResultItem]]
    economicEvents: NotRequired[list[TimeseriesResultItem]]
    mergerAndAcquisitionAnnouncement: NotRequired[list[TimeseriesResultItem]]
    otherCorporate: NotRequired[list[TimeseriesResultItem]]
    quarterlyAccountsPayable: NotRequired[list[TimeseriesResultItem]]
    quarterlyAccountsReceivable: NotRequired[list[TimeseriesResultItem]]
    quarterlyAccruedInterestReceivable: NotRequired[list[TimeseriesResultItem]]
    quarterlyAccumulatedDepreciation: NotRequired[list[TimeseriesResultItem]]
    quarterlyAdditionalPaidInCapital: NotRequired[list[TimeseriesResultItem]]
    quarterlyAdjustedGeographySegmentData: NotRequired[list[TimeseriesResultItem]]
    quarterlyAllowanceForDoubtfulAccountsReceivable: NotRequired[
        list[TimeseriesResultItem]
    ]
    quarterlyAmortization: NotRequired[list[TimeseriesResultItem]]
    quarterlyAmortizationCashFlow: NotRequired[list[TimeseriesResultItem]]
    quarterlyAmortizationOfIntangibles: NotRequired[list[TimeseriesResultItem]]
    quarterlyAmortizationOfIntangiblesIncomeStatement: NotRequired[
        list[TimeseriesResultItem]
    ]
    quarterlyAmortizationOfSecurities: NotRequired[list[TimeseriesResultItem]]
    quarterlyAssetImpairmentCharge: NotRequired[list[TimeseriesResultItem]]
    quarterlyAssetsHeldForSaleCurrent: NotRequired[list[TimeseriesResultItem]]
    quarterlyAvailableForSaleSecurities: NotRequired[list[TimeseriesResultItem]]
    quarterlyAverageDilutionEarnings: NotRequired[list[TimeseriesResultItem]]
    quarterlyBasicAccountingChange: NotRequired[list[TimeseriesResultItem]]
    quarterlyBasicAverageShares: NotRequired[list[TimeseriesResultItem]]
    quarterlyBasicContinuousOperations: NotRequired[list[TimeseriesResultItem]]
    quarterlyBasicDiscontinuousOperations: NotRequired[list[TimeseriesResultItem]]
    quarterlyBasicEPS: NotRequired[list[TimeseriesResultItem]]
    quarterlyBasicEPSOtherGainsLosses: NotRequired[list[TimeseriesResultItem]]
    quarterlyBasicExtraordinary: NotRequired[list[TimeseriesResultItem]]
    quarterlyBeginningCashPosition: NotRequired[list[TimeseriesResultItem]]
    quarterlyBuildingsAndImprovements: NotRequired[list[TimeseriesResultItem]]
    quarterlyCapitalExpenditure: NotRequired[list[TimeseriesResultItem]]
    quarterlyCapitalExpenditureReported: NotRequired[list[TimeseriesResultItem]]
    quarterlyCapitalLeaseObligations: NotRequired[list[TimeseriesResultItem]]
    quarterlyCapitalStock: NotRequired[list[TimeseriesResultItem]]
    quarterlyCashAndCashEquivalents: NotRequired[list[TimeseriesResultItem]]
    quarterlyCashCashEquivalentsAndFederalFundsSold: NotRequired[
        list[TimeseriesResultItem]
    ]
    quarterlyCashCashEquivalentsAndShortTermInvestments: NotRequired[
        list[TimeseriesResultItem]
    ]
    quarterlyCashDividendsPaid: NotRequired[list[TimeseriesResultItem]]
    quarterlyCashEquivalents: NotRequired[list[TimeseriesResultItem]]
    quarterlyCashFinancial: NotRequired[list[TimeseriesResultItem]]
    quarterlyCashFlowFromContinuingFinancingActivities: NotRequired[
        list[TimeseriesResultItem]
    ]
    quarterlyCashFlowFromContinuingInvestingActivities: NotRequired[
        list[TimeseriesResultItem]
    ]
    quarterlyCashFlowFromContinuingOperatingActivities: NotRequired[
        list[TimeseriesResultItem]
    ]
    quarterlyCashFlowFromDiscontinuedOperation: NotRequired[list[TimeseriesResultItem]]
    quarterlyCashFlowsfromusedinOperatingActivitiesDirect: NotRequired[
        list[TimeseriesResultItem]
    ]
    quarterlyCashFromDiscontinuedFinancingActivities: NotRequired[
        list[TimeseriesResultItem]
    ]
    quarterlyCashFromDiscontinuedInvestingActivities: NotRequired[
        list[TimeseriesResultItem]
    ]
    quarterlyCashFromDiscontinuedOperatingActivities: NotRequired[
        list[TimeseriesResultItem]
    ]
    quarterlyChangeInAccountPayable: NotRequired[list[TimeseriesResultItem]]
    quarterlyChangeInAccruedExpense: NotRequired[list[TimeseriesResultItem]]
    quarterlyChangeInDividendPayable: NotRequired[list[TimeseriesResultItem]]
    quarterlyChangeInIncomeTaxPayable: NotRequired[list[TimeseriesResultItem]]
    quarterlyChangeInInterestPayable: NotRequired[list[TimeseriesResultItem]]
    quarterlyChangeInInventory: NotRequired[list[TimeseriesResultItem]]
    quarterlyChangeInOtherCurrentAssets: NotRequired[list[TimeseriesResultItem]]
    quarterlyChangeInOtherCurrentLiabilities: NotRequired[list[TimeseriesResultItem]]
    quarterlyChangeInOtherWorkingCapital: NotRequired[list[TimeseriesResultItem]]
    quarterlyChangeInPayable: NotRequired[list[TimeseriesResultItem]]
    quarterlyChangeInPayablesAndAccruedExpense: NotRequired[list[TimeseriesResultItem]]
    quarterlyChangeInPrepaidAssets: NotRequired[list[TimeseriesResultItem]]
    quarterlyChangeInReceivables: NotRequired[list[TimeseriesResultItem]]
    quarterlyChangeInTaxPayable: NotRequired[list[TimeseriesResultItem]]
    quarterlyChangeInWorkingCapital: NotRequired[list[TimeseriesResultItem]]
    quarterlyChangesInAccountReceivables: NotRequired[list[TimeseriesResultItem]]
    quarterlyChangesInCash: NotRequired[list[TimeseriesResultItem]]
    quarterlyClassesofCashPayments: NotRequired[list[TimeseriesResultItem]]
    quarterlyClassesofCashReceiptsfromOperatingActivities: NotRequired[
        list[TimeseriesResultItem]
    ]
    quarterlyCommercialPaper: NotRequired[list[TimeseriesResultItem]]
    quarterlyCommonStock: NotRequired[list[TimeseriesResultItem]]
    quarterlyCommonStockDividendPaid: NotRequired[list[TimeseriesResultItem]]
    quarterlyCommonStockEquity: NotRequired[list[TimeseriesResultItem]]
    quarterlyCommonStockIssuance: NotRequired[list[TimeseriesResultItem]]
    quarterlyCommonStockPayments: NotRequired[list[TimeseriesResultItem]]
    quarterlyConstructionInProgress: NotRequired[list[TimeseriesResultItem]]
    quarterlyContinuingAndDiscontinuedBasicEPS: NotRequired[list[TimeseriesResultItem]]
    quarterlyContinuingAndDiscontinuedDilutedEPS: NotRequired[
        list[TimeseriesResultItem]
    ]
    quarterlyCostOfRevenue: NotRequired[list[TimeseriesResultItem]]
    quarterlyCurrentAccruedExpenses: NotRequired[list[TimeseriesResultItem]]
    quarterlyCurrentAssets: NotRequired[list[TimeseriesResultItem]]
    quarterlyCurrentCapitalLeaseObligation: NotRequired[list[TimeseriesResultItem]]
    quarterlyCurrentDebt: NotRequired[list[TimeseriesResultItem]]
    quarterlyCurrentDebtAndCapitalLeaseObligation: NotRequired[
        list[TimeseriesResultItem]
    ]
    quarterlyCurrentDeferredAssets: NotRequired[list[TimeseriesResultItem]]
    quarterlyCurrentDeferredLiabilities: NotRequired[list[TimeseriesResultItem]]
    quarterlyCurrentDeferredRevenue: NotRequired[list[TimeseriesResultItem]]
    quarterlyCurrentDeferredTaxesAssets: NotRequired[list[TimeseriesResultItem]]
    quarterlyCurrentDeferredTaxesLiabilities: NotRequired[list[TimeseriesResultItem]]
    quarterlyCurrentLiabilities: NotRequired[list[TimeseriesResultItem]]
    quarterlyCurrentNotesPayable: NotRequired[list[TimeseriesResultItem]]
    quarterlyCurrentProvisions: NotRequired[list[TimeseriesResultItem]]
    quarterlyDeferredIncomeTax: NotRequired[list[TimeseriesResultItem]]
    quarterlyDeferredTax: NotRequired[list[TimeseriesResultItem]]
    quarterlyDefinedPensionBenefit: NotRequired[list[TimeseriesResultItem]]
    quarterlyDepletion: NotRequired[list[TimeseriesResultItem]]
    quarterlyDepletionIncomeStatement: NotRequired[list[TimeseriesResultItem]]
    quarterlyDepreciation: NotRequired[list[TimeseriesResultItem]]
    quarterlyDepreciationAmortizationDepletion: NotRequired[list[TimeseriesResultItem]]
    quarterlyDepreciationAmortizationDepletionIncomeStatement: NotRequired[
        list[TimeseriesResultItem]
    ]
    quarterlyDepreciationAndAmortization: NotRequired[list[TimeseriesResultItem]]
    quarterlyDepreciationAndAmortizationInIncomeStatement: NotRequired[
        list[TimeseriesResultItem]
    ]
    quarterlyDepreciationIncomeStatement: NotRequired[list[TimeseriesResultItem]]
    quarterlyDerivativeProductLiabilities: NotRequired[list[TimeseriesResultItem]]
    quarterlyDilutedAccountingChange: NotRequired[list[TimeseriesResultItem]]
    quarterlyDilutedAverageShares: NotRequired[list[TimeseriesResultItem]]
    quarterlyDilutedContinuousOperations: NotRequired[list[TimeseriesResultItem]]
    quarterlyDilutedDiscontinuousOperations: NotRequired[list[TimeseriesResultItem]]
    quarterlyDilutedEPS: NotRequired[list[TimeseriesResultItem]]
    quarterlyDilutedEPSOtherGainsLosses: NotRequired[list[TimeseriesResultItem]]
    quarterlyDilutedExtraordinary: NotRequired[list[TimeseriesResultItem]]
    quarterlyDilutedNIAvailtoComStockholders: NotRequired[list[TimeseriesResultItem]]
    quarterlyDividendPaidCFO: NotRequired[list[TimeseriesResultItem]]
    quarterlyDividendPerShare: NotRequired[list[TimeseriesResultItem]]
    quarterlyDividendReceivedCFO: NotRequired[list[TimeseriesResultItem]]
    quarterlyDividendsPaidDirect: NotRequired[list[TimeseriesResultItem]]
    quarterlyDividendsPayable: NotRequired[list[TimeseriesResultItem]]
    quarterlyDividendsReceivedCFI: NotRequired[list[TimeseriesResultItem]]
    quarterlyDividendsReceivedDirect: NotRequired[list[TimeseriesResultItem]]
    quarterlyDomesticSales: NotRequired[list[TimeseriesResultItem]]
    quarterlyDuefromRelatedPartiesCurrent: NotRequired[list[TimeseriesResultItem]]
    quarterlyDuefromRelatedPartiesNonCurrent: NotRequired[list[TimeseriesResultItem]]
    quarterlyDuetoRelatedPartiesCurrent: NotRequired[list[TimeseriesResultItem]]
    quarterlyDuetoRelatedPartiesNonCurrent: NotRequired[list[TimeseriesResultItem]]
    quarterlyEBIT: NotRequired[list[TimeseriesResultItem]]
    quarterlyEBITDA: NotRequired[list[TimeseriesResultItem]]
    quarterlyEarningsFromEquityInterest: NotRequired[list[TimeseriesResultItem]]
    quarterlyEarningsFromEquityInterestNetOfTax: NotRequired[list[TimeseriesResultItem]]
    quarterlyEarningsLossesFromEquityInvestments: NotRequired[
        list[TimeseriesResultItem]
    ]
    quarterlyEffectOfExchangeRateChanges: NotRequired[list[TimeseriesResultItem]]
    quarterlyEmployeeBenefits: NotRequired[list[TimeseriesResultItem]]
    quarterlyEndCashPosition: NotRequired[list[TimeseriesResultItem]]
    quarterlyExcessTaxBenefitFromStockBasedCompensation: NotRequired[
        list[TimeseriesResultItem]
    ]
    quarterlyExciseTaxes: NotRequired[list[TimeseriesResultItem]]
    quarterlyFinancialAssets: NotRequired[list[TimeseriesResultItem]]
    quarterlyFinancialAssetsDesignatedasFairValueThroughProfitorLossTotal: NotRequired[
        list[TimeseriesResultItem]
    ]
    quarterlyFinancingCashFlow: NotRequired[list[TimeseriesResultItem]]
    quarterlyFinishedGoods: NotRequired[list[TimeseriesResultItem]]
    quarterlyFixedAssetsRevaluationReserve: NotRequired[list[TimeseriesResultItem]]
    quarterlyForeignCurrencyTranslationAdjustments: NotRequired[
        list[TimeseriesResultItem]
    ]
    quarterlyForeignSales: NotRequired[list[TimeseriesResultItem]]
    quarterlyFreeCashFlow: NotRequired[list[TimeseriesResultItem]]
    quarterlyGainLossOnInvestmentSecurities: NotRequired[list[TimeseriesResultItem]]
    quarterlyGainLossOnSaleOfBusiness: NotRequired[list[TimeseriesResultItem]]
    quarterlyGainLossOnSaleOfPPE: NotRequired[list[TimeseriesResultItem]]
    quarterlyGainOnSaleOfBusiness: NotRequired[list[TimeseriesResultItem]]
    quarterlyGainOnSaleOfPPE: NotRequired[list[TimeseriesResultItem]]
    quarterlyGainOnSaleOfSecurity: NotRequired[list[TimeseriesResultItem]]
    quarterlyGainsLossesNotAffectingRetainedEarnings: NotRequired[
        list[TimeseriesResultItem]
    ]
    quarterlyGeneralAndAdministrativeExpense: NotRequired[list[TimeseriesResultItem]]
    quarterlyGeneralPartnershipCapital: NotRequired[list[TimeseriesResultItem]]
    quarterlyGoodwill: NotRequired[list[TimeseriesResultItem]]
    quarterlyGoodwillAndOtherIntangibleAssets: NotRequired[list[TimeseriesResultItem]]
    quarterlyGrossAccountsReceivable: NotRequired[list[TimeseriesResultItem]]
    quarterlyGrossPPE: NotRequired[list[TimeseriesResultItem]]
    quarterlyGrossProfit: NotRequired[list[TimeseriesResultItem]]
    quarterlyHedgingAssetsCurrent: NotRequired[list[TimeseriesResultItem]]
    quarterlyHeldToMaturitySecurities: NotRequired[list[TimeseriesResultItem]]
    quarterlyImpairmentOfCapitalAssets: NotRequired[list[TimeseriesResultItem]]
    quarterlyIncomeTaxPaidSupplementalData: NotRequired[list[TimeseriesResultItem]]
    quarterlyIncomeTaxPayable: NotRequired[list[TimeseriesResultItem]]
    quarterlyInsuranceAndClaims: NotRequired[list[TimeseriesResultItem]]
    quarterlyInterestExpense: NotRequired[list[TimeseriesResultItem]]
    quarterlyInterestExpenseNonOperating: NotRequired[list[TimeseriesResultItem]]
    quarterlyInterestIncome: NotRequired[list[TimeseriesResultItem]]
    quarterlyInterestIncomeNonOperating: NotRequired[list[TimeseriesResultItem]]
    quarterlyInterestPaidCFF: NotRequired[list[TimeseriesResultItem]]
    quarterlyInterestPaidCFO: NotRequired[list[TimeseriesResultItem]]
    quarterlyInterestPaidDirect: NotRequired[list[TimeseriesResultItem]]
    quarterlyInterestPaidSupplementalData: NotRequired[list[TimeseriesResultItem]]
    quarterlyInterestPayable: NotRequired[list[TimeseriesResultItem]]
    quarterlyInterestReceivedCFI: NotRequired[list[TimeseriesResultItem]]
    quarterlyInterestReceivedCFO: NotRequired[list[TimeseriesResultItem]]
    quarterlyInterestReceivedDirect: NotRequired[list[TimeseriesResultItem]]
    quarterlyInventoriesAdjustmentsAllowances: NotRequired[list[TimeseriesResultItem]]
    quarterlyInventory: NotRequired[list[TimeseriesResultItem]]
    quarterlyInvestedCapital: NotRequired[list[TimeseriesResultItem]]
    quarterlyInvestingCashFlow: NotRequired[list[TimeseriesResultItem]]
    quarterlyInvestmentProperties: NotRequired[list[TimeseriesResultItem]]
    quarterlyInvestmentinFinancialAssets: NotRequired[list[TimeseriesResultItem]]
    quarterlyInvestmentsAndAdvances: NotRequired[list[TimeseriesResultItem]]
    quarterlyInvestmentsInOtherVenturesUnderEquityMethod: NotRequired[
        list[TimeseriesResultItem]
    ]
    quarterlyInvestmentsinAssociatesatCost: NotRequired[list[TimeseriesResultItem]]
    quarterlyInvestmentsinJointVenturesatCost: NotRequired[list[TimeseriesResultItem]]
    quarterlyInvestmentsinSubsidiariesatCost: NotRequired[list[TimeseriesResultItem]]
    quarterlyIssuanceOfCapitalStock: NotRequired[list[TimeseriesResultItem]]
    quarterlyIssuanceOfDebt: NotRequired[list[TimeseriesResultItem]]
    quarterlyLandAndImprovements: NotRequired[list[TimeseriesResultItem]]
    quarterlyLeases: NotRequired[list[TimeseriesResultItem]]
    quarterlyLiabilitiesHeldforSaleNonCurrent: NotRequired[list[TimeseriesResultItem]]
    quarterlyLimitedPartnershipCapital: NotRequired[list[TimeseriesResultItem]]
    quarterlyLineOfCredit: NotRequired[list[TimeseriesResultItem]]
    quarterlyLoansReceivable: NotRequired[list[TimeseriesResultItem]]
    quarterlyLongTermCapitalLeaseObligation: NotRequired[list[TimeseriesResultItem]]
    quarterlyLongTermDebt: NotRequired[list[TimeseriesResultItem]]
    quarterlyLongTermDebtAndCapitalLeaseObligation: NotRequired[
        list[TimeseriesResultItem]
    ]
    quarterlyLongTermDebtIssuance: NotRequired[list[TimeseriesResultItem]]
    quarterlyLongTermDebtPayments: NotRequired[list[TimeseriesResultItem]]
    quarterlyLongTermEquityInvestment: NotRequired[list[TimeseriesResultItem]]
    quarterlyLongTermProvisions: NotRequired[list[TimeseriesResultItem]]
    quarterlyLossAdjustmentExpense: NotRequired[list[TimeseriesResultItem]]
    quarterlyMachineryFurnitureEquipment: NotRequired[list[TimeseriesResultItem]]
    quarterlyMinimumPensionLiabilities: NotRequired[list[TimeseriesResultItem]]
    quarterlyMinorityInterest: NotRequired[list[TimeseriesResultItem]]
    quarterlyMinorityInterests: NotRequired[list[TimeseriesResultItem]]
    quarterlyNetBusinessPurchaseAndSale: NotRequired[list[TimeseriesResultItem]]
    quarterlyNetCommonStockIssuance: NotRequired[list[TimeseriesResultItem]]
    quarterlyNetDebt: NotRequired[list[TimeseriesResultItem]]
    quarterlyNetForeignCurrencyExchangeGainLoss: NotRequired[list[TimeseriesResultItem]]
    quarterlyNetIncome: NotRequired[list[TimeseriesResultItem]]
    quarterlyNetIncomeCommonStockholders: NotRequired[list[TimeseriesResultItem]]
    quarterlyNetIncomeContinuousOperations: NotRequired[list[TimeseriesResultItem]]
    quarterlyNetIncomeDiscontinuousOperations: NotRequired[list[TimeseriesResultItem]]
    quarterlyNetIncomeExtraordinary: NotRequired[list[TimeseriesResultItem]]
    quarterlyNetIncomeFromContinuingAndDiscontinuedOperation: NotRequired[
        list[TimeseriesResultItem]
    ]
    quarterlyNetIncomeFromContinuingOperationNetMinorityInterest: NotRequired[
        list[TimeseriesResultItem]
    ]
    quarterlyNetIncomeFromContinuingOperations: NotRequired[list[TimeseriesResultItem]]
    quarterlyNetIncomeFromTaxLossCarryforward: NotRequired[list[TimeseriesResultItem]]
    quarterlyNetIncomeIncludingNoncontrollingInterests: NotRequired[
        list[TimeseriesResultItem]
    ]
    quarterlyNetIntangiblesPurchaseAndSale: NotRequired[list[TimeseriesResultItem]]
    quarterlyNetInterestIncome: NotRequired[list[TimeseriesResultItem]]
    quarterlyNetInvestmentPropertiesPurchaseAndSale: NotRequired[
        list[TimeseriesResultItem]
    ]
    quarterlyNetInvestmentPurchaseAndSale: NotRequired[list[TimeseriesResultItem]]
    quarterlyNetIssuancePaymentsOfDebt: NotRequired[list[TimeseriesResultItem]]
    quarterlyNetLongTermDebtIssuance: NotRequired[list[TimeseriesResultItem]]
    quarterlyNetNonOperatingInterestIncomeExpense: NotRequired[
        list[TimeseriesResultItem]
    ]
    quarterlyNetOtherFinancingCharges: NotRequired[list[TimeseriesResultItem]]
    quarterlyNetOtherInvestingChanges: NotRequired[list[TimeseriesResultItem]]
    quarterlyNetPPE: NotRequired[list[TimeseriesResultItem]]
    quarterlyNetPPEPurchaseAndSale: NotRequired[list[TimeseriesResultItem]]
    quarterlyNetPolicyholderBenefitsAndClaims: NotRequired[list[TimeseriesResultItem]]
    quarterlyNetPreferredStockIssuance: NotRequired[list[TimeseriesResultItem]]
    quarterlyNetShortTermDebtIssuance: NotRequired[list[TimeseriesResultItem]]
    quarterlyNetTangibleAssets: NotRequired[list[TimeseriesResultItem]]
    quarterlyNonCurrentAccountsReceivable: NotRequired[list[TimeseriesResultItem]]
    quarterlyNonCurrentAccruedExpenses: NotRequired[list[TimeseriesResultItem]]
    quarterlyNonCurrentDeferredAssets: NotRequired[list[TimeseriesResultItem]]
    quarterlyNonCurrentDeferredLiabilities: NotRequired[list[TimeseriesResultItem]]
    quarterlyNonCurrentDeferredRevenue: NotRequired[list[TimeseriesResultItem]]
    quarterlyNonCurrentDeferredTaxesAssets: NotRequired[list[TimeseriesResultItem]]
    quarterlyNonCurrentDeferredTaxesLiabilities: NotRequired[list[TimeseriesResultItem]]
    quarterlyNonCurrentNoteReceivables: NotRequired[list[TimeseriesResultItem]]
    quarterlyNonCurrentPensionAndOtherPostretirementBenefitPlans: NotRequired[
        list[TimeseriesResultItem]
    ]
    quarterlyNonCurrentPrepaidAssets: NotRequired[list[TimeseriesResultItem]]
    quarterlyNormalizedBasicEPS: NotRequired[list[TimeseriesResultItem]]
    quarterlyNormalizedDilutedEPS: NotRequired[list[TimeseriesResultItem]]
    quarterlyNormalizedEBITDA: NotRequired[list[TimeseriesResultItem]]
    quarterlyNormalizedIncome: NotRequired[list[TimeseriesResultItem]]
    quarterlyNotesReceivable: NotRequired[list[TimeseriesResultItem]]
    quarterlyOccupancyAndEquipment: NotRequired[list[TimeseriesResultItem]]
    quarterlyOperatingCashFlow: NotRequired[list[TimeseriesResultItem]]
    quarterlyOperatingExpense: NotRequired[list[TimeseriesResultItem]]
    quarterlyOperatingGainsLosses: NotRequired[list[TimeseriesResultItem]]
    quarterlyOperatingIncome: NotRequired[list[TimeseriesResultItem]]
    quarterlyOperatingRevenue: NotRequired[list[TimeseriesResultItem]]
    quarterlyOrdinarySharesNumber: NotRequired[list[TimeseriesResultItem]]
    quarterlyOtherCapitalStock: NotRequired[list[TimeseriesResultItem]]
    quarterlyOtherCashAdjustmentInsideChangeinCash: NotRequired[
        list[TimeseriesResultItem]
    ]
    quarterlyOtherCashAdjustmentOutsideChangeinCash: NotRequired[
        list[TimeseriesResultItem]
    ]
    quarterlyOtherCashPaymentsfromOperatingActivities: NotRequired[
        list[TimeseriesResultItem]
    ]
    quarterlyOtherCashReceiptsfromOperatingActivities: NotRequired[
        list[TimeseriesResultItem]
    ]
    quarterlyOtherCurrentAssets: NotRequired[list[TimeseriesResultItem]]
    quarterlyOtherCurrentBorrowings: NotRequired[list[TimeseriesResultItem]]
    quarterlyOtherCurrentLiabilities: NotRequired[list[TimeseriesResultItem]]
    quarterlyOtherEquityAdjustments: NotRequired[list[TimeseriesResultItem]]
    quarterlyOtherEquityInterest: NotRequired[list[TimeseriesResultItem]]
    quarterlyOtherGandA: NotRequired[list[TimeseriesResultItem]]
    quarterlyOtherIncomeExpense: NotRequired[list[TimeseriesResultItem]]
    quarterlyOtherIntangibleAssets: NotRequired[list[TimeseriesResultItem]]
    quarterlyOtherInventories: NotRequired[list[TimeseriesResultItem]]
    quarterlyOtherInvestments: NotRequired[list[TimeseriesResultItem]]
    quarterlyOtherNonCashItems: NotRequired[list[TimeseriesResultItem]]
    quarterlyOtherNonCurrentAssets: NotRequired[list[TimeseriesResultItem]]
    quarterlyOtherNonCurrentLiabilities: NotRequired[list[TimeseriesResultItem]]
    quarterlyOtherNonInterestExpense: NotRequired[list[TimeseriesResultItem]]
    quarterlyOtherNonOperatingIncomeExpenses: NotRequired[list[TimeseriesResultItem]]
    quarterlyOtherOperatingExpenses: NotRequired[list[TimeseriesResultItem]]
    quarterlyOtherPayable: NotRequired[list[TimeseriesResultItem]]
    quarterlyOtherProperties: NotRequired[list[TimeseriesResultItem]]
    quarterlyOtherReceivables: NotRequired[list[TimeseriesResultItem]]
    quarterlyOtherShortTermInvestments: NotRequired[list[TimeseriesResultItem]]
    quarterlyOtherSpecialCharges: NotRequired[list[TimeseriesResultItem]]
    quarterlyOtherTaxes: NotRequired[list[TimeseriesResultItem]]
    quarterlyOtherunderPreferredStockDividend: NotRequired[list[TimeseriesResultItem]]
    quarterlyPayables: NotRequired[list[TimeseriesResultItem]]
    quarterlyPayablesAndAccruedExpenses: NotRequired[list[TimeseriesResultItem]]
    quarterlyPaymentsonBehalfofEmployees: NotRequired[list[TimeseriesResultItem]]
    quarterlyPaymentstoSuppliersforGoodsandServices: NotRequired[
        list[TimeseriesResultItem]
    ]
    quarterlyPensionAndEmployeeBenefitExpense: NotRequired[list[TimeseriesResultItem]]
    quarterlyPensionandOtherPostRetirementBenefitPlansCurrent: NotRequired[
        list[TimeseriesResultItem]
    ]
    quarterlyPolicyholderBenefitsCeded: NotRequired[list[TimeseriesResultItem]]
    quarterlyPolicyholderBenefitsGross: NotRequired[list[TimeseriesResultItem]]
    quarterlyPreferredSecuritiesOutsideStockEquity: NotRequired[
        list[TimeseriesResultItem]
    ]
    quarterlyPreferredSharesNumber: NotRequired[list[TimeseriesResultItem]]
    quarterlyPreferredStock: NotRequired[list[TimeseriesResultItem]]
    quarterlyPreferredStockDividendPaid: NotRequired[list[TimeseriesResultItem]]
    quarterlyPreferredStockDividends: NotRequired[list[TimeseriesResultItem]]
    quarterlyPreferredStockEquity: NotRequired[list[TimeseriesResultItem]]
    quarterlyPreferredStockIssuance: NotRequired[list[TimeseriesResultItem]]
    quarterlyPreferredStockPayments: NotRequired[list[TimeseriesResultItem]]
    quarterlyPrepaidAssets: NotRequired[list[TimeseriesResultItem]]
    quarterlyPretaxIncome: NotRequired[list[TimeseriesResultItem]]
    quarterlyProceedsFromStockOptionExercised: NotRequired[list[TimeseriesResultItem]]
    quarterlyProfessionalExpenseAndContractServicesExpense: NotRequired[
        list[TimeseriesResultItem]
    ]
    quarterlyProperties: NotRequired[list[TimeseriesResultItem]]
    quarterlyProvisionForDoubtfulAccounts: NotRequired[list[TimeseriesResultItem]]
    quarterlyProvisionandWriteOffofAssets: NotRequired[list[TimeseriesResultItem]]
    quarterlyPurchaseOfBusiness: NotRequired[list[TimeseriesResultItem]]
    quarterlyPurchaseOfIntangibles: NotRequired[list[TimeseriesResultItem]]
    quarterlyPurchaseOfInvestment: NotRequired[list[TimeseriesResultItem]]
    quarterlyPurchaseOfInvestmentProperties: NotRequired[list[TimeseriesResultItem]]
    quarterlyPurchaseOfPPE: NotRequired[list[TimeseriesResultItem]]
    quarterlyRawMaterials: NotRequired[list[TimeseriesResultItem]]
    quarterlyReceiptsfromCustomers: NotRequired[list[TimeseriesResultItem]]
    quarterlyReceiptsfromGovernmentGrants: NotRequired[list[TimeseriesResultItem]]
    quarterlyReceivables: NotRequired[list[TimeseriesResultItem]]
    quarterlyReceivablesAdjustmentsAllowances: NotRequired[list[TimeseriesResultItem]]
    quarterlyReconciledCostOfRevenue: NotRequired[list[TimeseriesResultItem]]
    quarterlyReconciledDepreciation: NotRequired[list[TimeseriesResultItem]]
    quarterlyRentAndLandingFees: NotRequired[list[TimeseriesResultItem]]
    quarterlyRentExpenseSupplemental: NotRequired[list[TimeseriesResultItem]]
    quarterlyRepaymentOfDebt: NotRequired[list[TimeseriesResultItem]]
    quarterlyReportedNormalizedBasicEPS: NotRequired[list[TimeseriesResultItem]]
    quarterlyReportedNormalizedDilutedEPS: NotRequired[list[TimeseriesResultItem]]
    quarterlyRepurchaseOfCapitalStock: NotRequired[list[TimeseriesResultItem]]
    quarterlyResearchAndDevelopment: NotRequired[list[TimeseriesResultItem]]
    quarterlyRestrictedCash: NotRequired[list[TimeseriesResultItem]]
    quarterlyRestrictedCommonStock: NotRequired[list[TimeseriesResultItem]]
    quarterlyRestructuringAndMergernAcquisition: NotRequired[list[TimeseriesResultItem]]
    quarterlyRetainedEarnings: NotRequired[list[TimeseriesResultItem]]
    quarterlySalariesAndWages: NotRequired[list[TimeseriesResultItem]]
    quarterlySaleOfBusiness: NotRequired[list[TimeseriesResultItem]]
    quarterlySaleOfIntangibles: NotRequired[list[TimeseriesResultItem]]
    quarterlySaleOfInvestment: NotRequired[list[TimeseriesResultItem]]
    quarterlySaleOfInvestmentProperties: NotRequired[list[TimeseriesResultItem]]
    quarterlySaleOfPPE: NotRequired[list[TimeseriesResultItem]]
    quarterlySecuritiesAmortization: NotRequired[list[TimeseriesResultItem]]
    quarterlySellingAndMarketingExpense: NotRequired[list[TimeseriesResultItem]]
    quarterlySellingGeneralAndAdministration: NotRequired[list[TimeseriesResultItem]]
    quarterlyShareIssued: NotRequired[list[TimeseriesResultItem]]
    quarterlyShortTermDebtIssuance: NotRequired[list[TimeseriesResultItem]]
    quarterlyShortTermDebtPayments: NotRequired[list[TimeseriesResultItem]]
    quarterlySpecialIncomeCharges: NotRequired[list[TimeseriesResultItem]]
    quarterlyStockBasedCompensation: NotRequired[list[TimeseriesResultItem]]
    quarterlyStockholdersEquity: NotRequired[list[TimeseriesResultItem]]
    quarterlyTangibleBookValue: NotRequired[list[TimeseriesResultItem]]
    quarterlyTaxEffectOfUnusualItems: NotRequired[list[TimeseriesResultItem]]
    quarterlyTaxLossCarryforwardBasicEPS: NotRequired[list[TimeseriesResultItem]]
    quarterlyTaxLossCarryforwardDilutedEPS: NotRequired[list[TimeseriesResultItem]]
    quarterlyTaxProvision: NotRequired[list[TimeseriesResultItem]]
    quarterlyTaxRateForCalcs: NotRequired[list[TimeseriesResultItem]]
    quarterlyTaxesReceivable: NotRequired[list[TimeseriesResultItem]]
    quarterlyTaxesRefundPaid: NotRequired[list[TimeseriesResultItem]]
    quarterlyTaxesRefundPaidDirect: NotRequired[list[TimeseriesResultItem]]
    quarterlyTotalAssets: NotRequired[list[TimeseriesResultItem]]
    quarterlyTotalCapitalization: NotRequired[list[TimeseriesResultItem]]
    quarterlyTotalDebt: NotRequired[list[TimeseriesResultItem]]
    quarterlyTotalEquityGrossMinorityInterest: NotRequired[list[TimeseriesResultItem]]
    quarterlyTotalExpenses: NotRequired[list[TimeseriesResultItem]]
    quarterlyTotalLiabilitiesNetMinorityInterest: NotRequired[
        list[TimeseriesResultItem]
    ]
    quarterlyTotalNonCurrentAssets: NotRequired[list[TimeseriesResultItem]]
    quarterlyTotalNonCurrentLiabilitiesNetMinorityInterest: NotRequired[
        list[TimeseriesResultItem]
    ]
    quarterlyTotalOperatingIncomeAsReported: NotRequired[list[TimeseriesResultItem]]
    quarterlyTotalOtherFinanceCost: NotRequired[list[TimeseriesResultItem]]
    quarterlyTotalPartnershipCapital: NotRequired[list[TimeseriesResultItem]]
    quarterlyTotalRevenue: NotRequired[list[TimeseriesResultItem]]
    quarterlyTotalTaxPayable: NotRequired[list[TimeseriesResultItem]]
    quarterlyTotalUnusualItems: NotRequired[list[TimeseriesResultItem]]
    quarterlyTotalUnusualItemsExcludingGoodwill: NotRequired[list[TimeseriesResultItem]]
    quarterlyTradeandOtherPayablesNonCurrent: NotRequired[list[TimeseriesResultItem]]
    quarterlyTradingSecurities: NotRequired[list[TimeseriesResultItem]]
    quarterlyTreasurySharesNumber: NotRequired[list[TimeseriesResultItem]]
    quarterlyTreasuryStock: NotRequired[list[TimeseriesResultItem]]
    quarterlyUnrealizedGainLoss: NotRequired[list[TimeseriesResultItem]]
    quarterlyUnrealizedGainLossOnInvestmentSecurities: NotRequired[
        list[TimeseriesResultItem]
    ]
    quarterlyWorkInProcess: NotRequired[list[TimeseriesResultItem]]
    quarterlyWorkingCapital: NotRequired[list[TimeseriesResultItem]]
    quarterlyWriteOff: NotRequired[list[TimeseriesResultItem]]
    shareHoldersAnnualMeetingsEvents: NotRequired[list[TimeseriesResultItem]]
    spEarningsReleaseEvents: NotRequired[list[TimeseriesResultItem]]
    trailingAdjustedGeographySegmentData: NotRequired[list[TimeseriesResultItem]]
    trailingAmortization: NotRequired[list[TimeseriesResultItem]]
    trailingAmortizationCashFlow: NotRequired[list[TimeseriesResultItem]]
    trailingAmortizationOfIntangibles: NotRequired[list[TimeseriesResultItem]]
    trailingAmortizationOfIntangiblesIncomeStatement: NotRequired[
        list[TimeseriesResultItem]
    ]
    trailingAmortizationOfSecurities: NotRequired[list[TimeseriesResultItem]]
    trailingAssetImpairmentCharge: NotRequired[list[TimeseriesResultItem]]
    trailingAverageDilutionEarnings: NotRequired[list[TimeseriesResultItem]]
    trailingBasicAccountingChange: NotRequired[list[TimeseriesResultItem]]
    trailingBasicAverageShares: NotRequired[list[TimeseriesResultItem]]
    trailingBasicContinuousOperations: NotRequired[list[TimeseriesResultItem]]
    trailingBasicDiscontinuousOperations: NotRequired[list[TimeseriesResultItem]]
    trailingBasicEPS: NotRequired[list[TimeseriesResultItem]]
    trailingBasicEPSOtherGainsLosses: NotRequired[list[TimeseriesResultItem]]
    trailingBasicExtraordinary: NotRequired[list[TimeseriesResultItem]]
    trailingBeginningCashPosition: NotRequired[list[TimeseriesResultItem]]
    trailingCapitalExpenditure: NotRequired[list[TimeseriesResultItem]]
    trailingCapitalExpenditureReported: NotRequired[list[TimeseriesResultItem]]
    trailingCashDividendsPaid: NotRequired[list[TimeseriesResultItem]]
    trailingCashFlowFromContinuingFinancingActivities: NotRequired[
        list[TimeseriesResultItem]
    ]
    trailingCashFlowFromContinuingInvestingActivities: NotRequired[
        list[TimeseriesResultItem]
    ]
    trailingCashFlowFromContinuingOperatingActivities: NotRequired[
        list[TimeseriesResultItem]
    ]
    trailingCashFlowFromDiscontinuedOperation: NotRequired[list[TimeseriesResultItem]]
    trailingCashFlowsfromusedinOperatingActivitiesDirect: NotRequired[
        list[TimeseriesResultItem]
    ]
    trailingCashFromDiscontinuedFinancingActivities: NotRequired[
        list[TimeseriesResultItem]
    ]
    trailingCashFromDiscontinuedInvestingActivities: NotRequired[
        list[TimeseriesResultItem]
    ]
    trailingCashFromDiscontinuedOperatingActivities: NotRequired[
        list[TimeseriesResultItem]
    ]
    trailingChangeInAccountPayable: NotRequired[list[TimeseriesResultItem]]
    trailingChangeInAccruedExpense: NotRequired[list[TimeseriesResultItem]]
    trailingChangeInDividendPayable: NotRequired[list[TimeseriesResultItem]]
    trailingChangeInIncomeTaxPayable: NotRequired[list[TimeseriesResultItem]]
    trailingChangeInInterestPayable: NotRequired[list[TimeseriesResultItem]]
    trailingChangeInInventory: NotRequired[list[TimeseriesResultItem]]
    trailingChangeInOtherCurrentAssets: NotRequired[list[TimeseriesResultItem]]
    trailingChangeInOtherCurrentLiabilities: NotRequired[list[TimeseriesResultItem]]
    trailingChangeInOtherWorkingCapital: NotRequired[list[TimeseriesResultItem]]
    trailingChangeInPayable: NotRequired[list[TimeseriesResultItem]]
    trailingChangeInPayablesAndAccruedExpense: NotRequired[list[TimeseriesResultItem]]
    trailingChangeInPrepaidAssets: NotRequired[list[TimeseriesResultItem]]
    trailingChangeInReceivables: NotRequired[list[TimeseriesResultItem]]
    trailingChangeInTaxPayable: NotRequired[list[TimeseriesResultItem]]
    trailingChangeInWorkingCapital: NotRequired[list[TimeseriesResultItem]]
    trailingChangesInAccountReceivables: NotRequired[list[TimeseriesResultItem]]
    trailingChangesInCash: NotRequired[list[TimeseriesResultItem]]
    trailingClassesofCashPayments: NotRequired[list[TimeseriesResultItem]]
    trailingClassesofCashReceiptsfromOperatingActivities: NotRequired[
        list[TimeseriesResultItem]
    ]
    trailingCommonStockDividendPaid: NotRequired[list[TimeseriesResultItem]]
    trailingCommonStockIssuance: NotRequired[list[TimeseriesResultItem]]
    trailingCommonStockPayments: NotRequired[list[TimeseriesResultItem]]
    trailingContinuingAndDiscontinuedBasicEPS: NotRequired[list[TimeseriesResultItem]]
    trailingContinuingAndDiscontinuedDilutedEPS: NotRequired[list[TimeseriesResultItem]]
    trailingCostOfRevenue: NotRequired[list[TimeseriesResultItem]]
    trailingDeferredIncomeTax: NotRequired[list[TimeseriesResultItem]]
    trailingDeferredTax: NotRequired[list[TimeseriesResultItem]]
    trailingDepletion: NotRequired[list[TimeseriesResultItem]]
    trailingDepletionIncomeStatement: NotRequired[list[TimeseriesResultItem]]
    trailingDepreciation: NotRequired[list[TimeseriesResultItem]]
    trailingDepreciationAmortizationDepletion: NotRequired[list[TimeseriesResultItem]]
    trailingDepreciationAmortizationDepletionIncomeStatement: NotRequired[
        list[TimeseriesResultItem]
    ]
    trailingDepreciationAndAmortization: NotRequired[list[TimeseriesResultItem]]
    trailingDepreciationAndAmortizationInIncomeStatement: NotRequired[
        list[TimeseriesResultItem]
    ]
    trailingDepreciationIncomeStatement: NotRequired[list[TimeseriesResultItem]]
    trailingDilutedAccountingChange: NotRequired[list[TimeseriesResultItem]]
    trailingDilutedAverageShares: NotRequired[list[TimeseriesResultItem]]
    trailingDilutedContinuousOperations: NotRequired[list[TimeseriesResultItem]]
    trailingDilutedDiscontinuousOperations: NotRequired[list[TimeseriesResultItem]]
    trailingDilutedEPS: NotRequired[list[TimeseriesResultItem]]
    trailingDilutedEPSOtherGainsLosses: NotRequired[list[TimeseriesResultItem]]
    trailingDilutedExtraordinary: NotRequired[list[TimeseriesResultItem]]
    trailingDilutedNIAvailtoComStockholders: NotRequired[list[TimeseriesResultItem]]
    trailingDividendPaidCFO: NotRequired[list[TimeseriesResultItem]]
    trailingDividendPerShare: NotRequired[list[TimeseriesResultItem]]
    trailingDividendReceivedCFO: NotRequired[list[TimeseriesResultItem]]
    trailingDividendsPaidDirect: NotRequired[list[TimeseriesResultItem]]
    trailingDividendsReceivedCFI: NotRequired[list[TimeseriesResultItem]]
    trailingDividendsReceivedDirect: NotRequired[list[TimeseriesResultItem]]
    trailingDomesticSales: NotRequired[list[TimeseriesResultItem]]
    trailingEBIT: NotRequired[list[TimeseriesResultItem]]
    trailingEBITDA: NotRequired[list[TimeseriesResultItem]]
    trailingEarningsFromEquityInterest: NotRequired[list[TimeseriesResultItem]]
    trailingEarningsFromEquityInterestNetOfTax: NotRequired[list[TimeseriesResultItem]]
    trailingEarningsLossesFromEquityInvestments: NotRequired[list[TimeseriesResultItem]]
    trailingEffectOfExchangeRateChanges: NotRequired[list[TimeseriesResultItem]]
    trailingEndCashPosition: NotRequired[list[TimeseriesResultItem]]
    trailingExcessTaxBenefitFromStockBasedCompensation: NotRequired[
        list[TimeseriesResultItem]
    ]
    trailingExciseTaxes: NotRequired[list[TimeseriesResultItem]]
    trailingFinancingCashFlow: NotRequired[list[TimeseriesResultItem]]
    trailingForeignSales: NotRequired[list[TimeseriesResultItem]]
    trailingFreeCashFlow: NotRequired[list[TimeseriesResultItem]]
    trailingGainLossOnInvestmentSecurities: NotRequired[list[TimeseriesResultItem]]
    trailingGainLossOnSaleOfBusiness: NotRequired[list[TimeseriesResultItem]]
    trailingGainLossOnSaleOfPPE: NotRequired[list[TimeseriesResultItem]]
    trailingGainOnSaleOfBusiness: NotRequired[list[TimeseriesResultItem]]
    trailingGainOnSaleOfPPE: NotRequired[list[TimeseriesResultItem]]
    trailingGainOnSaleOfSecurity: NotRequired[list[TimeseriesResultItem]]
    trailingGeneralAndAdministrativeExpense: NotRequired[list[TimeseriesResultItem]]
    trailingGrossProfit: NotRequired[list[TimeseriesResultItem]]
    trailingImpairmentOfCapitalAssets: NotRequired[list[TimeseriesResultItem]]
    trailingIncomeTaxPaidSupplementalData: NotRequired[list[TimeseriesResultItem]]
    trailingInsuranceAndClaims: NotRequired[list[TimeseriesResultItem]]
    trailingInterestExpense: NotRequired[list[TimeseriesResultItem]]
    trailingInterestExpenseNonOperating: NotRequired[list[TimeseriesResultItem]]
    trailingInterestIncome: NotRequired[list[TimeseriesResultItem]]
    trailingInterestIncomeNonOperating: NotRequired[list[TimeseriesResultItem]]
    trailingInterestPaidCFF: NotRequired[list[TimeseriesResultItem]]
    trailingInterestPaidCFO: NotRequired[list[TimeseriesResultItem]]
    trailingInterestPaidDirect: NotRequired[list[TimeseriesResultItem]]
    trailingInterestPaidSupplementalData: NotRequired[list[TimeseriesResultItem]]
    trailingInterestReceivedCFI: NotRequired[list[TimeseriesResultItem]]
    trailingInterestReceivedCFO: NotRequired[list[TimeseriesResultItem]]
    trailingInterestReceivedDirect: NotRequired[list[TimeseriesResultItem]]
    trailingInvestingCashFlow: NotRequired[list[TimeseriesResultItem]]
    trailingIssuanceOfCapitalStock: NotRequired[list[TimeseriesResultItem]]
    trailingIssuanceOfDebt: NotRequired[list[TimeseriesResultItem]]
    trailingLongTermDebtIssuance: NotRequired[list[TimeseriesResultItem]]
    trailingLongTermDebtPayments: NotRequired[list[TimeseriesResultItem]]
    trailingLossAdjustmentExpense: NotRequired[list[TimeseriesResultItem]]
    trailingMinorityInterests: NotRequired[list[TimeseriesResultItem]]
    trailingNetBusinessPurchaseAndSale: NotRequired[list[TimeseriesResultItem]]
    trailingNetCommonStockIssuance: NotRequired[list[TimeseriesResultItem]]
    trailingNetForeignCurrencyExchangeGainLoss: NotRequired[list[TimeseriesResultItem]]
    trailingNetIncome: NotRequired[list[TimeseriesResultItem]]
    trailingNetIncomeCommonStockholders: NotRequired[list[TimeseriesResultItem]]
    trailingNetIncomeContinuousOperations: NotRequired[list[TimeseriesResultItem]]
    trailingNetIncomeDiscontinuousOperations: NotRequired[list[TimeseriesResultItem]]
    trailingNetIncomeExtraordinary: NotRequired[list[TimeseriesResultItem]]
    trailingNetIncomeFromContinuingAndDiscontinuedOperation: NotRequired[
        list[TimeseriesResultItem]
    ]
    trailingNetIncomeFromContinuingOperationNetMinorityInterest: NotRequired[
        list[TimeseriesResultItem]
    ]
    trailingNetIncomeFromContinuingOperations: NotRequired[list[TimeseriesResultItem]]
    trailingNetIncomeFromTaxLossCarryforward: NotRequired[list[TimeseriesResultItem]]
    trailingNetIncomeIncludingNoncontrollingInterests: NotRequired[
        list[TimeseriesResultItem]
    ]
    trailingNetIntangiblesPurchaseAndSale: NotRequired[list[TimeseriesResultItem]]
    trailingNetInterestIncome: NotRequired[list[TimeseriesResultItem]]
    trailingNetInvestmentPropertiesPurchaseAndSale: NotRequired[
        list[TimeseriesResultItem]
    ]
    trailingNetInvestmentPurchaseAndSale: NotRequired[list[TimeseriesResultItem]]
    trailingNetIssuancePaymentsOfDebt: NotRequired[list[TimeseriesResultItem]]
    trailingNetLongTermDebtIssuance: NotRequired[list[TimeseriesResultItem]]
    trailingNetNonOperatingInterestIncomeExpense: NotRequired[
        list[TimeseriesResultItem]
    ]
    trailingNetOtherFinancingCharges: NotRequired[list[TimeseriesResultItem]]
    trailingNetOtherInvestingChanges: NotRequired[list[TimeseriesResultItem]]
    trailingNetPPEPurchaseAndSale: NotRequired[list[TimeseriesResultItem]]
    trailingNetPolicyholderBenefitsAndClaims: NotRequired[list[TimeseriesResultItem]]
    trailingNetPreferredStockIssuance: NotRequired[list[TimeseriesResultItem]]
    trailingNetShortTermDebtIssuance: NotRequired[list[TimeseriesResultItem]]
    trailingNormalizedBasicEPS: NotRequired[list[TimeseriesResultItem]]
    trailingNormalizedDilutedEPS: NotRequired[list[TimeseriesResultItem]]
    trailingNormalizedEBITDA: NotRequired[list[TimeseriesResultItem]]
    trailingNormalizedIncome: NotRequired[list[TimeseriesResultItem]]
    trailingOccupancyAndEquipment: NotRequired[list[TimeseriesResultItem]]
    trailingOperatingCashFlow: NotRequired[list[TimeseriesResultItem]]
    trailingOperatingExpense: NotRequired[list[TimeseriesResultItem]]
    trailingOperatingGainsLosses: NotRequired[list[TimeseriesResultItem]]
    trailingOperatingIncome: NotRequired[list[TimeseriesResultItem]]
    trailingOperatingRevenue: NotRequired[list[TimeseriesResultItem]]
    trailingOtherCashAdjustmentInsideChangeinCash: NotRequired[
        list[TimeseriesResultItem]
    ]
    trailingOtherCashAdjustmentOutsideChangeinCash: NotRequired[
        list[TimeseriesResultItem]
    ]
    trailingOtherCashPaymentsfromOperatingActivities: NotRequired[
        list[TimeseriesResultItem]
    ]
    trailingOtherCashReceiptsfromOperatingActivities: NotRequired[
        list[TimeseriesResultItem]
    ]
    trailingOtherGandA: NotRequired[list[TimeseriesResultItem]]
    trailingOtherIncomeExpense: NotRequired[list[TimeseriesResultItem]]
    trailingOtherNonCashItems: NotRequired[list[TimeseriesResultItem]]
    trailingOtherNonInterestExpense: NotRequired[list[TimeseriesResultItem]]
    trailingOtherNonOperatingIncomeExpenses: NotRequired[list[TimeseriesResultItem]]
    trailingOtherOperatingExpenses: NotRequired[list[TimeseriesResultItem]]
    trailingOtherSpecialCharges: NotRequired[list[TimeseriesResultItem]]
    trailingOtherTaxes: NotRequired[list[TimeseriesResultItem]]
    trailingOtherunderPreferredStockDividend: NotRequired[list[TimeseriesResultItem]]
    trailingPaymentsonBehalfofEmployees: NotRequired[list[TimeseriesResultItem]]
    trailingPaymentstoSuppliersforGoodsandServices: NotRequired[
        list[TimeseriesResultItem]
    ]
    trailingPensionAndEmployeeBenefitExpense: NotRequired[list[TimeseriesResultItem]]
    trailingPolicyholderBenefitsCeded: NotRequired[list[TimeseriesResultItem]]
    trailingPolicyholderBenefitsGross: NotRequired[list[TimeseriesResultItem]]
    trailingPreferredStockDividendPaid: NotRequired[list[TimeseriesResultItem]]
    trailingPreferredStockDividends: NotRequired[list[TimeseriesResultItem]]
    trailingPreferredStockIssuance: NotRequired[list[TimeseriesResultItem]]
    trailingPreferredStockPayments: NotRequired[list[TimeseriesResultItem]]
    trailingPretaxIncome: NotRequired[list[TimeseriesResultItem]]
    trailingProceedsFromStockOptionExercised: NotRequired[list[TimeseriesResultItem]]
    trailingProfessionalExpenseAndContractServicesExpense: NotRequired[
        list[TimeseriesResultItem]
    ]
    trailingProvisionForDoubtfulAccounts: NotRequired[list[TimeseriesResultItem]]
    trailingProvisionandWriteOffofAssets: NotRequired[list[TimeseriesResultItem]]
    trailingPurchaseOfBusiness: NotRequired[list[TimeseriesResultItem]]
    trailingPurchaseOfIntangibles: NotRequired[list[TimeseriesResultItem]]
    trailingPurchaseOfInvestment: NotRequired[list[TimeseriesResultItem]]
    trailingPurchaseOfInvestmentProperties: NotRequired[list[TimeseriesResultItem]]
    trailingPurchaseOfPPE: NotRequired[list[TimeseriesResultItem]]
    trailingReceiptsfromCustomers: NotRequired[list[TimeseriesResultItem]]
    trailingReceiptsfromGovernmentGrants: NotRequired[list[TimeseriesResultItem]]
    trailingReconciledCostOfRevenue: NotRequired[list[TimeseriesResultItem]]
    trailingReconciledDepreciation: NotRequired[list[TimeseriesResultItem]]
    trailingRentAndLandingFees: NotRequired[list[TimeseriesResultItem]]
    trailingRentExpenseSupplemental: NotRequired[list[TimeseriesResultItem]]
    trailingRepaymentOfDebt: NotRequired[list[TimeseriesResultItem]]
    trailingReportedNormalizedBasicEPS: NotRequired[list[TimeseriesResultItem]]
    trailingReportedNormalizedDilutedEPS: NotRequired[list[TimeseriesResultItem]]
    trailingRepurchaseOfCapitalStock: NotRequired[list[TimeseriesResultItem]]
    trailingResearchAndDevelopment: NotRequired[list[TimeseriesResultItem]]
    trailingRestructuringAndMergernAcquisition: NotRequired[list[TimeseriesResultItem]]
    trailingSalariesAndWages: NotRequired[list[TimeseriesResultItem]]
    trailingSaleOfBusiness: NotRequired[list[TimeseriesResultItem]]
    trailingSaleOfIntangibles: NotRequired[list[TimeseriesResultItem]]
    trailingSaleOfInvestment: NotRequired[list[TimeseriesResultItem]]
    trailingSaleOfInvestmentProperties: NotRequired[list[TimeseriesResultItem]]
    trailingSaleOfPPE: NotRequired[list[TimeseriesResultItem]]
    trailingSecuritiesAmortization: NotRequired[list[TimeseriesResultItem]]
    trailingSellingAndMarketingExpense: NotRequired[list[TimeseriesResultItem]]
    trailingSellingGeneralAndAdministration: NotRequired[list[TimeseriesResultItem]]
    trailingShortTermDebtIssuance: NotRequired[list[TimeseriesResultItem]]
    trailingShortTermDebtPayments: NotRequired[list[TimeseriesResultItem]]
    trailingSpecialIncomeCharges: NotRequired[list[TimeseriesResultItem]]
    trailingStockBasedCompensation: NotRequired[list[TimeseriesResultItem]]
    trailingTaxEffectOfUnusualItems: NotRequired[list[TimeseriesResultItem]]
    trailingTaxLossCarryforwardBasicEPS: NotRequired[list[TimeseriesResultItem]]
    trailingTaxLossCarryforwardDilutedEPS: NotRequired[list[TimeseriesResultItem]]
    trailingTaxProvision: NotRequired[list[TimeseriesResultItem]]
    trailingTaxRateForCalcs: NotRequired[list[TimeseriesResultItem]]
    trailingTaxesRefundPaid: NotRequired[list[TimeseriesResultItem]]
    trailingTaxesRefundPaidDirect: NotRequired[list[TimeseriesResultItem]]
    trailingTotalExpenses: NotRequired[list[TimeseriesResultItem]]
    trailingTotalOperatingIncomeAsReported: NotRequired[list[TimeseriesResultItem]]
    trailingTotalOtherFinanceCost: NotRequired[list[TimeseriesResultItem]]
    trailingTotalRevenue: NotRequired[list[TimeseriesResultItem]]
    trailingTotalUnusualItems: NotRequired[list[TimeseriesResultItem]]
    trailingTotalUnusualItemsExcludingGoodwill: NotRequired[list[TimeseriesResultItem]]
    trailingUnrealizedGainLossOnInvestmentSecurities: NotRequired[
        list[TimeseriesResultItem]
    ]
    trailingWriteOff: NotRequired[list[TimeseriesResultItem]]


class Timeseries(TypedDict):
    result: list[TimeseriesResult]
    error: Error


class TimeseriesResponseJson(TypedDict):
    timeseries: Timeseries


class OptionChainResultQuote(TypedDict):
    language: str
    region: str
    quoteType: str
    typeDisp: str
    quoteSourceName: str
    triggerable: bool
    customPriceAlertConfidence: str
    corporateActions: list[Any]
    preMarketTime: NotRequired[int]
    postMarketTime: NotRequired[int]
    regularMarketTime: int
    exchange: str
    messageBoardId: str
    exchangeTimezoneName: str
    exchangeTimezoneShortName: str
    gmtOffSetMilliseconds: int
    market: str
    esgPopulated: bool
    currency: str
    regularMarketChangePercent: float
    regularMarketPrice: float
    shortName: str
    longName: str
    hasPrePostMarketData: bool
    firstTradeDateMilliseconds: int
    tradeable: bool
    cryptoTradeable: bool
    preMarketChangePercent: NotRequired[float]
    preMarketPrice: NotRequired[float]
    preMarketChange: NotRequired[float]
    postMarketChangePercent: NotRequired[float]
    postMarketPrice: NotRequired[float]
    postMarketChange: NotRequired[float]
    regularMarketChange: float
    regularMarketDayHigh: float
    regularMarketDayRange: str
    regularMarketDayLow: float
    regularMarketVolume: int
    regularMarketPreviousClose: float
    bid: float
    ask: float
    bidSize: int
    askSize: int
    fullExchangeName: str
    financialCurrency: str
    regularMarketOpen: float
    averageDailyVolume3Month: int
    averageDailyVolume10Day: int
    fiftyTwoWeekLowChange: float
    fiftyTwoWeekLowChangePercent: float
    fiftyTwoWeekRange: str
    fiftyTwoWeekHighChange: float
    fiftyTwoWeekHighChangePercent: float
    fiftyTwoWeekLow: float
    fiftyTwoWeekHigh: float
    fiftyTwoWeekChangePercent: float
    dividendDate: int
    earningsTimestamp: int
    earningsTimestampStart: int
    earningsTimestampEnd: int
    earningsCallTimestampStart: int
    earningsCallTimestampEnd: int
    isEarningsDateEstimate: bool
    trailingAnnualDividendRate: float
    trailingPE: float
    dividendRate: float
    trailingAnnualDividendYield: float
    dividendYield: float
    epsTrailingTwelveMonths: float
    epsForward: float
    epsCurrentYear: float
    priceEpsCurrentYear: float
    sharesOutstanding: int
    bookValue: float
    fiftyDayAverage: float
    fiftyDayAverageChange: float
    fiftyDayAverageChangePercent: float
    twoHundredDayAverage: float
    twoHundredDayAverageChange: float
    twoHundredDayAverageChangePercent: float
    marketCap: int
    forwardPE: float
    priceToBook: float
    sourceInterval: int
    exchangeDataDelayedBy: int
    ipoExpectedDate: NotRequired[str]
    prevName: NotRequired[str]
    nameChangeDate: NotRequired[str]
    averageAnalystRating: str
    priceHint: int
    marketState: str
    displayName: str
    symbol: str


class CallPutItem(TypedDict):
    contractSymbol: str
    strike: float
    currency: str
    lastPrice: float
    change: float
    percentChange: float
    volume: NotRequired[int]
    openInterest: int
    bid: float
    ask: float
    contractSize: str
    expiration: int
    lastTradeDate: int
    impliedVolatility: float
    inTheMoney: bool


class OptionItem(TypedDict):
    expirationDate: int
    hasMiniOptions: bool
    calls: list[CallPutItem]
    puts: list[CallPutItem]


class OptionChainResult(TypedDict):
    underlyingSymbol: str
    expirationDates: list[int]
    strikes: list[float]
    hasMiniOptions: bool
    quote: OptionChainResultQuote
    options: list[OptionItem]


class OptionChain(TypedDict):
    result: list[OptionChainResult]
    error: Error


class OptionsResponseJson(TypedDict):
    optionChain: OptionChain


class SearchQuote(TypedDict):
    exchange: str
    shortname: str
    quoteType: str
    symbol: str
    index: str
    score: float
    typeDisp: str
    longname: str
    exchDisp: str
    sector: str
    sectorDisp: NotRequired[str]
    industry: str
    industryDisp: NotRequired[str]
    dispSecIndFlag: bool
    isYahooFinance: bool
    prevName: NotRequired[str]
    nameChangeDate: NotRequired[str]


class SearchNew(TypedDict):
    uuid: str
    title: str
    publisher: str
    link: str
    providerPublishTime: int
    type: str
    thumbnail: NotRequired[dict[str, Any]]
    relatedTickers: list[str]


class SearchNav(TypedDict):
    navName: NotRequired[str]
    navUrl: NotRequired[str]
    navType: NotRequired[str]
    symbols: NotRequired[list[str]]


class SearchResult(TypedDict):
    explains: list[Any]
    count: int
    quotes: list[SearchQuote]
    news: list[SearchNew]
    nav: list[SearchNav]
    lists: list[Any]
    researchReports: list[Any]
    screenerFieldResults: list[Any]
    totalTime: int
    timeTakenForQuotes: int
    timeTakenForNews: int
    timeTakenForAlgowatchlist: int
    timeTakenForPredefinedScreener: int
    timeTakenForCrunchbase: int
    timeTakenForNav: int
    timeTakenForResearchReports: int
    timeTakenForScreenerField: int
    timeTakenForCulturalAssets: int
    timeTakenForSearchLists: int


class RecommendationsFinanceResultItem(TypedDict):
    symbol: str
    score: float


class RecommendationsFinanceResult(TypedDict):
    symbol: str
    recommendedSymbols: list[RecommendationsFinanceResultItem]


class RecommendationsFinance(TypedDict):
    result: list[RecommendationsFinanceResult]
    error: Error


class RecommendationsResponseJson(TypedDict):
    finance: RecommendationsFinance


class InsightsFinanceResultInstrumentInfo(TypedDict):
    technicalEvents: dict[str, Any]
    keyTechnicals: dict[str, Any]
    valuation: dict[str, Any]


class InsightsFinanceResultCompanySnapshot(TypedDict):
    sectorInfo: str
    company: dict[str, Any]
    sector: dict[str, Any]


class InsightsFinanceResultUpsell(TypedDict):
    msBullishSummary: NotRequired[list[str]]
    msBearishSummary: NotRequired[list[str]]
    companyName: str
    msBullishBearishSummariesPublishDate: NotRequired[int]
    upsellReportType: NotRequired[str]


class InsightsFinanceResultUpselSearchDD(TypedDict):
    researchReports: dict[str, Any]


class InsightsFinanceResultEventsItem(TypedDict):
    eventType: str
    pricePeriod: str
    tradingHorizon: str
    tradeType: str
    imageUrl: str
    startDate: int
    endDate: int


class InsightsFinanceResultReportsItem(TypedDict):
    id: str
    headHtml: str
    provider: str
    reportDate: str
    reportTitle: str
    reportType: str
    tickers: list[str]
    title: str


class InsightsFinanceResultSigDevsItem(TypedDict):
    headline: str
    date: str


class InsightsFinanceResultSecReportsItem(TypedDict):
    id: str
    type: str
    title: str
    description: str
    filingDate: int
    snapshotUrl: str
    formType: str


class InsightsFinanceResultRecommendation(TypedDict):
    targetPrice: float
    provider: str
    rating: str


class InsightsFinanceResult(TypedDict):
    symbol: str
    instrumentInfo: InsightsFinanceResultInstrumentInfo
    companySnapshot: InsightsFinanceResultCompanySnapshot
    recommendation: InsightsFinanceResultRecommendation
    upsell: InsightsFinanceResultUpsell
    upsellSearchDD: InsightsFinanceResultUpselSearchDD
    events: list[InsightsFinanceResultEventsItem]
    reports: list[InsightsFinanceResultReportsItem]
    sigDevs: list[InsightsFinanceResultSigDevsItem]
    secReports: NotRequired[list[InsightsFinanceResultSecReportsItem]]


class InsightsFinance(TypedDict):
    result: list[InsightsFinanceResult]
    error: Error


class InsightsResponseJson(TypedDict):
    finance: InsightsFinance


class RatingsItem(TypedDict):
    analyst: str
    dir: Format
    mm: Format
    pt: Format
    fin_score: Format
    datapoints: int
    ticker: str
    uuid: str
    rating_current: str
    rating_sentiment: int
    pt_current: float
    adjusted_pt_current: float
    announcement_date: str


class RatingsResult(TypedDict):
    dir: RatingsItem
    mm: RatingsItem
    pt: RatingsItem
    fin_score: RatingsItem


class MarketSummaryResponseResult(TypedDict):
    language: str
    region: str
    quoteType: str
    typeDisp: str
    quoteSourceName: NotRequired[str]
    triggerable: bool
    customPriceAlertConfidence: str
    currency: NotRequired[str]
    contractSymbol: NotRequired[bool]
    headSymbolAsString: NotRequired[str]
    shortName: str
    regularMarketChange: float
    regularMarketChangePercent: float
    regularMarketTime: int
    regularMarketPrice: float
    regularMarketPreviousClose: float
    longName: NotRequired[str]
    exchange: str
    market: str
    fullExchangeName: str
    hasPrePostMarketData: bool
    firstTradeDateMilliseconds: int
    priceHint: NotRequired[int]
    marketState: str
    sourceInterval: int
    exchangeDataDelayedBy: int
    exchangeTimezoneName: str
    exchangeTimezoneShortName: str
    gmtOffSetMilliseconds: int
    esgPopulated: bool
    tradeable: bool
    cryptoTradeable: bool
    symbol: str


class MarketSummaryResponse(TypedDict):
    result: list[MarketSummaryResponseResult]
    marketCategoryLongName: None
    error: Error


class MarketSummaryResponseJson(TypedDict):
    marketSummaryResponse: MarketSummaryResponse


class TrendingFinanceResult(TypedDict):
    count: int
    quotes: list[dict[str, str]]
    jobTimestamp: int
    startInterval: int


class TrendingFinance(TypedDict):
    result: list[TrendingFinanceResult]
    error: Error


class TrendingResponseJson(TypedDict):
    finance: TrendingFinance


class CurrenciesResult(TypedDict):
    shortName: str
    longName: str
    symbol: str
    localLongName: str


class Currencies(TypedDict):
    result: list[CurrenciesResult]
    error: Error


class CurrenciesResponseJson(TypedDict):
    currencies: Currencies


class CalendarEventsFinanceResultIpoEventsItemRecord(TypedDict):
    ipoEvents: bool
    ticker: str
    companyShortName: str
    exchangeShortName: str
    startDateTime: int
    currencyName: str
    dealType: str
    dealId: str


class CalendarEventsFinanceResultIpoEventsItem(TypedDict):
    timestamp: int
    timestampString: str
    timezone: str
    count: int
    totalCount: int
    records: list[CalendarEventsFinanceResultIpoEventsItemRecord]


class CalendarEventsFinanceResultSecReportsItemRecord(TypedDict):
    secReports: bool
    id: str
    type: str
    description: str
    filingDate: int
    ticker: str
    companyName: str
    category: NotRequired[str]
    thumbnailUrl: str
    exhibits: list[dict[str, str]]


class CalendarEventsFinanceResultSecReportsItem(TypedDict):
    timestamp: int
    timestampString: str
    timezone: str
    count: int
    totalCount: int
    records: list[CalendarEventsFinanceResultSecReportsItemRecord]


class CalendarEventsFinanceResultEarningsItemRecord(TypedDict):
    earnings: bool
    ticker: str
    companyShortName: str
    dateIsEstimate: bool
    startDateTime: int
    startDateTimeType: str
    fiscalYear: str
    quarter: str
    epsActual: float
    epsEstimate: float
    surprisePercent: float
    rank: int
    gmtOffsetMilliSeconds: int


class CalendarEventsFinanceResultEarningsItem(TypedDict):
    timestamp: int
    timestampString: str
    timezone: str
    count: int
    totalCount: int
    records: list[CalendarEventsFinanceResultEarningsItemRecord]


class CalendarEventsFinanceResultEconomicEventsItemRecord(TypedDict):
    economicEvents: bool
    event: str
    countryCode: str
    eventTime: int
    period: str
    actual: str
    prior: str
    revisedFrom: NotRequired[str]
    description: str


class CalendarEventsFinanceResultEconomicEventsItem(TypedDict):
    timestamp: int
    timestampString: str
    timezone: str
    count: int
    totalCount: int
    records: list[CalendarEventsFinanceResultEconomicEventsItemRecord]


class CalendarEventsFinanceResult(TypedDict):
    ipoEvents: list[CalendarEventsFinanceResultIpoEventsItem]
    secReports: list[CalendarEventsFinanceResultSecReportsItem]
    earnings: list[CalendarEventsFinanceResultEarningsItem]
    economicEvents: list[CalendarEventsFinanceResultEconomicEventsItem]


class CalendarEventsFinance(TypedDict):
    result: CalendarEventsFinanceResult
    error: Error


class CalendarEventsResponseJson(TypedDict):
    finance: CalendarEventsFinance


QuoteSummaryModuleResult: TypeAlias = (
    AssetProfile
    | RecommendationTrend
    | IndexTrend
    | DefaultKeyStatistics
    | IndustryTrend
    | FundOwnership
    | SummaryDetail
    | InsiderHolders
    | CalendarEvents
    | UpgradeDowngradeHistory
    | Price
    | EarningsTrend
    | SecFilings
    | InstitutionOwnership
    | MajorHoldersBreakdown
    | EarningsHistory
    | MajorDirectHolders
    | SummaryProfile
    | NetSharePurchaseActivity
    | InsiderTransactions
    | SectorTrend
    | Earnings
    | PageViews
    | FinancialData
)

QuoteSummaryModuleReturnValue: TypeAlias = (
    AssetProfile
    | list[RecommendationTrendItem]
    | IndexTrend
    | DefaultKeyStatistics
    | IndustryTrend
    | list[FundOwnershipItem]
    | SummaryDetail
    | list[InsiderHolderItem]
    | CalendarEvents
    | list[UpgradeDowngradeHistoryItem]
    | Price
    | list[EarningsTrendItem]
    | SecFilings
    | list[InstitutionOwnershipItem]
    | MajorHoldersBreakdown
    | list[EarningsHistoryItem]
    | MajorDirectHolders
    | SummaryProfile
    | NetSharePurchaseActivity
    | list[InsiderTransactionItem]
    | SectorTrend
    | Earnings
    | PageViews
    | FinancialData
)

ResponseJson: TypeAlias = (
    ChartResponseJson
    | QuoteResponseJson
    | QuoteTypeResponseJson
    | QuoteSummaryResponseJson
    | TimeseriesResponseJson
    | OptionsResponseJson
    | SearchResult
    | RecommendationsResponseJson
    | InsightsResponseJson
    | RatingsResult
    | MarketSummaryResponseJson
    | TrendingResponseJson
    | CurrenciesResponseJson
    | CalendarEventsResponseJson
)

ResponseJsonResult: TypeAlias = (
    ChartResult
    | QuoteResult
    | QuoteTypeResult
    | QuoteSummaryResult
    | RecommendationsFinanceResult
    | InsightsFinanceResult
    | OptionChainResult
    | AssetProfile
    | list[RecommendationTrendItem]
    | IndexTrend
    | DefaultKeyStatistics
    | IndustryTrend
    | list[FundOwnershipItem]
    | SummaryDetail
    | list[InsiderHolderItem]
    | CalendarEvents
    | list[UpgradeDowngradeHistoryItem]
    | Price
    | list[EarningsTrendItem]
    | SecFilings
    | list[InstitutionOwnershipItem]
    | MajorHoldersBreakdown
    | list[EarningsHistoryItem]
    | MajorDirectHolders
    | SummaryProfile
    | NetSharePurchaseActivity
    | list[InsiderTransactionItem]
    | SectorTrend
    | Earnings
    | PageViews
    | FinancialData
    | list[TimeseriesResult]
    | TrendingFinanceResult
    | CalendarEventsFinanceResult
    | RatingsResult
    | SearchResult
)
