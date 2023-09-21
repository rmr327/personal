from datetime import datetime
import pandas as pd
import yahoo_fin.stock_info as si
from numpy import array, where
from dateutil.relativedelta import relativedelta
import finnhub
import numpy as np

pd.options.mode.chained_assignment = None


class StockData:
    def __init__(self, st_date, nd_date, aaa_bnd_rate):
        self.start_date = st_date
        self.end_date = nd_date
        self.aaa_bond_rate = aaa_bnd_rate
        # self.fin_hub_client = finnhub.Client(api_key="c52036qad3i9nnbv3e30")
        self.fin_hub_client = finnhub.Client(api_key="sandbox_c52036qad3i9nnbv3e3g")  # sandbox

    @staticmethod
    def get_earning_history(tick):
        earnings = pd.DataFrame.from_dict(si.get_earnings_history(tick))

        earnings = earnings.dropna()[['startdatetime', 'epsactual', 'startdatetimetype']]
        time_type_count = earnings.startdatetimetype.value_counts()
        max_count_time_types = time_type_count.idxmax()
        earnings = earnings.loc[earnings.startdatetimetype == max_count_time_types]
        earnings['startdatetime'] = pd.to_datetime(earnings.startdatetime)
        earnings['startdatetime'] = earnings.startdatetime.apply(lambda r_: r_.tz_localize(None))

        return earnings

    def get_price_history(self, tick):
        prices = si.get_data(tick).reset_index()
        prices['date'] = pd.to_datetime(prices['index'], format='%Y-%m-%d %H:%M:%S')
        prices = prices[['date', 'adjclose', 'volume']]
        relevant_prices = prices.loc[(prices.date >= self.start_date) & (prices.date <= self.end_date)]

        latest_price = prices.iloc[-1]

        return relevant_prices, latest_price

    def get_dividend_per_share_history(self, tick):
        dividends = si.get_dividends(tick, self.start_date, self.end_date)

        return dividends

    def get_tick_stats(self, tick):
        """
        Returns the first four criteria from the following link
        https://www.oldschoolvalue.com/investing-strategy/graham-stock-checklist-screen/
        """
        number_of_errors = 0
        basic_financials = self.get_basic_financials(tick)

        form_10_k = self._get_form_10_k_info_helper(tick)

        earnings = self.get_earning_history(tick)
        relevant_prices, latest_price = self.get_price_history(tick)

        date_bins = pd.Series(index=relevant_prices.date, data=array(relevant_prices.count)).resample('365D').count()
        date_bins = date_bins.index.values

        index_col = 'date_plus_1_year'

        mean_relevant_prices = self._get_mean_df_by_year(relevant_prices, date_bins)
        mean_relevant_prices.set_index(index_col, inplace=True)

        date_col = 'startdatetime'
        mean_earnings = self._get_mean_df_by_year(earnings, date_bins, date_col)
        mean_earnings.set_index(index_col, inplace=True)

        final_df = pd.concat([mean_earnings, mean_relevant_prices], axis=1)
        final_df['p/e'] = final_df.adjclose / final_df.epsactual
        final_df['e/p'] = 1 / final_df['p/e']

        latest_earnings = earnings.iloc[0]

        latest_pe = latest_price.adjclose / latest_earnings.epsactual

        # one
        all_pe = final_df['p/e'].values
        any_last_5_years_pe_lt_40_p_cur_pe = where(all_pe > latest_pe, True, False).any()

        # two
        latest_pe_twice_aaa_rate = ((1/latest_pe) * 100) > (2 * self.aaa_bond_rate)

        # three
        try:
            latest_dividend = self.get_dividend_per_share_history(tick).iloc[-4:].sum()['dividend']
        except KeyError:
            latest_dividend = 0

        latest_dividend_yield = latest_dividend / latest_price.adjclose

        div_yld_me_2_by_3_aa = (latest_dividend_yield * 100) > ((2/3) * self.aaa_bond_rate)

        # four
        tbvps = basic_financials['metric']['tangibleBookValuePerShareAnnual']
        try:
            tbvps_lt_2_by_3_aaa = latest_price.adjclose < ((2/3) * tbvps)
        except TypeError:
            number_of_errors += 1
            tbvps_lt_2_by_3_aaa = False

        try:
            form_10_k_rows = form_10_k.index.values
        except AttributeError:
            return False

        # five
        try:
            total_liabilities, total_current_asset = self._get_total_liabilities_current_assets_helper(form_10_k,
                                                                                                       form_10_k_rows,
                                                                                                       tick)
        except KeyError:
            form_10_k = self._get_form_10_k_info_helper(tick, 1)
            form_10_k_rows = form_10_k.index.values

            total_liabilities, total_current_asset = self._get_total_liabilities_current_assets_helper(form_10_k,
                                                                                                       form_10_k_rows,
                                                                                                       tick)
        if total_current_asset == 0:
            number_of_errors += 1

        ncav = (total_current_asset - total_liabilities) / latest_price['volume']
        stock_below_2_by_3_ncav = latest_price.adjclose < (2/3 * ncav)

        # six
        cols = [i_ for i_ in form_10_k_rows if ('debt' in i_) or ('Debt' in i_)]
        try:
            total_debt = form_10_k.loc[cols].drop_duplicates()  # .dropna().sum()['value']  # / latest_price['volume']
            total_debt = total_debt[pd.to_numeric(total_debt['value'], errors='coerce').notnull()]
            total_debt = total_debt.dropna().sum()['value'] / latest_price['volume']
        except TypeError:
            number_of_errors += 1
            total_debt = 0

        total_debt_lt_2_by_3_nvac = total_debt < (2/3 * ncav)

        # seven
        try:
            total_current_liabilities = form_10_k.loc['LiabilitiesCurrent']['value']
        except KeyError:
            try:
                total_current_liabilities = form_10_k.loc['afl:TotalPolicyLiabilities']['value']
            except KeyError:
                print('Missing current liabilities')
                print(form_10_k_rows)
                number_of_errors += 1
                total_current_liabilities = 0

        try:
            current_ratio_mt_2 = (total_current_asset / total_current_liabilities) > 2
        except ZeroDivisionError:
            current_ratio_mt_2 = True

        # eight
        tot_debt_lt_2_times_ncac = total_debt < (2 * ncav)

        # nine
        earnings['year'] = pd.DatetimeIndex(earnings['startdatetime']).year
        end_minus_ten = self.end_date.year - 10
        last_10_years_earnings = earnings.loc[earnings['year'] >= end_minus_ten]
        last_10_years_earnings_year_end = last_10_years_earnings.drop_duplicates(subset='year', keep="first")
        last_10_years_earnings_year_end.reset_index(inplace=True, drop=True)
        col = 'epsactual'
        last_10_years_earnings_year_end = self._get_percent_change_from_last(last_10_years_earnings_year_end, col)

        latest_earnings = last_10_years_earnings_year_end['epsactual'].iloc[0]
        earliest_earnings = last_10_years_earnings_year_end['epsactual'].iloc[-1]
        number_of_years = 10

        annual_compound_rate = (latest_earnings / earliest_earnings) ** (1 / number_of_years)
        annual_compound_eps_growth_rate_mt_7_percent = annual_compound_rate > 7

        # ten
        last_10_years_earnings_year_end['mt_5_%'] = \
            last_10_years_earnings_year_end['change_from_last'].apply(lambda r: 1 if r < -5 else 0)

        lt_2_declines_in_eps_mt_neg_5_percent = last_10_years_earnings_year_end['mt_5_%'].sum() < 2

        if not isinstance(tot_debt_lt_2_times_ncac, np.bool):
            number_of_errors += 1
            tot_debt_lt_2_times_ncac = False

        if not isinstance(stock_below_2_by_3_ncav, np.bool):
            number_of_errors += 1
            stock_below_2_by_3_ncav = False

        if not isinstance(total_debt_lt_2_by_3_nvac, np.bool):
            number_of_errors += 1
            total_debt_lt_2_by_3_nvac = False

        return {'any_last_5_years_pe_lt_40_p_cur_pe': any_last_5_years_pe_lt_40_p_cur_pe,
                'latest_pe_twice_aaa_rate': latest_pe_twice_aaa_rate, 'div_yld_me_2_by_3_aa': div_yld_me_2_by_3_aa,
                'tbvps_lt_2_by_3_aaa': tbvps_lt_2_by_3_aaa, 'stock_below_2_by_3_ncav': stock_below_2_by_3_ncav,
                'total_debt_lt_2_by_3_nvac': total_debt_lt_2_by_3_nvac, 'current_ratio_mt_2': current_ratio_mt_2,
                'tot_debt_lt_2_times_ncac': tot_debt_lt_2_times_ncac,
                'annual_compound_eps_growth_rate_mt_7_percent': annual_compound_eps_growth_rate_mt_7_percent,
                'lt_2_declines_in_eps_mt_neg_5_percent': lt_2_declines_in_eps_mt_neg_5_percent,
                'Number of errors': number_of_errors, 'tick': tick}

    def _get_form_10_k_info_helper(self, tick, idx=0):
        try:
            form_10_k = self.fin_hub_client.financials_reported(symbol=tick, freq='annual')['data'][idx]['report']['bs']
        except IndexError:
            print('Possibly new company')
            return False

        form_10_k = pd.DataFrame.from_dict(form_10_k)
        form_10_k.set_index('concept', inplace=True)

        return form_10_k

    @staticmethod
    def _get_total_liabilities_current_assets_helper(form_10_k, form_10_k_rows, tick):
        try:
            total_current_asset = form_10_k.loc['AssetsCurrent']['value']
            try:
                total_current_asset = int(total_current_asset)
            except ValueError:
                total_current_asset = 0
            except TypeError:
                total_current_asset = int(total_current_asset.mean())

        except KeyError:
            try:
                total_current_asset = form_10_k.loc['Assets']['value']
            except KeyError:
                print(f'{tick} missing current asset.')
                print(form_10_k_rows)
                total_current_asset = 0

        try:
            total_liabilities = form_10_k.loc['Liabilities']['value']
        except KeyError:
            val_1 = form_10_k.loc['LiabilitiesCurrent']['value']

            try:
                val_2 = form_10_k.loc['LiabilitiesNoncurrent']['value']
            except KeyError:
                try:
                    val_2 = form_10_k.loc['OtherLiabilitiesNoncurrent']['value']
                except KeyError:
                    val_2 = 0
                    print('Missing val 2 Noncurrent liabilities')
                    print(form_10_k_rows)
            total_liabilities = val_1 + val_2

        return total_liabilities, total_current_asset

    @staticmethod
    def _get_percent_change_from_last(df, use_col):
        length = len(df)
        df['change_from_last'] = None

        res_lis = []
        for i_ in range(length-1):
            final_val = df[use_col].iloc[i_]
            initial_val = df[use_col].iloc[i_+1]
            calc = ((final_val - initial_val) / initial_val) * 100

            if (final_val < initial_val) and (calc > 0):
                multiplier = -1
            elif (final_val > initial_val) and (calc < 0):
                multiplier = -1
            else:
                multiplier = 1

            res_lis.append(multiplier * calc)

        res_lis.append(0)
        df['change_from_last'] = res_lis

        return df

    def get_basic_financials(self, tick):
        return self.fin_hub_client.company_basic_financials(tick, 'all')

    @staticmethod
    def _get_mean_df_by_year(df, dates, date_col='date'):
        res_df = pd.DataFrame()
        previous_date = dates[0]

        for i_ in dates[1:]:
            r_rdf = df.loc[(df[date_col] >= previous_date) & (df[date_col] < i_)].mean(numeric_only=True)
            r_rdf['date_plus_1_year'] = previous_date
            previous_date = i_

            res_df = res_df.append(pd.DataFrame(r_rdf).T)

        r_rdf = df.loc[(df[date_col] >= previous_date)].mean(numeric_only=True)
        r_rdf['date_plus_1_year'] = previous_date

        res_df = res_df.append(pd.DataFrame(r_rdf).T)

        return res_df


if __name__ == '__main__':
    end_date = datetime.today()  # - relativedelta(days=365*5)
    start_date = end_date - relativedelta(days=365*5)
    aaa_bond_rate = 2.62
    tick_ = 'dis'

    sd = StockData(start_date, end_date, aaa_bond_rate)
    ret = sd.get_tick_stats(tick_)

    print(tick_)
    print(f'BOOL ---------------- METRIC')
    for r in ret:
        print(f'{r} :;:^:;;:^::;: {ret[r]}')
    print(21)

    # outcome  credit rating, credit spread,
    # predictor net debt to ebidta, cash ratio, cash flow to interest payment, industry sector,
    # credit rating, market cap, operating leverage,
