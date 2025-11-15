from typing import Any, AsyncGenerator, Generator, Type

import pytest
import pytest_asyncio
from pytest_mock import MockerFixture
from typeguard import TypeCheckError

from tests._assertions import (
    _assert_chart_result,
    _assert_insight_result,
    _assert_options_result,
    _assert_quote_result,
    _assert_quote_summary_result,
    _assert_quote_summary_single_module_result,
    _assert_quote_type_result,
    _assert_ratings_response_json,
    _assert_recommendation_result,
    _assert_search_response_json,
    _assert_timeseries_result,
)
from tests._utils import _get_json_fixture, _mock_200_response
from yafin import AsyncSymbol, Symbol
from yafin.const import (
    ANNUAL_BALANCE_SHEET_TYPES,
    ANNUAL_CASH_FLOW_TYPES,
    ANNUAL_INCOME_STATEMENT_TYPES,
    QUOTE_SUMMARY_MODULES,
)
from yafin.exceptions import TrailingBalanceSheetError
from yafin.symbol import _AsyncClientManager, _ClientManager


@pytest.fixture(scope='session')
def quote_json_mock(ticker: str) -> dict[str, Any]:
    """Quote response json mock."""
    return _get_json_fixture(file_name=f'{ticker.lower()}.json', folder_name='quote')


@pytest.fixture(scope='session')
def quote_type_json_mock(ticker: str) -> dict[str, Any]:
    """Quote_type response json mock."""
    return _get_json_fixture(
        file_name=f'{ticker.lower()}.json', folder_name='quote_type'
    )


@pytest.fixture(scope='session')
def search_json_mock(ticker: str) -> dict[str, Any]:
    """Search response json mock."""
    return _get_json_fixture(file_name=f'{ticker.lower()}.json', folder_name='search')


@pytest.fixture(scope='session')
def recommendations_json_mock(ticker: str) -> dict[str, Any]:
    """Recommendations response json mock."""
    return _get_json_fixture(
        file_name=f'{ticker.lower()}.json', folder_name='recommendations'
    )


@pytest.fixture(scope='session')
def insights_json_mock(ticker: str) -> dict[str, Any]:
    """Insights response json mock."""
    return _get_json_fixture(file_name=f'{ticker.lower()}.json', folder_name='insights')


@pytest.fixture(scope='session')
def calendar_events_json_mock(ticker: str) -> dict[str, Any]:
    """Quote summary response json mock with calendar events data."""
    return _get_json_fixture(
        file_name=f'calendar_events_{ticker.lower()}.json', folder_name='quote_summary'
    )


class TestUnitClientManager:
    """Unit tests for yafin._ClientManager module."""

    @pytest.fixture
    def client_manager(self) -> _ClientManager:
        """Fresh new instance of _ClientManager for each tests."""
        return _ClientManager()

    def test_client(self, client_manager: _ClientManager) -> None:
        """Test client attribute."""
        assert client_manager._client is None
        assert client_manager._refcount == 0

        client_manager._get_client()
        assert client_manager._client is not None
        assert client_manager._refcount == 1

        client_manager._release_client()
        assert client_manager._client is None
        assert client_manager._refcount == 0

    def test_client_singleton(self, client_manager: _ClientManager) -> None:
        """Test client attribute singleton pattern."""
        client1 = client_manager._get_client()
        client2 = client_manager._get_client()

        assert client_manager._client is not None
        assert client_manager._refcount == 2
        assert client1 is client2

        client_manager._release_client()
        assert client_manager._client is not None
        assert client_manager._refcount == 1

        client_manager._release_client()
        assert client_manager._client is None
        assert client_manager._refcount == 0


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

    @pytest.mark.parametrize(
        'kwargs',
        [
            dict(interval='1d'),
            dict(interval='1d', period_range='1y'),
            dict(
                interval='1d',
                period_range='1y',
                include_div=True,
                include_split=True,
                include_earn=True,
                include_capital_gain=True,
            ),
            dict(
                interval='1d',
                include_div=True,
                include_split=True,
                include_earn=True,
                include_capital_gain=True,
            ),
            dict(interval='1d', period_range='1y', include_div=True),
            dict(interval='1d', include_div=True),
            dict(interval='1d', period_range='1y', include_split=True),
            dict(interval='1d', include_split=True),
            dict(interval='1d', period_range='1y', include_earn=True),
            dict(interval='1d', include_earn=True),
            dict(interval='1d', period_range='1y', include_capital_gain=True),
            dict(interval='1d', include_capital_gain=True),
        ],
    )
    def test_get_chart(
        self,
        symbol: Symbol,
        kwargs: dict[str, Any],
        mocker: MockerFixture,
        chart_json_mock: dict[str, Any],
        period1: int | float | None,
        period2: int | float | None,
    ) -> None:
        """Test get_chart method."""
        _mock_200_response(
            mocker,
            patched_method='yafin.client.Session.get',
            response_json=chart_json_mock,
        )
        chart_result = symbol.get_chart(**kwargs, period1=period1, period2=period2)
        _assert_chart_result(chart_result, symbol.ticker)

    @pytest.mark.parametrize(
        'kwargs, err_cls',
        [
            (
                dict(
                    period_range='xxx',
                    interval='1d',
                    include_div=True,
                    include_split=True,
                    include_earn=True,
                    include_capital_gain=True,
                ),
                ValueError,
            ),
            (
                dict(
                    period_range=1,
                    interval='1d',
                    include_div=True,
                    include_split=True,
                    include_earn=True,
                    include_capital_gain=True,
                ),
                TypeCheckError,
            ),
            (
                dict(
                    period_range='1y',
                    interval='xxx',
                    include_div=True,
                    include_split=True,
                    include_earn=True,
                    include_capital_gain=True,
                ),
                ValueError,
            ),
            (
                dict(
                    period_range='1y',
                    interval=1,
                    include_div=True,
                    include_split=True,
                    include_earn=True,
                    include_capital_gain=True,
                ),
                TypeCheckError,
            ),
            (
                dict(
                    period_range='1y',
                    interval='1d',
                    include_div='xxx',
                    include_split=True,
                    include_earn=True,
                    include_capital_gain=True,
                ),
                TypeCheckError,
            ),
            (
                dict(
                    period_range='1y',
                    interval='1d',
                    include_div=True,
                    include_split='xxx',
                    include_earn=True,
                    include_capital_gain=True,
                ),
                TypeCheckError,
            ),
            (
                dict(
                    period_range='1y',
                    interval='1d',
                    include_div=True,
                    include_split=True,
                    include_earn='xxx',
                    include_capital_gain=True,
                ),
                TypeCheckError,
            ),
            (
                dict(
                    period_range='1y',
                    interval='1d',
                    include_div=True,
                    include_split=True,
                    include_earn=True,
                    include_capital_gain='xxx',
                ),
                TypeCheckError,
            ),
        ],
    )
    def test_get_chart_invalid_args(
        self, symbol: Symbol, kwargs: dict[str, Any], err_cls: Type[Exception]
    ) -> None:
        """Test get_chart method with invalid arguments."""
        with pytest.raises(err_cls):
            symbol.get_chart(**kwargs)

    def test_get_quote(
        self,
        symbol: Symbol,
        mocker: MockerFixture,
        quote_json_mock: dict[str, Any],
    ) -> None:
        """Test get_quote method."""
        _mock_200_response(
            mocker,
            patched_method='yafin.client.Session.get',
            response_json=quote_json_mock,
        )
        quote_result = symbol.get_quote()
        _assert_quote_result(quote_result, symbol.ticker)

    def test_get_quote_type(
        self,
        symbol: Symbol,
        mocker: MockerFixture,
        quote_type_json_mock: dict[str, Any],
    ) -> None:
        """Test get_quote_type method."""
        _mock_200_response(
            mocker,
            patched_method='yafin.client.Session.get',
            response_json=quote_type_json_mock,
        )
        quote_type_result = symbol.get_quote_type()
        _assert_quote_type_result(quote_type_result, symbol.ticker)

    def test_get_quote_summary_all_modules(
        self,
        symbol: Symbol,
        mocker: MockerFixture,
        quote_summary_all_modules_json_mock: dict[str, Any],
    ) -> None:
        """Test get_quote_summary_all_modules method."""
        _mock_200_response(
            mocker,
            patched_method='yafin.client.Session.get',
            response_json=quote_summary_all_modules_json_mock,
        )
        quote_summary_all_modules = symbol.get_quote_summary_all_modules()
        _assert_quote_summary_result(
            quote_summary_all_modules, modules=QUOTE_SUMMARY_MODULES
        )

    def test_get_quote_summary_single_module(
        self,
        symbol: Symbol,
        mocker: MockerFixture,
        asset_profile_json_mock: dict[str, Any],
    ) -> None:
        """Test _get_quote_summary_single_module method."""
        _mock_200_response(
            mocker,
            patched_method='yafin.client.Session.get',
            response_json=asset_profile_json_mock,
        )
        module = 'assetProfile'
        asset_profile = symbol._get_quote_summary_single_module(module)
        _assert_quote_summary_single_module_result(asset_profile, module)

    @pytest.mark.parametrize(
        'kwargs, err_cls',
        [
            (dict(module='xxx'), ValueError),
            (dict(module=1), TypeCheckError),
        ],
    )
    def test_get_quote_summary_single_module_invalid_args(
        self, symbol: Symbol, kwargs: dict[str, Any], err_cls: Type[Exception]
    ) -> None:
        """Test _get_quote_summary_single_module method with invalid arguments."""
        with pytest.raises(err_cls):
            symbol._get_quote_summary_single_module(**kwargs)

    def test_get_asset_profile(
        self,
        symbol: Symbol,
        mocker: MockerFixture,
        asset_profile_json_mock: dict[str, Any],
    ) -> None:
        """Test get_asset_profile method."""
        _mock_200_response(
            mocker,
            patched_method='yafin.client.Session.get',
            response_json=asset_profile_json_mock,
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
        _mock_200_response(
            mocker,
            patched_method='yafin.client.Session.get',
            response_json=summary_profile_json_mock,
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
        _mock_200_response(
            mocker,
            patched_method='yafin.client.Session.get',
            response_json=summary_detail_json_mock,
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
        _mock_200_response(
            mocker,
            patched_method='yafin.client.Session.get',
            response_json=price_json_mock,
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
        _mock_200_response(
            mocker,
            patched_method='yafin.client.Session.get',
            response_json=default_key_statistics_json_mock,
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
        _mock_200_response(
            mocker,
            patched_method='yafin.client.Session.get',
            response_json=financial_data_json_mock,
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
        _mock_200_response(
            mocker,
            patched_method='yafin.client.Session.get',
            response_json=calendar_events_json_mock,
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
        _mock_200_response(
            mocker,
            patched_method='yafin.client.Session.get',
            response_json=sec_filings_json_mock,
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
        _mock_200_response(
            mocker,
            patched_method='yafin.client.Session.get',
            response_json=upgrade_downgrade_history_json_mock,
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
        _mock_200_response(
            mocker,
            patched_method='yafin.client.Session.get',
            response_json=institution_ownership_json_mock,
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
        _mock_200_response(
            mocker,
            patched_method='yafin.client.Session.get',
            response_json=fund_ownership_json_mock,
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
        _mock_200_response(
            mocker,
            patched_method='yafin.client.Session.get',
            response_json=major_direct_holders_json_mock,
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
        _mock_200_response(
            mocker,
            patched_method='yafin.client.Session.get',
            response_json=major_holders_breakdown_json_mock,
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
        _mock_200_response(
            mocker,
            patched_method='yafin.client.Session.get',
            response_json=insider_transactions_json_mock,
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
        _mock_200_response(
            mocker,
            patched_method='yafin.client.Session.get',
            response_json=insider_holders_json_mock,
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
        _mock_200_response(
            mocker,
            patched_method='yafin.client.Session.get',
            response_json=net_share_purchase_activity_json_mock,
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
        _mock_200_response(
            mocker,
            patched_method='yafin.client.Session.get',
            response_json=earnings_json_mock,
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
        _mock_200_response(
            mocker,
            patched_method='yafin.client.Session.get',
            response_json=earnings_history_json_mock,
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
        _mock_200_response(
            mocker,
            patched_method='yafin.client.Session.get',
            response_json=earnings_trend_json_mock,
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
        _mock_200_response(
            mocker,
            patched_method='yafin.client.Session.get',
            response_json=industry_trend_json_mock,
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
        _mock_200_response(
            mocker,
            patched_method='yafin.client.Session.get',
            response_json=index_trend_json_mock,
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
        _mock_200_response(
            mocker,
            patched_method='yafin.client.Session.get',
            response_json=sector_trend_json_mock,
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
        _mock_200_response(
            mocker,
            patched_method='yafin.client.Session.get',
            response_json=recommendation_trend_json_mock,
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
        _mock_200_response(
            mocker,
            patched_method='yafin.client.Session.get',
            response_json=page_views_json_mock,
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
        _mock_200_response(
            mocker,
            patched_method='yafin.client.Session.get',
            response_json=timeseries_income_statement_json_mock,
        )
        annual_income_stmt = symbol._get_financials(
            frequency='annual', typ='income_statement', period1=period1, period2=period2
        )
        _assert_timeseries_result(
            annual_income_stmt,
            types=ANNUAL_INCOME_STATEMENT_TYPES,
            ticker=symbol.ticker,
        )

    @pytest.mark.parametrize(
        'kwargs, err_cls',
        [
            (dict(frequency=1, typ='income_statement'), TypeCheckError),
            (dict(frequency='annual', typ=1), TypeCheckError),
            (
                dict(frequency='annual', typ='income_statement', period1='xxx'),
                TypeCheckError,
            ),
            (
                dict(frequency='annual', typ='income_statement', period2='xxx'),
                TypeCheckError,
            ),
        ],
    )
    def test_get_financials_invalid_args(
        self, symbol: Symbol, kwargs: dict[str, Any], err_cls: Type[Exception]
    ) -> None:
        """Test _get_financials method with invalid arguments.."""
        with pytest.raises(err_cls):
            symbol._get_financials(**kwargs)

    def test_get_income_statement(
        self,
        symbol: Symbol,
        mocker: MockerFixture,
        timeseries_income_statement_json_mock: dict[str, Any],
        period1: int | float | None,
        period2: int | float | None,
    ) -> None:
        """Test get_income_statement method."""
        _mock_200_response(
            mocker,
            patched_method='yafin.client.Session.get',
            response_json=timeseries_income_statement_json_mock,
        )
        annual_income_stmt = symbol.get_income_statement(
            frequency='annual', period1=period1, period2=period2
        )
        _assert_timeseries_result(
            annual_income_stmt,
            types=ANNUAL_INCOME_STATEMENT_TYPES,
            ticker=symbol.ticker,
        )

    @pytest.mark.parametrize(
        'kwargs, err_cls',
        [
            (dict(frequency='xxx'), ValueError),
            (dict(frequency=1), TypeCheckError),
            (dict(frequency='annual', period1='xxx'), TypeCheckError),
            (dict(frequency='annual', period2='xxx'), TypeCheckError),
        ],
    )
    def test_get_income_statement_invalid_args(
        self, symbol: Symbol, kwargs: dict[str, Any], err_cls: Type[Exception]
    ) -> None:
        """Test get_income_statement method with invalid arguments.."""
        with pytest.raises(err_cls):
            symbol.get_income_statement(**kwargs)

    def test_get_balance_sheet(
        self,
        symbol: Symbol,
        mocker: MockerFixture,
        timeseries_balance_sheet_json_mock: dict[str, Any],
        period1: int | float | None,
        period2: int | float | None,
    ) -> None:
        """Test get_balance_sheet method."""
        _mock_200_response(
            mocker,
            patched_method='yafin.client.Session.get',
            response_json=timeseries_balance_sheet_json_mock,
        )
        annual_balance_sheet = symbol.get_balance_sheet(
            frequency='annual', period1=period1, period2=period2
        )
        _assert_timeseries_result(
            annual_balance_sheet, types=ANNUAL_BALANCE_SHEET_TYPES, ticker=symbol.ticker
        )

    @pytest.mark.parametrize(
        'kwargs, err_cls',
        [
            (dict(frequency='trailing'), TrailingBalanceSheetError),
            (dict(frequency='xxx'), ValueError),
            (dict(frequency=1), TypeCheckError),
            (dict(frequency='annual', period1='xxx'), TypeCheckError),
            (dict(frequency='annual', period2='xxx'), TypeCheckError),
        ],
    )
    def test_get_balance_sheet_invalid_args(
        self, symbol: Symbol, kwargs: dict[str, Any], err_cls: Type[Exception]
    ) -> None:
        """Test get_balance_sheet method."""
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
        _mock_200_response(
            mocker,
            patched_method='yafin.client.Session.get',
            response_json=timeseries_cash_flow_json_mock,
        )
        annual_cash_flow = symbol.get_cash_flow(
            frequency='annual', period1=period1, period2=period2
        )
        _assert_timeseries_result(
            annual_cash_flow, types=ANNUAL_CASH_FLOW_TYPES, ticker=symbol.ticker
        )

    @pytest.mark.parametrize(
        'kwargs, err_cls',
        [
            (dict(frequency='xxx'), ValueError),
            (dict(frequency=1), TypeCheckError),
            (dict(frequency='annual', period1='xxx'), TypeCheckError),
            (dict(frequency='annual', period2='xxx'), TypeCheckError),
        ],
    )
    def test_get_cash_flow_invalid_args(
        self, symbol: Symbol, kwargs: dict[str, Any], err_cls: Type[Exception]
    ) -> None:
        """Test get_cash_flow method with invalid arguments."""
        with pytest.raises(err_cls):
            symbol.get_cash_flow(**kwargs)

    def test_get_options(
        self,
        symbol: Symbol,
        mocker: MockerFixture,
        options_json_mock: dict[str, Any],
    ) -> None:
        """Test get_options method."""
        _mock_200_response(
            mocker,
            patched_method='yafin.client.Session.get',
            response_json=options_json_mock,
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
        _mock_200_response(
            mocker,
            patched_method='yafin.client.Session.get',
            response_json=search_json_mock,
        )
        search = symbol.get_search()
        _assert_search_response_json(search)

    def test_get_recommendations(
        self,
        symbol: Symbol,
        mocker: MockerFixture,
        recommendations_json_mock: dict[str, Any],
    ) -> None:
        """Test get_recommendations method."""
        _mock_200_response(
            mocker,
            patched_method='yafin.client.Session.get',
            response_json=recommendations_json_mock,
        )
        recommendations = symbol.get_recommendations()
        _assert_recommendation_result(recommendations, symbol.ticker)

    def test_get_insights(
        self,
        symbol: Symbol,
        mocker: MockerFixture,
        insights_json_mock: dict[str, Any],
    ) -> None:
        """Test get_insights method."""
        _mock_200_response(
            mocker,
            patched_method='yafin.client.Session.get',
            response_json=insights_json_mock,
        )
        insights = symbol.get_insights()
        _assert_insight_result(insights, symbol.ticker)

    def test_get_ratings(
        self,
        symbol: Symbol,
        mocker: MockerFixture,
        ratings_json_mock: dict[str, Any],
    ) -> None:
        """Test get_ratings method."""
        _mock_200_response(
            mocker,
            patched_method='yafin.client.Session.get',
            response_json=ratings_json_mock,
        )
        ratings = symbol.get_ratings()
        _assert_ratings_response_json(ratings)


class TestUnitAsyncClientManager:
    """Unit tests for yafin._AsyncClientManager module."""

    @pytest_asyncio.fixture
    async def async_client_manager(self) -> _AsyncClientManager:
        """Fresh new instance of _ClientManager for each tests."""
        return _AsyncClientManager()

    @pytest.mark.asyncio
    async def test_client(self, async_client_manager: _AsyncClientManager) -> None:
        """Test client attribute."""
        assert async_client_manager._client is None
        assert async_client_manager._refcount == 0

        await async_client_manager._get_client()
        assert async_client_manager._client is not None
        assert async_client_manager._refcount == 1

        await async_client_manager._release_client()
        assert async_client_manager._client is None
        assert async_client_manager._refcount == 0

    @pytest.mark.asyncio
    async def test_client_singleton(
        self, async_client_manager: _AsyncClientManager
    ) -> None:
        """Test client attribute singleton pattern."""
        client1 = await async_client_manager._get_client()
        client2 = await async_client_manager._get_client()

        assert async_client_manager._client is not None
        assert async_client_manager._refcount == 2
        assert client1 is client2

        await async_client_manager._release_client()
        assert async_client_manager._client is not None
        assert async_client_manager._refcount == 1

        await async_client_manager._release_client()
        assert async_client_manager._client is None
        assert async_client_manager._refcount == 0


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

    @pytest.mark.parametrize(
        'kwargs',
        [
            dict(interval='1d'),
            dict(interval='1d', period_range='1y'),
            dict(
                interval='1d',
                period_range='1y',
                include_div=True,
                include_split=True,
                include_earn=True,
                include_capital_gain=True,
            ),
            dict(
                interval='1d',
                include_div=True,
                include_split=True,
                include_earn=True,
                include_capital_gain=True,
            ),
            dict(interval='1d', period_range='1y', include_div=True),
            dict(interval='1d', include_div=True),
            dict(interval='1d', period_range='1y', include_split=True),
            dict(interval='1d', include_split=True),
            dict(interval='1d', period_range='1y', include_earn=True),
            dict(interval='1d', include_earn=True),
            dict(interval='1d', period_range='1y', include_capital_gain=True),
            dict(interval='1d', include_capital_gain=True),
        ],
    )
    @pytest.mark.asyncio
    async def test_get_chart(
        self,
        async_symbol: AsyncSymbol,
        kwargs: dict[str, Any],
        mocker: MockerFixture,
        chart_json_mock: dict[str, Any],
        period1: int | float | None,
        period2: int | float | None,
    ) -> None:
        """Test get_chart method."""
        _mock_200_response(
            mocker,
            patched_method='yafin.client.AsyncSession.get',
            response_json=chart_json_mock,
            async_mock=True,
        )
        chart_result = await async_symbol.get_chart(
            **kwargs, period1=period1, period2=period2
        )
        _assert_chart_result(chart_result, async_symbol.ticker)

    @pytest.mark.parametrize(
        'kwargs, err_cls',
        [
            (
                dict(
                    period_range='xxx',
                    interval='1d',
                    include_div=True,
                    include_split=True,
                    include_earn=True,
                    include_capital_gain=True,
                ),
                ValueError,
            ),
            (
                dict(
                    period_range=1,
                    interval='1d',
                    include_div=True,
                    include_split=True,
                    include_earn=True,
                    include_capital_gain=True,
                ),
                TypeCheckError,
            ),
            (
                dict(
                    period_range='1y',
                    interval='xxx',
                    include_div=True,
                    include_split=True,
                    include_earn=True,
                    include_capital_gain=True,
                ),
                ValueError,
            ),
            (
                dict(
                    period_range='1y',
                    interval=1,
                    include_div=True,
                    include_split=True,
                    include_earn=True,
                    include_capital_gain=True,
                ),
                TypeCheckError,
            ),
            (
                dict(
                    period_range='1y',
                    interval='1d',
                    include_div='xxx',
                    include_split=True,
                    include_earn=True,
                    include_capital_gain=True,
                ),
                TypeCheckError,
            ),
            (
                dict(
                    period_range='1y',
                    interval='1d',
                    include_div=True,
                    include_split='xxx',
                    include_earn=True,
                    include_capital_gain=True,
                ),
                TypeCheckError,
            ),
            (
                dict(
                    period_range='1y',
                    interval='1d',
                    include_div=True,
                    include_split=True,
                    include_earn='xxx',
                    include_capital_gain=True,
                ),
                TypeCheckError,
            ),
            (
                dict(
                    period_range='1y',
                    interval='1d',
                    include_div=True,
                    include_split=True,
                    include_earn=True,
                    include_capital_gain='xxx',
                ),
                TypeCheckError,
            ),
        ],
    )
    @pytest.mark.asyncio
    async def test_get_chart_invalid_args(
        self,
        async_symbol: AsyncSymbol,
        kwargs: dict[str, Any],
        err_cls: Type[Exception],
    ) -> None:
        """Test get_chart method with invalid arguments."""
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
        _mock_200_response(
            mocker,
            patched_method='yafin.client.AsyncSession.get',
            response_json=quote_json_mock,
            async_mock=True,
        )
        quote_result = await async_symbol.get_quote()
        _assert_quote_result(quote_result, async_symbol.ticker)

    @pytest.mark.asyncio
    async def test_get_quote_type(
        self,
        async_symbol: AsyncSymbol,
        mocker: MockerFixture,
        quote_type_json_mock: dict[str, Any],
    ) -> None:
        """Test get_quote_type method."""
        _mock_200_response(
            mocker,
            patched_method='yafin.client.AsyncSession.get',
            response_json=quote_type_json_mock,
            async_mock=True,
        )
        quote_type_result = await async_symbol.get_quote_type()
        _assert_quote_type_result(quote_type_result, async_symbol.ticker)

    @pytest.mark.asyncio
    async def test_get_quote_summary_all_modules(
        self,
        async_symbol: AsyncSymbol,
        mocker: MockerFixture,
        quote_summary_all_modules_json_mock: dict[str, Any],
    ) -> None:
        """Test get_quote_summary_all_modules method."""
        _mock_200_response(
            mocker,
            patched_method='yafin.client.AsyncSession.get',
            response_json=quote_summary_all_modules_json_mock,
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
        _mock_200_response(
            mocker,
            patched_method='yafin.client.AsyncSession.get',
            response_json=asset_profile_json_mock,
            async_mock=True,
        )
        module = 'assetProfile'
        asset_profile = await async_symbol._get_quote_summary_single_module(module)
        _assert_quote_summary_single_module_result(asset_profile, module)

    @pytest.mark.parametrize(
        'kwargs, err_cls',
        [
            (dict(module='xxx'), ValueError),
            (dict(module=1), TypeCheckError),
        ],
    )
    @pytest.mark.asyncio
    async def test_get_quote_summary_single_module_invalid_args(
        self,
        async_symbol: AsyncSymbol,
        kwargs: dict[str, Any],
        err_cls: Type[Exception],
    ) -> None:
        """Test _get_quote_summary_single_module method with invalid arguments."""
        with pytest.raises(err_cls):
            await async_symbol._get_quote_summary_single_module(**kwargs)

    @pytest.mark.asyncio
    async def test_get_asset_profile(
        self,
        async_symbol: AsyncSymbol,
        mocker: MockerFixture,
        asset_profile_json_mock: dict[str, Any],
    ) -> None:
        """Test get_asset_profile method."""
        _mock_200_response(
            mocker,
            patched_method='yafin.client.AsyncSession.get',
            response_json=asset_profile_json_mock,
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
        _mock_200_response(
            mocker,
            patched_method='yafin.client.AsyncSession.get',
            response_json=summary_profile_json_mock,
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
        _mock_200_response(
            mocker,
            patched_method='yafin.client.AsyncSession.get',
            response_json=summary_detail_json_mock,
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
        _mock_200_response(
            mocker,
            patched_method='yafin.client.AsyncSession.get',
            response_json=price_json_mock,
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
        _mock_200_response(
            mocker,
            patched_method='yafin.client.AsyncSession.get',
            response_json=default_key_statistics_json_mock,
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
        _mock_200_response(
            mocker,
            patched_method='yafin.client.AsyncSession.get',
            response_json=financial_data_json_mock,
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
        _mock_200_response(
            mocker,
            patched_method='yafin.client.AsyncSession.get',
            response_json=calendar_events_json_mock,
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
        _mock_200_response(
            mocker,
            patched_method='yafin.client.AsyncSession.get',
            response_json=sec_filings_json_mock,
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
        _mock_200_response(
            mocker,
            patched_method='yafin.client.AsyncSession.get',
            response_json=upgrade_downgrade_history_json_mock,
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
        _mock_200_response(
            mocker,
            patched_method='yafin.client.AsyncSession.get',
            response_json=institution_ownership_json_mock,
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
        _mock_200_response(
            mocker,
            patched_method='yafin.client.AsyncSession.get',
            response_json=fund_ownership_json_mock,
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
        _mock_200_response(
            mocker,
            patched_method='yafin.client.AsyncSession.get',
            response_json=major_direct_holders_json_mock,
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
        _mock_200_response(
            mocker,
            patched_method='yafin.client.AsyncSession.get',
            response_json=major_holders_breakdown_json_mock,
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
        _mock_200_response(
            mocker,
            patched_method='yafin.client.AsyncSession.get',
            response_json=insider_transactions_json_mock,
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
        _mock_200_response(
            mocker,
            patched_method='yafin.client.AsyncSession.get',
            response_json=insider_holders_json_mock,
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
        _mock_200_response(
            mocker,
            patched_method='yafin.client.AsyncSession.get',
            response_json=net_share_purchase_activity_json_mock,
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
        _mock_200_response(
            mocker,
            patched_method='yafin.client.AsyncSession.get',
            response_json=earnings_json_mock,
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
        _mock_200_response(
            mocker,
            patched_method='yafin.client.AsyncSession.get',
            response_json=earnings_history_json_mock,
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
        _mock_200_response(
            mocker,
            patched_method='yafin.client.AsyncSession.get',
            response_json=earnings_trend_json_mock,
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
        _mock_200_response(
            mocker,
            patched_method='yafin.client.AsyncSession.get',
            response_json=industry_trend_json_mock,
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
        _mock_200_response(
            mocker,
            patched_method='yafin.client.AsyncSession.get',
            response_json=index_trend_json_mock,
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
        _mock_200_response(
            mocker,
            patched_method='yafin.client.AsyncSession.get',
            response_json=sector_trend_json_mock,
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
        _mock_200_response(
            mocker,
            patched_method='yafin.client.AsyncSession.get',
            response_json=recommendation_trend_json_mock,
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
        _mock_200_response(
            mocker,
            patched_method='yafin.client.AsyncSession.get',
            response_json=page_views_json_mock,
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
        _mock_200_response(
            mocker,
            patched_method='yafin.client.AsyncSession.get',
            response_json=timeseries_income_statement_json_mock,
            async_mock=True,
        )
        annual_income_stmt = await async_symbol._get_financials(
            frequency='annual', typ='income_statement', period1=period1, period2=period2
        )
        _assert_timeseries_result(
            annual_income_stmt,
            types=ANNUAL_INCOME_STATEMENT_TYPES,
            ticker=async_symbol.ticker,
        )

    @pytest.mark.parametrize(
        'kwargs, err_cls',
        [
            (dict(frequency=1, typ='income_statement'), TypeCheckError),
            (dict(frequency='annual', typ=1), TypeCheckError),
            (
                dict(frequency='annual', typ='income_statement', period1='xxx'),
                TypeCheckError,
            ),
            (
                dict(frequency='annual', typ='income_statement', period2='xxx'),
                TypeCheckError,
            ),
        ],
    )
    @pytest.mark.asyncio
    async def test_get_financials_invalid_args(
        self,
        async_symbol: AsyncSymbol,
        kwargs: dict[str, Any],
        err_cls: Type[Exception],
    ) -> None:
        """Test _get_financials method with invalid arguments.."""
        with pytest.raises(err_cls):
            await async_symbol._get_financials(**kwargs)

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
        _mock_200_response(
            mocker,
            patched_method='yafin.client.AsyncSession.get',
            response_json=timeseries_income_statement_json_mock,
            async_mock=True,
        )
        annual_income_stmt = await async_symbol.get_income_statement(
            frequency='annual', period1=period1, period2=period2
        )
        _assert_timeseries_result(
            annual_income_stmt,
            types=ANNUAL_INCOME_STATEMENT_TYPES,
            ticker=async_symbol.ticker,
        )

    @pytest.mark.parametrize(
        'kwargs, err_cls',
        [
            (dict(frequency='xxx'), ValueError),
            (dict(frequency=1), TypeCheckError),
            (dict(frequency='annual', period1='xxx'), TypeCheckError),
            (dict(frequency='annual', period2='xxx'), TypeCheckError),
        ],
    )
    @pytest.mark.asyncio
    async def test_get_income_statement_invalid_args(
        self,
        async_symbol: AsyncSymbol,
        kwargs: dict[str, Any],
        err_cls: Type[Exception],
    ) -> None:
        """Test get_income_statement method with invalid arguments.."""
        with pytest.raises(err_cls):
            await async_symbol.get_income_statement(**kwargs)

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
        _mock_200_response(
            mocker,
            patched_method='yafin.client.AsyncSession.get',
            response_json=timeseries_balance_sheet_json_mock,
            async_mock=True,
        )
        annual_balance_sheet = await async_symbol.get_balance_sheet(
            frequency='annual', period1=period1, period2=period2
        )
        _assert_timeseries_result(
            annual_balance_sheet,
            types=ANNUAL_BALANCE_SHEET_TYPES,
            ticker=async_symbol.ticker,
        )

    @pytest.mark.parametrize(
        'kwargs, err_cls',
        [
            (dict(frequency='trailing'), TrailingBalanceSheetError),
            (dict(frequency='xxx'), ValueError),
            (dict(frequency=1), TypeCheckError),
            (dict(frequency='annual', period1='xxx'), TypeCheckError),
            (dict(frequency='annual', period2='xxx'), TypeCheckError),
        ],
    )
    @pytest.mark.asyncio
    async def test_get_balance_sheet_invalid_args(
        self,
        async_symbol: AsyncSymbol,
        kwargs: dict[str, Any],
        err_cls: Type[Exception],
    ) -> None:
        """Test get_balance_sheet method."""
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
        _mock_200_response(
            mocker,
            patched_method='yafin.client.AsyncSession.get',
            response_json=timeseries_cash_flow_json_mock,
            async_mock=True,
        )
        annual_cash_flow = await async_symbol.get_cash_flow(
            frequency='annual', period1=period1, period2=period2
        )
        _assert_timeseries_result(
            annual_cash_flow, types=ANNUAL_CASH_FLOW_TYPES, ticker=async_symbol.ticker
        )

    @pytest.mark.parametrize(
        'kwargs, err_cls',
        [
            (dict(frequency='xxx'), ValueError),
            (dict(frequency=1), TypeCheckError),
            (dict(frequency='annual', period1='xxx'), TypeCheckError),
            (dict(frequency='annual', period2='xxx'), TypeCheckError),
        ],
    )
    @pytest.mark.asyncio
    async def test_get_cash_flow_invalid_args(
        self,
        async_symbol: AsyncSymbol,
        kwargs: dict[str, Any],
        err_cls: Type[Exception],
    ) -> None:
        """Test get_cash_flow method with invalid arguments."""
        with pytest.raises(err_cls):
            await async_symbol.get_cash_flow(**kwargs)

    @pytest.mark.asyncio
    async def test_get_options(
        self,
        async_symbol: AsyncSymbol,
        mocker: MockerFixture,
        options_json_mock: dict[str, Any],
    ) -> None:
        """Test get_options method."""
        _mock_200_response(
            mocker,
            patched_method='yafin.client.AsyncSession.get',
            response_json=options_json_mock,
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
        _mock_200_response(
            mocker,
            patched_method='yafin.client.AsyncSession.get',
            response_json=search_json_mock,
            async_mock=True,
        )
        search = await async_symbol.get_search()
        _assert_search_response_json(search)

    @pytest.mark.asyncio
    async def test_get_recommendations(
        self,
        async_symbol: AsyncSymbol,
        mocker: MockerFixture,
        recommendations_json_mock: dict[str, Any],
    ) -> None:
        """Test get_recommendations method."""
        _mock_200_response(
            mocker,
            patched_method='yafin.client.AsyncSession.get',
            response_json=recommendations_json_mock,
            async_mock=True,
        )
        recommendations = await async_symbol.get_recommendations()
        _assert_recommendation_result(recommendations, async_symbol.ticker)

    @pytest.mark.asyncio
    async def test_get_insights(
        self,
        async_symbol: AsyncSymbol,
        mocker: MockerFixture,
        insights_json_mock: dict[str, Any],
    ) -> None:
        """Test get_insights method."""
        _mock_200_response(
            mocker,
            patched_method='yafin.client.AsyncSession.get',
            response_json=insights_json_mock,
            async_mock=True,
        )
        insights = await async_symbol.get_insights()
        _assert_insight_result(insights, async_symbol.ticker)

    @pytest.mark.asyncio
    async def test_get_ratings(
        self,
        async_symbol: AsyncSymbol,
        mocker: MockerFixture,
        ratings_json_mock: dict[str, Any],
    ) -> None:
        """Test get_ratings method."""
        _mock_200_response(
            mocker,
            patched_method='yafin.client.AsyncSession.get',
            response_json=ratings_json_mock,
            async_mock=True,
        )
        ratings = await async_symbol.get_ratings()
        _assert_ratings_response_json(ratings)
