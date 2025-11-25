from typing import Any, AsyncGenerator, Generator

import pytest
import pytest_asyncio
from pytest_mock import MockerFixture

from tests._assertions import (
    _assert_chart_result,
    _assert_insights_result,
    _assert_options_result,
    _assert_quote_summary_result,
    _assert_quote_summary_single_module_result,
    _assert_quote_types_result,
    _assert_quotes_result,
    _assert_ratings_result,
    _assert_recommendations_result,
    _assert_search_result,
    _assert_timeseries_result,
)
from tests._utils import _get_json_fixture, _mock_response
from yafin import AsyncSymbol, Symbol
from yafin.const import (
    ANNUAL_BALANCE_SHEET_TYPES,
    ANNUAL_CASH_FLOW_TYPES,
    ANNUAL_INCOME_STATEMENT_TYPES,
    QUOTE_SUMMARY_MODULES,
)


@pytest.fixture
def quote_json_mock(ticker: str) -> dict[str, Any]:
    """Quote response json mock."""
    return _get_json_fixture(file_name=f'{ticker.lower()}.json', folder_name='quote')


@pytest.fixture
def quote_type_json_mock(ticker: str) -> dict[str, Any]:
    """Quote_type response json mock."""
    return _get_json_fixture(
        file_name=f'{ticker.lower()}.json', folder_name='quote_type'
    )


@pytest.fixture
def search_json_mock(ticker: str) -> dict[str, Any]:
    """Search response json mock."""
    return _get_json_fixture(file_name=f'{ticker.lower()}.json', folder_name='search')


@pytest.fixture
def recommendations_json_mock(ticker: str) -> dict[str, Any]:
    """Recommendations response json mock."""
    return _get_json_fixture(
        file_name=f'{ticker.lower()}.json', folder_name='recommendations'
    )


@pytest.fixture
def insights_json_mock(ticker: str) -> dict[str, Any]:
    """Insights response json mock."""
    return _get_json_fixture(file_name=f'{ticker.lower()}.json', folder_name='insights')


@pytest.fixture
def calendar_events_json_mock(ticker: str) -> dict[str, Any]:
    """Quote summary response json mock with calendar events data."""
    return _get_json_fixture(
        file_name=f'calendar_events_{ticker.lower()}.json', folder_name='quote_summary'
    )


@pytest.fixture(scope='session')
def asset_profile_json_mock(ticker: str) -> dict[str, Any]:
    """Quote summary response json mock with asset profile data."""
    return _get_json_fixture(
        file_name=f'asset_profile_{ticker.lower()}.json', folder_name='quote_summary'
    )


@pytest.fixture(scope='session')
def summary_profile_json_mock(ticker: str) -> dict[str, Any]:
    """Quote summary response json mock with summary profile data."""
    return _get_json_fixture(
        file_name=f'summary_profile_{ticker.lower()}.json', folder_name='quote_summary'
    )


@pytest.fixture(scope='session')
def summary_detail_json_mock(ticker: str) -> dict[str, Any]:
    """Quote summary response json mock with summary detail data."""
    return _get_json_fixture(
        file_name=f'summary_detail_{ticker.lower()}.json', folder_name='quote_summary'
    )


@pytest.fixture(scope='session')
def esg_scores_json_mock(ticker: str) -> dict[str, Any]:
    """Quote summary response json mock with esg scores data."""
    return _get_json_fixture(
        file_name=f'esg_scores_{ticker.lower()}.json', folder_name='quote_summary'
    )


@pytest.fixture(scope='session')
def price_json_mock(ticker: str) -> dict[str, Any]:
    """Quote summary response json mock with price data."""
    return _get_json_fixture(
        file_name=f'price_{ticker.lower()}.json', folder_name='quote_summary'
    )


@pytest.fixture(scope='session')
def default_key_statistics_json_mock(ticker: str) -> dict[str, Any]:
    """Quote summary response json mock with default key statistics data."""
    return _get_json_fixture(
        file_name=f'default_key_statistics_{ticker.lower()}.json',
        folder_name='quote_summary',
    )


@pytest.fixture(scope='session')
def financial_data_json_mock(ticker: str) -> dict[str, Any]:
    """Quote summary response json mock with financial data."""
    return _get_json_fixture(
        file_name=f'financial_data_{ticker.lower()}.json', folder_name='quote_summary'
    )


@pytest.fixture(scope='session')
def sec_filings_json_mock(ticker: str) -> dict[str, Any]:
    """Quote summary response json mock with sec filings data."""
    return _get_json_fixture(
        file_name=f'sec_filings_{ticker.lower()}.json', folder_name='quote_summary'
    )


@pytest.fixture(scope='session')
def upgrade_downgrade_history_json_mock(ticker: str) -> dict[str, Any]:
    """Quote summary response json mock with upgrade downgrade history data."""
    return _get_json_fixture(
        file_name=f'upgrade_downgrade_history_{ticker.lower()}.json',
        folder_name='quote_summary',
    )


@pytest.fixture(scope='session')
def institution_ownership_json_mock(ticker: str) -> dict[str, Any]:
    """Quote summary response json mock with institution ownership data."""
    return _get_json_fixture(
        file_name=f'institution_ownership_{ticker.lower()}.json',
        folder_name='quote_summary',
    )


@pytest.fixture(scope='session')
def fund_ownership_json_mock(ticker: str) -> dict[str, Any]:
    """Quote summary response json mock with fund ownership data."""
    return _get_json_fixture(
        file_name=f'fund_ownership_{ticker.lower()}.json', folder_name='quote_summary'
    )


@pytest.fixture(scope='session')
def major_direct_holders_json_mock(ticker: str) -> dict[str, Any]:
    """Quote summary response json mock with major direct holders data."""
    return _get_json_fixture(
        file_name=f'major_direct_holders_{ticker.lower()}.json',
        folder_name='quote_summary',
    )


@pytest.fixture(scope='session')
def major_holders_breakdown_json_mock(ticker: str) -> dict[str, Any]:
    """Quote summary response json mock with major holders breakdown data."""
    return _get_json_fixture(
        file_name=f'major_holders_breakdown_{ticker.lower()}.json',
        folder_name='quote_summary',
    )


@pytest.fixture(scope='session')
def insider_transactions_json_mock(ticker: str) -> dict[str, Any]:
    """Quote summary response json mock with insider transactions data."""
    return _get_json_fixture(
        file_name=f'insider_transactions_{ticker.lower()}.json',
        folder_name='quote_summary',
    )


@pytest.fixture(scope='session')
def insider_holders_json_mock(ticker: str) -> dict[str, Any]:
    """Quote summary response json mock with insider holders data."""
    return _get_json_fixture(
        file_name=f'insider_holders_{ticker.lower()}.json', folder_name='quote_summary'
    )


@pytest.fixture(scope='session')
def net_share_purchase_activity_json_mock(ticker: str) -> dict[str, Any]:
    """Quote summary response json mock with net share purchase activity data."""  # noqa: E501
    return _get_json_fixture(
        file_name=f'net_share_purchase_activity_{ticker.lower()}.json',
        folder_name='quote_summary',
    )


@pytest.fixture(scope='session')
def earnings_json_mock(ticker: str) -> dict[str, Any]:
    """Quote summary response json mock with net earnings data."""
    return _get_json_fixture(
        file_name=f'earnings_{ticker.lower()}.json', folder_name='quote_summary'
    )


@pytest.fixture(scope='session')
def earnings_history_json_mock(ticker: str) -> dict[str, Any]:
    """Quote summary response json mock with net earnings history data."""
    return _get_json_fixture(
        file_name=f'earnings_history_{ticker.lower()}.json', folder_name='quote_summary'
    )


@pytest.fixture(scope='session')
def earnings_trend_json_mock(ticker: str) -> dict[str, Any]:
    """Quote summary response json mock with net earnings trend data."""
    return _get_json_fixture(
        file_name=f'earnings_trend_{ticker.lower()}.json', folder_name='quote_summary'
    )


@pytest.fixture(scope='session')
def industry_trend_json_mock(ticker: str) -> dict[str, Any]:
    """Quote summary response json mock with net industry trend data."""
    return _get_json_fixture(
        file_name=f'industry_trend_{ticker.lower()}.json', folder_name='quote_summary'
    )


@pytest.fixture(scope='session')
def index_trend_json_mock(ticker: str) -> dict[str, Any]:
    """Quote summary response json mock with net index trend data."""
    return _get_json_fixture(
        file_name=f'index_trend_{ticker.lower()}.json', folder_name='quote_summary'
    )


@pytest.fixture(scope='session')
def sector_trend_json_mock(ticker: str) -> dict[str, Any]:
    """Quote summary response json mock with net sector trend data."""
    return _get_json_fixture(
        file_name=f'sector_trend_{ticker.lower()}.json', folder_name='quote_summary'
    )


@pytest.fixture(scope='session')
def recommendation_trend_json_mock(ticker: str) -> dict[str, Any]:
    """Quote summary response json mock with net recommendations trend data."""
    return _get_json_fixture(
        file_name=f'recommendation_trend_{ticker.lower()}.json',
        folder_name='quote_summary',
    )


@pytest.fixture(scope='session')
def page_views_json_mock(ticker: str) -> dict[str, Any]:
    """Quote summary response json mock with net page views data."""
    return _get_json_fixture(
        file_name=f'page_views_{ticker.lower()}.json', folder_name='quote_summary'
    )


class TestUnitSymbol:
    """Unit tests for yafin.Symbol."""

    def test_client(self) -> None:
        """Test client attribute."""
        symbol = Symbol('META')
        assert symbol._client is None

        symbol._get_client()
        assert symbol._client

        symbol.close()
        assert symbol._client is None

        with Symbol('META') as symbol:
            assert symbol._client

        assert symbol._client is None

    def test_client_singleton(self) -> None:
        """Test client attribute singleton pattern."""
        meta = Symbol('META')
        aapl = Symbol('AAPL')

        meta._get_client()
        aapl._get_client()

        # test it is singleton
        assert meta._client is aapl._client

        meta.close()
        aapl.close()

    def test_close(self) -> None:
        """Test client attribute singleton pattern."""
        meta = Symbol('META')
        aapl = Symbol('AAPL')

        meta._get_client()
        aapl._get_client()

        assert meta._client
        assert aapl._client

        # meta close should not close the aapl client
        meta.close()
        assert meta._client is None
        assert aapl._client

        aapl.close()
        assert meta._client is None
        assert aapl._client is None

    @pytest.fixture
    def symbol(self, ticker: str) -> Generator[Symbol, None, None]:
        """Fresh new instance of Symbol for each tests."""
        with Symbol(ticker) as symbol:
            yield symbol

    def test_get_chart(
        self,
        symbol: Symbol,
        chart_kwargs: dict[str, Any],
        mocker: MockerFixture,
        chart_json_mock: dict[str, Any],
        interval: str,
        period_range: str | None,
        period1: int | float | None,
        period2: int | float | None,
    ) -> None:
        """Test get_chart method."""
        _mock_response(
            mocker,
            patched_method='yafin.client.Session.get',
            response_jsons=[chart_json_mock],
        )
        chart_result = symbol.get_chart(
            interval=interval,
            period_range=period_range,
            period1=period1,
            period2=period2,
            **chart_kwargs,
        )
        _assert_chart_result(chart_result, symbol.ticker)

    def test_get_chart_invalid_args(
        self,
        symbol: Symbol,
        invalid_chart_kwargs_err_tuple: tuple[dict[str, Any], type[Exception]],
    ) -> None:
        """Test get_chart method with invalid arguments."""
        kwargs, err_cls = invalid_chart_kwargs_err_tuple
        with pytest.raises(err_cls):
            symbol.get_chart(**kwargs)

    def test_get_quote(
        self,
        symbol: Symbol,
        mocker: MockerFixture,
        quote_json_mock: dict[str, Any],
    ) -> None:
        """Test get_quote method."""
        _mock_response(
            mocker,
            patched_method='yafin.client.Session.get',
            response_jsons=[quote_json_mock],
        )
        quotes_result = symbol.get_quote()
        _assert_quotes_result(quotes_result, symbol.ticker)

    def test_get_quote_type(
        self,
        symbol: Symbol,
        mocker: MockerFixture,
        quote_type_json_mock: dict[str, Any],
    ) -> None:
        """Test get_quote_type method."""
        _mock_response(
            mocker,
            patched_method='yafin.client.Session.get',
            response_jsons=[quote_type_json_mock],
        )
        quote_types_result = symbol.get_quote_type()
        _assert_quote_types_result(quote_types_result, symbol.ticker)

    def test_get_quote_summary_all_modules(
        self,
        symbol: Symbol,
        mocker: MockerFixture,
        quote_summary_all_modules_json_mock: dict[str, Any],
    ) -> None:
        """Test get_quote_summary_all_modules method."""
        _mock_response(
            mocker,
            patched_method='yafin.client.Session.get',
            response_jsons=[quote_summary_all_modules_json_mock],
        )
        quote_summary_all_modules = symbol.get_quote_summary_all_modules()
        _assert_quote_summary_result(quote_summary_all_modules, QUOTE_SUMMARY_MODULES)

    def test_get_quote_summary_single_module(
        self,
        symbol: Symbol,
        mocker: MockerFixture,
        asset_profile_json_mock: dict[str, Any],
    ) -> None:
        """Test _get_quote_summary_single_module method."""
        _mock_response(
            mocker,
            patched_method='yafin.client.Session.get',
            response_jsons=[asset_profile_json_mock],
        )
        module = 'assetProfile'
        asset_profile = symbol._get_quote_summary_single_module(module)
        _assert_quote_summary_single_module_result(asset_profile, module)

    def test_get_quote_summary_single_module_invalid_args(self, symbol: Symbol) -> None:
        """Test _get_quote_summary_single_module method with invalid arguments."""
        with pytest.raises(ValueError):
            symbol._get_quote_summary_single_module(module='xxx')

    def test_get_asset_profile(
        self,
        symbol: Symbol,
        mocker: MockerFixture,
        asset_profile_json_mock: dict[str, Any],
    ) -> None:
        """Test get_asset_profile method."""
        _mock_response(
            mocker,
            patched_method='yafin.client.Session.get',
            response_jsons=[asset_profile_json_mock],
        )
        asset_profile = symbol.get_asset_profile()
        _assert_quote_summary_single_module_result(asset_profile, 'assetProfile')

    def test_get_summary_profile(
        self,
        symbol: Symbol,
        mocker: MockerFixture,
        summary_profile_json_mock: dict[str, Any],
    ) -> None:
        """Test get_summary_profile method."""
        _mock_response(
            mocker,
            patched_method='yafin.client.Session.get',
            response_jsons=[summary_profile_json_mock],
        )
        summary_profile = symbol.get_summary_profile()
        _assert_quote_summary_single_module_result(summary_profile, 'summaryProfile')

    def test_get_summary_detail(
        self,
        symbol: Symbol,
        mocker: MockerFixture,
        summary_detail_json_mock: dict[str, Any],
    ) -> None:
        """Test get_summary_detail method."""
        _mock_response(
            mocker,
            patched_method='yafin.client.Session.get',
            response_jsons=[summary_detail_json_mock],
        )
        summary_detail = symbol.get_summary_detail()
        _assert_quote_summary_single_module_result(summary_detail, 'summaryDetail')

    def test_get_price(
        self,
        symbol: Symbol,
        mocker: MockerFixture,
        price_json_mock: dict[str, Any],
    ) -> None:
        """Test get_price method."""
        _mock_response(
            mocker,
            patched_method='yafin.client.Session.get',
            response_jsons=[price_json_mock],
        )
        price = symbol.get_price()
        _assert_quote_summary_single_module_result(price, 'price')

    def test_get_default_key_statistics(
        self,
        symbol: Symbol,
        mocker: MockerFixture,
        default_key_statistics_json_mock: dict[str, Any],
    ) -> None:
        """Test get_default_key_statistics method."""
        _mock_response(
            mocker,
            patched_method='yafin.client.Session.get',
            response_jsons=[default_key_statistics_json_mock],
        )
        default_key_statistics = symbol.get_default_key_statistics()
        _assert_quote_summary_single_module_result(
            default_key_statistics, 'defaultKeyStatistics'
        )

    def test_get_financial_data(
        self,
        symbol: Symbol,
        mocker: MockerFixture,
        financial_data_json_mock: dict[str, Any],
    ) -> None:
        """Test get_financial_data method."""
        _mock_response(
            mocker,
            patched_method='yafin.client.Session.get',
            response_jsons=[financial_data_json_mock],
        )
        financial_data = symbol.get_financial_data()
        _assert_quote_summary_single_module_result(financial_data, 'financialData')

    def test_get_calendar_events(
        self,
        symbol: Symbol,
        mocker: MockerFixture,
        calendar_events_json_mock: dict[str, Any],
    ) -> None:
        """Test get_calendar_events method."""
        _mock_response(
            mocker,
            patched_method='yafin.client.Session.get',
            response_jsons=[calendar_events_json_mock],
        )
        calendar_events = symbol.get_calendar_events()
        _assert_quote_summary_single_module_result(calendar_events, 'calendarEvents')

    def test_get_sec_filings(
        self,
        symbol: Symbol,
        mocker: MockerFixture,
        sec_filings_json_mock: dict[str, Any],
    ) -> None:
        """Test get_sec_filings method."""
        _mock_response(
            mocker,
            patched_method='yafin.client.Session.get',
            response_jsons=[sec_filings_json_mock],
        )
        sec_filings = symbol.get_sec_filings()
        _assert_quote_summary_single_module_result(sec_filings, 'secFilings')

    def test_get_upgrade_downgrade_history(
        self,
        symbol: Symbol,
        mocker: MockerFixture,
        upgrade_downgrade_history_json_mock: dict[str, Any],
    ) -> None:
        """Test get_upgrade_downgrade_history method."""
        _mock_response(
            mocker,
            patched_method='yafin.client.Session.get',
            response_jsons=[upgrade_downgrade_history_json_mock],
        )
        upgrade_downgrade_history = symbol.get_upgrade_downgrade_history()
        _assert_quote_summary_single_module_result(
            upgrade_downgrade_history, 'upgradeDowngradeHistory'
        )

    def test_get_institution_ownership(
        self,
        symbol: Symbol,
        mocker: MockerFixture,
        institution_ownership_json_mock: dict[str, Any],
    ) -> None:
        """Test get_institution_ownership method."""
        _mock_response(
            mocker,
            patched_method='yafin.client.Session.get',
            response_jsons=[institution_ownership_json_mock],
        )
        institution_ownership = symbol.get_institution_ownership()
        _assert_quote_summary_single_module_result(
            institution_ownership, 'institutionOwnership'
        )

    def test_get_fund_ownership(
        self,
        symbol: Symbol,
        mocker: MockerFixture,
        fund_ownership_json_mock: dict[str, Any],
    ) -> None:
        """Test get_fund_ownership method."""
        _mock_response(
            mocker,
            patched_method='yafin.client.Session.get',
            response_jsons=[fund_ownership_json_mock],
        )
        fund_ownership = symbol.get_fund_ownership()
        _assert_quote_summary_single_module_result(fund_ownership, 'fundOwnership')

    def test_get_major_direct_holders(
        self,
        symbol: Symbol,
        mocker: MockerFixture,
        major_direct_holders_json_mock: dict[str, Any],
    ) -> None:
        """Test get_major_direct_holders method."""
        _mock_response(
            mocker,
            patched_method='yafin.client.Session.get',
            response_jsons=[major_direct_holders_json_mock],
        )
        major_direct_holders = symbol.get_major_direct_holders()
        _assert_quote_summary_single_module_result(
            major_direct_holders, 'majorDirectHolders'
        )

    def test_get_major_holders_breakdown(
        self,
        symbol: Symbol,
        mocker: MockerFixture,
        major_holders_breakdown_json_mock: dict[str, Any],
    ) -> None:
        """Test get_major_holders_breakdown method."""
        _mock_response(
            mocker,
            patched_method='yafin.client.Session.get',
            response_jsons=[major_holders_breakdown_json_mock],
        )
        major_holders_breakdown = symbol.get_major_holders_breakdown()
        _assert_quote_summary_single_module_result(
            major_holders_breakdown, 'majorHoldersBreakdown'
        )

    def test_get_insider_transactions(
        self,
        symbol: Symbol,
        mocker: MockerFixture,
        insider_transactions_json_mock: dict[str, Any],
    ) -> None:
        """Test get_insider_transactions method."""
        _mock_response(
            mocker,
            patched_method='yafin.client.Session.get',
            response_jsons=[insider_transactions_json_mock],
        )
        insider_transactions = symbol.get_insider_transactions()
        _assert_quote_summary_single_module_result(
            insider_transactions, 'insiderTransactions'
        )

    def test_get_insider_holders(
        self,
        symbol: Symbol,
        mocker: MockerFixture,
        insider_holders_json_mock: dict[str, Any],
    ) -> None:
        """Test get_insider_holders method."""
        _mock_response(
            mocker,
            patched_method='yafin.client.Session.get',
            response_jsons=[insider_holders_json_mock],
        )
        insider_holders = symbol.get_insider_holders()
        _assert_quote_summary_single_module_result(insider_holders, 'insiderHolders')

    def test_get_net_share_purchase_activity(
        self,
        symbol: Symbol,
        mocker: MockerFixture,
        net_share_purchase_activity_json_mock: dict[str, Any],
    ) -> None:
        """Test get_net_share_purchase_activity method."""
        _mock_response(
            mocker,
            patched_method='yafin.client.Session.get',
            response_jsons=[net_share_purchase_activity_json_mock],
        )
        net_share_purchase_activity = symbol.get_net_share_purchase_activity()
        _assert_quote_summary_single_module_result(
            net_share_purchase_activity, 'netSharePurchaseActivity'
        )

    def test_get_earnings(
        self,
        symbol: Symbol,
        mocker: MockerFixture,
        earnings_json_mock: dict[str, Any],
    ) -> None:
        """Test get_earnings method."""
        _mock_response(
            mocker,
            patched_method='yafin.client.Session.get',
            response_jsons=[earnings_json_mock],
        )
        earnings = symbol.get_earnings()
        _assert_quote_summary_single_module_result(earnings, 'earnings')

    def test_get_earnings_history(
        self,
        symbol: Symbol,
        mocker: MockerFixture,
        earnings_history_json_mock: dict[str, Any],
    ) -> None:
        """Test get_earnings_history method."""
        _mock_response(
            mocker,
            patched_method='yafin.client.Session.get',
            response_jsons=[earnings_history_json_mock],
        )
        earnings_history = symbol.get_earnings_history()
        _assert_quote_summary_single_module_result(earnings_history, 'earningsHistory')

    def test_get_earnings_trend(
        self,
        symbol: Symbol,
        mocker: MockerFixture,
        earnings_trend_json_mock: dict[str, Any],
    ) -> None:
        """Test get_earnings_trend method."""
        _mock_response(
            mocker,
            patched_method='yafin.client.Session.get',
            response_jsons=[earnings_trend_json_mock],
        )
        earnings_trend = symbol.get_earnings_trend()
        _assert_quote_summary_single_module_result(earnings_trend, 'earningsTrend')

    def test_get_industry_trend(
        self,
        symbol: Symbol,
        mocker: MockerFixture,
        industry_trend_json_mock: dict[str, Any],
    ) -> None:
        """Test get_industry_trend method."""
        _mock_response(
            mocker,
            patched_method='yafin.client.Session.get',
            response_jsons=[industry_trend_json_mock],
        )
        industry_trend = symbol.get_industry_trend()
        _assert_quote_summary_single_module_result(industry_trend, 'industryTrend')

    def test_get_index_trend(
        self,
        symbol: Symbol,
        mocker: MockerFixture,
        index_trend_json_mock: dict[str, Any],
    ) -> None:
        """Test get_index_trend method."""
        _mock_response(
            mocker,
            patched_method='yafin.client.Session.get',
            response_jsons=[index_trend_json_mock],
        )
        index_trend = symbol.get_index_trend()
        _assert_quote_summary_single_module_result(index_trend, 'indexTrend')

    def test_get_sector_trend(
        self,
        symbol: Symbol,
        mocker: MockerFixture,
        sector_trend_json_mock: dict[str, Any],
    ) -> None:
        """Test get_sector_trend method."""
        _mock_response(
            mocker,
            patched_method='yafin.client.Session.get',
            response_jsons=[sector_trend_json_mock],
        )
        sector_trend = symbol.get_sector_trend()
        _assert_quote_summary_single_module_result(sector_trend, 'sectorTrend')

    def test_get_recommendation_trend(
        self,
        symbol: Symbol,
        mocker: MockerFixture,
        recommendation_trend_json_mock: dict[str, Any],
    ) -> None:
        """Test get_recommendation_trend method."""
        _mock_response(
            mocker,
            patched_method='yafin.client.Session.get',
            response_jsons=[recommendation_trend_json_mock],
        )
        recommendation_trend = symbol.get_recommendation_trend()
        _assert_quote_summary_single_module_result(
            recommendation_trend, 'recommendationTrend'
        )

    def test_get_page_views(
        self,
        symbol: Symbol,
        mocker: MockerFixture,
        page_views_json_mock: dict[str, Any],
    ) -> None:
        """Test get_page_views method."""
        _mock_response(
            mocker,
            patched_method='yafin.client.Session.get',
            response_jsons=[page_views_json_mock],
        )
        page_views = symbol.get_page_views()
        _assert_quote_summary_single_module_result(page_views, 'pageViews')

    def test_get_financials(
        self,
        symbol: Symbol,
        mocker: MockerFixture,
        timeseries_income_statement_json_mock: dict[str, Any],
        period1: int | float | None,
        period2: int | float | None,
    ) -> None:
        """Test _get_financials method."""
        _mock_response(
            mocker,
            patched_method='yafin.client.Session.get',
            response_jsons=[timeseries_income_statement_json_mock],
        )
        annual_income_stmt = symbol._get_financials(
            frequency='annual', typ='income_statement', period1=period1, period2=period2
        )
        _assert_timeseries_result(
            annual_income_stmt, symbol.ticker, ANNUAL_INCOME_STATEMENT_TYPES
        )

    def test_get_income_statement(
        self,
        symbol: Symbol,
        mocker: MockerFixture,
        timeseries_income_statement_json_mock: dict[str, Any],
        period1: int | float | None,
        period2: int | float | None,
    ) -> None:
        """Test get_income_statement method."""
        _mock_response(
            mocker,
            patched_method='yafin.client.Session.get',
            response_jsons=[timeseries_income_statement_json_mock],
        )
        annual_income_stmt = symbol.get_income_statement(
            frequency='annual', period1=period1, period2=period2
        )
        _assert_timeseries_result(
            annual_income_stmt, symbol.ticker, ANNUAL_INCOME_STATEMENT_TYPES
        )

    def test_get_income_statement_invalid_args(self, symbol: Symbol) -> None:
        """Test get_income_statement method with invalid arguments.."""
        with pytest.raises(ValueError):
            symbol.get_income_statement(frequency='xxx')

    def test_get_balance_sheet(
        self,
        symbol: Symbol,
        mocker: MockerFixture,
        timeseries_balance_sheet_json_mock: dict[str, Any],
        period1: int | float | None,
        period2: int | float | None,
    ) -> None:
        """Test get_balance_sheet method."""
        _mock_response(
            mocker,
            patched_method='yafin.client.Session.get',
            response_jsons=[timeseries_balance_sheet_json_mock],
        )
        annual_balance_sheet = symbol.get_balance_sheet(
            frequency='annual', period1=period1, period2=period2
        )
        _assert_timeseries_result(
            annual_balance_sheet, symbol.ticker, ANNUAL_BALANCE_SHEET_TYPES
        )

    def test_get_balance_sheet_invalid_args(
        self,
        symbol: Symbol,
        invalid_balance_sheet_kwargs_err_tuple: tuple[dict[str, Any], type[Exception]],
    ) -> None:
        """Test get_balance_sheet method."""
        kwargs, err_cls = invalid_balance_sheet_kwargs_err_tuple
        with pytest.raises(err_cls):
            symbol.get_balance_sheet(**kwargs)

    def test_get_cash_flow(
        self,
        symbol: Symbol,
        mocker: MockerFixture,
        timeseries_cash_flow_json_mock: dict[str, Any],
        period1: int | float | None,
        period2: int | float | None,
    ) -> None:
        """Test get_cash_flow method."""
        _mock_response(
            mocker,
            patched_method='yafin.client.Session.get',
            response_jsons=[timeseries_cash_flow_json_mock],
        )
        annual_cash_flow = symbol.get_cash_flow(
            frequency='annual', period1=period1, period2=period2
        )
        _assert_timeseries_result(
            annual_cash_flow, symbol.ticker, ANNUAL_CASH_FLOW_TYPES
        )

    def test_get_cash_flow_invalid_args(self, symbol: Symbol) -> None:
        """Test get_cash_flow method with invalid arguments."""
        with pytest.raises(ValueError):
            symbol.get_cash_flow(frequency='xxx')

    def test_get_options(
        self,
        symbol: Symbol,
        mocker: MockerFixture,
        options_json_mock: dict[str, Any],
    ) -> None:
        """Test get_options method."""
        _mock_response(
            mocker,
            patched_method='yafin.client.Session.get',
            response_jsons=[options_json_mock],
        )
        options = symbol.get_options()
        _assert_options_result(options, symbol.ticker)

    def test_get_search(
        self,
        symbol: Symbol,
        mocker: MockerFixture,
        search_json_mock: dict[str, Any],
    ) -> None:
        """Test get_search method."""
        _mock_response(
            mocker,
            patched_method='yafin.client.Session.get',
            response_jsons=[search_json_mock],
        )
        search = symbol.get_search()
        _assert_search_result(search)

    def test_get_recommendations(
        self,
        symbol: Symbol,
        mocker: MockerFixture,
        recommendations_json_mock: dict[str, Any],
    ) -> None:
        """Test get_recommendations method."""
        _mock_response(
            mocker,
            patched_method='yafin.client.Session.get',
            response_jsons=[recommendations_json_mock],
        )
        recommendations_result = symbol.get_recommendations()
        _assert_recommendations_result(recommendations_result, symbol.ticker)

    def test_get_insights(
        self,
        symbol: Symbol,
        mocker: MockerFixture,
        insights_json_mock: dict[str, Any],
    ) -> None:
        """Test get_insights method."""
        _mock_response(
            mocker,
            patched_method='yafin.client.Session.get',
            response_jsons=[insights_json_mock],
        )
        insights_result = symbol.get_insights()
        _assert_insights_result(insights_result, symbol.ticker)

    def test_get_ratings(
        self,
        symbol: Symbol,
        mocker: MockerFixture,
        ratings_json_mock: dict[str, Any],
    ) -> None:
        """Test get_ratings method."""
        _mock_response(
            mocker,
            patched_method='yafin.client.Session.get',
            response_jsons=[ratings_json_mock],
        )
        ratings = symbol.get_ratings()
        _assert_ratings_result(ratings, symbol.ticker)


class TestUnitAsyncSymbol:
    """Unit tests for yafin.AsyncSymbol."""

    @pytest.mark.asyncio
    async def test_client(self) -> None:
        """Test client attribute."""
        async_symbol = AsyncSymbol('META')
        assert async_symbol._client is None

        await async_symbol._get_client()
        assert async_symbol._client

        await async_symbol.close()
        assert async_symbol._client is None

        async with AsyncSymbol('META') as async_symbol:
            assert async_symbol._client

        assert async_symbol._client is None

    @pytest.mark.asyncio
    async def test_client_singleton(self) -> None:
        """Test client attribute singleton pattern."""
        meta = AsyncSymbol('META')
        aapl = AsyncSymbol('AAPL')

        await meta._get_client()
        await aapl._get_client()

        # test it is singleton
        assert meta._client is aapl._client

        await meta.close()
        await aapl.close()

    @pytest.mark.asyncio
    async def test_close(self) -> None:
        """Test client attribute singleton pattern."""
        meta = AsyncSymbol('META')
        aapl = AsyncSymbol('AAPL')

        await meta._get_client()
        await aapl._get_client()

        assert meta._client
        assert aapl._client

        # meta close should not close the aapl client
        await meta.close()
        assert meta._client is None
        assert aapl._client

        await aapl.close()
        assert meta._client is None
        assert aapl._client is None

    @pytest_asyncio.fixture
    async def async_symbol(self, ticker: str) -> AsyncGenerator[AsyncSymbol, None]:
        """Fresh new instance of AsyncSymbol for each tests."""
        async with AsyncSymbol(ticker) as async_symbol:
            yield async_symbol

    @pytest.mark.asyncio
    async def test_get_chart(
        self,
        async_symbol: AsyncSymbol,
        chart_kwargs: dict[str, Any],
        mocker: MockerFixture,
        chart_json_mock: dict[str, Any],
        interval: str,
        period_range: str | None,
        period1: int | float | None,
        period2: int | float | None,
    ) -> None:
        """Test get_chart method."""
        _mock_response(
            mocker,
            patched_method='yafin.client.AsyncSession.get',
            response_jsons=[chart_json_mock],
            async_mock=True,
        )
        chart_result = await async_symbol.get_chart(
            interval=interval,
            period_range=period_range,
            period1=period1,
            period2=period2,
            **chart_kwargs,
        )
        _assert_chart_result(chart_result, async_symbol.ticker)

    @pytest.mark.asyncio
    async def test_get_chart_invalid_args(
        self,
        async_symbol: AsyncSymbol,
        invalid_chart_kwargs_err_tuple: tuple[dict[str, Any], type[Exception]],
    ) -> None:
        """Test get_chart method with invalid arguments."""
        kwargs, err_cls = invalid_chart_kwargs_err_tuple
        with pytest.raises(err_cls):
            await async_symbol.get_chart(**kwargs)

    @pytest.mark.asyncio
    async def test_get_quote(
        self,
        async_symbol: AsyncSymbol,
        mocker: MockerFixture,
        quote_json_mock: dict[str, Any],
    ) -> None:
        """Test get_quote method."""
        _mock_response(
            mocker,
            patched_method='yafin.client.AsyncSession.get',
            response_jsons=[quote_json_mock],
            async_mock=True,
        )
        quotes_result = await async_symbol.get_quote()
        _assert_quotes_result(quotes_result, async_symbol.ticker)

    @pytest.mark.asyncio
    async def test_get_quote_type(
        self,
        async_symbol: AsyncSymbol,
        mocker: MockerFixture,
        quote_type_json_mock: dict[str, Any],
    ) -> None:
        """Test get_quote_type method."""
        _mock_response(
            mocker,
            patched_method='yafin.client.AsyncSession.get',
            response_jsons=[quote_type_json_mock],
            async_mock=True,
        )
        quote_types_result = await async_symbol.get_quote_type()
        _assert_quote_types_result(quote_types_result, async_symbol.ticker)

    @pytest.mark.asyncio
    async def test_get_quote_summary_all_modules(
        self,
        async_symbol: AsyncSymbol,
        mocker: MockerFixture,
        quote_summary_all_modules_json_mock: dict[str, Any],
    ) -> None:
        """Test get_quote_summary_all_modules method."""
        _mock_response(
            mocker,
            patched_method='yafin.client.AsyncSession.get',
            response_jsons=[quote_summary_all_modules_json_mock],
            async_mock=True,
        )
        quote_summary_all_modules = await async_symbol.get_quote_summary_all_modules()
        _assert_quote_summary_result(
            quote_summary_all_modules, modules=QUOTE_SUMMARY_MODULES
        )

    @pytest.mark.asyncio
    async def test_get_quote_summary_single_module(
        self,
        async_symbol: AsyncSymbol,
        mocker: MockerFixture,
        asset_profile_json_mock: dict[str, Any],
    ) -> None:
        """Test _get_quote_summary_single_module method."""
        _mock_response(
            mocker,
            patched_method='yafin.client.AsyncSession.get',
            response_jsons=[asset_profile_json_mock],
            async_mock=True,
        )
        module = 'assetProfile'
        asset_profile = await async_symbol._get_quote_summary_single_module(module)
        _assert_quote_summary_single_module_result(asset_profile, module)

    @pytest.mark.asyncio
    async def test_get_quote_summary_single_module_invalid_args(
        self, async_symbol: AsyncSymbol
    ) -> None:
        """Test _get_quote_summary_single_module method with invalid arguments."""
        with pytest.raises(ValueError):
            await async_symbol._get_quote_summary_single_module(module='xxx')

    @pytest.mark.asyncio
    async def test_get_asset_profile(
        self,
        async_symbol: AsyncSymbol,
        mocker: MockerFixture,
        asset_profile_json_mock: dict[str, Any],
    ) -> None:
        """Test get_asset_profile method."""
        _mock_response(
            mocker,
            patched_method='yafin.client.AsyncSession.get',
            response_jsons=[asset_profile_json_mock],
            async_mock=True,
        )
        asset_profile = await async_symbol.get_asset_profile()
        _assert_quote_summary_single_module_result(asset_profile, 'assetProfile')

    @pytest.mark.asyncio
    async def test_get_summary_profile(
        self,
        async_symbol: AsyncSymbol,
        mocker: MockerFixture,
        summary_profile_json_mock: dict[str, Any],
    ) -> None:
        """Test get_summary_profile method."""
        _mock_response(
            mocker,
            patched_method='yafin.client.AsyncSession.get',
            response_jsons=[summary_profile_json_mock],
            async_mock=True,
        )
        summary_profile = await async_symbol.get_summary_profile()
        _assert_quote_summary_single_module_result(summary_profile, 'summaryProfile')

    @pytest.mark.asyncio
    async def test_get_summary_detail(
        self,
        async_symbol: AsyncSymbol,
        mocker: MockerFixture,
        summary_detail_json_mock: dict[str, Any],
    ) -> None:
        """Test get_summary_detail method."""
        _mock_response(
            mocker,
            patched_method='yafin.client.AsyncSession.get',
            response_jsons=[summary_detail_json_mock],
            async_mock=True,
        )
        summary_detail = await async_symbol.get_summary_detail()
        _assert_quote_summary_single_module_result(summary_detail, 'summaryDetail')

    @pytest.mark.asyncio
    async def test_get_price(
        self,
        async_symbol: AsyncSymbol,
        mocker: MockerFixture,
        price_json_mock: dict[str, Any],
    ) -> None:
        """Test get_price method."""
        _mock_response(
            mocker,
            patched_method='yafin.client.AsyncSession.get',
            response_jsons=[price_json_mock],
            async_mock=True,
        )
        price = await async_symbol.get_price()
        _assert_quote_summary_single_module_result(price, 'price')

    @pytest.mark.asyncio
    async def test_get_default_key_statistics(
        self,
        async_symbol: AsyncSymbol,
        mocker: MockerFixture,
        default_key_statistics_json_mock: dict[str, Any],
    ) -> None:
        """Test get_default_key_statistics method."""
        _mock_response(
            mocker,
            patched_method='yafin.client.AsyncSession.get',
            response_jsons=[default_key_statistics_json_mock],
            async_mock=True,
        )
        default_key_statistics = await async_symbol.get_default_key_statistics()
        _assert_quote_summary_single_module_result(
            default_key_statistics, 'defaultKeyStatistics'
        )

    @pytest.mark.asyncio
    async def test_get_financial_data(
        self,
        async_symbol: AsyncSymbol,
        mocker: MockerFixture,
        financial_data_json_mock: dict[str, Any],
    ) -> None:
        """Test get_financial_data method."""
        _mock_response(
            mocker,
            patched_method='yafin.client.AsyncSession.get',
            response_jsons=[financial_data_json_mock],
            async_mock=True,
        )
        financial_data = await async_symbol.get_financial_data()
        _assert_quote_summary_single_module_result(financial_data, 'financialData')

    @pytest.mark.asyncio
    async def test_get_calendar_events(
        self,
        async_symbol: AsyncSymbol,
        mocker: MockerFixture,
        calendar_events_json_mock: dict[str, Any],
    ) -> None:
        """Test get_calendar_events method."""
        _mock_response(
            mocker,
            patched_method='yafin.client.AsyncSession.get',
            response_jsons=[calendar_events_json_mock],
            async_mock=True,
        )
        calendar_events = await async_symbol.get_calendar_events()
        _assert_quote_summary_single_module_result(calendar_events, 'calendarEvents')

    @pytest.mark.asyncio
    async def test_get_sec_filings(
        self,
        async_symbol: AsyncSymbol,
        mocker: MockerFixture,
        sec_filings_json_mock: dict[str, Any],
    ) -> None:
        """Test get_sec_filings method."""
        _mock_response(
            mocker,
            patched_method='yafin.client.AsyncSession.get',
            response_jsons=[sec_filings_json_mock],
            async_mock=True,
        )
        sec_filings = await async_symbol.get_sec_filings()
        _assert_quote_summary_single_module_result(sec_filings, 'secFilings')

    @pytest.mark.asyncio
    async def test_get_upgrade_downgrade_history(
        self,
        async_symbol: AsyncSymbol,
        mocker: MockerFixture,
        upgrade_downgrade_history_json_mock: dict[str, Any],
    ) -> None:
        """Test get_upgrade_downgrade_history method."""
        _mock_response(
            mocker,
            patched_method='yafin.client.AsyncSession.get',
            response_jsons=[upgrade_downgrade_history_json_mock],
            async_mock=True,
        )
        upgrade_downgrade_history = await async_symbol.get_upgrade_downgrade_history()
        _assert_quote_summary_single_module_result(
            upgrade_downgrade_history, 'upgradeDowngradeHistory'
        )

    @pytest.mark.asyncio
    async def test_get_institution_ownership(
        self,
        async_symbol: AsyncSymbol,
        mocker: MockerFixture,
        institution_ownership_json_mock: dict[str, Any],
    ) -> None:
        """Test get_institution_ownership method."""
        _mock_response(
            mocker,
            patched_method='yafin.client.AsyncSession.get',
            response_jsons=[institution_ownership_json_mock],
            async_mock=True,
        )
        institution_ownership = await async_symbol.get_institution_ownership()
        _assert_quote_summary_single_module_result(
            institution_ownership, 'institutionOwnership'
        )

    @pytest.mark.asyncio
    async def test_get_fund_ownership(
        self,
        async_symbol: AsyncSymbol,
        mocker: MockerFixture,
        fund_ownership_json_mock: dict[str, Any],
    ) -> None:
        """Test get_fund_ownership method."""
        _mock_response(
            mocker,
            patched_method='yafin.client.AsyncSession.get',
            response_jsons=[fund_ownership_json_mock],
            async_mock=True,
        )
        fund_ownership = await async_symbol.get_fund_ownership()
        _assert_quote_summary_single_module_result(fund_ownership, 'fundOwnership')

    @pytest.mark.asyncio
    async def test_get_major_direct_holders(
        self,
        async_symbol: AsyncSymbol,
        mocker: MockerFixture,
        major_direct_holders_json_mock: dict[str, Any],
    ) -> None:
        """Test get_major_direct_holders method."""
        _mock_response(
            mocker,
            patched_method='yafin.client.AsyncSession.get',
            response_jsons=[major_direct_holders_json_mock],
            async_mock=True,
        )
        major_direct_holders = await async_symbol.get_major_direct_holders()
        _assert_quote_summary_single_module_result(
            major_direct_holders, 'majorDirectHolders'
        )

    @pytest.mark.asyncio
    async def test_get_major_holders_breakdown(
        self,
        async_symbol: AsyncSymbol,
        mocker: MockerFixture,
        major_holders_breakdown_json_mock: dict[str, Any],
    ) -> None:
        """Test get_major_holders_breakdown method."""
        _mock_response(
            mocker,
            patched_method='yafin.client.AsyncSession.get',
            response_jsons=[major_holders_breakdown_json_mock],
            async_mock=True,
        )
        major_holders_breakdown = await async_symbol.get_major_holders_breakdown()
        _assert_quote_summary_single_module_result(
            major_holders_breakdown, 'majorHoldersBreakdown'
        )

    @pytest.mark.asyncio
    async def test_get_insider_transactions(
        self,
        async_symbol: AsyncSymbol,
        mocker: MockerFixture,
        insider_transactions_json_mock: dict[str, Any],
    ) -> None:
        """Test get_insider_transactions method."""
        _mock_response(
            mocker,
            patched_method='yafin.client.AsyncSession.get',
            response_jsons=[insider_transactions_json_mock],
            async_mock=True,
        )
        insider_transactions = await async_symbol.get_insider_transactions()
        _assert_quote_summary_single_module_result(
            insider_transactions, 'insiderTransactions'
        )

    @pytest.mark.asyncio
    async def test_get_insider_holders(
        self,
        async_symbol: AsyncSymbol,
        mocker: MockerFixture,
        insider_holders_json_mock: dict[str, Any],
    ) -> None:
        """Test get_insider_holders method."""
        _mock_response(
            mocker,
            patched_method='yafin.client.AsyncSession.get',
            response_jsons=[insider_holders_json_mock],
            async_mock=True,
        )
        insider_holders = await async_symbol.get_insider_holders()
        _assert_quote_summary_single_module_result(insider_holders, 'insiderHolders')

    @pytest.mark.asyncio
    async def test_get_net_share_purchase_activity(
        self,
        async_symbol: AsyncSymbol,
        mocker: MockerFixture,
        net_share_purchase_activity_json_mock: dict[str, Any],
    ) -> None:
        """Test get_net_share_purchase_activity method."""
        _mock_response(
            mocker,
            patched_method='yafin.client.AsyncSession.get',
            response_jsons=[net_share_purchase_activity_json_mock],
            async_mock=True,
        )
        net_share_purchase_activity = (
            await async_symbol.get_net_share_purchase_activity()
        )
        _assert_quote_summary_single_module_result(
            net_share_purchase_activity, 'netSharePurchaseActivity'
        )

    @pytest.mark.asyncio
    async def test_get_earnings(
        self,
        async_symbol: AsyncSymbol,
        mocker: MockerFixture,
        earnings_json_mock: dict[str, Any],
    ) -> None:
        """Test get_earnings method."""
        _mock_response(
            mocker,
            patched_method='yafin.client.AsyncSession.get',
            response_jsons=[earnings_json_mock],
            async_mock=True,
        )
        earnings = await async_symbol.get_earnings()
        _assert_quote_summary_single_module_result(earnings, 'earnings')

    @pytest.mark.asyncio
    async def test_get_earnings_history(
        self,
        async_symbol: AsyncSymbol,
        mocker: MockerFixture,
        earnings_history_json_mock: dict[str, Any],
    ) -> None:
        """Test get_earnings_history method."""
        _mock_response(
            mocker,
            patched_method='yafin.client.AsyncSession.get',
            response_jsons=[earnings_history_json_mock],
            async_mock=True,
        )
        earnings_history = await async_symbol.get_earnings_history()
        _assert_quote_summary_single_module_result(earnings_history, 'earningsHistory')

    @pytest.mark.asyncio
    async def test_get_earnings_trend(
        self,
        async_symbol: AsyncSymbol,
        mocker: MockerFixture,
        earnings_trend_json_mock: dict[str, Any],
    ) -> None:
        """Test get_earnings_trend method."""
        _mock_response(
            mocker,
            patched_method='yafin.client.AsyncSession.get',
            response_jsons=[earnings_trend_json_mock],
            async_mock=True,
        )
        earnings_trend = await async_symbol.get_earnings_trend()
        _assert_quote_summary_single_module_result(earnings_trend, 'earningsTrend')

    @pytest.mark.asyncio
    async def test_get_industry_trend(
        self,
        async_symbol: AsyncSymbol,
        mocker: MockerFixture,
        industry_trend_json_mock: dict[str, Any],
    ) -> None:
        """Test get_industry_trend method."""
        _mock_response(
            mocker,
            patched_method='yafin.client.AsyncSession.get',
            response_jsons=[industry_trend_json_mock],
            async_mock=True,
        )
        industry_trend = await async_symbol.get_industry_trend()
        _assert_quote_summary_single_module_result(industry_trend, 'industryTrend')

    @pytest.mark.asyncio
    async def test_get_index_trend(
        self,
        async_symbol: AsyncSymbol,
        mocker: MockerFixture,
        index_trend_json_mock: dict[str, Any],
    ) -> None:
        """Test get_index_trend method."""
        _mock_response(
            mocker,
            patched_method='yafin.client.AsyncSession.get',
            response_jsons=[index_trend_json_mock],
            async_mock=True,
        )
        index_trend = await async_symbol.get_index_trend()
        _assert_quote_summary_single_module_result(index_trend, 'indexTrend')

    @pytest.mark.asyncio
    async def test_get_sector_trend(
        self,
        async_symbol: AsyncSymbol,
        mocker: MockerFixture,
        sector_trend_json_mock: dict[str, Any],
    ) -> None:
        """Test get_sector_trend method."""
        _mock_response(
            mocker,
            patched_method='yafin.client.AsyncSession.get',
            response_jsons=[sector_trend_json_mock],
            async_mock=True,
        )
        sector_trend = await async_symbol.get_sector_trend()
        _assert_quote_summary_single_module_result(sector_trend, 'sectorTrend')

    @pytest.mark.asyncio
    async def test_get_recommendation_trend(
        self,
        async_symbol: AsyncSymbol,
        mocker: MockerFixture,
        recommendation_trend_json_mock: dict[str, Any],
    ) -> None:
        """Test get_recommendation_trend method."""
        _mock_response(
            mocker,
            patched_method='yafin.client.AsyncSession.get',
            response_jsons=[recommendation_trend_json_mock],
            async_mock=True,
        )
        recommendation_trend = await async_symbol.get_recommendation_trend()
        _assert_quote_summary_single_module_result(
            recommendation_trend, 'recommendationTrend'
        )

    @pytest.mark.asyncio
    async def test_get_page_views(
        self,
        async_symbol: AsyncSymbol,
        mocker: MockerFixture,
        page_views_json_mock: dict[str, Any],
    ) -> None:
        """Test get_page_views method."""
        _mock_response(
            mocker,
            patched_method='yafin.client.AsyncSession.get',
            response_jsons=[page_views_json_mock],
            async_mock=True,
        )
        page_views = await async_symbol.get_page_views()
        _assert_quote_summary_single_module_result(page_views, 'pageViews')

    @pytest.mark.asyncio
    async def test_get_financials(
        self,
        async_symbol: AsyncSymbol,
        mocker: MockerFixture,
        timeseries_income_statement_json_mock: dict[str, Any],
        period1: int | float | None,
        period2: int | float | None,
    ) -> None:
        """Test _get_financials method."""
        _mock_response(
            mocker,
            patched_method='yafin.client.AsyncSession.get',
            response_jsons=[timeseries_income_statement_json_mock],
            async_mock=True,
        )
        annual_income_stmt = await async_symbol._get_financials(
            frequency='annual', typ='income_statement', period1=period1, period2=period2
        )
        _assert_timeseries_result(
            annual_income_stmt, async_symbol.ticker, ANNUAL_INCOME_STATEMENT_TYPES
        )

    @pytest.mark.asyncio
    async def test_get_income_statement(
        self,
        async_symbol: AsyncSymbol,
        mocker: MockerFixture,
        timeseries_income_statement_json_mock: dict[str, Any],
        period1: int | float | None,
        period2: int | float | None,
    ) -> None:
        """Test get_income_statement method."""
        _mock_response(
            mocker,
            patched_method='yafin.client.AsyncSession.get',
            response_jsons=[timeseries_income_statement_json_mock],
            async_mock=True,
        )
        annual_income_stmt = await async_symbol.get_income_statement(
            frequency='annual', period1=period1, period2=period2
        )
        _assert_timeseries_result(
            annual_income_stmt, async_symbol.ticker, ANNUAL_INCOME_STATEMENT_TYPES
        )

    @pytest.mark.asyncio
    async def test_get_income_statement_invalid_args(
        self, async_symbol: AsyncSymbol
    ) -> None:
        """Test get_income_statement method with invalid arguments.."""
        with pytest.raises(ValueError):
            await async_symbol.get_income_statement(frequency='xxx')

    @pytest.mark.asyncio
    async def test_get_balance_sheet(
        self,
        async_symbol: AsyncSymbol,
        mocker: MockerFixture,
        timeseries_balance_sheet_json_mock: dict[str, Any],
        period1: int | float | None,
        period2: int | float | None,
    ) -> None:
        """Test get_balance_sheet method."""
        _mock_response(
            mocker,
            patched_method='yafin.client.AsyncSession.get',
            response_jsons=[timeseries_balance_sheet_json_mock],
            async_mock=True,
        )
        annual_balance_sheet = await async_symbol.get_balance_sheet(
            frequency='annual', period1=period1, period2=period2
        )
        _assert_timeseries_result(
            annual_balance_sheet, async_symbol.ticker, ANNUAL_BALANCE_SHEET_TYPES
        )

    @pytest.mark.asyncio
    async def test_get_balance_sheet_invalid_args(
        self,
        async_symbol: AsyncSymbol,
        invalid_balance_sheet_kwargs_err_tuple: tuple[dict[str, Any], type[Exception]],
    ) -> None:
        """Test get_balance_sheet method."""
        kwargs, err_cls = invalid_balance_sheet_kwargs_err_tuple
        with pytest.raises(err_cls):
            await async_symbol.get_balance_sheet(**kwargs)

    @pytest.mark.asyncio
    async def test_get_cash_flow(
        self,
        async_symbol: AsyncSymbol,
        mocker: MockerFixture,
        timeseries_cash_flow_json_mock: dict[str, Any],
        period1: int | float | None,
        period2: int | float | None,
    ) -> None:
        """Test get_cash_flow method."""
        _mock_response(
            mocker,
            patched_method='yafin.client.AsyncSession.get',
            response_jsons=[timeseries_cash_flow_json_mock],
            async_mock=True,
        )
        annual_cash_flow = await async_symbol.get_cash_flow(
            frequency='annual', period1=period1, period2=period2
        )
        _assert_timeseries_result(
            annual_cash_flow, async_symbol.ticker, ANNUAL_CASH_FLOW_TYPES
        )

    @pytest.mark.asyncio
    async def test_get_cash_flow_invalid_args(self, async_symbol: AsyncSymbol) -> None:
        """Test get_cash_flow method with invalid arguments."""
        with pytest.raises(ValueError):
            await async_symbol.get_cash_flow(frequency='xxx')

    @pytest.mark.asyncio
    async def test_get_options(
        self,
        async_symbol: AsyncSymbol,
        mocker: MockerFixture,
        options_json_mock: dict[str, Any],
    ) -> None:
        """Test get_options method."""
        _mock_response(
            mocker,
            patched_method='yafin.client.AsyncSession.get',
            response_jsons=[options_json_mock],
            async_mock=True,
        )
        options = await async_symbol.get_options()
        _assert_options_result(options, async_symbol.ticker)

    @pytest.mark.asyncio
    async def test_get_search(
        self,
        async_symbol: AsyncSymbol,
        mocker: MockerFixture,
        search_json_mock: dict[str, Any],
    ) -> None:
        """Test get_search method."""
        _mock_response(
            mocker,
            patched_method='yafin.client.AsyncSession.get',
            response_jsons=[search_json_mock],
            async_mock=True,
        )
        search = await async_symbol.get_search()
        _assert_search_result(search)

    @pytest.mark.asyncio
    async def test_get_recommendations(
        self,
        async_symbol: AsyncSymbol,
        mocker: MockerFixture,
        recommendations_json_mock: dict[str, Any],
    ) -> None:
        """Test get_recommendations method."""
        _mock_response(
            mocker,
            patched_method='yafin.client.AsyncSession.get',
            response_jsons=[recommendations_json_mock],
            async_mock=True,
        )
        recommendations_result = await async_symbol.get_recommendations()
        _assert_recommendations_result(recommendations_result, async_symbol.ticker)

    @pytest.mark.asyncio
    async def test_get_insights(
        self,
        async_symbol: AsyncSymbol,
        mocker: MockerFixture,
        insights_json_mock: dict[str, Any],
    ) -> None:
        """Test get_insights method."""
        _mock_response(
            mocker,
            patched_method='yafin.client.AsyncSession.get',
            response_jsons=[insights_json_mock],
            async_mock=True,
        )
        insights_result = await async_symbol.get_insights()
        _assert_insights_result(insights_result, async_symbol.ticker)

    @pytest.mark.asyncio
    async def test_get_ratings(
        self,
        async_symbol: AsyncSymbol,
        mocker: MockerFixture,
        ratings_json_mock: dict[str, Any],
    ) -> None:
        """Test get_ratings method."""
        _mock_response(
            mocker,
            patched_method='yafin.client.AsyncSession.get',
            response_jsons=[ratings_json_mock],
            async_mock=True,
        )
        ratings_result = await async_symbol.get_ratings()
        _assert_ratings_result(ratings_result, async_symbol.ticker)
