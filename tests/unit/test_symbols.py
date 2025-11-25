from typing import Any, AsyncGenerator, Generator

import pytest
import pytest_asyncio
from pytest_mock import MockerFixture

from tests._assertions import (
    _assert_chart_result_list,
    _assert_insights_result_list,
    _assert_options_result_list,
    _assert_quote_summary_result_list,
    _assert_quote_summary_single_module_result_list,
    _assert_quote_types_result_list,
    _assert_quotes_result_list,
    _assert_ratings_result_list,
    _assert_recommendations_result_list,
    _assert_search_result,
    _assert_timeseries_result_list,
)
from tests._utils import _get_json_fixture, _mock_response
from yafin import AsyncSymbols, Symbols
from yafin.const import (
    ANNUAL_BALANCE_SHEET_TYPES,
    ANNUAL_CASH_FLOW_TYPES,
    ANNUAL_INCOME_STATEMENT_TYPES,
    QUOTE_SUMMARY_MODULES,
)


@pytest.fixture
def tickers_list(tickers: str) -> list[str]:
    """Fresh new instance of tickers_list for each tests."""
    return tickers.split(',')


@pytest.fixture
def chart_json_mocks(tickers_list: list[str]) -> list[dict[str, Any]]:
    """Chart response json mocks with data for 1y, 1d."""
    return [
        _get_json_fixture(file_name=f'{ticker.lower()}_1d_1y.json', folder_name='chart')
        for ticker in tickers_list
    ]


@pytest.fixture
def quote_summary_all_modules_json_mocks(
    tickers_list: list[str],
) -> list[dict[str, Any]]:
    """Quote_summary response json mocks with all modules data."""
    return [
        _get_json_fixture(
            file_name=f'all_modules_{ticker.lower()}.json', folder_name='quote_summary'
        )
        for ticker in tickers_list
    ]


@pytest.fixture
def asset_profile_json_mocks(tickers_list: list[str]) -> list[dict[str, Any]]:
    """Quote summary response json mocks with asset profile data."""
    return [
        _get_json_fixture(
            file_name=f'asset_profile_{ticker.lower()}.json',
            folder_name='quote_summary',
        )
        for ticker in tickers_list
    ]


@pytest.fixture
def summary_profile_json_mocks(tickers_list: list[str]) -> list[dict[str, Any]]:
    """Quote summary response json mocks with summary profile data."""
    return [
        _get_json_fixture(
            file_name=f'summary_profile_{ticker.lower()}.json',
            folder_name='quote_summary',
        )
        for ticker in tickers_list
    ]


@pytest.fixture
def summary_detail_json_mocks(tickers_list: list[str]) -> list[dict[str, Any]]:
    """Quote summary response json mocks with summary detail data."""
    return [
        _get_json_fixture(
            file_name=f'summary_detail_{ticker.lower()}.json',
            folder_name='quote_summary',
        )
        for ticker in tickers_list
    ]


@pytest.fixture
def esg_scores_json_mocks(tickers_list: list[str]) -> list[dict[str, Any]]:
    """Quote summary response json mocks with esg scores data."""
    return [
        _get_json_fixture(
            file_name=f'esg_scores_{ticker.lower()}.json', folder_name='quote_summary'
        )
        for ticker in tickers_list
    ]


@pytest.fixture
def price_json_mocks(tickers_list: list[str]) -> list[dict[str, Any]]:
    """Quote summary response json mocks with price data."""
    return [
        _get_json_fixture(
            file_name=f'price_{ticker.lower()}.json', folder_name='quote_summary'
        )
        for ticker in tickers_list
    ]


@pytest.fixture
def default_key_statistics_json_mocks(tickers_list: list[str]) -> list[dict[str, Any]]:
    """Quote summary response json mocks with default key statistics data."""
    return [
        _get_json_fixture(
            file_name=f'default_key_statistics_{ticker.lower()}.json',
            folder_name='quote_summary',
        )
        for ticker in tickers_list
    ]


@pytest.fixture
def financial_data_json_mocks(tickers_list: list[str]) -> list[dict[str, Any]]:
    """Quote summary response json mocks with financial data."""
    return [
        _get_json_fixture(
            file_name=f'financial_data_{ticker.lower()}.json',
            folder_name='quote_summary',
        )
        for ticker in tickers_list
    ]


@pytest.fixture
def sec_filings_json_mocks(tickers_list: list[str]) -> list[dict[str, Any]]:
    """Quote summary response json mocks with sec filings data."""
    return [
        _get_json_fixture(
            file_name=f'sec_filings_{ticker.lower()}.json', folder_name='quote_summary'
        )
        for ticker in tickers_list
    ]


@pytest.fixture
def upgrade_downgrade_history_json_mocks(
    tickers_list: list[str],
) -> list[dict[str, Any]]:
    """Quote summary response json mocks with upgrade downgrade history data."""
    return [
        _get_json_fixture(
            file_name=f'upgrade_downgrade_history_{ticker.lower()}.json',
            folder_name='quote_summary',
        )
        for ticker in tickers_list
    ]


@pytest.fixture
def institution_ownership_json_mocks(tickers_list: list[str]) -> list[dict[str, Any]]:
    """Quote summary response json mocks with institution ownership data."""
    return [
        _get_json_fixture(
            file_name=f'institution_ownership_{ticker.lower()}.json',
            folder_name='quote_summary',
        )
        for ticker in tickers_list
    ]


@pytest.fixture
def fund_ownership_json_mocks(tickers_list: list[str]) -> list[dict[str, Any]]:
    """Quote summary response json mocks with fund ownership data."""
    return [
        _get_json_fixture(
            file_name=f'fund_ownership_{ticker.lower()}.json',
            folder_name='quote_summary',
        )
        for ticker in tickers_list
    ]


@pytest.fixture
def major_direct_holders_json_mocks(tickers_list: list[str]) -> list[dict[str, Any]]:
    """Quote summary response json mocks with major direct holders data."""
    return [
        _get_json_fixture(
            file_name=f'major_direct_holders_{ticker.lower()}.json',
            folder_name='quote_summary',
        )
        for ticker in tickers_list
    ]


@pytest.fixture
def major_holders_breakdown_json_mocks(tickers_list: list[str]) -> list[dict[str, Any]]:
    """Quote summary response json mocks with major holders breakdown data."""
    return [
        _get_json_fixture(
            file_name=f'major_holders_breakdown_{ticker.lower()}.json',
            folder_name='quote_summary',
        )
        for ticker in tickers_list
    ]


@pytest.fixture
def insider_transactions_json_mocks(tickers_list: list[str]) -> list[dict[str, Any]]:
    """Quote summary response json mocks with insider transactions data."""
    return [
        _get_json_fixture(
            file_name=f'insider_transactions_{ticker.lower()}.json',
            folder_name='quote_summary',
        )
        for ticker in tickers_list
    ]


@pytest.fixture
def insider_holders_json_mocks(tickers_list: list[str]) -> list[dict[str, Any]]:
    """Quote summary response json mocks with insider holders data."""
    return [
        _get_json_fixture(
            file_name=f'insider_holders_{ticker.lower()}.json',
            folder_name='quote_summary',
        )
        for ticker in tickers_list
    ]


@pytest.fixture
def net_share_purchase_activity_json_mocks(
    tickers_list: list[str],
) -> list[dict[str, Any]]:
    """Quote summary response json mocks with net share purchase activity data."""  # noqa: E501
    return [
        _get_json_fixture(
            file_name=f'net_share_purchase_activity_{ticker.lower()}.json',
            folder_name='quote_summary',
        )
        for ticker in tickers_list
    ]


@pytest.fixture
def earnings_json_mocks(tickers_list: list[str]) -> list[dict[str, Any]]:
    """Quote summary response json mocks with net earnings data."""
    return [
        _get_json_fixture(
            file_name=f'earnings_{ticker.lower()}.json', folder_name='quote_summary'
        )
        for ticker in tickers_list
    ]


@pytest.fixture
def earnings_history_json_mocks(tickers_list: list[str]) -> list[dict[str, Any]]:
    """Quote summary response json mocks with net earnings history data."""
    return [
        _get_json_fixture(
            file_name=f'earnings_history_{ticker.lower()}.json',
            folder_name='quote_summary',
        )
        for ticker in tickers_list
    ]


@pytest.fixture
def earnings_trend_json_mocks(tickers_list: list[str]) -> list[dict[str, Any]]:
    """Quote summary response json mocks with net earnings trend data."""
    return [
        _get_json_fixture(
            file_name=f'earnings_trend_{ticker.lower()}.json',
            folder_name='quote_summary',
        )
        for ticker in tickers_list
    ]


@pytest.fixture
def industry_trend_json_mocks(tickers_list: list[str]) -> list[dict[str, Any]]:
    """Quote summary response json mocks with net industry trend data."""
    return [
        _get_json_fixture(
            file_name=f'industry_trend_{ticker.lower()}.json',
            folder_name='quote_summary',
        )
        for ticker in tickers_list
    ]


@pytest.fixture
def index_trend_json_mocks(tickers_list: list[str]) -> list[dict[str, Any]]:
    """Quote summary response json mocks with net index trend data."""
    return [
        _get_json_fixture(
            file_name=f'index_trend_{ticker.lower()}.json', folder_name='quote_summary'
        )
        for ticker in tickers_list
    ]


@pytest.fixture
def sector_trend_json_mocks(tickers_list: list[str]) -> list[dict[str, Any]]:
    """Quote summary response json mocks with net sector trend data."""
    return [
        _get_json_fixture(
            file_name=f'sector_trend_{ticker.lower()}.json', folder_name='quote_summary'
        )
        for ticker in tickers_list
    ]


@pytest.fixture
def recommendation_trend_json_mocks(tickers_list: list[str]) -> list[dict[str, Any]]:
    """Quote summary response json mocks with net recommendations trend data."""
    return [
        _get_json_fixture(
            file_name=f'recommendation_trend_{ticker.lower()}.json',
            folder_name='quote_summary',
        )
        for ticker in tickers_list
    ]


@pytest.fixture
def page_views_json_mocks(tickers_list: list[str]) -> list[dict[str, Any]]:
    """Quote summary response json mocks with net page views data."""
    return [
        _get_json_fixture(
            file_name=f'page_views_{ticker.lower()}.json', folder_name='quote_summary'
        )
        for ticker in tickers_list
    ]


@pytest.fixture
def calendar_events_json_mocks(tickers_list: list[str]) -> list[dict[str, Any]]:
    """Quote summary response json mock with calendar events data."""
    return [
        _get_json_fixture(
            file_name=f'calendar_events_{ticker.lower()}.json',
            folder_name='quote_summary',
        )
        for ticker in tickers_list
    ]


@pytest.fixture
def timeseries_income_statement_json_mocks(
    tickers_list: list[str],
) -> list[dict[str, Any]]:
    """Timeseries response json mocks with annual income statement data."""
    return [
        _get_json_fixture(
            file_name=f'income_statement_{ticker.lower()}.json',
            folder_name='timeseries',
        )
        for ticker in tickers_list
    ]


@pytest.fixture
def timeseries_balance_sheet_json_mocks(
    tickers_list: list[str],
) -> list[dict[str, Any]]:
    """Timeseries response json mocks with annual balance sheet data."""
    return [
        _get_json_fixture(
            file_name=f'balance_sheet_{ticker.lower()}.json', folder_name='timeseries'
        )
        for ticker in tickers_list
    ]


@pytest.fixture
def timeseries_cash_flow_json_mocks(tickers_list: list[str]) -> list[dict[str, Any]]:
    """Timeseries response json mocks with annual cash flow data."""
    return [
        _get_json_fixture(
            file_name=f'cash_flow_{ticker.lower()}.json', folder_name='timeseries'
        )
        for ticker in tickers_list
    ]


@pytest.fixture
def quote_json_mock(tickers_name: str) -> dict[str, Any]:
    """Quote response json mock."""
    return _get_json_fixture(file_name=f'{tickers_name}.json', folder_name='quote')


@pytest.fixture
def quote_type_json_mock(tickers_name: str) -> dict[str, Any]:
    """Quote_type response json mock."""
    return _get_json_fixture(file_name=f'{tickers_name}.json', folder_name='quote_type')


@pytest.fixture
def search_json_mock(tickers_name: str) -> dict[str, Any]:
    """Search response json mock."""
    return _get_json_fixture(file_name=f'{tickers_name}.json', folder_name='search')


@pytest.fixture
def recommendations_json_mock(tickers_name: str) -> dict[str, Any]:
    """Recommendations response json mock."""
    return _get_json_fixture(
        file_name=f'{tickers_name}.json', folder_name='recommendations'
    )


@pytest.fixture
def insights_json_mock(tickers_name: str) -> dict[str, Any]:
    """Insights response json mock."""
    return _get_json_fixture(file_name=f'{tickers_name}.json', folder_name='insights')


@pytest.fixture
def options_json_mocks(tickers_list: list[str]) -> list[dict[str, Any]]:
    """Options response json mocks."""
    return [
        _get_json_fixture(file_name=f'{ticker.lower()}.json', folder_name='options')
        for ticker in tickers_list
    ]


@pytest.fixture
def ratings_json_mocks(tickers_list: list[str]) -> list[dict[str, Any]]:
    """Ratings response json mocks."""
    return [
        _get_json_fixture(file_name=f'{ticker.lower()}.json', folder_name='ratings')
        for ticker in tickers_list
    ]


class TestUnitSymbols:
    """Unit tests for yafin.Symbols."""

    def test_client(self) -> None:
        """Test client attribute."""
        symbols = Symbols('NETA,AAPL')
        assert symbols._client is None

        symbols._get_client()
        assert symbols._client

        symbols.close()
        assert symbols._client is None

        with Symbols('NETA,AAPL') as symbols:
            assert symbols._client

        assert symbols._client is None

    def test_client_singleton(self) -> None:
        """Test client attribute singleton pattern."""
        meta_aapl = Symbols('NETA,AAPL')
        googl_msft = Symbols('GOOGL,MSFT')

        meta_aapl._get_client()
        googl_msft._get_client()

        # test it is singleton
        assert meta_aapl._client is googl_msft._client

        meta_aapl.close()
        googl_msft.close()

    def test_close(self) -> None:
        """Test client attribute singleton pattern."""
        meta_aapl = Symbols('NETA,AAPL')
        googl_msft = Symbols('GOOGL,MSFT')

        meta_aapl._get_client()
        googl_msft._get_client()

        assert meta_aapl._client
        assert googl_msft._client

        # meta close should not close the aapl client
        meta_aapl.close()
        assert meta_aapl._client is None
        assert googl_msft._client

        googl_msft.close()
        assert meta_aapl._client is None
        assert googl_msft._client is None

    @pytest.fixture
    def symbols(self, tickers: str) -> Generator[Symbols, None, None]:
        """Fresh new instance of Symbols for each tests."""
        with Symbols(tickers) as symbols:
            yield symbols

    def test_get_chart(
        self,
        symbols: Symbols,
        chart_kwargs: dict[str, Any],
        mocker: MockerFixture,
        chart_json_mocks: list[dict[str, Any]],
        interval: str,
        period_range: str | None,
        period1: int | float | None,
        period2: int | float | None,
    ) -> None:
        """Test get_chart method."""
        _mock_response(
            mocker,
            patched_method='yafin.client.Session.get',
            response_jsons=chart_json_mocks,
        )
        chart_result_list = symbols.get_chart(
            interval=interval,
            period_range=period_range,
            period1=period1,
            period2=period2,
            **chart_kwargs,
        )
        _assert_chart_result_list(chart_result_list, symbols.tickers)

    def test_get_chart_invalid_args(
        self,
        symbols: Symbols,
        invalid_chart_kwargs_err_tuple: tuple[dict[str, Any], type[Exception]],
    ) -> None:
        """Test get_chart method with invalid arguments."""
        kwargs, err_cls = invalid_chart_kwargs_err_tuple
        with pytest.raises(err_cls):
            symbols.get_chart(**kwargs)

    def test_get_quote(
        self,
        symbols: Symbols,
        mocker: MockerFixture,
        quote_json_mock: dict[str, Any],
    ) -> None:
        """Test get_quote method."""
        _mock_response(
            mocker,
            patched_method='yafin.client.Session.get',
            response_jsons=[quote_json_mock],
        )
        quotes_result_list = symbols.get_quote()
        _assert_quotes_result_list(quotes_result_list, symbols.tickers)

    def test_get_quote_type(
        self,
        symbols: Symbols,
        mocker: MockerFixture,
        quote_type_json_mock: dict[str, Any],
    ) -> None:
        """Test get_quote_type method."""
        _mock_response(
            mocker,
            patched_method='yafin.client.Session.get',
            response_jsons=[quote_type_json_mock],
        )
        quote_types_result_list = symbols.get_quote_type()
        _assert_quote_types_result_list(quote_types_result_list, symbols.tickers)

    def test_get_quote_summary_all_modules(
        self,
        symbols: Symbols,
        mocker: MockerFixture,
        quote_summary_all_modules_json_mocks: list[dict[str, Any]],
    ) -> None:
        """Test get_quote_summary_all_modules method."""
        _mock_response(
            mocker,
            patched_method='yafin.client.Session.get',
            response_jsons=quote_summary_all_modules_json_mocks,
        )
        quote_summary_all_modules = symbols.get_quote_summary_all_modules()
        _assert_quote_summary_result_list(
            quote_summary_all_modules, symbols.tickers, QUOTE_SUMMARY_MODULES
        )

    def test_get_asset_profile(
        self,
        symbols: Symbols,
        mocker: MockerFixture,
        asset_profile_json_mocks: list[dict[str, Any]],
    ) -> None:
        """Test get_asset_profile method."""
        _mock_response(
            mocker,
            patched_method='yafin.client.Session.get',
            response_jsons=asset_profile_json_mocks,
        )
        asset_profile_list = symbols.get_asset_profile()
        _assert_quote_summary_single_module_result_list(
            asset_profile_list, symbols.tickers, 'assetProfile'
        )

    def test_get_summary_profile(
        self,
        symbols: Symbols,
        mocker: MockerFixture,
        summary_profile_json_mocks: list[dict[str, Any]],
    ) -> None:
        """Test get_summary_profile method."""
        _mock_response(
            mocker,
            patched_method='yafin.client.Session.get',
            response_jsons=summary_profile_json_mocks,
        )
        summary_profile_list = symbols.get_summary_profile()
        _assert_quote_summary_single_module_result_list(
            summary_profile_list, symbols.tickers, 'summaryProfile'
        )

    def test_get_summary_detail(
        self,
        symbols: Symbols,
        mocker: MockerFixture,
        summary_detail_json_mocks: list[dict[str, Any]],
    ) -> None:
        """Test get_summary_detail method."""
        _mock_response(
            mocker,
            patched_method='yafin.client.Session.get',
            response_jsons=summary_detail_json_mocks,
        )
        summary_detail_list = symbols.get_summary_detail()
        _assert_quote_summary_single_module_result_list(
            summary_detail_list, symbols.tickers, 'summaryDetail'
        )

    def test_get_price(
        self,
        symbols: Symbols,
        mocker: MockerFixture,
        price_json_mocks: list[dict[str, Any]],
    ) -> None:
        """Test get_price method."""
        _mock_response(
            mocker,
            patched_method='yafin.client.Session.get',
            response_jsons=price_json_mocks,
        )
        price_list = symbols.get_price()
        _assert_quote_summary_single_module_result_list(
            price_list, symbols.tickers, 'price'
        )

    def test_get_default_key_statistics(
        self,
        symbols: Symbols,
        mocker: MockerFixture,
        default_key_statistics_json_mocks: list[dict[str, Any]],
    ) -> None:
        """Test get_default_key_statistics method."""
        _mock_response(
            mocker,
            patched_method='yafin.client.Session.get',
            response_jsons=default_key_statistics_json_mocks,
        )
        default_key_statistics_list = symbols.get_default_key_statistics()
        _assert_quote_summary_single_module_result_list(
            default_key_statistics_list, symbols.tickers, 'defaultKeyStatistics'
        )

    def test_get_financial_data(
        self,
        symbols: Symbols,
        mocker: MockerFixture,
        financial_data_json_mocks: list[dict[str, Any]],
    ) -> None:
        """Test get_financial_data method."""
        _mock_response(
            mocker,
            patched_method='yafin.client.Session.get',
            response_jsons=financial_data_json_mocks,
        )
        financial_data_list = symbols.get_financial_data()
        _assert_quote_summary_single_module_result_list(
            financial_data_list, symbols.tickers, 'financialData'
        )

    def test_get_calendar_events(
        self,
        symbols: Symbols,
        mocker: MockerFixture,
        calendar_events_json_mocks: list[dict[str, Any]],
    ) -> None:
        """Test get_calendar_events method."""
        _mock_response(
            mocker,
            patched_method='yafin.client.Session.get',
            response_jsons=calendar_events_json_mocks,
        )
        calendar_events_list = symbols.get_calendar_events()
        _assert_quote_summary_single_module_result_list(
            calendar_events_list, symbols.tickers, 'calendarEvents'
        )

    def test_get_sec_filings(
        self,
        symbols: Symbols,
        mocker: MockerFixture,
        sec_filings_json_mocks: list[dict[str, Any]],
    ) -> None:
        """Test get_sec_filings method."""
        _mock_response(
            mocker,
            patched_method='yafin.client.Session.get',
            response_jsons=sec_filings_json_mocks,
        )
        sec_filings_list = symbols.get_sec_filings()
        _assert_quote_summary_single_module_result_list(
            sec_filings_list, symbols.tickers, 'secFilings'
        )

    def test_get_upgrade_downgrade_history(
        self,
        symbols: Symbols,
        mocker: MockerFixture,
        upgrade_downgrade_history_json_mocks: list[dict[str, Any]],
    ) -> None:
        """Test get_upgrade_downgrade_history method."""
        _mock_response(
            mocker,
            patched_method='yafin.client.Session.get',
            response_jsons=upgrade_downgrade_history_json_mocks,
        )
        upgrade_downgrade_history_list = symbols.get_upgrade_downgrade_history()
        _assert_quote_summary_single_module_result_list(
            upgrade_downgrade_history_list, symbols.tickers, 'upgradeDowngradeHistory'
        )

    def test_get_institution_ownership(
        self,
        symbols: Symbols,
        mocker: MockerFixture,
        institution_ownership_json_mocks: list[dict[str, Any]],
    ) -> None:
        """Test get_institution_ownership method."""
        _mock_response(
            mocker,
            patched_method='yafin.client.Session.get',
            response_jsons=institution_ownership_json_mocks,
        )
        institution_ownership_list = symbols.get_institution_ownership()
        _assert_quote_summary_single_module_result_list(
            institution_ownership_list, symbols.tickers, 'institutionOwnership'
        )

    def test_get_fund_ownership(
        self,
        symbols: Symbols,
        mocker: MockerFixture,
        fund_ownership_json_mocks: list[dict[str, Any]],
    ) -> None:
        """Test get_fund_ownership method."""
        _mock_response(
            mocker,
            patched_method='yafin.client.Session.get',
            response_jsons=fund_ownership_json_mocks,
        )
        fund_ownership_list = symbols.get_fund_ownership()
        _assert_quote_summary_single_module_result_list(
            fund_ownership_list, symbols.tickers, 'fundOwnership'
        )

    def test_get_major_direct_holders(
        self,
        symbols: Symbols,
        mocker: MockerFixture,
        major_direct_holders_json_mocks: list[dict[str, Any]],
    ) -> None:
        """Test get_major_direct_holders method."""
        _mock_response(
            mocker,
            patched_method='yafin.client.Session.get',
            response_jsons=major_direct_holders_json_mocks,
        )
        major_direct_holders_list = symbols.get_major_direct_holders()
        _assert_quote_summary_single_module_result_list(
            major_direct_holders_list, symbols.tickers, 'majorDirectHolders'
        )

    def test_get_major_holders_breakdown(
        self,
        symbols: Symbols,
        mocker: MockerFixture,
        major_holders_breakdown_json_mocks: list[dict[str, Any]],
    ) -> None:
        """Test get_major_holders_breakdown method."""
        _mock_response(
            mocker,
            patched_method='yafin.client.Session.get',
            response_jsons=major_holders_breakdown_json_mocks,
        )
        major_holders_breakdown_list = symbols.get_major_holders_breakdown()
        _assert_quote_summary_single_module_result_list(
            major_holders_breakdown_list, symbols.tickers, 'majorHoldersBreakdown'
        )

    def test_get_insider_transactions(
        self,
        symbols: Symbols,
        mocker: MockerFixture,
        insider_transactions_json_mocks: list[dict[str, Any]],
    ) -> None:
        """Test get_insider_transactions method."""
        _mock_response(
            mocker,
            patched_method='yafin.client.Session.get',
            response_jsons=insider_transactions_json_mocks,
        )
        insider_transactions_list = symbols.get_insider_transactions()
        _assert_quote_summary_single_module_result_list(
            insider_transactions_list, symbols.tickers, 'insiderTransactions'
        )

    def test_get_insider_holders(
        self,
        symbols: Symbols,
        mocker: MockerFixture,
        insider_holders_json_mocks: list[dict[str, Any]],
    ) -> None:
        """Test get_insider_holders method."""
        _mock_response(
            mocker,
            patched_method='yafin.client.Session.get',
            response_jsons=insider_holders_json_mocks,
        )
        insider_holders_list = symbols.get_insider_holders()
        _assert_quote_summary_single_module_result_list(
            insider_holders_list, symbols.tickers, 'insiderHolders'
        )

    def test_get_net_share_purchase_activity(
        self,
        symbols: Symbols,
        mocker: MockerFixture,
        net_share_purchase_activity_json_mocks: list[dict[str, Any]],
    ) -> None:
        """Test get_net_share_purchase_activity method."""
        _mock_response(
            mocker,
            patched_method='yafin.client.Session.get',
            response_jsons=net_share_purchase_activity_json_mocks,
        )
        net_share_purchase_activity_list = symbols.get_net_share_purchase_activity()
        _assert_quote_summary_single_module_result_list(
            net_share_purchase_activity_list,
            symbols.tickers,
            'netSharePurchaseActivity',
        )

    def test_get_earnings(
        self,
        symbols: Symbols,
        mocker: MockerFixture,
        earnings_json_mocks: list[dict[str, Any]],
    ) -> None:
        """Test get_earnings method."""
        _mock_response(
            mocker,
            patched_method='yafin.client.Session.get',
            response_jsons=earnings_json_mocks,
        )
        earnings_list = symbols.get_earnings()
        _assert_quote_summary_single_module_result_list(
            earnings_list, symbols.tickers, 'earnings'
        )

    def test_get_earnings_history(
        self,
        symbols: Symbols,
        mocker: MockerFixture,
        earnings_history_json_mocks: list[dict[str, Any]],
    ) -> None:
        """Test get_earnings_history method."""
        _mock_response(
            mocker,
            patched_method='yafin.client.Session.get',
            response_jsons=earnings_history_json_mocks,
        )
        earnings_history_list = symbols.get_earnings_history()
        _assert_quote_summary_single_module_result_list(
            earnings_history_list, symbols.tickers, 'earningsHistory'
        )

    def test_get_earnings_trend(
        self,
        symbols: Symbols,
        mocker: MockerFixture,
        earnings_trend_json_mocks: list[dict[str, Any]],
    ) -> None:
        """Test get_earnings_trend method."""
        _mock_response(
            mocker,
            patched_method='yafin.client.Session.get',
            response_jsons=earnings_trend_json_mocks,
        )
        earnings_trend_list = symbols.get_earnings_trend()
        _assert_quote_summary_single_module_result_list(
            earnings_trend_list, symbols.tickers, 'earningsTrend'
        )

    def test_get_industry_trend(
        self,
        symbols: Symbols,
        mocker: MockerFixture,
        industry_trend_json_mocks: list[dict[str, Any]],
    ) -> None:
        """Test get_industry_trend method."""
        _mock_response(
            mocker,
            patched_method='yafin.client.Session.get',
            response_jsons=industry_trend_json_mocks,
        )
        industry_trend_list = symbols.get_industry_trend()
        _assert_quote_summary_single_module_result_list(
            industry_trend_list, symbols.tickers, 'industryTrend'
        )

    def test_get_index_trend(
        self,
        symbols: Symbols,
        mocker: MockerFixture,
        index_trend_json_mocks: list[dict[str, Any]],
    ) -> None:
        """Test get_index_trend method."""
        _mock_response(
            mocker,
            patched_method='yafin.client.Session.get',
            response_jsons=index_trend_json_mocks,
        )
        index_trend_list = symbols.get_index_trend()
        _assert_quote_summary_single_module_result_list(
            index_trend_list, symbols.tickers, 'indexTrend'
        )

    def test_get_sector_trend(
        self,
        symbols: Symbols,
        mocker: MockerFixture,
        sector_trend_json_mocks: list[dict[str, Any]],
    ) -> None:
        """Test get_sector_trend method."""
        _mock_response(
            mocker,
            patched_method='yafin.client.Session.get',
            response_jsons=sector_trend_json_mocks,
        )
        sector_trend_list = symbols.get_sector_trend()
        _assert_quote_summary_single_module_result_list(
            sector_trend_list, symbols.tickers, 'sectorTrend'
        )

    def test_get_recommendation_trend(
        self,
        symbols: Symbols,
        mocker: MockerFixture,
        recommendation_trend_json_mocks: list[dict[str, Any]],
    ) -> None:
        """Test get_recommendation_trend method."""
        _mock_response(
            mocker,
            patched_method='yafin.client.Session.get',
            response_jsons=recommendation_trend_json_mocks,
        )
        recommendation_trend_list = symbols.get_recommendation_trend()
        _assert_quote_summary_single_module_result_list(
            recommendation_trend_list, symbols.tickers, 'recommendationTrend'
        )

    def test_get_page_views(
        self,
        symbols: Symbols,
        mocker: MockerFixture,
        page_views_json_mocks: list[dict[str, Any]],
    ) -> None:
        """Test get_page_views method."""
        _mock_response(
            mocker,
            patched_method='yafin.client.Session.get',
            response_jsons=page_views_json_mocks,
        )
        page_views_list = symbols.get_page_views()
        _assert_quote_summary_single_module_result_list(
            page_views_list, symbols.tickers, 'pageViews'
        )

    def test_get_income_statement(
        self,
        symbols: Symbols,
        mocker: MockerFixture,
        timeseries_income_statement_json_mocks: list[dict[str, Any]],
        period1: int | float | None,
        period2: int | float | None,
    ) -> None:
        """Test get_income_statement method."""
        _mock_response(
            mocker,
            patched_method='yafin.client.Session.get',
            response_jsons=timeseries_income_statement_json_mocks,
        )
        annual_income_stmt_list = symbols.get_income_statement(
            frequency='annual', period1=period1, period2=period2
        )
        _assert_timeseries_result_list(
            annual_income_stmt_list, symbols.tickers, ANNUAL_INCOME_STATEMENT_TYPES
        )

    def test_get_income_statement_invalid_args(self, symbols: Symbols) -> None:
        """Test get_income_statement method with invalid arguments.."""
        with pytest.raises(ValueError):
            symbols.get_income_statement(frequency='xxx')

    def test_get_balance_sheet(
        self,
        symbols: Symbols,
        mocker: MockerFixture,
        timeseries_balance_sheet_json_mocks: list[dict[str, Any]],
        period1: int | float | None,
        period2: int | float | None,
    ) -> None:
        """Test get_balance_sheet method."""
        _mock_response(
            mocker,
            patched_method='yafin.client.Session.get',
            response_jsons=timeseries_balance_sheet_json_mocks,
        )
        annual_balance_sheets_list = symbols.get_balance_sheet(
            frequency='annual', period1=period1, period2=period2
        )
        _assert_timeseries_result_list(
            annual_balance_sheets_list, symbols.tickers, ANNUAL_BALANCE_SHEET_TYPES
        )

    def test_get_balance_sheet_invalid_args(
        self,
        symbols: Symbols,
        invalid_balance_sheet_kwargs_err_tuple: tuple[dict[str, Any], type[Exception]],
    ) -> None:
        """Test get_balance_sheet method."""
        kwargs, err_cls = invalid_balance_sheet_kwargs_err_tuple
        with pytest.raises(err_cls):
            symbols.get_balance_sheet(**kwargs)

    def test_get_cash_flow(
        self,
        symbols: Symbols,
        mocker: MockerFixture,
        timeseries_cash_flow_json_mocks: list[dict[str, Any]],
        period1: int | float | None,
        period2: int | float | None,
    ) -> None:
        """Test get_cash_flow method."""
        _mock_response(
            mocker,
            patched_method='yafin.client.Session.get',
            response_jsons=timeseries_cash_flow_json_mocks,
        )
        annual_cash_flows_list = symbols.get_cash_flow(
            frequency='annual', period1=period1, period2=period2
        )
        _assert_timeseries_result_list(
            annual_cash_flows_list, symbols.tickers, ANNUAL_CASH_FLOW_TYPES
        )

    def test_get_cash_flow_invalid_args(self, symbols: Symbols) -> None:
        """Test get_cash_flow method with invalid arguments."""
        with pytest.raises(ValueError):
            symbols.get_cash_flow(frequency='xxx')

    def test_get_search(
        self,
        symbols: Symbols,
        mocker: MockerFixture,
        search_json_mock: dict[str, Any],
    ) -> None:
        """Test get_search method."""
        _mock_response(
            mocker,
            patched_method='yafin.client.Session.get',
            response_jsons=[search_json_mock],
        )
        search = symbols.get_search()
        _assert_search_result(search)

    def test_get_recommendations(
        self,
        symbols: Symbols,
        mocker: MockerFixture,
        recommendations_json_mock: dict[str, Any],
    ) -> None:
        """Test get_recommendations method."""
        _mock_response(
            mocker,
            patched_method='yafin.client.Session.get',
            response_jsons=[recommendations_json_mock],
        )
        recommendations_result_list = symbols.get_recommendations()
        _assert_recommendations_result_list(
            recommendations_result_list, symbols.tickers
        )

    def test_get_insights(
        self,
        symbols: Symbols,
        mocker: MockerFixture,
        insights_json_mock: dict[str, Any],
    ) -> None:
        """Test get_insights method."""
        _mock_response(
            mocker,
            patched_method='yafin.client.Session.get',
            response_jsons=[insights_json_mock],
        )
        insights_result_list = symbols.get_insights()
        _assert_insights_result_list(insights_result_list, symbols.tickers)

    def test_get_options(
        self,
        symbols: Symbols,
        mocker: MockerFixture,
        options_json_mocks: list[dict[str, Any]],
    ) -> None:
        """Test get_options method."""
        _mock_response(
            mocker,
            patched_method='yafin.client.Session.get',
            response_jsons=options_json_mocks,
        )
        options_result_list = symbols.get_options()
        _assert_options_result_list(options_result_list, symbols.tickers)

    def test_get_ratings(
        self,
        symbols: Symbols,
        mocker: MockerFixture,
        ratings_json_mocks: list[dict[str, Any]],
    ) -> None:
        """Test get_ratings method."""
        _mock_response(
            mocker,
            patched_method='yafin.client.Session.get',
            response_jsons=ratings_json_mocks,
        )
        ratings_result_list = symbols.get_ratings()
        _assert_ratings_result_list(ratings_result_list, symbols.tickers)


class TestUnitAsyncSymbols:
    """Unit tests for yafin.AsyncSymbols."""

    @pytest.mark.asyncio
    async def test_client(self) -> None:
        """Test client attribute."""
        async_symbols = AsyncSymbols('NETA,AAPL')
        assert async_symbols._client is None

        await async_symbols._get_client()
        assert async_symbols._client

        await async_symbols.close()
        assert async_symbols._client is None

        async with AsyncSymbols('NETA,AAPL') as async_symbols:
            assert async_symbols._client

        assert async_symbols._client is None

    @pytest.mark.asyncio
    async def test_client_singleton(self) -> None:
        """Test client attribute singleton pattern."""
        meta_aapl = AsyncSymbols('NETA,AAPL')
        googl_msft = AsyncSymbols('GOOGL,MSFT')

        await meta_aapl._get_client()
        await googl_msft._get_client()

        # test it is singleton
        assert meta_aapl._client is googl_msft._client

        await meta_aapl.close()
        await googl_msft.close()

    @pytest.mark.asyncio
    async def test_close(self) -> None:
        """Test client attribute singleton pattern."""
        meta_aapl = AsyncSymbols('NETA,AAPL')
        googl_msft = AsyncSymbols('GOOGL,MSFT')

        await meta_aapl._get_client()
        await googl_msft._get_client()

        assert meta_aapl._client
        assert googl_msft._client

        # meta close should not close the aapl client
        await meta_aapl.close()
        assert meta_aapl._client is None
        assert googl_msft._client

        await googl_msft.close()
        assert meta_aapl._client is None
        assert googl_msft._client is None

    @pytest_asyncio.fixture
    async def async_symbols(self, tickers: str) -> AsyncGenerator[AsyncSymbols, None]:
        """Fresh new instance of AsyncSymbols for each tests."""
        async with AsyncSymbols(tickers) as async_symbols:
            yield async_symbols

    @pytest.mark.asyncio
    async def test_get_chart(
        self,
        async_symbols: AsyncSymbols,
        chart_kwargs: dict[str, Any],
        mocker: MockerFixture,
        chart_json_mocks: list[dict[str, Any]],
        interval: str,
        period_range: str | None,
        period1: int | float | None,
        period2: int | float | None,
    ) -> None:
        """Test get_chart method."""
        _mock_response(
            mocker,
            patched_method='yafin.client.AsyncSession.get',
            response_jsons=chart_json_mocks,
            async_mock=True,
        )
        chart_result_list = await async_symbols.get_chart(
            interval=interval,
            period_range=period_range,
            period1=period1,
            period2=period2,
            **chart_kwargs,
        )
        _assert_chart_result_list(chart_result_list, async_symbols.tickers)

    @pytest.mark.asyncio
    async def test_get_chart_invalid_args(
        self,
        async_symbols: AsyncSymbols,
        invalid_chart_kwargs_err_tuple: tuple[dict[str, Any], type[Exception]],
    ) -> None:
        """Test get_chart method with invalid arguments."""
        kwargs, err_cls = invalid_chart_kwargs_err_tuple
        with pytest.raises(err_cls):
            await async_symbols.get_chart(**kwargs)

    @pytest.mark.asyncio
    async def test_get_quote(
        self,
        async_symbols: AsyncSymbols,
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
        quotes_result_list = await async_symbols.get_quote()
        _assert_quotes_result_list(quotes_result_list, async_symbols.tickers)

    @pytest.mark.asyncio
    async def test_get_quote_type(
        self,
        async_symbols: AsyncSymbols,
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
        quote_types_result_list = await async_symbols.get_quote_type()
        _assert_quote_types_result_list(quote_types_result_list, async_symbols.tickers)

    @pytest.mark.asyncio
    async def test_get_quote_summary_all_modules(
        self,
        async_symbols: AsyncSymbols,
        mocker: MockerFixture,
        quote_summary_all_modules_json_mocks: list[dict[str, Any]],
    ) -> None:
        """Test get_quote_summary_all_modules method."""
        _mock_response(
            mocker,
            patched_method='yafin.client.AsyncSession.get',
            response_jsons=quote_summary_all_modules_json_mocks,
            async_mock=True,
        )
        quote_summary_all_modules = await async_symbols.get_quote_summary_all_modules()
        _assert_quote_summary_result_list(
            quote_summary_all_modules, async_symbols.tickers, QUOTE_SUMMARY_MODULES
        )

    @pytest.mark.asyncio
    async def test_get_asset_profile(
        self,
        async_symbols: AsyncSymbols,
        mocker: MockerFixture,
        asset_profile_json_mocks: list[dict[str, Any]],
    ) -> None:
        """Test get_asset_profile method."""
        _mock_response(
            mocker,
            patched_method='yafin.client.AsyncSession.get',
            response_jsons=asset_profile_json_mocks,
            async_mock=True,
        )
        asset_profile_list = await async_symbols.get_asset_profile()
        _assert_quote_summary_single_module_result_list(
            asset_profile_list, async_symbols.tickers, 'assetProfile'
        )

    @pytest.mark.asyncio
    async def test_get_summary_profile(
        self,
        async_symbols: AsyncSymbols,
        mocker: MockerFixture,
        summary_profile_json_mocks: list[dict[str, Any]],
    ) -> None:
        """Test get_summary_profile method."""
        _mock_response(
            mocker,
            patched_method='yafin.client.AsyncSession.get',
            response_jsons=summary_profile_json_mocks,
            async_mock=True,
        )
        summary_profile_list = await async_symbols.get_summary_profile()
        _assert_quote_summary_single_module_result_list(
            summary_profile_list, async_symbols.tickers, 'summaryProfile'
        )

    @pytest.mark.asyncio
    async def test_get_summary_detail(
        self,
        async_symbols: AsyncSymbols,
        mocker: MockerFixture,
        summary_detail_json_mocks: list[dict[str, Any]],
    ) -> None:
        """Test get_summary_detail method."""
        _mock_response(
            mocker,
            patched_method='yafin.client.AsyncSession.get',
            response_jsons=summary_detail_json_mocks,
            async_mock=True,
        )
        summary_detail_list = await async_symbols.get_summary_detail()
        _assert_quote_summary_single_module_result_list(
            summary_detail_list, async_symbols.tickers, 'summaryDetail'
        )

    @pytest.mark.asyncio
    async def test_get_price(
        self,
        async_symbols: AsyncSymbols,
        mocker: MockerFixture,
        price_json_mocks: list[dict[str, Any]],
    ) -> None:
        """Test get_price method."""
        _mock_response(
            mocker,
            patched_method='yafin.client.AsyncSession.get',
            response_jsons=price_json_mocks,
            async_mock=True,
        )
        price_list = await async_symbols.get_price()
        _assert_quote_summary_single_module_result_list(
            price_list, async_symbols.tickers, 'price'
        )

    @pytest.mark.asyncio
    async def test_get_default_key_statistics(
        self,
        async_symbols: AsyncSymbols,
        mocker: MockerFixture,
        default_key_statistics_json_mocks: list[dict[str, Any]],
    ) -> None:
        """Test get_default_key_statistics method."""
        _mock_response(
            mocker,
            patched_method='yafin.client.AsyncSession.get',
            response_jsons=default_key_statistics_json_mocks,
            async_mock=True,
        )
        default_key_statistics_list = await async_symbols.get_default_key_statistics()
        _assert_quote_summary_single_module_result_list(
            default_key_statistics_list, async_symbols.tickers, 'defaultKeyStatistics'
        )

    @pytest.mark.asyncio
    async def test_get_financial_data(
        self,
        async_symbols: AsyncSymbols,
        mocker: MockerFixture,
        financial_data_json_mocks: list[dict[str, Any]],
    ) -> None:
        """Test get_financial_data method."""
        _mock_response(
            mocker,
            patched_method='yafin.client.AsyncSession.get',
            response_jsons=financial_data_json_mocks,
            async_mock=True,
        )
        financial_data_list = await async_symbols.get_financial_data()
        _assert_quote_summary_single_module_result_list(
            financial_data_list, async_symbols.tickers, 'financialData'
        )

    @pytest.mark.asyncio
    async def test_get_calendar_events(
        self,
        async_symbols: AsyncSymbols,
        mocker: MockerFixture,
        calendar_events_json_mocks: list[dict[str, Any]],
    ) -> None:
        """Test get_calendar_events method."""
        _mock_response(
            mocker,
            patched_method='yafin.client.AsyncSession.get',
            response_jsons=calendar_events_json_mocks,
            async_mock=True,
        )
        calendar_events_list = await async_symbols.get_calendar_events()
        _assert_quote_summary_single_module_result_list(
            calendar_events_list, async_symbols.tickers, 'calendarEvents'
        )

    @pytest.mark.asyncio
    async def test_get_sec_filings(
        self,
        async_symbols: AsyncSymbols,
        mocker: MockerFixture,
        sec_filings_json_mocks: list[dict[str, Any]],
    ) -> None:
        """Test get_sec_filings method."""
        _mock_response(
            mocker,
            patched_method='yafin.client.AsyncSession.get',
            response_jsons=sec_filings_json_mocks,
            async_mock=True,
        )
        sec_filings_list = await async_symbols.get_sec_filings()
        _assert_quote_summary_single_module_result_list(
            sec_filings_list, async_symbols.tickers, 'secFilings'
        )

    @pytest.mark.asyncio
    async def test_get_upgrade_downgrade_history(
        self,
        async_symbols: AsyncSymbols,
        mocker: MockerFixture,
        upgrade_downgrade_history_json_mocks: list[dict[str, Any]],
    ) -> None:
        """Test get_upgrade_downgrade_history method."""
        _mock_response(
            mocker,
            patched_method='yafin.client.AsyncSession.get',
            response_jsons=upgrade_downgrade_history_json_mocks,
            async_mock=True,
        )
        upgrade_downgrade_history_list = (
            await async_symbols.get_upgrade_downgrade_history()
        )
        _assert_quote_summary_single_module_result_list(
            upgrade_downgrade_history_list,
            async_symbols.tickers,
            'upgradeDowngradeHistory',
        )

    @pytest.mark.asyncio
    async def test_get_institution_ownership(
        self,
        async_symbols: AsyncSymbols,
        mocker: MockerFixture,
        institution_ownership_json_mocks: list[dict[str, Any]],
    ) -> None:
        """Test get_institution_ownership method."""
        _mock_response(
            mocker,
            patched_method='yafin.client.AsyncSession.get',
            response_jsons=institution_ownership_json_mocks,
            async_mock=True,
        )
        institution_ownership_list = await async_symbols.get_institution_ownership()
        _assert_quote_summary_single_module_result_list(
            institution_ownership_list, async_symbols.tickers, 'institutionOwnership'
        )

    @pytest.mark.asyncio
    async def test_get_fund_ownership(
        self,
        async_symbols: AsyncSymbols,
        mocker: MockerFixture,
        fund_ownership_json_mocks: list[dict[str, Any]],
    ) -> None:
        """Test get_fund_ownership method."""
        _mock_response(
            mocker,
            patched_method='yafin.client.AsyncSession.get',
            response_jsons=fund_ownership_json_mocks,
            async_mock=True,
        )
        fund_ownership_list = await async_symbols.get_fund_ownership()
        _assert_quote_summary_single_module_result_list(
            fund_ownership_list, async_symbols.tickers, 'fundOwnership'
        )

    @pytest.mark.asyncio
    async def test_get_major_direct_holders(
        self,
        async_symbols: AsyncSymbols,
        mocker: MockerFixture,
        major_direct_holders_json_mocks: list[dict[str, Any]],
    ) -> None:
        """Test get_major_direct_holders method."""
        _mock_response(
            mocker,
            patched_method='yafin.client.AsyncSession.get',
            response_jsons=major_direct_holders_json_mocks,
            async_mock=True,
        )
        major_direct_holders_list = await async_symbols.get_major_direct_holders()
        _assert_quote_summary_single_module_result_list(
            major_direct_holders_list, async_symbols.tickers, 'majorDirectHolders'
        )

    @pytest.mark.asyncio
    async def test_get_major_holders_breakdown(
        self,
        async_symbols: AsyncSymbols,
        mocker: MockerFixture,
        major_holders_breakdown_json_mocks: list[dict[str, Any]],
    ) -> None:
        """Test get_major_holders_breakdown method."""
        _mock_response(
            mocker,
            patched_method='yafin.client.AsyncSession.get',
            response_jsons=major_holders_breakdown_json_mocks,
            async_mock=True,
        )
        major_holders_breakdown_list = await async_symbols.get_major_holders_breakdown()
        _assert_quote_summary_single_module_result_list(
            major_holders_breakdown_list, async_symbols.tickers, 'majorHoldersBreakdown'
        )

    @pytest.mark.asyncio
    async def test_get_insider_transactions(
        self,
        async_symbols: AsyncSymbols,
        mocker: MockerFixture,
        insider_transactions_json_mocks: list[dict[str, Any]],
    ) -> None:
        """Test get_insider_transactions method."""
        _mock_response(
            mocker,
            patched_method='yafin.client.AsyncSession.get',
            response_jsons=insider_transactions_json_mocks,
            async_mock=True,
        )
        insider_transactions_list = await async_symbols.get_insider_transactions()
        _assert_quote_summary_single_module_result_list(
            insider_transactions_list, async_symbols.tickers, 'insiderTransactions'
        )

    @pytest.mark.asyncio
    async def test_get_insider_holders(
        self,
        async_symbols: AsyncSymbols,
        mocker: MockerFixture,
        insider_holders_json_mocks: list[dict[str, Any]],
    ) -> None:
        """Test get_insider_holders method."""
        _mock_response(
            mocker,
            patched_method='yafin.client.AsyncSession.get',
            response_jsons=insider_holders_json_mocks,
            async_mock=True,
        )
        insider_holders_list = await async_symbols.get_insider_holders()
        _assert_quote_summary_single_module_result_list(
            insider_holders_list, async_symbols.tickers, 'insiderHolders'
        )

    @pytest.mark.asyncio
    async def test_get_net_share_purchase_activity(
        self,
        async_symbols: AsyncSymbols,
        mocker: MockerFixture,
        net_share_purchase_activity_json_mocks: list[dict[str, Any]],
    ) -> None:
        """Test get_net_share_purchase_activity method."""
        _mock_response(
            mocker,
            patched_method='yafin.client.AsyncSession.get',
            response_jsons=net_share_purchase_activity_json_mocks,
            async_mock=True,
        )
        net_share_purchase_activity_list = (
            await async_symbols.get_net_share_purchase_activity()
        )
        _assert_quote_summary_single_module_result_list(
            net_share_purchase_activity_list,
            async_symbols.tickers,
            'netSharePurchaseActivity',
        )

    @pytest.mark.asyncio
    async def test_get_earnings(
        self,
        async_symbols: AsyncSymbols,
        mocker: MockerFixture,
        earnings_json_mocks: list[dict[str, Any]],
    ) -> None:
        """Test get_earnings method."""
        _mock_response(
            mocker,
            patched_method='yafin.client.AsyncSession.get',
            response_jsons=earnings_json_mocks,
            async_mock=True,
        )
        earnings_list = await async_symbols.get_earnings()
        _assert_quote_summary_single_module_result_list(
            earnings_list, async_symbols.tickers, 'earnings'
        )

    @pytest.mark.asyncio
    async def test_get_earnings_history(
        self,
        async_symbols: AsyncSymbols,
        mocker: MockerFixture,
        earnings_history_json_mocks: list[dict[str, Any]],
    ) -> None:
        """Test get_earnings_history method."""
        _mock_response(
            mocker,
            patched_method='yafin.client.AsyncSession.get',
            response_jsons=earnings_history_json_mocks,
            async_mock=True,
        )
        earnings_history_list = await async_symbols.get_earnings_history()
        _assert_quote_summary_single_module_result_list(
            earnings_history_list, async_symbols.tickers, 'earningsHistory'
        )

    @pytest.mark.asyncio
    async def test_get_earnings_trend(
        self,
        async_symbols: AsyncSymbols,
        mocker: MockerFixture,
        earnings_trend_json_mocks: list[dict[str, Any]],
    ) -> None:
        """Test get_earnings_trend method."""
        _mock_response(
            mocker,
            patched_method='yafin.client.AsyncSession.get',
            response_jsons=earnings_trend_json_mocks,
            async_mock=True,
        )
        earnings_trend_list = await async_symbols.get_earnings_trend()
        _assert_quote_summary_single_module_result_list(
            earnings_trend_list, async_symbols.tickers, 'earningsTrend'
        )

    @pytest.mark.asyncio
    async def test_get_industry_trend(
        self,
        async_symbols: AsyncSymbols,
        mocker: MockerFixture,
        industry_trend_json_mocks: list[dict[str, Any]],
    ) -> None:
        """Test get_industry_trend method."""
        _mock_response(
            mocker,
            patched_method='yafin.client.AsyncSession.get',
            response_jsons=industry_trend_json_mocks,
            async_mock=True,
        )
        industry_trend_list = await async_symbols.get_industry_trend()
        _assert_quote_summary_single_module_result_list(
            industry_trend_list, async_symbols.tickers, 'industryTrend'
        )

    @pytest.mark.asyncio
    async def test_get_index_trend(
        self,
        async_symbols: AsyncSymbols,
        mocker: MockerFixture,
        index_trend_json_mocks: list[dict[str, Any]],
    ) -> None:
        """Test get_index_trend method."""
        _mock_response(
            mocker,
            patched_method='yafin.client.AsyncSession.get',
            response_jsons=index_trend_json_mocks,
            async_mock=True,
        )
        index_trend_list = await async_symbols.get_index_trend()
        _assert_quote_summary_single_module_result_list(
            index_trend_list, async_symbols.tickers, 'indexTrend'
        )

    @pytest.mark.asyncio
    async def test_get_sector_trend(
        self,
        async_symbols: AsyncSymbols,
        mocker: MockerFixture,
        sector_trend_json_mocks: list[dict[str, Any]],
    ) -> None:
        """Test get_sector_trend method."""
        _mock_response(
            mocker,
            patched_method='yafin.client.AsyncSession.get',
            response_jsons=sector_trend_json_mocks,
            async_mock=True,
        )
        sector_trend_list = await async_symbols.get_sector_trend()
        _assert_quote_summary_single_module_result_list(
            sector_trend_list, async_symbols.tickers, 'sectorTrend'
        )

    @pytest.mark.asyncio
    async def test_get_recommendation_trend(
        self,
        async_symbols: AsyncSymbols,
        mocker: MockerFixture,
        recommendation_trend_json_mocks: list[dict[str, Any]],
    ) -> None:
        """Test get_recommendation_trend method."""
        _mock_response(
            mocker,
            patched_method='yafin.client.AsyncSession.get',
            response_jsons=recommendation_trend_json_mocks,
            async_mock=True,
        )
        recommendation_trend_list = await async_symbols.get_recommendation_trend()
        _assert_quote_summary_single_module_result_list(
            recommendation_trend_list, async_symbols.tickers, 'recommendationTrend'
        )

    @pytest.mark.asyncio
    async def test_get_page_views(
        self,
        async_symbols: AsyncSymbols,
        mocker: MockerFixture,
        page_views_json_mocks: list[dict[str, Any]],
    ) -> None:
        """Test get_page_views method."""
        _mock_response(
            mocker,
            patched_method='yafin.client.AsyncSession.get',
            response_jsons=page_views_json_mocks,
            async_mock=True,
        )
        page_views_list = await async_symbols.get_page_views()
        _assert_quote_summary_single_module_result_list(
            page_views_list, async_symbols.tickers, 'pageViews'
        )

    @pytest.mark.asyncio
    async def test_get_income_statement(
        self,
        async_symbols: AsyncSymbols,
        mocker: MockerFixture,
        timeseries_income_statement_json_mocks: list[dict[str, Any]],
        period1: int | float | None,
        period2: int | float | None,
    ) -> None:
        """Test get_income_statement method."""
        _mock_response(
            mocker,
            patched_method='yafin.client.AsyncSession.get',
            response_jsons=timeseries_income_statement_json_mocks,
            async_mock=True,
        )
        annual_income_stmt_list = await async_symbols.get_income_statement(
            frequency='annual', period1=period1, period2=period2
        )
        _assert_timeseries_result_list(
            annual_income_stmt_list,
            async_symbols.tickers,
            ANNUAL_INCOME_STATEMENT_TYPES,
        )

    @pytest.mark.asyncio
    async def test_get_income_statement_invalid_args(
        self, async_symbols: AsyncSymbols
    ) -> None:
        """Test get_income_statement method with invalid arguments.."""
        with pytest.raises(ValueError):
            await async_symbols.get_income_statement(frequency='xxx')

    @pytest.mark.asyncio
    async def test_get_balance_sheet(
        self,
        async_symbols: AsyncSymbols,
        mocker: MockerFixture,
        timeseries_balance_sheet_json_mocks: list[dict[str, Any]],
        period1: int | float | None,
        period2: int | float | None,
    ) -> None:
        """Test get_balance_sheet method."""
        _mock_response(
            mocker,
            patched_method='yafin.client.AsyncSession.get',
            response_jsons=timeseries_balance_sheet_json_mocks,
            async_mock=True,
        )
        annual_balance_sheets_list = await async_symbols.get_balance_sheet(
            frequency='annual', period1=period1, period2=period2
        )
        _assert_timeseries_result_list(
            annual_balance_sheets_list,
            async_symbols.tickers,
            ANNUAL_BALANCE_SHEET_TYPES,
        )

    @pytest.mark.asyncio
    async def test_get_balance_sheet_invalid_args(
        self,
        async_symbols: AsyncSymbols,
        invalid_balance_sheet_kwargs_err_tuple: tuple[dict[str, Any], type[Exception]],
    ) -> None:
        """Test get_balance_sheet method."""
        kwargs, err_cls = invalid_balance_sheet_kwargs_err_tuple
        with pytest.raises(err_cls):
            await async_symbols.get_balance_sheet(**kwargs)

    @pytest.mark.asyncio
    async def test_get_cash_flow(
        self,
        async_symbols: AsyncSymbols,
        mocker: MockerFixture,
        timeseries_cash_flow_json_mocks: list[dict[str, Any]],
        period1: int | float | None,
        period2: int | float | None,
    ) -> None:
        """Test get_cash_flow method."""
        _mock_response(
            mocker,
            patched_method='yafin.client.AsyncSession.get',
            response_jsons=timeseries_cash_flow_json_mocks,
            async_mock=True,
        )
        annual_cash_flows_list = await async_symbols.get_cash_flow(
            frequency='annual', period1=period1, period2=period2
        )
        _assert_timeseries_result_list(
            annual_cash_flows_list, async_symbols.tickers, ANNUAL_CASH_FLOW_TYPES
        )

    @pytest.mark.asyncio
    async def test_get_cash_flow_invalid_args(
        self, async_symbols: AsyncSymbols
    ) -> None:
        """Test get_cash_flow method with invalid arguments."""
        with pytest.raises(ValueError):
            await async_symbols.get_cash_flow(frequency='xxx')

    @pytest.mark.asyncio
    async def test_get_search(
        self,
        async_symbols: AsyncSymbols,
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
        search = await async_symbols.get_search()
        _assert_search_result(search)

    @pytest.mark.asyncio
    async def test_get_recommendations(
        self,
        async_symbols: AsyncSymbols,
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
        recommendations_result_list = await async_symbols.get_recommendations()
        _assert_recommendations_result_list(
            recommendations_result_list, async_symbols.tickers
        )

    @pytest.mark.asyncio
    async def test_get_insights(
        self,
        async_symbols: AsyncSymbols,
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
        insights_result_list = await async_symbols.get_insights()
        _assert_insights_result_list(insights_result_list, async_symbols.tickers)

    @pytest.mark.asyncio
    async def test_get_options(
        self,
        async_symbols: AsyncSymbols,
        mocker: MockerFixture,
        options_json_mocks: list[dict[str, Any]],
    ) -> None:
        """Test get_options method."""
        _mock_response(
            mocker,
            patched_method='yafin.client.AsyncSession.get',
            response_jsons=options_json_mocks,
            async_mock=True,
        )
        options_result_list = await async_symbols.get_options()
        _assert_options_result_list(options_result_list, async_symbols.tickers)

    @pytest.mark.asyncio
    async def test_get_ratings(
        self,
        async_symbols: AsyncSymbols,
        mocker: MockerFixture,
        ratings_json_mocks: list[dict[str, Any]],
    ) -> None:
        """Test get_ratings method."""
        _mock_response(
            mocker,
            patched_method='yafin.client.AsyncSession.get',
            response_jsons=ratings_json_mocks,
            async_mock=True,
        )
        ratings_result_list = await async_symbols.get_ratings()
        _assert_ratings_result_list(ratings_result_list, async_symbols.tickers)
