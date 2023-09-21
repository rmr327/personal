import finnhub
import pandas as pd
from datetime import datetime

if __name__ == '__main__':
    tick = 'aapl'

    # Setup client
    finnhub_client = finnhub.Client(api_key="c52036qad3i9nnbv3e30")

    start_dt = int(datetime(2021, 2, 14, 0, 0).timestamp())
    end_dt = int(datetime(2021, 9, 22, 0, 0).timestamp())

    # Stock candles
    # res = pd.DataFrame(finnhub_client.stock_candles(tick, 'M', start_dt, end_dt))
    # res['datetime'] = res['t'].apply(lambda x: datetime.fromtimestamp(x))

    # Aggregate Indicators
    # agg = finnhub_client.aggregate_indicator(tick, 'W')
    # agg_df = pd.DataFrame([tick], columns=['Tick'])
    # ta = agg['technicalAnalysis']['count']
    # ts = agg['technicalAnalysis']['signal']
    # adx = agg['trend']['adx']
    # t = agg['trend']['trending']
    # agg_df[['buy', 'sell', 'neutral', 'signal', 'adx', 'trending']] = [ta['buy'], ta['sell'], ta['neutral'],
    # ts, adx, t]

    # Basic financials
    print(finnhub_client.company_basic_financials(tick, 'all'))

    # General news
    # general_news = pd.DataFrame(finnhub_client.general_news('general', min_id=0))

    # Company Profile 2
    company_profile = pd.DataFrame(finnhub_client.company_profile2(symbol=tick), index=[0])

    # Stock symbols
    # stock_symbols = pd.DataFrame(finnhub_client.stock_symbols('US')[0:5])

    # Company News
    # Need to use _from instead of from to avoid conflict
    company_news = pd.DataFrame(finnhub_client.company_news(tick, _from="2020-06-01", to="2021-09-24"))

    # News sentiment
    # news_sentiment = pd.DataFrame(finnhub_client.news_sentiment(tick))

    # Company Peers
    company_peers = finnhub_client.company_peers(tick)

    # Basic financials
    Base_financials = pd.DataFrame(finnhub_client.company_basic_financials(tick, 'all')).reset_index()

    # Insider transactions
    insider_transaction = pd.DataFrame(finnhub_client.stock_insider_transactions(tick, '2021-01-01', '2021-09-24'))

    for k in insider_transaction['data'].iloc[0].keys():
        insider_transaction[k] = insider_transaction['data'].apply(lambda r: r[k])

    insider_transaction = insider_transaction.drop(['data'], axis=1)

    # Financials as reported
    financials_as_reported = pd.DataFrame(finnhub_client.financials_reported(symbol=tick, freq='annual'))

    for k in financials_as_reported['data'].iloc[0].keys():
        financials_as_reported[k] = financials_as_reported['data'].apply(lambda r: r[k])

    financials_as_reported = financials_as_reported.drop(['data'], axis=1)

    financials_as_reported = financials_as_reported.drop(['report'], axis=1)

    # IPO calendar
    # ipo_calender = pd.DataFrame(finnhub_client.ipo_calendar(_from="2020-05-01", to="2020-06-01"))
    #
    # for k in ipo_calender['ipoCalendar'].iloc[0].keys():
    #     ipo_calender[k] = ipo_calender['ipoCalendar'].apply(lambda r: r[k])
    #
    # ipo_calender = ipo_calender.drop(['ipoCalendar'], axis=1)

    # Recommendation trends
    recommendation_trends = pd.DataFrame(finnhub_client.recommendation_trends(tick))

    # Earnings surprises
    earning_surprise = pd.DataFrame(finnhub_client.company_earnings(tick, limit=100))

    # Quote
    # quote = pd.DataFrame(finnhub_client.quote('AAPL'), index=[0])

    # Indices Constituents
    indices_constituents = finnhub_client.indices_const(symbol="SOXL")

    # Pattern recognition
    pattern_recognitions = pd.DataFrame(finnhub_client.pattern_recognition(tick, 'M'))
    for k in pattern_recognitions['points'].iloc[0].keys():
        try:
            pattern_recognitions[k] = pattern_recognitions['points'].apply(lambda r: r[k])
        except KeyError:
            pass

    pattern_recognitions = pattern_recognitions.drop(['points'], axis=1)
    pattern_recognitions['sortTime'] = pattern_recognitions['sortTime'].apply(lambda r: datetime.fromtimestamp(r))
    pattern_recognitions['atime'] = pattern_recognitions['atime'].apply(lambda r: datetime.fromtimestamp(r))
    pattern_recognitions['dtime'] = pattern_recognitions['dtime'].apply(lambda r: datetime.fromtimestamp(r))

    # Support resistance
    support_resistance = finnhub_client.support_resistance(tick, 'W')

    # More indicators
    # https: // docs.google.com / spreadsheets / d / 1
    # ylUvKHVYN2E87WdwIza8ROaCpd48ggEl1k5i5SgA29k / edit  # gid=0
    # Technical Indicator
    techindicator = finnhub_client.technical_indicator(symbol=tick, resolution='W', _from=start_dt, to=end_dt,
                                                       indicator='rsi', indicator_fields={"timeperiod": 7})
    techindicator = pd.DataFrame(techindicator)

    # Social sentiment
    social_sentiment = finnhub_client.stock_social_sentiment(tick, _from='2021-01-01', to='2021-09-24')
    social_sentiment_reddit = pd.DataFrame(social_sentiment['reddit'])

    # Covid-19
    # covid_info = pd.DataFrame(finnhub_client.covid19())
    print(21)
