import asyncio
import json
from datetime import datetime

from logging_config import setup_logging

from yafin import AsyncClient, AsyncSymbol


async def main() -> None:  # noqa: D103
    setup_logging()

    client = AsyncClient()

    meta_1y_chart = await client.get_chart(
        ticker='META', period_range='1y', interval='1d'
    )
    print(json.dumps(meta_1y_chart, indent=2))

    await client.close()

    async with AsyncClient() as client:
        aapl_5d_chart = await client.get_chart(
            ticker='AAPL', period_range='5d', interval='1h', events='div,split'
        )
        print(json.dumps(aapl_5d_chart, indent=2))

        aapl_meta_quotes = await client.get_quote(tickers='AAPL,META')
        print(json.dumps(aapl_meta_quotes, indent=2))

        meta_quote_summary = await client.get_quote_summary(
            ticker='META',
            modules='assetProfile,price,defaultKeyStatistics,calendarEvents',
        )
        print(json.dumps(meta_quote_summary, indent=2))

        aapl_ttm_income_stmt = await client.get_timeseries(
            ticker='AAPL',
            types='trailingNetIncome,trailingPretaxIncome,trailingEBIT,trailingEBITDA,trailingGrossProfit',
        )
        print(json.dumps(aapl_ttm_income_stmt, indent=2))

        meta_annual_balance_sheet = await client.get_timeseries(
            ticker='META',
            types='annualNetDebt,annualTotalDebt',
            period1=datetime(2020, 1, 1).timestamp(),
            period2=datetime.now().timestamp(),
        )
        print(json.dumps(meta_annual_balance_sheet, indent=2))

        aapl_quarterly_cash_flow = await client.get_timeseries(
            ticker='AAPL', types='quarterlyFreeCashFlow,quarterlyOperatingCashFlow'
        )
        print(json.dumps(aapl_quarterly_cash_flow, indent=2))

        meta_options = await client.get_options(ticker='META')
        print(json.dumps(meta_options, indent=2))

        meta_search = await client.get_search(tickers='META')
        print(json.dumps(meta_search, indent=2))

        meta_recommendations = await client.get_recommendations(ticker='META')
        print(json.dumps(meta_recommendations, indent=2))

        meta_insights = await client.get_insights(ticker='META')
        print(json.dumps(meta_insights, indent=2))

        market_summaries = await client.get_market_summaries()
        print(json.dumps(market_summaries, indent=2))

        trending = await client.get_trending()
        print(json.dumps(trending, indent=2))

        currencies = await client.get_currencies()
        print(json.dumps(currencies, indent=2))

    aapl = AsyncSymbol('AAPL')

    aapl_5d_chart = await aapl.get_chart(
        period_range='5d', interval='1h', include_div=True, include_split=False
    )

    await aapl.close()

    async with AsyncSymbol('META') as meta:
        meta_1y_chart = await meta.get_chart(period_range='1y', interval='1d')
        print(json.dumps(meta_1y_chart, indent=2))

        print(json.dumps(aapl_5d_chart, indent=2))

        meta_quote = await meta.get_quote()
        print(json.dumps(meta_quote, indent=2))

        meta_quote_summary_all_modules = await meta.get_quote_summary_all_modules()
        print(json.dumps(meta_quote_summary_all_modules, indent=2))

        meta_quote_type = await meta.get_quote_type()
        print(json.dumps(meta_quote_type, indent=2))

        meta_asset_profile = await meta.get_asset_profile()
        print(json.dumps(meta_asset_profile, indent=2))

        meta_summary_profile = await meta.get_summary_profile()
        print(json.dumps(meta_summary_profile, indent=2))

        meta_summary_detail = await meta.get_summary_detail()
        print(json.dumps(meta_summary_detail, indent=2))

        meta_income_statement_history = await meta.get_income_statement_history()
        print(json.dumps(meta_income_statement_history, indent=2))

        meta_income_statement_history_quarterly = (
            await meta.get_income_statement_history_quarterly()
        )
        print(json.dumps(meta_income_statement_history_quarterly, indent=2))

        meta_balance_sheet_history = await meta.get_balance_sheet_history()
        print(json.dumps(meta_balance_sheet_history, indent=2))

        meta_balance_sheet_history_quarterly = (
            await meta.get_balance_sheet_history_quarterly()
        )
        print(json.dumps(meta_balance_sheet_history_quarterly, indent=2))

        meta_cashflow_statement_history = await meta.get_cashflow_statement_history()
        print(json.dumps(meta_cashflow_statement_history, indent=2))

        meta_cashflow_statement_history_quarterly = (
            await meta.get_cashflow_statement_history_quarterly()
        )
        print(json.dumps(meta_cashflow_statement_history_quarterly, indent=2))

        meta_esg_scores = await meta.get_esg_scores()
        print(json.dumps(meta_esg_scores, indent=2))

        meta_price = await meta.get_price()
        print(json.dumps(meta_price, indent=2))

        meta_default_key_statistics = await meta.get_default_key_statistics()
        print(json.dumps(meta_default_key_statistics, indent=2))

        meta_financial_data = await meta.get_financial_data()
        print(json.dumps(meta_financial_data, indent=2))

        meta_calendar_events = await meta.get_calendar_events()
        print(json.dumps(meta_calendar_events, indent=2))

        meta_sec_filings = await meta.get_sec_filings()
        print(json.dumps(meta_sec_filings, indent=2))

        meta_upgrade_downgrade_history = await meta.get_upgrade_downgrade_history()
        print(json.dumps(meta_upgrade_downgrade_history, indent=2))

        meta_institution_ownership = await meta.get_institution_ownership()
        print(json.dumps(meta_institution_ownership, indent=2))

        meta_fund_ownership = await meta.get_fund_ownership()
        print(json.dumps(meta_fund_ownership, indent=2))

        meta_major_direct_holders = await meta.get_major_direct_holders()
        print(json.dumps(meta_major_direct_holders, indent=2))

        meta_major_holders_breakdown = await meta.get_major_holders_breakdown()
        print(json.dumps(meta_major_holders_breakdown, indent=2))

        meta_insider_transactions = await meta.get_insider_transactions()
        print(json.dumps(meta_insider_transactions, indent=2))

        meta_insider_holders = await meta.get_insider_holders()
        print(json.dumps(meta_insider_holders, indent=2))

        meta_net_share_purchase_activity = await meta.get_net_share_purchase_activity()
        print(json.dumps(meta_net_share_purchase_activity, indent=2))

        meta_earnings = await meta.get_earnings()
        print(json.dumps(meta_earnings, indent=2))

        meta_earnings_history = await meta.get_earnings_history()
        print(json.dumps(meta_earnings_history, indent=2))

        meta_earnings_trend = await meta.get_earnings_trend()
        print(json.dumps(meta_earnings_trend, indent=2))

        meta_industry_trend = await meta.get_industry_trend()
        print(json.dumps(meta_industry_trend, indent=2))

        meta_index_trend = await meta.get_index_trend()
        print(json.dumps(meta_index_trend, indent=2))

        meta_sector_trend = await meta.get_sector_trend()
        print(json.dumps(meta_sector_trend, indent=2))

        meta_recommendation_trend = await meta.get_recommendation_trend()
        print(json.dumps(meta_recommendation_trend, indent=2))

        meta_page_views = await meta.get_page_views()
        print(json.dumps(meta_page_views, indent=2))

        meta_get_income_statement = await meta.get_income_statement(
            frequency='trailing'
        )
        print(json.dumps(meta_get_income_statement, indent=2))

        meta_get_balance_sheet = await meta.get_balance_sheet(
            frequency='annual',
            period1=datetime(2020, 1, 1).timestamp(),
            period2=datetime.now().timestamp(),
        )
        print(json.dumps(meta_get_balance_sheet, indent=2))

        meta_get_cash_flow = await meta.get_cash_flow(frequency='quarterly')
        print(json.dumps(meta_get_cash_flow, indent=2))

        meta_options = await meta.get_options()
        print(json.dumps(meta_options, indent=2))

        meta_search = await meta.get_search()
        print(json.dumps(meta_search, indent=2))

        meta_recommendations = await meta.get_recommendations()
        print(json.dumps(meta_recommendations, indent=2))

        meta_insights = await meta.get_insights()
        print(json.dumps(meta_insights, indent=2))


if __name__ == '__main__':
    asyncio.run(main())
